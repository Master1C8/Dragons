using System.Globalization;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 3 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: slot-code-probe macos|windows SOURCE_DLL FRESH_WORK_OUTPUT_DLL");
string Hash(byte[] b) => Convert.ToHexString(SHA256.HashData(b)).ToLowerInvariant();
var sourceHashes = new Dictionary<string,string> {
    ["macos"] = "f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb",
    ["windows"] = "8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2"
};
if (Hash(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
var bytes = File.ReadAllBytes(args[1]);
if (Hash(bytes) != sourceHashes[args[0]]) throw new InvalidOperationException("Unsupported source assembly");
string work = Path.GetFullPath(Path.Combine(Directory.GetCurrentDirectory(), "localization", "work"));
string output = Path.GetFullPath(args[2]);
if (!Directory.Exists(work) || (File.GetAttributes(work) & FileAttributes.ReparsePoint) != 0 ||
    Path.GetDirectoryName(output) != work || Path.GetExtension(output) != ".dll")
    throw new InvalidOperationException("Output must be a fresh DLL directly in project work");
if (File.Exists(output)) throw new InvalidOperationException("Output already exists");
const string marker = "ЖЪЬ42"; // Synthetic sample only; never a game translation.
const string setter = "System.Void TMPro.TMP_Text::set_text(System.String)";
using var module = ModuleDefinition.ReadModule(new MemoryStream(bytes));
var method = module.Types.Single(t => t.FullName == "MenuSlotsNew").Methods.Single(m => m.Name == "OnShow" && m.HasBody);
var offsets = new[] { 0x85, 0x101, 0x17c };
var sites = new HashSet<int>();
foreach (var (offset, slot) in offsets.Select((o, i) => (o, i + 1))) {
    var instruction = method.Body.Instructions.Single(i => i.Offset == offset);
    if (instruction.OpCode.Code != Code.Ldstr || (string)instruction.Operand != "NEW" ||
        instruction.Previous?.Operand is not FieldReference field || field.FullName != $"TMPro.TextMeshProUGUI MenuSlotsNew::slot{slot}Progress" ||
        instruction.Next?.OpCode.Code != Code.Callvirt || instruction.Next.Operand is not MethodReference call || call.FullName != setter)
        throw new InvalidOperationException("Unexpected slot text binding");
    sites.Add(method.Body.Instructions.IndexOf(instruction));
    instruction.Operand = marker;
}
IEnumerable<TypeDefinition> All(IEnumerable<TypeDefinition> types) {
    foreach (var type in types) { yield return type; foreach (var nested in All(type.NestedTypes)) yield return nested; }
}
string Operand(object value, Dictionary<Instruction,int> indices) => value switch {
    null => "", Instruction i => "target:" + indices[i], Instruction[] a => "targets:" + string.Join(",", a.Select(x => indices[x])),
    VariableDefinition v => "local:" + v.Index, ParameterDefinition p => "param:" + p.Index,
    MemberReference m => "member:" + m.FullName, IFormattable f => f.ToString(null, CultureInfo.InvariantCulture), _ => value.ToString()
};
Dictionary<string,string> Bodies(ModuleDefinition source, bool patched) {
    var result = new Dictionary<string,string>(StringComparer.Ordinal);
    foreach (var type in All(source.Types)) foreach (var m in type.Methods.Where(m => m.HasBody)) {
        var code = m.Body.Instructions;
        var indices = code.Select((ins, i) => (ins, i)).ToDictionary(x => x.ins, x => x.i);
        var text = new StringBuilder();
        text.Append(m.Body.InitLocals).Append('|').Append(m.Body.MaxStackSize).Append('|');
        foreach (var v in m.Body.Variables) text.Append(v.VariableType.FullName).Append(';');
        foreach (var h in m.Body.ExceptionHandlers) text.Append("EH:").Append(h.HandlerType).Append(':')
            .Append(h.TryStart == null ? -1 : indices[h.TryStart]).Append(':').Append(h.TryEnd == null ? -1 : indices[h.TryEnd]).Append(':')
            .Append(h.HandlerStart == null ? -1 : indices[h.HandlerStart]).Append(':').Append(h.HandlerEnd == null ? -1 : indices[h.HandlerEnd]).Append(':')
            .Append(h.FilterStart == null ? -1 : indices[h.FilterStart]).Append(':').Append(h.CatchType?.FullName).Append(';');
        for (int i = 0; i < code.Count; i++) {
            var ins = code[i];
            if (m.FullName == method.FullName && sites.Contains(i)) {
                if (ins.OpCode.Code != Code.Ldstr || (string)ins.Operand != (patched ? marker : "NEW"))
                    throw new InvalidOperationException("Unexpected source or output slot text");
                text.Append("<verified-slot-sample>;");
            } else text.Append(ins.OpCode.Name).Append(':').Append(Operand(ins.Operand, indices)).Append(';');
        }
        if (!result.TryAdd(m.FullName, text.ToString())) throw new InvalidOperationException("Ambiguous method identity");
    }
    return result;
}
using var memory = new MemoryStream(); module.Write(memory); var built = memory.ToArray();
using var original = ModuleDefinition.ReadModule(new MemoryStream(bytes));
using var rebuilt = ModuleDefinition.ReadModule(new MemoryStream(built));
var before = Bodies(original, false); var after = Bodies(rebuilt, true);
if (before.Count != after.Count || before.Any(kv => !after.TryGetValue(kv.Key, out var v) || v != kv.Value))
    throw new InvalidOperationException("Unintended change in existing method bodies");
string tmp = Path.Combine(work, ".slot-code-probe-" + Guid.NewGuid().ToString("N") + ".tmp");
try {
    using (var file = new FileStream(tmp, FileMode.CreateNew, FileAccess.Write, FileShare.None)) { file.Write(built); file.Flush(true); }
    File.Move(tmp, output, false);
} finally { if (File.Exists(tmp)) File.Delete(tmp); }
Console.WriteLine(JsonSerializer.Serialize(new { schema = 1, testOnly = true, platform = args[0],
    sourceSha256 = sourceHashes[args[0]], outputSha256 = Hash(built), changedOffsets = offsets, verifiedExistingMethodBodies = before.Count,
    limitations = "Synthetic test DLL only. No full metadata equivalence, runtime display, save behavior, localization package or player installation is established." }));
