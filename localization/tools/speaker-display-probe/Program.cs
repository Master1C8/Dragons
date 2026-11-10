using System.Globalization;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

bool production = args.Length is 9 or 10 && args[6] == "--locale";
if ((!production && args.Length is not (4 or 6)) || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: speaker-display-probe macos|windows SOURCE_DLL MAP_JSON OUTPUT_DLL [INLINE_RUNTIME_DLL INLINE_RUNTIME_SHA256 [--locale LOCALE FALLBACK_TEXT [ALEXANDER_BODY]]]");
bool includeInline = production || args.Length == 6;
string alexanderBody = args.Length == 10 ? args[9] : null;
const string AlexanderId = "line:4b36ea4e";
if (alexanderBody != null && (!alexanderBody.EndsWith(':') || string.IsNullOrWhiteSpace(alexanderBody[..^1]) ||
    alexanderBody.Any(c => char.IsControl(c) || "<>[]{}".Contains(c))))
    throw new ArgumentException("Alexander presentation requires plain text ending with a colon");
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
if ((!production && Path.GetDirectoryName(output) != work) || Path.GetExtension(output) != ".dll")
    throw new InvalidOperationException("Output must be a fresh DLL directly in project work");
using var json = JsonDocument.Parse(File.ReadAllBytes(args[2]));
if (json.RootElement.ValueKind != JsonValueKind.Object) throw new InvalidOperationException("Invalid mapping document");
var rootFields = json.RootElement.EnumerateObject().ToArray();
if (rootFields.Length != 3 || rootFields.Select(x => x.Name).Distinct().Count() != 3 ||
    !rootFields.Select(x => x.Name).OrderBy(x => x).SequenceEqual(new[] { "locale", "map", "schema" }))
    throw new InvalidOperationException("Unexpected mapping fields");
if (json.RootElement.GetProperty("schema").GetInt32() != 1 ||
    json.RootElement.GetProperty("locale").GetString() != (production ? args[7] : "ru"))
    throw new InvalidOperationException("Unsupported mapping identity");
var mapElement = json.RootElement.GetProperty("map");
if (mapElement.ValueKind != JsonValueKind.Object) throw new InvalidOperationException("Mapping must be an object");
var map = new Dictionary<string, string>(StringComparer.Ordinal);
foreach (var item in mapElement.EnumerateObject()) {
    if ((item.Name != "Ryan" && item.Name != "Conrad") || item.Value.ValueKind != JsonValueKind.String ||
        !map.TryAdd(item.Name, item.Value.GetString())) throw new InvalidOperationException("Invalid or duplicate source speaker");
    var text = map[item.Name];
    if (string.IsNullOrWhiteSpace(text) || text.Length > 40 || text.Any(c => char.IsControl(c) || "<>[]{}:".Contains(c)) ||
        (includeInline && !SpeakerLabel.IsValid(text)))
        throw new InvalidOperationException("Invalid display label");
}
if (map.Count != 2) throw new InvalidOperationException("Both known speaker mappings are required");

IEnumerable<TypeDefinition> All(IEnumerable<TypeDefinition> types) {
    foreach (var type in types) { yield return type; foreach (var child in All(type.NestedTypes)) yield return child; }
}
const string Getter = "System.String Yarn.Unity.LocalizedLine::get_CharacterName()";
const string Setter = "System.Void TMPro.TMP_Text::set_text(System.String)";
string helperName = production ? "VnSpeakerDisplay" : "VnSyntheticSpeakerDisplay";
string helperFullName = "Yarn.Unity." + helperName;
const string TextGetter = "Yarn.Markup.MarkupParseResult Yarn.Unity.LocalizedLine::get_Text()";
const string BodyGetter = "Yarn.Markup.MarkupParseResult Yarn.Unity.LocalizedLine::get_TextWithoutCharacterName()";
string runtimeAssembly = production ? "Dragons.SpeakerPresentation" : "Dragons.SyntheticSpeakerInline";
string runtimeMethod = $"Yarn.Markup.MarkupParseResult {runtimeAssembly}.InlineSpeakerView::Create(Yarn.Unity.LocalizedLine,System.String,System.String)";
string runtimeNameReader = $"System.String {runtimeAssembly}.InlineSpeakerView::NameFromView(Yarn.Markup.MarkupParseResult,Yarn.Unity.LocalizedLine)";
using var module = ModuleDefinition.ReadModule(new MemoryStream(sourceBytes));
if (module.Types.Any(t => t.FullName == helperFullName)) throw new InvalidOperationException("Helper already exists");
var all = All(module.Types).ToArray();
var nameType = module.Types.Single(t => t.FullName == "Yarn.Unity.LocalizedLine");
var getter = nameType.Methods.Single(m => m.FullName == Getter);
var equality = all.SelectMany(t => t.Methods).Where(m => m.HasBody).SelectMany(m => m.Body.Instructions)
    .Select(i => i.Operand).OfType<MethodReference>()
    .First(m => m.FullName == "System.Boolean System.String::op_Equality(System.String,System.String)");
var sites = new List<Instruction>();
var siteKeys = new HashSet<string>(StringComparer.Ordinal);
var specialSites = new Dictionary<string, (string Before, string After)>(StringComparer.Ordinal);
var inlineIds = new SortedDictionary<string, string>(StringComparer.Ordinal);
string inlineSiteKey = null;
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

var helperType = new TypeDefinition("Yarn.Unity", helperName,
    TypeAttributes.NotPublic | TypeAttributes.Abstract | TypeAttributes.Sealed | TypeAttributes.BeforeFieldInit, module.TypeSystem.Object);
var helper = new MethodDefinition("GetDisplayName", MethodAttributes.Assembly | MethodAttributes.Static | MethodAttributes.HideBySig, module.TypeSystem.String);
helper.Parameters.Add(new ParameterDefinition("line", ParameterAttributes.None, nameType));
var il = helper.Body.GetILProcessor();
if (!production) {
    helper.Body.InitLocals = true;
    helper.Body.Variables.Add(new VariableDefinition(module.TypeSystem.String));
    il.Append(il.Create(OpCodes.Ldarg_0)); il.Append(il.Create(OpCodes.Callvirt, getter)); il.Append(il.Create(OpCodes.Stloc_0));
    foreach (var pair in map.OrderBy(x => x.Key, StringComparer.Ordinal)) {
        var next = il.Create(OpCodes.Nop);
        il.Append(il.Create(OpCodes.Ldloc_0)); il.Append(il.Create(OpCodes.Ldstr, pair.Key));
        il.Append(il.Create(OpCodes.Call, equality)); il.Append(il.Create(OpCodes.Brfalse, next));
        il.Append(il.Create(OpCodes.Ldstr, pair.Value)); il.Append(il.Create(OpCodes.Ret)); il.Append(next);
    }
    il.Append(il.Create(OpCodes.Ldloc_0)); il.Append(il.Create(OpCodes.Ret));
}
helperType.Methods.Add(helper); module.Types.Add(helperType);
foreach (var site in sites) { site.OpCode = OpCodes.Call; site.Operand = helper; }
if (includeInline) {
    var runtimeBytes = File.ReadAllBytes(args[4]);
    if (Sha(runtimeBytes) != args[5]) throw new InvalidOperationException("Inline runtime fingerprint mismatch");
    using var runtime = AssemblyDefinition.ReadAssembly(new MemoryStream(runtimeBytes));
    if (runtime.Name.Name != runtimeAssembly || !runtime.CustomAttributes.Any(a =>
        a.AttributeType.FullName == "System.Runtime.Versioning.TargetFrameworkAttribute" &&
        (string)a.ConstructorArguments[0].Value == ".NETStandard,Version=v2.1"))
        throw new InvalidOperationException("Unexpected inline runtime assembly");
    var factory = runtime.MainModule.GetTypes().SelectMany(t => t.Methods).Single(m =>
        m.FullName == runtimeMethod && m.IsPublic && m.IsStatic);

    var manifestBytes = File.ReadAllBytes(Path.Combine(Directory.GetCurrentDirectory(),
        "localization", "evidence", "yarn-protected-partial-20261107.json"));
    if (Sha(manifestBytes) != "bff5f4ce3b270dedf77f31518a3bb75efe72d93617796baeff71cbebb5872be3")
        throw new InvalidOperationException("Unsupported speaker prefix manifest");
    using var manifest = JsonDocument.Parse(manifestBytes);
    foreach (var row in manifest.RootElement.GetProperty("prefixProtection").EnumerateArray()) {
        string prefix = row.GetProperty("expectedPrefix").GetProperty(args[0]).GetString();
        string speaker = prefix == "Ryan: " ? "Ryan" : prefix == "Conrad: " ? "Conrad" :
            throw new InvalidOperationException("Unknown protected speaker prefix");
        inlineIds.Add(row.GetProperty("id").GetString(), speaker);
    }
    if (inlineIds.Count != 18) throw new InvalidOperationException("Incomplete inline speaker IDs");

    var presenter = all.Single(t => t.FullName == "Yarn.Unity.LinePresenter/<RunLineAsync>d__23")
        .Methods.Single(m => m.Name == "MoveNext" && m.HasBody);
    var site = presenter.Body.Instructions.Single(i => i.Offset == 0x009c);
    var textGetter = nameType.Methods.Single(m => m.FullName == TextGetter);
    if (site.OpCode.Code != Code.Callvirt || ((MethodReference)site.Operand).FullName != TextGetter ||
        site.Next.OpCode.Code != Code.Stfld || ((FieldReference)site.Next.Operand).Name != "<text>5__2")
        throw new InvalidOperationException("Unexpected inline presenter consumer");
    inlineSiteKey = presenter.FullName + "#" + presenter.Body.Instructions.IndexOf(site);
    siteKeys.Add(inlineSiteKey);

    var external = new MethodReference(factory.Name, textGetter.ReturnType, module.ImportReference(factory.DeclaringType));
    external.Parameters.Add(new ParameterDefinition(nameType));
    external.Parameters.Add(new ParameterDefinition(module.TypeSystem.String));
    external.Parameters.Add(new ParameterDefinition(module.TypeSystem.String));
    var bridge = new MethodDefinition("GetInlineText", MethodAttributes.Assembly | MethodAttributes.Static |
        MethodAttributes.HideBySig, textGetter.ReturnType);
    bridge.Parameters.Add(new ParameterDefinition("line", ParameterAttributes.None, nameType));
    helperType.Methods.Add(bridge);
    var instructions = bridge.Body.GetILProcessor();
    var cases = map.Keys.ToDictionary(name => name, name => instructions.Create(OpCodes.Pop));
    var textId = nameType.Fields.Single(f => f.Name == "TextID" && f.FieldType.FullName == "System.String");
    if (alexanderBody != null) {
        string source = manifest.RootElement.GetProperty("fullValueProtection").EnumerateArray()
            .Single(row => row.GetProperty("id").GetString() == AlexanderId)
            .GetProperty("expected").GetProperty(args[0]).GetString();
        if (!source.EndsWith(':')) throw new InvalidOperationException("Unexpected Alexander source binding");
        MethodReference RuntimeMethod(string name, params TypeReference[] parameters) {
            var method = new MethodReference(name, textGetter.ReturnType, external.DeclaringType);
            foreach (var parameter in parameters) method.Parameters.Add(new ParameterDefinition(parameter));
            if (!factory.DeclaringType.Methods.Any(m => m.FullName == method.FullName && m.IsPublic && m.IsStatic))
                throw new InvalidOperationException($"Missing runtime helper {name}");
            return method;
        }
        MethodDefinition NewView(string name) {
            var method = new MethodDefinition(name, MethodAttributes.Assembly | MethodAttributes.Static |
                MethodAttributes.HideBySig, textGetter.ReturnType);
            method.Parameters.Add(new ParameterDefinition("line", ParameterAttributes.None, nameType));
            helperType.Methods.Add(method);
            return method;
        }
        var special = NewView("GetAlexanderText");
        var edit = special.Body.GetILProcessor();
        edit.Append(edit.Create(OpCodes.Ldarg_0));
        edit.Append(edit.Create(OpCodes.Ldstr, source));
        edit.Append(edit.Create(OpCodes.Ldstr, alexanderBody));
        edit.Append(edit.Create(OpCodes.Call, RuntimeMethod("CreateAlexanderBody", nameType,
            module.TypeSystem.String, module.TypeSystem.String)));
        edit.Append(edit.Create(OpCodes.Ret));
        var body = NewView("GetBodyText");
        edit = body.Body.GetILProcessor();
        edit.Append(edit.Create(OpCodes.Ldarg_0));
        edit.Append(edit.Create(OpCodes.Call, special));
        edit.Append(edit.Create(OpCodes.Ldarg_0));
        edit.Append(edit.Create(OpCodes.Call, RuntimeMethod("BodyFromView", textGetter.ReturnType, nameType)));
        edit.Append(edit.Create(OpCodes.Ret));
        var ordinary = instructions.Create(OpCodes.Ldarg_0);
        instructions.Append(instructions.Create(OpCodes.Ldarg_0));
        instructions.Append(instructions.Create(OpCodes.Ldfld, textId));
        instructions.Append(instructions.Create(OpCodes.Ldstr, AlexanderId));
        instructions.Append(instructions.Create(OpCodes.Call, equality));
        instructions.Append(instructions.Create(OpCodes.Brfalse, ordinary));
        instructions.Append(instructions.Create(OpCodes.Ldarg_0));
        instructions.Append(instructions.Create(OpCodes.Call, special));
        instructions.Append(instructions.Create(OpCodes.Ret));
        instructions.Append(ordinary);
        var options = all.Single(t => t.FullName == "Yarn.Unity.OptionsPresenter/<RunOptionsAsync>d__18")
            .Methods.Single(m => m.Name == "MoveNext" && m.HasBody);
        void Replace(MethodDefinition method, int offset, string expected, MethodDefinition replacement) {
            var ins = method.Body.Instructions.Single(i => i.Offset == offset);
            if (ins.OpCode.Code != Code.Callvirt || (ins.Operand as MethodReference)?.FullName != expected)
                throw new InvalidOperationException("Unexpected Alexander presenter consumer");
            var key = method.FullName + "#" + method.Body.Instructions.IndexOf(ins);
            specialSites.Add(key, (expected, replacement.FullName));
            ins.OpCode = OpCodes.Call;
            ins.Operand = replacement;
        }
        Replace(presenter, 0x00af, BodyGetter, body);
        Replace(presenter, 0x00c2, BodyGetter, body);
        Replace(presenter, 0x00e0, Getter, helper);
        Replace(options, 0x0208, TextGetter, special);
        Replace(options, 0x0223, Getter, helper);
        Replace(options, 0x0243, BodyGetter, body);
        Replace(options, 0x0282, BodyGetter, body);
    } else instructions.Append(instructions.Create(OpCodes.Ldarg_0));
    instructions.Append(instructions.Create(OpCodes.Ldfld, textId));
    foreach (var pair in inlineIds) {
        instructions.Append(instructions.Create(OpCodes.Dup));
        instructions.Append(instructions.Create(OpCodes.Ldstr, pair.Key));
        instructions.Append(instructions.Create(OpCodes.Call, equality));
        instructions.Append(instructions.Create(OpCodes.Brtrue, cases[pair.Value]));
    }
    instructions.Append(instructions.Create(OpCodes.Pop));
    instructions.Append(instructions.Create(OpCodes.Ldarg_0));
    instructions.Append(instructions.Create(OpCodes.Callvirt, textGetter));
    instructions.Append(instructions.Create(OpCodes.Ret));
    foreach (var pair in map.OrderBy(x => x.Key, StringComparer.Ordinal)) {
        instructions.Append(cases[pair.Key]);
        instructions.Append(instructions.Create(OpCodes.Ldarg_0));
        instructions.Append(instructions.Create(OpCodes.Ldstr, pair.Key));
        instructions.Append(instructions.Create(OpCodes.Ldstr, pair.Value));
        instructions.Append(instructions.Create(OpCodes.Call, external));
        instructions.Append(instructions.Create(OpCodes.Ret));
    }
    site.OpCode = OpCodes.Call;
    site.Operand = bridge;
    if (production) {
        // The same ID and prefix checks govern both presenter branches. Read
        // the character from the display view without modifying the original.
        il.Append(il.Create(OpCodes.Ldarg_0));
        il.Append(il.Create(OpCodes.Call, bridge));
        il.Append(il.Create(OpCodes.Ldarg_0));
        var nameFromView = runtime.MainModule.GetTypes().SelectMany(t => t.Methods).Single(m =>
            m.FullName == runtimeNameReader && m.DeclaringType == factory.DeclaringType && m.IsPublic && m.IsStatic);
        var nameReader = new MethodReference(nameFromView.Name, module.TypeSystem.String, external.DeclaringType);
        nameReader.Parameters.Add(new ParameterDefinition(textGetter.ReturnType));
        nameReader.Parameters.Add(new ParameterDefinition(nameType));
        il.Append(il.Create(OpCodes.Call, nameReader));
        il.Append(il.Create(OpCodes.Ret));
    }
}
const string originalFallback = "!! ERROR: Missing line!";
string fallback = production ? args[8] : originalFallback;
var fallbackSites = new HashSet<string>(StringComparer.Ordinal);
if (production) {
    if (string.IsNullOrWhiteSpace(fallback) || fallback.IndexOfAny(new[] { '<', '>', '\r', '\n', '\0' }) >= 0)
        throw new ArgumentException("Expected a single plain-text fallback");
    var initializer = nameType.Methods.Single(m => m.Name == ".cctor");
    foreach (int offset in new[] { 0x18, 0x39 }) {
        var ins = initializer.Body.Instructions.Single(i => i.Offset == offset);
        if (ins.OpCode.Code != Code.Ldstr || !Equals(ins.Operand, originalFallback))
            throw new InvalidOperationException("Unexpected fallback literal");
        fallbackSites.Add(initializer.FullName + "#" + initializer.Body.Instructions.IndexOf(ins));
        ins.Operand = fallback;
    }
}
using var buffer = new MemoryStream(); module.Write(buffer);
var outputBytes = buffer.ToArray();

// Compare all original method bodies after verifying the permitted call rewrites.
string Operand(object value, Dictionary<Instruction, int> indices) => value switch {
    null => "", Instruction i => "target:" + indices[i],
    Instruction[] a => "targets:" + string.Join(",", a.Select(x => indices[x])),
    VariableDefinition v => "local:" + v.Index, ParameterDefinition p => "param:" + p.Index,
    MemberReference m => "member:" + m.FullName,
    IFormattable f => f.ToString(null, CultureInfo.InvariantCulture), _ => value.ToString()
};
Dictionary<string, string> Bodies(ModuleDefinition source, bool patched) {
    var result = new Dictionary<string, string>(StringComparer.Ordinal);
    foreach (var type in All(source.Types).Where(t => t.FullName != helperFullName)) foreach (var method in type.Methods.Where(m => m.HasBody)) {
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
            string siteKey = method.FullName + "#" + i;
            if (siteKeys.Contains(siteKey)) {
                string target = (ins.Operand as MethodReference)?.FullName;
                string expectedGetter = siteKey == inlineSiteKey ? TextGetter : Getter;
                string expectedHelper = siteKey == inlineSiteKey
                    ? $"Yarn.Markup.MarkupParseResult {helperFullName}::GetInlineText(Yarn.Unity.LocalizedLine)"
                    : $"System.String {helperFullName}::GetDisplayName(Yarn.Unity.LocalizedLine)";
                if ((!patched && (ins.OpCode.Code != Code.Callvirt || target != expectedGetter)) ||
                    (patched && (ins.OpCode.Code != Code.Call || target != expectedHelper)))
                    throw new InvalidOperationException("Unexpected speaker call-site rewrite");
                text.Append("<verified-speaker-call>;");
            } else if (specialSites.TryGetValue(siteKey, out var change)) {
                if (ins.OpCode.Code != (patched ? Code.Call : Code.Callvirt) ||
                    (ins.Operand as MethodReference)?.FullName != (patched ? change.After : change.Before))
                    throw new InvalidOperationException("Unexpected Alexander call-site rewrite");
                text.Append("<verified-alexander-call>;");
            } else if (fallbackSites.Contains(siteKey)) {
                if (ins.OpCode.Code != Code.Ldstr || !Equals(ins.Operand, patched ? fallback : originalFallback))
                    throw new InvalidOperationException("Unexpected fallback rewrite");
                text.Append("<verified-fallback>;");
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
var rebuiltHelper = rebuilt.Types.Single(t => t.FullName == helperFullName).Methods.Single(m => m.Name == "GetDisplayName");
var literals = rebuiltHelper.Body.Instructions.Where(i => i.OpCode.Code == Code.Ldstr).Select(i => (string)i.Operand).ToArray();
var expectedLiterals = map.OrderBy(x => x.Key, StringComparer.Ordinal).SelectMany(x => new[] { x.Key, x.Value }).ToArray();
if (!production && !literals.SequenceEqual(expectedLiterals)) throw new InvalidOperationException("Helper mapping read-back failed");
if (production && !rebuiltHelper.Body.Instructions.Select(i => i.OpCode.Code)
    .SequenceEqual(new[] { Code.Ldarg_0, Code.Call, Code.Ldarg_0, Code.Call, Code.Ret }))
    throw new InvalidOperationException("Display-name helper read-back failed");
var expectedReferences = original.AssemblyReferences.Select(a => a.FullName).ToList();
if (includeInline) {
    var bridge = rebuilt.Types.Single(t => t.FullName == helperFullName).Methods.Single(m => m.Name == "GetInlineText");
    if (production && (!Equals(rebuiltHelper.Body.Instructions[1].Operand, bridge) ||
        rebuiltHelper.Body.Instructions[3].Operand is not MethodReference reader ||
        reader.FullName != runtimeNameReader || reader.DeclaringType.Scope.Name != runtimeAssembly))
        throw new InvalidOperationException("Unexpected display-name helper calls");
    var runtimeCalls = bridge.Body.Instructions.Where(i => i.OpCode.Code == Code.Call &&
        ((MethodReference)i.Operand).FullName == runtimeMethod).Select(i => (MethodReference)i.Operand).ToArray();
    if (runtimeCalls.Length != 2 || runtimeCalls[0].DeclaringType.Scope.Name != runtimeAssembly ||
        runtimeCalls[1].DeclaringType.Scope.Name != runtimeAssembly ||
        !bridge.Body.Instructions.Where(i => i.OpCode.Code == Code.Ldstr).Select(i => (string)i.Operand)
            .SequenceEqual((alexanderBody == null ? Array.Empty<string>() : new[] { AlexanderId })
                .Concat(inlineIds.Keys).Concat(expectedLiterals)))
        throw new InvalidOperationException("Inline bridge read-back failed");
    expectedReferences.Add(rebuilt.AssemblyReferences.Single(a => a.Name == runtimeAssembly).FullName);
}
if (!rebuilt.AssemblyReferences.Select(a => a.FullName).SequenceEqual(expectedReferences))
    throw new InvalidOperationException("Unexpected assembly dependency changes");
string temporary = Path.Combine(Path.GetDirectoryName(output), ".speaker-probe-" + Guid.NewGuid().ToString("N") + ".tmp");
try {
    using (var file = new FileStream(temporary, FileMode.CreateNew, FileAccess.Write, FileShare.None)) {
        file.Write(outputBytes);
        file.Flush(true);
    }
    File.Move(temporary, output, false);
} finally {
    if (File.Exists(temporary)) File.Delete(temporary);
}
var report = new { schema = 1, testOnly = !production, platform = args[0],
    sourceSha256 = expectedHashes[args[0]], outputSha256 = Sha(outputBytes), mappedSpeakers = map.Keys.OrderBy(x => x).ToArray(),
    changedDisplayCallSites = siteKeys.Concat(specialSites.Keys).OrderBy(x => x).ToArray(), verifiedExistingMethodBodies = before.Count,
    limitations = "Synthetic test-only DLL. No runtime, font, package, metadata-wide equivalence or nonstandard colon-source support is established." };
if (includeInline) {
    var details = JsonSerializer.SerializeToNode(report).AsObject();
    details["inlineRuntimeSha256"] = args[5];
    details["inlineIds"] = JsonSerializer.SerializeToNode(inlineIds.Keys.ToArray());
    if (production) {
        details.Remove("limitations");
        details["locale"] = args[7];
        details["fallbackChanged"] = fallback != originalFallback;
        if (alexanderBody != null) details["alexanderBodyId"] = AlexanderId;
    }
    Console.WriteLine(details.ToJsonString());
} else Console.WriteLine(JsonSerializer.Serialize(report));
