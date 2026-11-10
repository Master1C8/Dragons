using Mono.Cecil;
using Mono.Cecil.Cil;

internal static class WrapHooks
{
    private const string Width = "DeferWidthOverflow";
    private const string Save = "SkipWrapState";

    internal static void Attach(MethodDefinition method, TypeReference owner, ModuleDefinition layout)
    {
        var body = method.Body;
        var ui = method.DeclaringType.Name == "TextMeshProUGUI";
        Instruction At(int worldOffset) => body.Instructions.Single(i => i.Offset == worldOffset - (ui ? 1 : 0));
        var width = At(0x21be);
        var save = At(0x3d98);
        var widthEnd = At(0x2ad1);
        var saveEnd = At(0x3fe1);
        if (width.Previous.OpCode != OpCodes.Ble_Un || width.Previous.Operand != widthEnd ||
            !LoadsField(width.Next, "m_TextWrappingMode") || !LoadsField(save.Next, "m_TextWrappingMode") ||
            saveEnd.Previous.OpCode != OpCodes.Call ||
            (saveEnd.Previous.Operand as MethodReference)?.Name != "SaveWordWrappingState")
            throw new InvalidDataException("Unexpected TMP width or wrap-save branch");

        var tmp = method.Module.GetType("TMPro.TMP_Text");
        var count = tmp.Fields.Single(f => f.Name == "m_characterCount");
        var line = tmp.Fields.Single(f => f.Name == "m_firstCharacterOfLine");
        var glyph = body.Variables[6];
        if (glyph.VariableType.FullName != "System.UInt32")
            throw new InvalidDataException("Unexpected TMP wrap glyph local");
        var il = body.GetILProcessor();
        Insert(width, widthEnd, Width, includeLine: true);
        Insert(save, saveEnd, Save, includeLine: false);

        void Insert(Instruction anchor, Instruction target, string name, bool includeLine)
        {
            var types = method.Module.TypeSystem;
            var signature = new List<TypeReference> { tmp, types.UInt32, types.Int32 };
            if (includeLine)
                signature.Add(types.Int32);
            var companion = layout.GetType(owner.FullName).Methods.Single(m => m.Name == name);
            if (!companion.IsPublic || !companion.IsStatic || companion.ReturnType.FullName != types.Boolean.FullName ||
                !companion.Parameters.Select(p => p.ParameterType.FullName).SequenceEqual(signature.Select(t => t.FullName)))
                throw new InvalidDataException($"Unexpected wrap helper signature for {name}");
            var call = new MethodReference(name, types.Boolean, owner);
            foreach (var parameter in signature)
                call.Parameters.Add(new ParameterDefinition(parameter));
            var block = new List<Instruction>
            {
                Instruction.Create(OpCodes.Ldarg_0),
                Instruction.Create(OpCodes.Ldloc_S, glyph),
                Instruction.Create(OpCodes.Ldarg_0),
                Instruction.Create(OpCodes.Ldfld, count),
            };
            if (includeLine)
            {
                block.Add(Instruction.Create(OpCodes.Ldarg_0));
                block.Add(Instruction.Create(OpCodes.Ldfld, line));
            }
            block.Add(Instruction.Create(OpCodes.Call, call));
            block.Add(Instruction.Create(OpCodes.Brtrue, target));

            foreach (var instruction in body.Instructions)
                if (instruction.Operand == anchor)
                    instruction.Operand = block[0];
                else if (instruction.Operand is Instruction[] targets)
                    for (var i = 0; i < targets.Length; i++)
                        if (targets[i] == anchor)
                            targets[i] = block[0];
            foreach (var instruction in block)
                il.InsertBefore(anchor, instruction);
        }
    }

    internal static Dictionary<Instruction, Instruction> Normalize(MethodDefinition method)
    {
        var skipped = new Dictionary<Instruction, Instruction>();
        Check(Width, includeLine: true);
        Check(Save, includeLine: false);
        return skipped;

        void Check(string name, bool includeLine)
        {
            var call = method.Body.Instructions.Single(i => i.OpCode == OpCodes.Call &&
                i.Operand is MethodReference m && m.DeclaringType.FullName == "Dragons.PreparedText.RenderHook" &&
                m.Name == name);
            var branch = call.Next;
            var anchor = branch.Next;
            var count = includeLine ? call.Previous.Previous.Previous : call.Previous;
            var first = count.Previous.Previous.Previous;
            if (branch.OpCode != OpCodes.Brtrue || anchor.OpCode != OpCodes.Ldarg_0 ||
                !LoadsField(anchor.Next, "m_TextWrappingMode") || !LoadsField(count, "m_characterCount") ||
                first.OpCode != OpCodes.Ldarg_0 || first.Next.OpCode != OpCodes.Ldloc_S ||
                (first.Next.Operand as VariableDefinition)?.Index != 6 || count.Previous.OpCode != OpCodes.Ldarg_0 ||
                includeLine && (!LoadsField(call.Previous, "m_firstCharacterOfLine") ||
                    call.Previous.Previous.OpCode != OpCodes.Ldarg_0) ||
                (includeLine ? first.Previous.Operand != branch.Operand :
                    (branch.Operand as Instruction)?.Previous.Operand is not MethodReference save ||
                    save.Name != "SaveWordWrappingState"))
                throw new InvalidDataException($"TMP wrap hook failed read-back: {name}");
            for (var instruction = first; instruction != anchor; instruction = instruction.Next)
                skipped.Add(instruction, anchor);
        }
    }

    private static bool LoadsField(Instruction instruction, string name) =>
        instruction.OpCode == OpCodes.Ldfld && instruction.Operand is FieldReference field && field.Name == name;
}
