using System.Security.Cryptography;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

const string CecilSha = "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf";
var builds = new Dictionary<string, string> {
    ["macos"] = "f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb",
    ["windows"] = "8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2",
    ["macos-settings"] = "a16b7a3a94bd62e059694a311f68dec012aa66696a6eff9880ceb9087e6c915d",
    ["windows-settings"] = "b6f215bc0eef09035d800a2fab01bed0a8ffeba8f85ba00cfb329ebf009c1f90",
    ["macos-yarn-unity"] = "54953f9c071aa3ca5b52eb8b12b8e0bedc73f7665a506c61acbef0c58ac340ef",
    ["windows-yarn-unity"] = "3d5def40f51540e79dbb6a897993fe006022cf1f16933a1b47a69334085ad89d",
    ["macos-tmp"] = "a25a11167a5a7339d611c364a6525fc172d19fe5caa6aa95d6866fd1d36d0743",
    ["windows-tmp"] = "e22d8f83e97d0a27bed0480cfd52d13a6b26b1e74e3ad67e6a17316090ec3f9f",
    ["macos-unity-ui"] = "34d58694fe13e5b9e49407a541e358277d13b0da4d864d28793ac18094e2bac4",
    ["windows-unity-ui"] = "e31bf1ba3ebcd9e63c1c8530d6be7799b079c4f9a5dcc29a695e4be5b26aa613"
};
string Hash(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
if (args.Length < 2 || args.Length > 3 || !builds.ContainsKey(args[0]) ||
    (args.Length == 3 && args[2] != "--context"))
    throw new ArgumentException("Usage: managed-strings <pinned-build-key> <original managed DLL> [--context]");
bool includeContext = args.Length == 3;
if (Hash(File.ReadAllBytes(typeof(AssemblyDefinition).Assembly.Location)) != CecilSha)
    throw new InvalidOperationException("Unsupported Mono.Cecil binary");
var bytes = File.ReadAllBytes(args[1]);
if (Hash(bytes) != builds[args[0]]) throw new InvalidOperationException("Unsupported or modified game assembly");
using var stream = new MemoryStream(bytes, writable: false);
using var asm = AssemblyDefinition.ReadAssembly(stream);
IEnumerable<TypeDefinition> Types(IEnumerable<TypeDefinition> roots) {
    foreach (var type in roots) {
        yield return type;
        foreach (var nested in Types(type.NestedTypes)) yield return nested;
    }
}
var records = new List<object>();
var identities = new HashSet<string>();
foreach (var type in Types(asm.MainModule.Types))
foreach (var method in type.Methods.Where(x => x.HasBody)) {
    int ordinal = 0;
    var instructions = method.Body.Instructions;
    for (int index = 0; index < instructions.Count; index++) {
        var ins = instructions[index];
        if (ins.OpCode.Code != Code.Ldstr) continue;
        if (ins.Operand is not string value) throw new InvalidOperationException("Invalid ldstr operand");
        var id = method.FullName + "#ldstr:" + ordinal++;
        if (!identities.Add(id)) throw new InvalidOperationException("Duplicate instruction identity");
        if (includeContext) {
            var following = instructions.Skip(index + 1).Take(12)
                .Select(x => new { offset = x.Offset, opcode = x.OpCode.Name, operand = x.Operand?.ToString() })
                .ToList();
            records.Add(new { id, method = method.FullName, methodToken = method.MetadataToken.ToInt32(),
                ilOffset = ins.Offset, value, following });
            continue;
        }
        var followingCalls = instructions.Skip(index + 1).Take(12)
            .Where(x => x.OpCode.Code is Code.Call or Code.Callvirt or Code.Newobj)
            .Select(x => new { offset = x.Offset, opcode = x.OpCode.Name, target = x.Operand?.ToString() })
            .ToList();
        records.Add(new { id, method = method.FullName, methodToken = method.MetadataToken.ToInt32(),
            ilOffset = ins.Offset, value, followingCalls });
    }
}
var output = new { schema = 1, platform = args[0], assemblySha256 = builds[args[0]],
    cecilSha256 = CecilSha, sourceInstructionCount = records.Count, strings = records,
    limitations = includeContext
        ? "Only ldstr instructions and their following instruction windows in the selected pinned assembly. These windows do not prove general dataflow or runtime visibility."
        : "Only ldstr instructions in the selected pinned managed assembly. Following calls are nearby instructions, not proven dataflow. No reachability, display role, generated strings, other assemblies, assets or reflection paths are classified." };
Console.WriteLine(JsonSerializer.Serialize(output, new JsonSerializerOptions { WriteIndented = true }));
