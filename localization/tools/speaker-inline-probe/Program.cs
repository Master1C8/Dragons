using System.Security.Cryptography;
using System.Reflection;
using System.Runtime.Loader;
using System.Text.Json;
using Dragons.SyntheticSpeakerInline;
using Yarn.Markup;
using Yarn.Unity;

bool production = args.Length >= 6;
if (args.Length is not (2 or 5 or 6 or 7) || args[0] is not ("macos" or "windows"))
    throw new ArgumentException("Usage: speaker-inline-probe macos|windows PAIRED_YARN_JSON [PATCHED_SHA256 INLINE_RUNTIME_DLL INLINE_RUNTIME_SHA256 [FALLBACK_TEXT [ALEXANDER_BODY]]]");

string Hash(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
void Require(bool condition, string message)
{
    if (!condition) throw new InvalidOperationException(message);
}

string unityHash = args[0] == "macos"
    ? "54953f9c071aa3ca5b52eb8b12b8e0bedc73f7665a506c61acbef0c58ac340ef"
    : "3d5def40f51540e79dbb6a897993fe006022cf1f16933a1b47a69334085ad89d";
Require(Hash(typeof(LineParser).Assembly.Location) == "d10c640b1b0b3664241b19137d3f0c27ffa8ba75e0fcf5dac183bbcc89b78f7e",
    "Unsupported Yarn core");
bool patched = args.Length >= 5;
string loadedUnityHash = Hash(typeof(LocalizedLine).Assembly.Location);
Require(loadedUnityHash == (patched ? args[2] : unityHash), "Unsupported Yarn Unity assembly");
Require(Hash(args[1]) == "52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995",
    "Unsupported paired Yarn source");

var parser = new LineParser();
LocalizedLine ReadLine(string id, string source) =>
    new() { TextID = id, RawText = source, Text = parser.ParseString(source, "en", true) };
MethodInfo? bridge = null;
MethodInfo? nameBridge = null;
Type? displayType = null;
if (patched)
{
    Require(Hash(args[3]) == args[4], "Inline runtime fingerprint mismatch");
    AssemblyLoadContext.Default.LoadFromAssemblyPath(Path.GetFullPath(args[3]));
    string helper = production ? "Yarn.Unity.VnSpeakerDisplay" : "Yarn.Unity.VnSyntheticSpeakerDisplay";
    displayType = typeof(LocalizedLine).Assembly.GetType(helper, true)!;
    bridge = displayType.GetMethod("GetInlineText", BindingFlags.NonPublic | BindingFlags.Static)
        ?? throw new InvalidOperationException("Missing injected inline bridge");
    if (production)
    {
        nameBridge = displayType.GetMethod("GetDisplayName", BindingFlags.NonPublic | BindingFlags.Static)
            ?? throw new InvalidOperationException("Missing injected name bridge");
        var missing = (LocalizedLine)typeof(LocalizedLine).GetField("InvalidLine",
            BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static)!.GetValue(null)!;
        Require(missing.RawText == args[5] && missing.Text.Text == args[5], "Fallback representations differ");
    }
}
MarkupParseResult Display(LocalizedLine line, string name, string label) => bridge == null
    ? InlineSpeakerView.Create(line, name, label)
    : (MarkupParseResult)bridge.Invoke(null, new object[] { line })!;

void CheckMapped(LocalizedLine line, string expectedName, string displayName)
{
    var original = line.Text;
    var originalAttributes = original.Attributes.ToArray();
    var id = line.TextID;
    var raw = line.RawText;
    var body = line.TextWithoutCharacterName.Text;
    Require(line.CharacterName == expectedName, $"Unexpected source identity: {id}");
    var display = Display(line, expectedName, displayName);
    Require(display.Text == displayName + ": " + body, $"Unexpected inline display: {id}");
    if (nameBridge != null)
        Require((string?)nameBridge.Invoke(null, new object[] { line }) == displayName, $"Unexpected separate name: {id}");
    Require(display.Attributes.Count == originalAttributes.Length &&
        !ReferenceEquals(original.Attributes, display.Attributes), $"Incorrect attribute copy: {id}");
    int delta = displayName.Length - expectedName.Length;
    for (int i = 0; i < originalAttributes.Length; i++)
    {
        var before = originalAttributes[i];
        var after = display.Attributes[i];
        Require(before.Name == after.Name, $"Attribute order changed: {id}");
        if (before.Name == "character")
        {
            Require(after.Position == 0 && after.Length == displayName.Length + 2 &&
                after.TryGetProperty("name", out string? annotation) && annotation == displayName,
                $"Incorrect display attribute: {id}");
            continue;
        }
        Require(after.Position == before.Position + delta && after.Length == before.Length &&
            before.Properties.Count == after.Properties.Count &&
            before.Properties.All(pair => after.Properties.TryGetValue(pair.Key, out var value) &&
                value.Equals(pair.Value)) &&
            original.TextForAttribute(before) == display.TextForAttribute(after), $"Body markup changed: {id}");
    }
    Require(line.TextID == id && line.RawText == raw && line.CharacterName == expectedName &&
        line.Text.Text == original.Text && line.Text.Attributes.SequenceEqual(originalAttributes) &&
        line.TextWithoutCharacterName.Text == body, $"Source line changed: {id}");
}

void CheckUnchanged(LocalizedLine line)
{
    var display = Display(line, "Ryan", "Жж");
    Require(display.Text == line.Text.Text && ReferenceEquals(display.Attributes, line.Text.Attributes),
        $"Unexpected fallback rewrite: {line.TextID}");
    if (nameBridge != null)
        Require((string?)nameBridge.Invoke(null, new object[] { line }) == line.CharacterName,
            $"Unexpected separate name rewrite: {line.TextID}");
}

using var source = JsonDocument.Parse(File.ReadAllBytes(args[1]));
var mappedIds = new List<string>();
foreach (var scene in source.RootElement.GetProperty("scenes").EnumerateObject())
foreach (var entry in scene.Value.EnumerateArray())
{
    string text = entry.GetProperty("source").GetProperty(args[0]).GetString()!;
    string? name = text.StartsWith("Ryan: ", StringComparison.Ordinal) ? "Ryan"
        : text.StartsWith("Conrad: ", StringComparison.Ordinal) ? "Conrad" : null;
    if (name is null) continue;
    string id = entry.GetProperty("id").GetString()!;
    CheckMapped(ReadLine(id, text), name, name == "Ryan" ? "Жж" : "ЪъЬьЯяЖ");
    mappedIds.Add(id);
}
Require(mappedIds.Count == 18 && mappedIds.Distinct().Count() == 18, "Unexpected source coverage");
foreach (var (name, id) in new[] { ("Ryan", "line:f5f5b815"), ("Conrad", "line:5660dc8b") })
{
    var marked = ReadLine(id, name + ": [b]Test[/b] [pause duration=\"0.5\" /]next <i>line</i>");
    Require(marked.Text.Attributes.Any(attribute => attribute.Name == "b" && attribute.Length == 4) &&
        marked.Text.Attributes.Any(attribute => attribute.Name == "pause" && attribute.Length == 0),
        "Test case lost its ranged or zero-length markup");
    CheckMapped(marked, name, name == "Ryan" ? "Жж" : "ЪъЬьЯяЖ");
}
if (!patched)
    CheckMapped(ReadLine("test-same-length", "Conrad: [b]Test[/b]"), "Conrad", "ЪъЬьЯя");
foreach (string text in new[] { "Text", "Other: Text", "title: Conrad_OutroDone",
    "The most prestigious college hosting prestigious professors like me:" })
    CheckUnchanged(ReadLine("line:f5f5b815", text));
var overlapping = ReadLine("line:f5f5b815", "Ryan: [b]Test[/b]");
int markup = overlapping.Text.Attributes.FindIndex(attribute => attribute.Name == "b");
overlapping.Text.Attributes[markup] = overlapping.Text.Attributes[markup].Shift(-1);
CheckUnchanged(overlapping);
var mismatchedRaw = ReadLine("line:f5f5b815", "Ryan: Test");
mismatchedRaw.RawText = "Other: Test";
CheckUnchanged(mismatchedRaw);
if (patched)
{
    CheckUnchanged(ReadLine("line:unknown", "Ryan: Test"));
    CheckUnchanged(ReadLine("line:f5f5b815", "Conrad: Test"));
}
if (args.Length == 7)
{
    const string id = "line:4b36ea4e";
    var english = source.RootElement.GetProperty("scenes").GetProperty("Alexander_2").EnumerateArray()
        .Single(row => row.GetProperty("id").GetString() == id).GetProperty("source").GetProperty(args[0]).GetString()!;
    var line = ReadLine(id, english);
    var original = line.Text;
    Require(line.CharacterName == english[..^1] && line.TextWithoutCharacterName.Text == "",
        "Original Alexander parse changed");
    MarkupParseResult ReadView(string method, LocalizedLine item) =>
        (MarkupParseResult)displayType!.GetMethod(method, BindingFlags.NonPublic | BindingFlags.Static)!
            .Invoke(null, new object[] { item })!;
    foreach (string method in new[] { "GetAlexanderText", "GetInlineText", "GetBodyText" })
    {
        var result = ReadView(method, line);
        Require(result.Text == args[6] && result.Attributes.Count == 0, $"Incorrect Alexander view: {method}");
    }
    Require(nameBridge!.Invoke(null, new object[] { line }) == null, "Alexander text leaked into the name");
    Require(line.TextID == id && line.RawText == english && line.CharacterName == english[..^1] &&
        line.TextWithoutCharacterName.Text == "" && ReferenceEquals(original.Attributes, line.Text.Attributes),
        "Alexander source line changed");
    CheckUnchanged(ReadLine("line:other", english));
    CheckUnchanged(ReadLine(id, english.Replace("college", "university")));
    var wrongParsed = ReadLine(id, english.Replace("college", "university"));
    wrongParsed.RawText = english;
    CheckUnchanged(wrongParsed);
    var ordinary = ReadLine("line:f5f5b815", "Ryan: Test");
    Require(ReadView("GetBodyText", ordinary).Text == "Test" &&
        ReferenceEquals(ReadView("GetAlexanderText", ordinary).Attributes, ordinary.Text.Attributes),
        "Special body helper changed an ordinary speaker");
}
var report = new { schema = 1, testOnly = true, platform = args[0],
    sourceYarnUnitySha256 = unityHash, mappedIds, markupControls = patched ? 2 : 3,
    unchangedControls = patched ? 8 : 6, executedPatchedBridge = patched, loadedUnityHash,
    inlineRuntimeSha256 = patched ? args[4] : null };
if (args.Length == 7)
{
    var specialReport = JsonSerializer.SerializeToNode(report)!.AsObject();
    specialReport["alexanderBodyVerified"] = true;
    Console.WriteLine(specialReport.ToJsonString());
}
else Console.WriteLine(JsonSerializer.Serialize(report));
