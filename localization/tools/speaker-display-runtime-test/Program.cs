using System.Reflection;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

if (args.Length != 4 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: speaker-display-runtime-test macos|windows ORIGINAL_MANAGED PATCHED_DLL EXPECTED_PATCHED_SHA256");
string Sha(byte[] data) => Convert.ToHexString(SHA256.HashData(data)).ToLowerInvariant();
var manifests = new Dictionary<string, string> {
    ["macos"] = "b3186bc39207255e937f5856be09906dc1a428d83a964d5f368f30861e32603c",
    ["windows"] = "9a14fcb1198ca8308ad90a38a1988367074c1f2ec8b6f0a8d97ef3d3c074fc56"
};
var managed = Path.GetFullPath(args[1]);
var files = Directory.GetFiles(managed).Where(p => p.EndsWith(".dll", StringComparison.Ordinal))
    .OrderBy(p => Path.GetFileName(p), StringComparer.Ordinal).ToArray();
if (files.Any(p => Path.GetFileName(p).Any(c => c > 127))) throw new InvalidOperationException("Non-ASCII managed filename");
string manifest = string.Concat(files.Select(p => $"{Path.GetFileName(p)}|{Sha(File.ReadAllBytes(p))}\n"));
if (Sha(Encoding.UTF8.GetBytes(manifest)) != manifests[args[0]]) throw new InvalidOperationException("Unsupported managed inventory");
var patched = Path.GetFullPath(args[2]);
var patchedHash = Sha(File.ReadAllBytes(patched));
if (args[3].Length != 64 || patchedHash != args[3]) throw new InvalidOperationException("Patched DLL fingerprint mismatch");
AssemblyLoadContext.Default.Resolving += (ctx, name) => {
    var path = Path.Combine(managed, name.Name + ".dll");
    return File.Exists(path) ? ctx.LoadFromAssemblyPath(path) : null;
};
var yarn = AssemblyLoadContext.Default.LoadFromAssemblyPath(Path.Combine(managed, "YarnSpinner.dll"));
var unity = AssemblyLoadContext.Default.LoadFromAssemblyPath(patched);
var parserType = yarn.GetType("Yarn.Markup.LineParser", true);
var parser = Activator.CreateInstance(parserType);
var parse = parserType.GetMethod("ParseString", new[] { typeof(string), typeof(string), typeof(bool) });
var lineType = unity.GetType("Yarn.Unity.LocalizedLine", true);
var getter = lineType.GetProperty("CharacterName");
var textProperty = lineType.GetProperty("Text");
var helper = unity.GetType("Yarn.Unity.VnSyntheticSpeakerDisplay", true).GetMethod("GetDisplayName", BindingFlags.Static | BindingFlags.NonPublic);
var cases = new[] {
    (source: "Ryan: TEST", original: "Ryan", display: "Жж"),
    (source: "Conrad: TEST", original: "Conrad", display: "ЪъЬь"),
    (source: "Other: TEST", original: "Other", display: "Other"),
    (source: "Ryan2: TEST", original: "Ryan2", display: "Ryan2"),
    (source: "Ordinary phrase:", original: "Ordinary phrase", display: "Ordinary phrase"),
    (source: "The most prestigious college hosting prestigious professors like me:",
     original: "The most prestigious college hosting prestigious professors like me",
     display: "The most prestigious college hosting prestigious professors like me"),
    (source: "TEST", original: (string)null, display: (string)null)
};
var checks = new List<object>();
foreach (var sample in cases) {
    var parsed = parse.Invoke(parser, new object[] { sample.source, "en", true });
    var line = Activator.CreateInstance(lineType);
    textProperty.SetValue(line, parsed);
    var before = (string)getter.GetValue(line);
    var shown = (string)helper.Invoke(null, new[] { line });
    var after = (string)getter.GetValue(line);
    if (before != sample.original || after != sample.original || shown != sample.display)
        throw new InvalidOperationException($"Unexpected synthetic speaker mapping: {sample.source}");
    var noName = lineType.GetProperty("TextWithoutCharacterName").GetValue(line);
    var body = (string)noName.GetType().GetProperty("Text").GetValue(noName);
    if (sample.source.StartsWith("The most prestigious college", StringComparison.Ordinal) && body != "")
        throw new InvalidOperationException("Unexpected nonempty body for colon-ended source line");
    checks.Add(new { sample.source, identityBefore = before, display = shown, identityAfter = after, body });
}
Console.WriteLine(JsonSerializer.Serialize(new { schema = 1, testOnly = true, platform = args[0],
    managedInventorySha256 = manifests[args[0]], patchedSha256 = patchedHash, checks,
    limitations = "Desktop .NET executes the actual pinned Yarn parser and patched helper via reflection. Unity UI, injected call-site execution, game runtime, rendering, font, options, and nonstandard source adaptation remain untested." },
    new JsonSerializerOptions { WriteIndented = true }));
