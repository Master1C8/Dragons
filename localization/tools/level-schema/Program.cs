using System.Security.Cryptography;
using Mono.Cecil;

if (args.Length != 2 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: level-schema macos|windows Assembly-CSharp.dll");
string Sha(byte[] data) => Convert.ToHexString(SHA256.HashData(data)).ToLowerInvariant();
var assemblyHashes = new Dictionary<string, string> {
    ["macos"] = "f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb",
    ["windows"] = "8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2"
};
var input = File.ReadAllBytes(args[1]);
if (Sha(input) != assemblyHashes[args[0]]) throw new InvalidOperationException("Unsupported source assembly");
if (Sha(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
using var module = ModuleDefinition.ReadModule(new MemoryStream(input));
var type = module.Types.Single(x => x.FullName == "LevelConfiguration");
if (type.BaseType.FullName != "UnityEngine.ScriptableObject") throw new InvalidOperationException("Unexpected base type");
var arrays = new[] { "setFlags", "endFlags", "progressDialogs", "idleDialogs", "nagDialogs" };
foreach (var name in arrays) {
    var field = type.Fields.Single(x => x.Name == name);
    if (field.FieldType.FullName != "System.String[]" || field.IsStatic ||
        !field.CustomAttributes.Any(x => x.AttributeType.FullName == "UnityEngine.SerializeField"))
        throw new InvalidOperationException($"Unexpected array field: {name}");
    Console.WriteLine($"{field.Name}: {field.FieldType.FullName}, SerializeField");
}
