using System.Security.Cryptography;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 2 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: objective-source macos|windows Assembly-CSharp.dll");
string Sha(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
var hashes = new Dictionary<string, string> {
    ["macos"] = "f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb",
    ["windows"] = "8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2"
};
var input = File.ReadAllBytes(args[1]);
if (Sha(input) != hashes[args[0]]) throw new InvalidOperationException("Unsupported source assembly");
if (Sha(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
using var module = ModuleDefinition.ReadModule(new MemoryStream(input));
TypeDefinition Type(string name) => module.Types.Single(x => x.FullName == name);
MethodDefinition Method(string type, string method) => Type(type).Methods.Single(x => x.Name == method && x.HasBody);
var expected = new Dictionary<string, string> {
    ["Objective"] = "DEFAULT", ["ObjectiveDirty"] = "DIRTY",
    ["ObjectiveSoapy"] = "SOAPY", ["ObjectiveTooBright"] = "TOO BRIGHT"
};
foreach (var (typeName, value) in expected) {
    var type = Type(typeName);
    if (typeName != "Objective" && type.BaseType.FullName != "Objective") throw new InvalidOperationException("Unexpected base type");
    var method = Method(typeName, "GetName");
    var code = method.Body.Instructions;
    if (method.ReturnType.FullName != "System.String" || code.Count != 2 || code[0].OpCode.Code != Code.Ldstr ||
        (string)code[0].Operand != value || code[1].OpCode.Code != Code.Ret)
        throw new InvalidOperationException($"Unexpected GetName implementation: {typeName}");
}
var created = Method("ObjectiveManager", "Start").Body.Instructions
    .Where(x => x.OpCode.Code == Code.Newobj && x.Operand is MethodReference m && m.DeclaringType.Name.StartsWith("Objective"))
    .Select(x => ((MethodReference)x.Operand).DeclaringType.Name).ToArray();
if (!created.SequenceEqual(new[] { "ObjectiveDirty", "ObjectiveSoapy", "ObjectiveTooBright" }))
    throw new InvalidOperationException("Unexpected objective construction");
var display = Method("ObjectiveDisplay", "SetObjective").Body.Instructions;
if (Type("ObjectiveDisplay").Fields.Single(x => x.Name == "objectiveText").FieldType.FullName != "TMPro.TextMeshPro")
    throw new InvalidOperationException("Unexpected objective text field type");
var chain = display.Select((x, i) => (x, i)).Where(pair => pair.x.Operand is MethodReference m &&
    m.FullName == "System.String Objective::GetName()").ToArray();
if (chain.Length != 1 || chain[0].x.OpCode.Code != Code.Callvirt || chain[0].i + 1 >= display.Count ||
    display[chain[0].i + 1].OpCode.Code != Code.Callvirt ||
    ((MethodReference)display[chain[0].i + 1].Operand).FullName != "System.Void TMPro.TMP_Text::set_text(System.String)")
    throw new InvalidOperationException("Unexpected objective display chain");
var report = new { schema = 1, platform = args[0], assemblySha256 = hashes[args[0]],
    objectiveNames = expected, constructedInStart = created,
    displayGetNameOffset = chain[0].x.Offset, displaySetTextOffset = display[chain[0].i + 1].Offset,
    limitations = "Pinned Assembly-CSharp static IL only; runtime construction, presentation, dynamic types and other assemblies require separate review." };
Console.WriteLine(JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true }));
