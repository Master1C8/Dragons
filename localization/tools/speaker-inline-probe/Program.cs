using System.Security.Cryptography;
using System.Text.Json;
using Yarn.Markup;
using Yarn.Unity;

if (args.Length != 2 || args[0] is not ("macos" or "windows"))
    throw new ArgumentException("Usage: speaker-inline-probe macos|windows PAIRED_YARN_JSON");

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
Require(Hash(typeof(LocalizedLine).Assembly.Location) == unityHash, "Unsupported Yarn Unity assembly");
Require(Hash(args[1]) == "52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995",
    "Unsupported paired Yarn source");

var parser = new LineParser();
LocalizedLine ReadLine(string id, string source) =>
    new() { TextID = id, RawText = source, Text = parser.ParseString(source, "en", true) };

void CheckMapped(LocalizedLine line, string expectedName, string displayName)
{
    var original = line.Text;
    var originalAttributes = original.Attributes.ToArray();
    var id = line.TextID;
    var raw = line.RawText;
    var body = line.TextWithoutCharacterName.Text;
    Require(line.CharacterName == expectedName, $"Unexpected source identity: {id}");
    var display = InlineSpeakerView.Create(line, displayName);
    Require(display.Text == displayName + ": " + body, $"Unexpected inline display: {id}");
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
    var display = InlineSpeakerView.Create(line, "Жж");
    Require(display.Text == line.Text.Text && ReferenceEquals(display.Attributes, line.Text.Attributes),
        $"Unexpected fallback rewrite: {line.TextID}");
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
foreach (string name in new[] { "Ryan", "Conrad" })
{
    var marked = ReadLine("test-markup-" + name, name + ": [b]Test[/b] [pause duration=\"0.5\" /]next <i>line</i>");
    Require(marked.Text.Attributes.Any(attribute => attribute.Name == "b" && attribute.Length == 4) &&
        marked.Text.Attributes.Any(attribute => attribute.Name == "pause" && attribute.Length == 0),
        "Test case lost its ranged or zero-length markup");
    CheckMapped(marked, name, name == "Ryan" ? "Жж" : "ЪъЬьЯяЖ");
}
CheckMapped(ReadLine("test-same-length", "Conrad: [b]Test[/b]"), "Conrad", "ЪъЬьЯя");
foreach (string text in new[] { "Text", "Other: Text", "title: Conrad_OutroDone",
    "The most prestigious college hosting prestigious professors like me:" })
    CheckUnchanged(ReadLine("test-fallback", text));
var overlapping = ReadLine("test-overlap", "Ryan: [b]Test[/b]");
int markup = overlapping.Text.Attributes.FindIndex(attribute => attribute.Name == "b");
overlapping.Text.Attributes[markup] = overlapping.Text.Attributes[markup].Shift(-1);
CheckUnchanged(overlapping);
var mismatchedRaw = ReadLine("test-mismatched-raw", "Ryan: Test");
mismatchedRaw.RawText = "Other: Test";
CheckUnchanged(mismatchedRaw);
Console.WriteLine(JsonSerializer.Serialize(new { schema = 1, testOnly = true, platform = args[0],
    sourceYarnUnitySha256 = unityHash, mappedIds, markupControls = 3, unchangedControls = 6 }));
