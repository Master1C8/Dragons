using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 2 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: text-setter-consumers macos|windows MANAGED_DIR");
string Sha(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
var expected = new Dictionary<string, string> {
    ["macos"] = "b3186bc39207255e937f5856be09906dc1a428d83a964d5f368f30861e32603c",
    ["windows"] = "9a14fcb1198ca8308ad90a38a1988367074c1f2ec8b6f0a8d97ef3d3c074fc56"
};
if (Sha(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
var files = Directory.GetFiles(args[1]).Where(p => p.EndsWith(".dll", StringComparison.Ordinal))
    .OrderBy(p => Path.GetFileName(p), StringComparer.Ordinal)
    .Select(p => (name: Path.GetFileName(p), bytes: File.ReadAllBytes(p))).ToArray();
if (files.Any(f => f.name.Any(c => c > 127))) throw new InvalidOperationException("Non-ASCII filename requires ordering review");
var manifestHash = Sha(Encoding.UTF8.GetBytes(string.Concat(files.Select(f => $"{f.name}|{Sha(f.bytes)}\n"))));
if (manifestHash != expected[args[0]]) throw new InvalidOperationException("Unsupported managed assembly inventory");
IEnumerable<TypeDefinition> All(IEnumerable<TypeDefinition> ts) {
    foreach (var t in ts) { yield return t; foreach (var n in All(t.NestedTypes)) yield return n; }
}
var hits = new List<object>();
var factoryHits = new List<object>();
var dropdownFieldHits = new List<object>();
var multiSelectHits = new List<object>();
foreach (var file in files) {
    using var module = ModuleDefinition.ReadModule(new MemoryStream(file.bytes));
    foreach (var type in All(module.Types)) foreach (var method in type.Methods.Where(m => m.HasBody)) {
        var ins = method.Body.Instructions;
        for (int index = 0; index < ins.Count; index++) {
            var i = ins[index];
            if (i.Operand is MethodReference selector && selector.DeclaringType.FullName == "TMPro.TMP_Dropdown" && selector.Name == "set_MultiSelect")
                multiSelectHits.Add(new { assembly = file.name, method = method.FullName, offset = i.Offset, opcode = i.OpCode.Name, member = selector.FullName });
            if (i.Operand is FieldReference mode && mode.DeclaringType.FullName == "TMPro.TMP_Dropdown" && mode.Name == "m_MultiSelect")
                multiSelectHits.Add(new { assembly = file.name, method = method.FullName, offset = i.Offset, opcode = i.OpCode.Name, member = mode.FullName });
            if (i.OpCode.Code is Code.Call or Code.Callvirt && i.Operand is MethodReference factory &&
                (factory.DeclaringType.FullName == "TMPro.TMP_DefaultControls" ||
                 factory.DeclaringType.FullName == "UnityEngine.UI.DefaultControls") && factory.Name.StartsWith("Create", StringComparison.Ordinal))
                factoryHits.Add(new { assembly = file.name, method = method.FullName, offset = i.Offset, factory = factory.FullName });
            if (i.Operand is FieldReference field && field.DeclaringType.FullName == "TMPro.TMP_Dropdown" &&
                (field.Name == "k_NothingOption" || field.Name == "k_EverythingOption" || field.Name == "k_MixedOption"))
                dropdownFieldHits.Add(new { assembly = file.name, method = method.FullName, offset = i.Offset,
                    opcode = i.OpCode.Name, field = field.FullName });
            if (i.OpCode.Code is not (Code.Call or Code.Callvirt) || i.Operand is not MethodReference target ||
                target.Name != "set_text" || target.ReturnType.FullName != "System.Void" ||
                target.Parameters.Count != 1 || target.Parameters[0].ParameterType.FullName != "System.String") continue;
            var preceding = ins.Skip(Math.Max(0, index - 4)).Take(Math.Min(index, 4)).Select(p => new {
                offset = p.Offset, opcode = p.OpCode.Name,
                operand = p.Operand is Instruction branch ? $"IL_{branch.Offset:x4}" : p.Operand?.ToString()
            }).ToArray();
            hits.Add(new { assembly = file.name, method = method.FullName, offset = i.Offset,
                setter = target.FullName, preceding });
        }
    }
}
Console.WriteLine(JsonSerializer.Serialize(new { schema = 1, platform = args[0], assemblyCount = files.Length,
    managedInventorySha256 = manifestHash, sites = hits, defaultControlFactoryCallSites = factoryHits,
    selectedDropdownFieldReferences = dropdownFieldHits, multiSelectReferences = multiSelectHits,
    limitations = "Direct calls to a one-string set_text method in pinned root Managed DLLs only. The preceding instruction window is not dataflow and does not establish visibility, ownership, or all textual sinks. Reflection, dynamic assemblies, non-setter paths, serialized strings and native code remain outside scope." },
    new JsonSerializerOptions { WriteIndented = true }));
