using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 2 || args[0] is not ("macos" or "windows"))
    throw new ArgumentException("Usage: input-action-source macos|windows ORIGINAL_ASSEMBLY_CSHARP");
string Hash(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
var expected = new Dictionary<string, string> {
    ["macos"] = "f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb",
    ["windows"] = "8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2"
};
var bytes = File.ReadAllBytes(args[1]);
if (Hash(bytes) != expected[args[0]]) throw new InvalidOperationException("Unsupported game assembly");
if (Hash(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
using var module = ModuleDefinition.ReadModule(new MemoryStream(bytes));
var ctor = module.Types.Single(t => t.FullName == "InputSystem_Actions").Methods.Single(m => m.Name == ".ctor" && m.HasBody);
var code = ctor.Body.Instructions;
var strings = code.Select((instruction, index) => (instruction, index)).Where(x => x.instruction.OpCode.Code == Code.Ldstr).ToArray();
if (strings.Length != 28) throw new InvalidOperationException("Unexpected input constructor string count");
var first = strings[0];
if (code[first.index + 1].OpCode.Code != Code.Call || code[first.index + 1].Operand is not MethodReference loader ||
    loader.FullName != "UnityEngine.InputSystem.InputActionAsset UnityEngine.InputSystem.InputActionAsset::FromJson(System.String)")
    throw new InvalidOperationException("Unexpected input JSON consumer");
string sourceJson = (string)first.instruction.Operand;
using var json = JsonDocument.Parse(sourceJson);
var maps = new Dictionary<string, HashSet<string>>(StringComparer.Ordinal);
foreach (var map in json.RootElement.GetProperty("maps").EnumerateArray()) {
    string name = map.GetProperty("name").GetString();
    var actions = new HashSet<string>(StringComparer.Ordinal);
    foreach (var action in map.GetProperty("actions").EnumerateArray())
        if (!actions.Add(action.GetProperty("name").GetString())) throw new InvalidOperationException("Duplicate action name");
    if (!maps.TryAdd(name, actions)) throw new InvalidOperationException("Duplicate map name");
}
var references = new List<object>();
string currentMap = null;
foreach (var item in strings.Skip(1)) {
    if (code[item.index + 1].OpCode.Code != Code.Ldc_I4_1 || code[item.index + 2].OpCode.Code != Code.Callvirt ||
        code[item.index + 2].Operand is not MethodReference called)
        throw new InvalidOperationException("Unexpected action lookup sequence");
    string name = (string)item.instruction.Operand;
    string role;
    if (called.FullName == "UnityEngine.InputSystem.InputActionMap UnityEngine.InputSystem.InputActionAsset::FindActionMap(System.String,System.Boolean)") {
        if (!maps.ContainsKey(name)) throw new InvalidOperationException("Referenced map missing from input JSON");
        currentMap = name; role = "map-key";
    } else if (called.FullName == "UnityEngine.InputSystem.InputAction UnityEngine.InputSystem.InputActionMap::FindAction(System.String,System.Boolean)") {
        if (currentMap == null || !maps[currentMap].Contains(name)) throw new InvalidOperationException("Referenced action missing from input map");
        role = "action-key";
    } else throw new InvalidOperationException("Unexpected input lookup method");
    references.Add(new { id = ctor.FullName + "#ldstr:" + (references.Count + 1), name, map = currentMap,
                         offset = item.instruction.Offset, consumer = called.FullName, role });
}
Console.WriteLine(JsonSerializer.Serialize(new { schema = 1, platform = args[0], assemblySha256 = expected[args[0]],
    jsonLiteral = new { id = ctor.FullName + "#ldstr:0", offset = first.instruction.Offset,
                        utf8Sha256 = Hash(Encoding.UTF8.GetBytes(sourceJson)), characters = sourceJson.Length,
                        consumer = loader.FullName, role = "preserve-exactly-input-config" },
    mapCount = maps.Count, actionCount = maps.Sum(x => x.Value.Count), references,
    limitations = "Static pinned constructor and embedded JSON only. User-visible input hints, dynamic remapping, other input assets and runtime behavior remain unverified." },
    new JsonSerializerOptions { WriteIndented = true }));
