using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

internal static class RenderPlans
{
    internal const string ResourceName = "Dragons.PreparedText.Plans";
    internal const string ApplyName = "System.Void Dragons.PreparedText.RenderHook::Apply(TMPro.TMP_Text)";
    private static readonly string[] Renderers = { "TMPro.TextMeshPro", "TMPro.TextMeshProUGUI" };

    internal static byte[] Encode(JsonElement rows)
    {
        using var stream = new MemoryStream();
        using var writer = new BinaryWriter(stream);
        writer.Write(3);
        writer.Write(rows.GetArrayLength());
        foreach (var row in rows.EnumerateArray())
        {
            var logical = row.GetProperty("logical").GetString()!;
            var prepared = row.GetProperty("prepared").GetString()!;
            var paragraphLevel = row.GetProperty("paragraphLevel").GetInt32();
            var offsets = ReadInts(row, "offsets");
            var ends = ReadInts(row, "clusterEnds");
            var sourceEnds = ReadInts(row, "sourceClusterEnds");
            var levels = ReadInts(row, "levels");
            var reset = row.GetProperty("trailingReset").EnumerateArray().Select(v => v.GetBoolean()).ToArray();
            if (paragraphLevel is < 0 or > 1 || !Increasing(offsets, -1) || offsets[^1] >= prepared.Length ||
                !Increasing(ends, 0) || ends[^1] != offsets.Length ||
                !Increasing(sourceEnds, 0) || sourceEnds[^1] > logical.Length ||
                ends.Length != sourceEnds.Length || ends.Length != levels.Length || ends.Length != reset.Length ||
                levels.Any(level => level is < 0 or > 126))
                throw new InvalidDataException("Invalid prepared render plan boundaries");

            writer.Write(logical);
            writer.Write(prepared);
            writer.Write((byte)paragraphLevel);
            writer.Write(offsets.Length);
            foreach (var offset in offsets)
                writer.Write(offset);
            writer.Write(ends.Length);
            for (var i = 0; i < ends.Length; i++)
            {
                writer.Write(ends[i]);
                writer.Write(sourceEnds[i]);
                writer.Write((byte)levels[i]);
                writer.Write(reset[i]);
            }
        }
        return stream.ToArray();

        static int[] ReadInts(JsonElement row, string key) =>
            row.GetProperty(key).EnumerateArray().Select(v => v.GetInt32()).ToArray();

        static bool Increasing(int[] values, int lowerBound)
        {
            if (values.Length == 0)
                return false;
            foreach (var value in values)
            {
                if (value <= lowerBound)
                    return false;
                lowerBound = value;
            }
            return true;
        }
    }

    internal static void Attach(ModuleDefinition module, string layoutPath, byte[] plans)
    {
        using var layout = ModuleDefinition.ReadModule(layoutPath);
        var apply = layout.GetType("Dragons.PreparedText.RenderHook").Methods.Single(m => m.FullName == ApplyName);
        if (!apply.IsPublic || !apply.IsStatic)
            throw new InvalidDataException("Expected a public static render hook");
        var scope = AssemblyNameReference.Parse(layout.Assembly.Name.FullName);
        module.AssemblyReferences.Add(scope);
        var owner = new TypeReference(apply.DeclaringType.Namespace, apply.DeclaringType.Name, module, scope);
        var call = new MethodReference(apply.Name, module.TypeSystem.Void, owner);
        call.Parameters.Add(new ParameterDefinition(module.GetType("TMPro.TMP_Text")));
        module.Resources.Add(new EmbeddedResource(ResourceName, ManifestResourceAttributes.Private, plans));
        foreach (var method in Methods(module))
        {
            var (branch, join) = Join(method);
            var il = method.Body.GetILProcessor();
            var load = Instruction.Create(OpCodes.Ldarg_0);
            il.InsertBefore(join, load);
            il.InsertBefore(join, Instruction.Create(OpCodes.Call, call));
            branch.Operand = load;
        }
    }

    // Normalize the verified insertion when comparing against stock IL.
    internal static (Instruction Load, Instruction Call, Instruction Join)? Inspect(MethodDefinition method)
    {
        if (method.Name != "GenerateTextMesh" || !Renderers.Contains(method.DeclaringType.FullName))
            return null;
        var (_, load) = Join(method);
        var call = load.Next;
        if (load.OpCode != OpCodes.Ldarg_0 || call.OpCode != OpCodes.Call ||
            (call.Operand as MethodReference)?.FullName != ApplyName)
            throw new InvalidDataException("Unexpected TMP renderer hook");
        return (load, call, call.Next);
    }

    private static IEnumerable<MethodDefinition> Methods(ModuleDefinition module) =>
        Renderers.Select(name => module.GetType(name).Methods.Single(m => m.Name == "GenerateTextMesh"));

    private static (Instruction Branch, Instruction Join) Join(MethodDefinition method)
    {
        var field = method.Body.Instructions.Single(i => i.OpCode == OpCodes.Ldfld &&
            i.Operand is FieldReference f && f.Name == "OnPreRenderText");
        var duplicate = field.Next;
        var whenSubscribed = duplicate.Next;
        var pop = whenSubscribed.Next;
        var branch = pop.Next;
        if (duplicate.OpCode != OpCodes.Dup || whenSubscribed.OpCode != OpCodes.Brtrue_S ||
            pop.OpCode != OpCodes.Pop || branch.OpCode != OpCodes.Br_S ||
            whenSubscribed.Operand != branch.Next || branch.Operand is not Instruction join ||
            join.Previous.OpCode != OpCodes.Callvirt ||
            join.Previous.Operand is not MethodReference invoke || invoke.Name != "Invoke")
            throw new InvalidDataException("Unexpected TMP render event branch");
        return (branch, join);
    }
}
