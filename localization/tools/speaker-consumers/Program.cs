using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Mono.Cecil;

if (args.Length != 2 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: speaker-consumers macos|windows MANAGED_DIR");
string Sha(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
var expected = new Dictionary<string, string> {
    ["macos"] = "b3186bc39207255e937f5856be09906dc1a428d83a964d5f368f30861e32603c",
    ["windows"] = "9a14fcb1198ca8308ad90a38a1988367074c1f2ec8b6f0a8d97ef3d3c074fc56"
};
if (Sha(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
var files = Directory.GetFiles(args[1]).Where(p => p.EndsWith(".dll", StringComparison.Ordinal))
    .OrderBy(p => Path.GetFileName(p), StringComparer.Ordinal).Select(p => (name: Path.GetFileName(p), bytes: File.ReadAllBytes(p))).ToArray();
if (files.Any(f => f.name.Any(c => c > 127))) throw new InvalidOperationException("Non-ASCII managed filename requires explicit ordering review");
var manifest = string.Concat(files.Select(f => $"{f.name}|{Sha(f.bytes)}\n"));
var manifestHash = Sha(Encoding.UTF8.GetBytes(manifest));
if (manifestHash != expected[args[0]]) throw new InvalidOperationException("Unsupported managed assembly inventory");
IEnumerable<TypeDefinition> All(IEnumerable<TypeDefinition> input) {
    foreach (var type in input) { yield return type; foreach (var child in All(type.NestedTypes)) yield return child; }
}
var hits = new List<object>();
object awakeNameSetup = null;
foreach (var file in files) {
    using var module = ModuleDefinition.ReadModule(new MemoryStream(file.bytes));
    if (file.name == "YarnSpinner.Unity.dll") {
        var presenter = module.Types.Single(t => t.FullName == "Yarn.Unity.LinePresenter");
        var awake = presenter.Methods.Single(m => m.Name == "Awake" && m.HasBody);
        var selected = awake.Body.Instructions.Where(i => i.Offset <= 0x28).ToArray();
        if (!selected.Any(i => i.OpCode.Code == Mono.Cecil.Cil.Code.Callvirt && i.Operand is MethodReference m &&
                               m.FullName == "UnityEngine.GameObject UnityEngine.Component::get_gameObject()") ||
            !selected.Any(i => i.OpCode.Code == Mono.Cecil.Cil.Code.Stfld && i.Operand is FieldReference f &&
                               f.FullName == "UnityEngine.GameObject Yarn.Unity.LinePresenter::characterNameContainer"))
            throw new InvalidOperationException("Unexpected presenter Awake name setup");
        awakeNameSetup = selected.Select(i => new { offset = i.Offset, opcode = i.OpCode.Name,
                                                    operand = i.Operand?.ToString() }).ToArray();
    }
    foreach (var type in All(module.Types)) foreach (var method in type.Methods.Where(m => m.HasBody)) {
        var code = method.Body.Instructions;
        for (var i = 0; i < code.Count; i++) {
            var instruction = code[i];
            if (instruction.Operand is MethodReference called &&
                called.FullName == "System.String Yarn.Unity.LocalizedLine::get_CharacterName()") {
                var next = i + 1 < code.Count ? code[i + 1] : null;
                hits.Add(new { assembly = file.name, method = method.FullName, offset = instruction.Offset,
                    opcode = instruction.OpCode.Name, nextOpcode = next?.OpCode.Name,
                    nextOperand = next?.Operand?.ToString() });
            }
        }
    }
}
if (awakeNameSetup is null) throw new InvalidOperationException("Missing Yarn Unity assembly");
var report = new { schema = 1, platform = args[0], assemblyCount = files.Length,
    managedInventorySha256 = manifestHash, directCharacterNameGetterReferences = hits, awakeNameSetup,
    limitations = "Direct IL references in pinned root Managed/*.dll only. Reflection, dynamically loaded assemblies, parsed text access without this getter, other assets and runtime mutation are not covered." };
Console.WriteLine(JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true }));
