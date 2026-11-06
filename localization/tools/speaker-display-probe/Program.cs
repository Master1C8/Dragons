using System.Globalization;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 4 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: speaker-display-probe macos|windows SOURCE_DLL SYNTHETIC_MAP_JSON OUTPUT_DLL");
string Sha(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
var expectedHashes = new Dictionary<string, string> {
    ["macos"] = "54953f9c071aa3ca5b52eb8b12b8e0bedc73f7665a506c61acbef0c58ac340ef",
    ["windows"] = "3d5def40f51540e79dbb6a897993fe006022cf1f16933a1b47a69334085ad89d"
};
var sourceBytes = File.ReadAllBytes(args[1]);
if (Sha(sourceBytes) != expectedHashes[args[0]]) throw new InvalidOperationException("Unsupported source DLL");
if (Sha(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
string work = Path.GetFullPath(Path.Combine(Directory.GetCurrentDirectory(), "localization", "work"));
if (!Directory.Exists(work) || (File.GetAttributes(work) & FileAttributes.ReparsePoint) != 0)
    throw new InvalidOperationException("Expected a real project work directory");
string output = Path.GetFullPath(args[3]);
if (Path.GetDirectoryName(output) != work || Path.GetExtension(output) != ".dll")
    throw new InvalidOperationException("Output must be a fresh DLL directly in project work");
using var json = JsonDocument.Parse(File.ReadAllBytes(args[2]));
if (json.RootElement.ValueKind != JsonValueKind.Object) throw new InvalidOperationException("Invalid mapping document");
var rootFields = json.RootElement.EnumerateObject().ToArray();
if (rootFields.Length != 3 || rootFields.Select(x => x.Name).Distinct().Count() != 3 ||
    !rootFields.Select(x => x.Name).OrderBy(x => x).SequenceEqual(new[] { "locale", "map", "schema" }))
    throw new InvalidOperationException("Unexpected mapping fields");
if (json.RootElement.GetProperty("schema").GetInt32() != 1 || json.RootElement.GetProperty("locale").GetString() != "ru")
    throw new InvalidOperationException("Unsupported mapping identity");
var mapElement = json.RootElement.GetProperty("map");
if (mapElement.ValueKind != JsonValueKind.Object) throw new InvalidOperationException("Mapping must be an object");
var map = new Dictionary<string, string>(StringComparer.Ordinal);
foreach (var item in mapElement.EnumerateObject()) {
    if ((item.Name != "Ryan" && item.Name != "Conrad") || item.Value.ValueKind != JsonValueKind.String ||
        !map.TryAdd(item.Name, item.Value.GetString())) throw new InvalidOperationException("Invalid or duplicate source speaker");
    var text = map[item.Name];
    if (string.IsNullOrWhiteSpace(text) || text.Length > 40 || text.Any(c => char.IsControl(c) || "<>[]{}:".Contains(c)))
        throw new InvalidOperationException("Invalid display label");
}
if (map.Count != 2) throw new InvalidOperationException("Both known speaker mappings are required");

IEnumerable<TypeDefinition> All(IEnumerable<TypeDefinition> types) {
    foreach (var type in types) { yield return type; foreach (var child in All(type.NestedTypes)) yield return child; }
}
const string Getter = "System.String Yarn.Unity.LocalizedLine::get_CharacterName()";
const string Setter = "System.Void TMPro.TMP_Text::set_text(System.String)";
const string HelperType = "Yarn.Unity.VnSyntheticSpeakerDisplay";
using var module = ModuleDefinition.ReadModule(new MemoryStream(sourceBytes));
if (module.Types.Any(t => t.FullName == HelperType)) throw new InvalidOperationException("Helper already exists");
var all = All(module.Types).ToArray();
var nameType = module.Types.Single(t => t.FullName == "Yarn.Unity.LocalizedLine");
var getter = nameType.Methods.Single(m => m.FullName == Getter);
var equality = all.SelectMany(t => t.Methods).Where(m => m.HasBody).SelectMany(m => m.Body.Instructions)
    .Select(i => i.Operand).OfType<MethodReference>()
    .First(m => m.FullName == "System.Boolean System.String::op_Equality(System.String,System.String)");
var sites = new List<Instruction>();
var siteKeys = new HashSet<string>(StringComparer.Ordinal);
foreach (var type in all) foreach (var method in type.Methods.Where(m => m.HasBody)) {
    var code = method.Body.Instructions;
    for (int i = 0; i + 1 < code.Count; i++) {
        if (code[i].OpCode.Code != Code.Callvirt || code[i].Operand is not MethodReference g || g.FullName != Getter ||
            code[i + 1].OpCode.Code != Code.Callvirt || code[i + 1].Operand is not MethodReference s || s.FullName != Setter) continue;
        if (!(method.FullName.Contains("Yarn.Unity.LinePresenter/<RunLineAsync>") ||
              method.FullName.Contains("Yarn.Unity.OptionsPresenter/<RunOptionsAsync>")))
            throw new InvalidOperationException("Unexpected speaker display consumer");
        sites.Add(code[i]); siteKeys.Add(method.FullName + "#" + i);
    }
}
if (sites.Count != 2 || siteKeys.Count != 2) throw new InvalidOperationException("Expected exactly two speaker display sites");

var helperType = new TypeDefinition("Yarn.Unity", "VnSyntheticSpeakerDisplay",
    TypeAttributes.NotPublic | TypeAttributes.Abstract | TypeAttributes.Sealed | TypeAttributes.BeforeFieldInit, module.TypeSystem.Object);
var helper = new MethodDefinition("GetDisplayName", MethodAttributes.Assembly | MethodAttributes.Static | MethodAttributes.HideBySig, module.TypeSystem.String);
helper.Parameters.Add(new ParameterDefinition("line", ParameterAttributes.None, nameType));
helper.Body.InitLocals = true;
helper.Body.Variables.Add(new VariableDefinition(module.TypeSystem.String));
var il = helper.Body.GetILProcessor();
il.Append(il.Create(OpCodes.Ldarg_0)); il.Append(il.Create(OpCodes.Callvirt, getter)); il.Append(il.Create(OpCodes.Stloc_0));
foreach (var pair in map.OrderBy(x => x.Key, StringComparer.Ordinal)) {
    var next = il.Create(OpCodes.Nop);
    il.Append(il.Create(OpCodes.Ldloc_0)); il.Append(il.Create(OpCodes.Ldstr, pair.Key));
    il.Append(il.Create(OpCodes.Call, equality)); il.Append(il.Create(OpCodes.Brfalse, next));
    il.Append(il.Create(OpCodes.Ldstr, pair.Value)); il.Append(il.Create(OpCodes.Ret)); il.Append(next);
}
il.Append(il.Create(OpCodes.Ldloc_0)); il.Append(il.Create(OpCodes.Ret));
helperType.Methods.Add(helper); module.Types.Add(helperType);
foreach (var site in sites) { site.OpCode = OpCodes.Call; site.Operand = helper; }
using var buffer = new MemoryStream(); module.Write(buffer);
var outputBytes = buffer.ToArray();

// Compare all original method bodies after re-reading the emitted DLL. The two
// permitted call sites are normalized after asserting their exact old/new targets.
string Operand(object value, Dictionary<Instruction, int> indices) => value switch {
    null => "", Instruction i => "target:" + indices[i],
    Instruction[] a => "targets:" + string.Join(",", a.Select(x => indices[x])),
    VariableDefinition v => "local:" + v.Index, ParameterDefinition p => "param:" + p.Index,
    MemberReference m => "member:" + m.FullName,
    IFormattable f => f.ToString(null, CultureInfo.InvariantCulture), _ => value.ToString()
};
Dictionary<string, string> Bodies(ModuleDefinition source, bool patched) {
    var result = new Dictionary<string, string>(StringComparer.Ordinal);
    foreach (var type in All(source.Types).Where(t => t.FullName != HelperType)) foreach (var method in type.Methods.Where(m => m.HasBody)) {
        var code = method.Body.Instructions;
        var indices = code.Select((ins, i) => (ins, i)).ToDictionary(x => x.ins, x => x.i);
        var text = new StringBuilder();
        text.Append(method.Body.InitLocals).Append('|').Append(method.Body.MaxStackSize).Append('|');
        foreach (var v in method.Body.Variables) text.Append(v.VariableType.FullName).Append(';');
        foreach (var h in method.Body.ExceptionHandlers) text.Append("EH:").Append(h.HandlerType).Append(':')
            .Append(h.TryStart == null ? -1 : indices[h.TryStart]).Append(':').Append(h.TryEnd == null ? -1 : indices[h.TryEnd]).Append(':')
            .Append(h.HandlerStart == null ? -1 : indices[h.HandlerStart]).Append(':').Append(h.HandlerEnd == null ? -1 : indices[h.HandlerEnd]).Append(':')
            .Append(h.FilterStart == null ? -1 : indices[h.FilterStart]).Append(':').Append(h.CatchType?.FullName).Append(';');
        for (int i = 0; i < code.Count; i++) {
            var ins = code[i];
            if (siteKeys.Contains(method.FullName + "#" + i)) {
                string target = (ins.Operand as MethodReference)?.FullName;
                if ((!patched && (ins.OpCode.Code != Code.Callvirt || target != Getter)) ||
                    (patched && (ins.OpCode.Code != Code.Call || target != "System.String Yarn.Unity.VnSyntheticSpeakerDisplay::GetDisplayName(Yarn.Unity.LocalizedLine)")))
                    throw new InvalidOperationException("Unexpected speaker call-site rewrite");
                text.Append("<verified-speaker-call>;");
            } else text.Append(ins.OpCode.Name).Append(':').Append(Operand(ins.Operand, indices)).Append(';');
        }
        if (!result.TryAdd(method.FullName, text.ToString())) throw new InvalidOperationException("Ambiguous method identity");
    }
    return result;
}
using var original = ModuleDefinition.ReadModule(new MemoryStream(sourceBytes));
using var rebuilt = ModuleDefinition.ReadModule(new MemoryStream(outputBytes));
var before = Bodies(original, false); var after = Bodies(rebuilt, true);
if (before.Count != after.Count || before.Any(kv => !after.TryGetValue(kv.Key, out var value) || value != kv.Value))
    throw new InvalidOperationException("Unexpected change in existing method bodies");
var rebuiltHelper = rebuilt.Types.Single(t => t.FullName == HelperType).Methods.Single(m => m.Name == "GetDisplayName");
var literals = rebuiltHelper.Body.Instructions.Where(i => i.OpCode.Code == Code.Ldstr).Select(i => (string)i.Operand).ToArray();
var expectedLiterals = map.OrderBy(x => x.Key, StringComparer.Ordinal).SelectMany(x => new[] { x.Key, x.Value }).ToArray();
if (!literals.SequenceEqual(expectedLiterals)) throw new InvalidOperationException("Helper mapping read-back failed");
string temporary = Path.Combine(work, ".speaker-probe-" + Guid.NewGuid().ToString("N") + ".tmp");
try {
    using (var file = new FileStream(temporary, FileMode.CreateNew, FileAccess.Write, FileShare.None)) {
        file.Write(outputBytes);
        file.Flush(true);
    }
    File.Move(temporary, output, false);
} finally {
    if (File.Exists(temporary)) File.Delete(temporary);
}
Console.WriteLine(JsonSerializer.Serialize(new { schema = 1, testOnly = true, platform = args[0],
    sourceSha256 = expectedHashes[args[0]], outputSha256 = Sha(outputBytes), mappedSpeakers = map.Keys.OrderBy(x => x).ToArray(),
    changedDisplayCallSites = siteKeys.OrderBy(x => x).ToArray(), verifiedExistingMethodBodies = before.Count,
    limitations = "Synthetic test-only DLL. No runtime, font, package, metadata-wide equivalence or nonstandard colon-source support is established." }));
