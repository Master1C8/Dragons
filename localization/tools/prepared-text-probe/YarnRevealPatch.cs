using System.Security.Cryptography;
using Mono.Cecil;
using Mono.Cecil.Cil;

internal static class YarnRevealPatch
{
    private const string StateMachine = "Yarn.Unity.LetterTypewriter/<RunTypewriter>d__12";
    private const string Helper = "Dragons.PreparedText.RenderHook";

    internal static void Write(string stock, string layoutPath, string output,
        Func<ModuleDefinition, Dictionary<string, string>> fingerprint)
    {
        var source = File.ReadAllBytes(stock);
        var hash = Convert.ToHexString(SHA256.HashData(source)).ToLowerInvariant();
        if (hash is not ("54953f9c071aa3ca5b52eb8b12b8e0bedc73f7665a506c61acbef0c58ac340ef" or
                         "3d5def40f51540e79dbb6a897993fe006022cf1f16933a1b47a69334085ad89d"))
            throw new InvalidDataException("Expected a pinned Dragons Yarn assembly");

        using var module = ModuleDefinition.ReadModule(new MemoryStream(source));
        using var layout = ModuleDefinition.ReadModule(layoutPath);
        var before = fingerprint(module);
        var moveNext = module.GetType(StateMachine).Methods.Single(m => m.Name == "MoveNext");
        var instructions = moveNext.Body.Instructions;
        var count = instructions.Single(i => Calls(i, "TMPro.TMP_Text", "GetTextInfo"));
        var field = count.Next;
        var setters = instructions.Where(i => Calls(i, "TMPro.TMP_Text", "set_maxVisibleCharacters")).ToArray();
        if (setters.Length != 3 || field.OpCode != OpCodes.Ldfld ||
            (field.Operand as FieldReference)?.Name != "characterCount")
            throw new InvalidDataException("Unexpected Yarn count or reveal sites");
        var advance = setters[1];
        var finish = setters[2];
        var add = advance.Previous;
        var one = add.Previous;
        var get = one.Previous;
        var dup = get.Previous;
        var logicalIndex = moveNext.DeclaringType.Fields.Single(f => f.Name == "<i>5__5");
        if (add.OpCode != OpCodes.Add || one.OpCode != OpCodes.Ldc_I4_1 ||
            !Calls(get, "TMPro.TMP_Text", "get_maxVisibleCharacters") || dup.OpCode != OpCodes.Dup ||
            finish.Previous.OpCode != OpCodes.Ldfld ||
            (finish.Previous.Operand as FieldReference)?.Name != "<visibleCharacterCount>5__3")
            throw new InvalidDataException("Unexpected Yarn progression or completion sites");

        var scope = AssemblyNameReference.Parse(layout.Assembly.Name.FullName);
        module.AssemblyReferences.Add(scope);
        var type = new TypeReference("Dragons.PreparedText", "RenderHook", module, scope);
        var tmp = ((MethodReference)count.Operand).DeclaringType;
        MethodReference Bind(string name, TypeReference returnType, TypeReference argument)
        {
            var companion = layout.GetType(Helper).Methods.Single(m => m.Name == name);
            if (!companion.IsPublic || !companion.IsStatic || companion.ReturnType.FullName != returnType.FullName ||
                !companion.Parameters.Select(p => p.ParameterType.FullName).SequenceEqual(new[] { tmp.FullName, argument.FullName }))
                throw new InvalidDataException($"Unexpected companion signature for {name}");
            var reference = new MethodReference(name, returnType, type);
            reference.Parameters.Add(new ParameterDefinition(tmp));
            reference.Parameters.Add(new ParameterDefinition(argument));
            return reference;
        }

        var edits = new[]
        {
            (count, OpCodes.Call, (object?)Bind("GetLogicalCount", module.TypeSystem.Int32, module.TypeSystem.String)),
            (field, OpCodes.Nop, null),
            (dup, OpCodes.Ldarg_0, null),
            (get, OpCodes.Ldfld, logicalIndex),
            (one, OpCodes.Nop, null),
            (add, OpCodes.Nop, null),
            (advance, OpCodes.Call, Bind("Advance", module.TypeSystem.Void, module.TypeSystem.Int32)),
            (finish, OpCodes.Call, Bind("Finish", module.TypeSystem.Void, module.TypeSystem.Int32)),
        };
        var originals = edits.Select(e => (Index: instructions.IndexOf(e.Item1), e.Item1.OpCode, e.Item1.Operand)).ToArray();
        foreach (var (instruction, opcode, operand) in edits)
        {
            instruction.OpCode = opcode;
            instruction.Operand = operand;
        }

        using var stream = new MemoryStream();
        module.Write(stream);
        var patched = stream.ToArray();
        using var reopened = ModuleDefinition.ReadModule(new MemoryStream(patched));
        var verified = reopened.GetType(StateMachine).Methods.Single(m => m.Name == "MoveNext").Body.Instructions;
        for (var i = 0; i < edits.Length; i++)
        {
            var (index, originalOpcode, originalOperand) = originals[i];
            var instruction = verified[index];
            if (instruction.OpCode != edits[i].Item2 || instruction.Operand?.ToString() != edits[i].Item3?.ToString())
                throw new InvalidDataException("Yarn reveal patch did not survive read-back");
            instruction.OpCode = originalOpcode;
            instruction.Operand = originalOperand;
        }
        var after = fingerprint(reopened);
        if (before.Count != after.Count || before.Any(entry => !after.TryGetValue(entry.Key, out var body) || body != entry.Value))
            throw new InvalidDataException("Original Yarn bodies changed beyond the verified reveal sites");
        using var destination = new FileStream(output, FileMode.CreateNew);
        destination.Write(patched);
        Console.WriteLine($"Verified {before.Count} Yarn bodies and three reveal sites against {hash}");
    }

    private static bool Calls(Instruction instruction, string owner, string name) =>
        instruction.OpCode == OpCodes.Callvirt && instruction.Operand is MethodReference method &&
        method.DeclaringType.FullName == owner && method.Name == name;
}
