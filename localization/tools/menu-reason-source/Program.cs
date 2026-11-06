using System.Security.Cryptography;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 2 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: menu-reason-source macos|windows Assembly-CSharp.dll");
string Sha(byte[] data) => Convert.ToHexString(SHA256.HashData(data)).ToLowerInvariant();
var hashes = new Dictionary<string, string> {
    ["macos"] = "f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb",
    ["windows"] = "8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2"
};
var bytes = File.ReadAllBytes(args[1]);
if (Sha(bytes) != hashes[args[0]]) throw new InvalidOperationException("Unsupported source assembly");
if (Sha(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
using var module = ModuleDefinition.ReadModule(new MemoryStream(bytes));
IEnumerable<TypeDefinition> All(IEnumerable<TypeDefinition> types) {
    foreach (var type in types) { yield return type; foreach (var child in All(type.NestedTypes)) yield return child; }
}
var all = All(module.Types).ToArray();
var menu = all.Single(x => x.FullName == "MenuSlotsNew").Methods.Single(x => x.Name == "OnEvent" && x.HasBody);
var code = menu.Body.Instructions;
var occurrences = code.Select((ins, i) => (ins, i)).Where(x => x.ins.OpCode.Code == Code.Ldstr && (string)x.ins.Operand == "Delete Save?").ToArray();
if (occurrences.Length != 3) throw new InvalidOperationException("Unexpected reason occurrences");
foreach (var (ins, i) in occurrences) {
    if (i < 1 || i + 3 >= code.Count || code[i - 1].OpCode.Code != Code.Ldstr || (string)code[i - 1].Operand != "Menu_DeleteSave" ||
        code[i + 1].OpCode.Code != Code.Ldstr || (string)code[i + 1].Operand != "PlayGame" ||
        code[i + 2].OpCode.Code != Code.Newobj || ((MethodReference)code[i + 2].Operand).DeclaringType.Name != "MenuTransitionDataLevelLoad" ||
        code[i + 3].OpCode.Code != Code.Newobj || ((MethodReference)code[i + 3].Operand).FullName !=
            "System.Void MenuResponseTransition::.ctor(System.String,System.String,MenuTransitionData)")
        throw new InvalidOperationException($"Unexpected transition arguments at {ins.Offset}");
}
var transition = all.Single(x => x.FullName == "MenuResponseTransition");
var ctor = transition.Methods.Single(x => x.IsConstructor && x.Parameters.Count == 3 && x.HasBody);
var store = ctor.Body.Instructions.Select((ins, i) => (ins, i)).Single(x => x.ins.OpCode.Code == Code.Stfld &&
    x.ins.Operand is FieldReference f && f.FullName == "System.String MenuResponseTransition::reason");
if (store.i == 0 || ctor.Body.Instructions[store.i - 1].OpCode.Code != Code.Ldarg_2)
    throw new InvalidOperationException("Transition reason is not the second constructor argument");
var accesses = new List<string>();
var calls = new List<string>();
foreach (var type in all) foreach (var method in type.Methods.Where(m => m.HasBody)) foreach (var ins in method.Body.Instructions) {
    if (ins.Operand is FieldReference f && f.FullName == "System.String MenuResponseTransition::reason")
        accesses.Add($"{method.FullName} IL_{ins.Offset:x4} {ins.OpCode}");
    if (ins.Operand is MethodReference m && m.Name == "GetReason")
        calls.Add($"{method.FullName} IL_{ins.Offset:x4} {m.FullName}");
}
accesses.Sort(StringComparer.Ordinal); calls.Sort(StringComparer.Ordinal);
var report = new { schema = 1, platform = args[0], assemblySha256 = hashes[args[0]],
    transitionReasonLiteral = "Delete Save?", occurrenceOffsets = occurrences.Select(x => x.ins.Offset).ToArray(),
    destination = "Menu_DeleteSave", reasonFieldAccesses = accesses, getReasonReferences = calls,
    limitations = "Static direct IL references in one pinned game assembly; reflection, other assemblies and runtime visibility are not established." };
Console.WriteLine(JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true }));
