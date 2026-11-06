using System.Security.Cryptography;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 2 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: speaker-presentation-flow macos|windows YARN_UNITY_DLL");
string Sha(byte[] b) => Convert.ToHexString(SHA256.HashData(b)).ToLowerInvariant();
var expected = new Dictionary<string, string> {
    ["macos"] = "54953f9c071aa3ca5b52eb8b12b8e0bedc73f7665a506c61acbef0c58ac340ef",
    ["windows"] = "3d5def40f51540e79dbb6a897993fe006022cf1f16933a1b47a69334085ad89d"
};
if (Sha(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
var input = File.ReadAllBytes(args[1]);
if (Sha(input) != expected[args[0]]) throw new InvalidOperationException("Unsupported Yarn Unity DLL");
using var module = ModuleDefinition.ReadModule(new MemoryStream(input));
var segments = new List<object>();
foreach (var selection in new[] {
    (type: "Yarn.Unity.LinePresenter", state: "<RunLineAsync>d__23", first: 0x7f, last: 0x11c),
    (type: "Yarn.Unity.OptionsPresenter", state: "<RunOptionsAsync>d__18", first: 0x1db, last: 0x290)
}) {
    var method = module.Types.Single(t => t.FullName == selection.type).NestedTypes
        .Single(t => t.Name == selection.state).Methods.Single(m => m.Name == "MoveNext" && m.HasBody);
    var instructions = method.Body.Instructions.Where(i => i.Offset >= selection.first && i.Offset <= selection.last).ToArray();
    if (instructions.Length == 0 || instructions[0].Offset != selection.first || instructions[^1].Offset != selection.last)
        throw new InvalidOperationException("Unexpected presenter instruction bounds");
    segments.Add(new { method = method.FullName, instructions = instructions.Select(i => new {
        offset = i.Offset, opcode = i.OpCode.Name,
        operand = i.Operand is Instruction target ? $"IL_{target.Offset:x4}" : i.Operand?.ToString()
    }).ToArray() });
}
Console.WriteLine(JsonSerializer.Serialize(new { schema = 1, platform = args[0], sourceSha256 = expected[args[0]], segments,
    limitations = "Static instruction slices only; serialized defaults and runtime mutations are separate evidence. No rendering, reachability, complete metadata, dynamic consumers or game execution is established." },
    new JsonSerializerOptions { WriteIndented = true }));
