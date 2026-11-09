#nullable enable
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text.Json;
using Yarn;
using Yarn.Unity;

const string questionNode = "Alexander_questions";
const string exitId = "line:66fb84fe";
const string oncePrefix = "Yarn.Internal.Once.";
const string hasAsked = "has_asked_question";
const BindingFlags all = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance | BindingFlags.Static;
if (args.Length != 5 || args[0] is not ("macos" or "windows"))
    throw new ArgumentException("Usage: runtime macos|windows ORIGINAL_PROGRAM ORIGINAL_MANAGED PROBE_DLL PROBE_SHA256");
string Sha(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
var programBytes = File.ReadAllBytes(args[1]);
var expectedProgram = args[0] == "macos"
    ? "a67bbfc37dca0b29b1be740e36b570e9d524a46ef2fdf5574e0f58278c0ff1e6"
    : "cbaaba712e0cc699d0cdf98f4b8b86060c666d6196fa91cd0a9d9a237c104466";
var expectedYarnUnity = args[0] == "macos"
    ? "54953f9c071aa3ca5b52eb8b12b8e0bedc73f7665a506c61acbef0c58ac340ef"
    : "3d5def40f51540e79dbb6a897993fe006022cf1f16933a1b47a69334085ad89d";
Require(Sha(programBytes) == expectedProgram, "unsupported original program");
Require(Sha(File.ReadAllBytes(typeof(Dialogue).Assembly.Location)) ==
    "d10c640b1b0b3664241b19137d3f0c27ffa8ba75e0fcf5dac183bbcc89b78f7e", "unsupported Yarn VM");
Require(Sha(File.ReadAllBytes(typeof(InMemoryVariableStorage).Assembly.Location)) ==
    expectedYarnUnity, "unsupported Yarn Unity variable store");
var program = Yarn.Program.Parser.ParseFrom(programBytes);
var managed = Path.GetFullPath(args[2]);
AssemblyLoadContext.Default.Resolving += (context, name) => {
    string file = Path.Combine(managed, name.Name + ".dll");
    return File.Exists(file) ? context.LoadFromAssemblyPath(file) : null;
};
var probeBytes = File.ReadAllBytes(args[3]);
Require(Sha(probeBytes) == args[4], "modified probe assembly");
using var probe = new MemoryStream(probeBytes, writable: false);
var game = AssemblyLoadContext.Default.LoadFromStream(probe);
var sceneType = game.GetType("WalkNWashSceneState", true)!;
var registryType = game.GetType("WalkNWash.Flags.FlagRegistry", true)!;
var flagsType = game.GetType("WalkNWash.Flags.Flags", true)!;
var nodeType = game.GetType("SimpleJSON.JSONNode", true)!;

InMemoryVariableStorage Prepare() {
    // Use the original managed store without invoking the native MonoBehaviour constructor.
    var store = (InMemoryVariableStorage)RuntimeHelpers.GetUninitializedObject(typeof(InMemoryVariableStorage));
    typeof(InMemoryVariableStorage).GetField("variables", all)!.SetValue(store, new Dictionary<string, object>());
    typeof(InMemoryVariableStorage).GetField("variableTypes", all)!.SetValue(store, new Dictionary<string, Type>());
    typeof(VariableStorageBehaviour).GetField("changeListeners", all)!.SetValue(store, new Dictionary<string, List<Delegate>>());
    typeof(VariableStorageBehaviour).GetField("globalChangeListeners", all)!.SetValue(store, new List<Delegate>());
    var scene = RuntimeHelpers.GetUninitializedObject(sceneType);
    sceneType.GetField("instance", all)!.SetValue(null, scene);
    sceneType.GetField("VnProbeStorage", all)!.SetValue(null, store);
    flagsType.GetField("<Registry>k__BackingField", all)!.SetValue(null, Activator.CreateInstance(registryType, true));
    store.SetValue("$dragonHead", "test-head");
    var listener = sceneType.GetMethod("OnYarnFlagSet", all)!.CreateDelegate<Action<string, object>>(scene);
    store.AddChangeListener(listener);
    return store;
}

object Registry() => flagsType.GetProperty("Registry", all)!.GetValue(null)!;

Dialogue Start(InMemoryVariableStorage store) {
    var dialogue = new Dialogue(store);
    dialogue.SetProgram(program);
    dialogue.LogDebugMessage = _ => {};
    dialogue.LogErrorMessage = message => throw new InvalidOperationException(message);
    dialogue.CommandHandler = _ => {};
    dialogue.LineHandler = _ => {};
    return dialogue;
}

string[] RestoreAndRead(string json, string restoredKey) {
    var store = Prepare();
    var restarted = Start(store);
    store.Clear();
    var parsed = nodeType.GetMethod("Parse", all, [typeof(string)])!.Invoke(null, [json]);
    registryType.GetMethod("FromJson", all, [nodeType])!.Invoke(Registry(), [parsed]);
    Require((int)sceneType.GetField("currentLevel", all)!.GetValue(sceneType.GetField("instance", all)!.GetValue(null))! == 6,
        "save level not restored");
    Require(store.TryGetValue<bool>("$" + restoredKey, out bool consumed) && consumed, "loaded once flag missing");
    Require(store.TryGetValue<bool>("$" + hasAsked, out bool askedAgain) && !askedAgain, "loaded exit flag wrong");
    string[]? menu = null;
    restarted.OptionsHandler = set => menu = set.Options.Where(o => o.IsAvailable).Select(o => o.Line.ID).ToArray();
    restarted.SetNode(questionNode);
    restarted.Continue();
    return menu ?? throw new InvalidOperationException("reloaded menu missing");
}
string[] questions = ["line:fc7aaaa0", "line:daa040eb", "line:21c0526b", "line:c2bdc402",
    "line:838cdf1b", "line:72a9b5bb", "line:a5a8a9d5"];

foreach (var chosen in questions) {
    string onceKey = oncePrefix + chosen;
    string wrongKey = onceKey[..^1] + (onceKey[^1] == '0' ? '1' : '0');
    var originalStore = Prepare();
    var dialogue = Start(originalStore);
    bool selectedQuestion = false;
    bool selectedExit = false;
    dialogue.OptionsHandler = set => {
        var options = set.Options.Where(option => option.IsAvailable).ToArray();
        bool rootMenu = set.Options.Any(option => option.Line.ID == exitId);
        var selected = options[0];
        if (rootMenu) {
            string next = selectedQuestion ? exitId : chosen;
            selected = options.Single(option => option.Line.ID == next);
            selectedQuestion = true;
            selectedExit = next == exitId;
        }
        dialogue.SetSelectedOption(selected.ID);
    };
    bool exited = false;
    dialogue.LineHandler = line => { if (line.ID == "line:3027bcf7") exited = true; };
    dialogue.SetNode(questionNode);
    for (int step = 0; step < 60 && !exited && (step == 0 || dialogue.IsActive); step++) dialogue.Continue();
    Require(exited && selectedExit, "original VM route did not exit");
    Require(originalStore.TryGetValue<bool>("$" + onceKey, out bool selected) && selected, "VM did not set once flag");
    Require(originalStore.TryGetValue<bool>("$" + hasAsked, out bool asked) && !asked, "VM did not reset exit flag");

    var serialized = registryType.GetMethod("ToJson", all, [typeof(int)])!.Invoke(Registry(), [6])!.ToString()!;
    using var document = JsonDocument.Parse(serialized);
    var entries = document.RootElement.EnumerateArray().Where(e => e.TryGetProperty("id", out _))
        .ToDictionary(e => e.GetProperty("id").GetString()!);
    Require(entries.Keys.Order().SequenceEqual(new[] { onceKey, hasAsked }.Order()), "save IDs are missing, extra or prefixed");
    Require(entries[onceKey].GetProperty("boolValue").GetBoolean(), "saved once flag false");
    Require(!entries[hasAsked].GetProperty("boolValue").GetBoolean(), "saved exit flag true");

    var same = RestoreAndRead(serialized, onceKey);
    var keyOffset = serialized.IndexOf(onceKey, StringComparison.Ordinal);
    Require(keyOffset >= 0 && keyOffset == serialized.LastIndexOf(onceKey, StringComparison.Ordinal),
        "negative control needs one exact save-key occurrence");
    var wrongSave = serialized[..keyOffset] + wrongKey + serialized[(keyOffset + onceKey.Length)..];
    var changed = RestoreAndRead(wrongSave, wrongKey);
    Require(same.SequenceEqual(questions.Where(id => id != chosen)), "original key did not suppress only the chosen option");
    Require(changed.SequenceEqual(questions), "changed key did not restore the original question menu");
    Console.WriteLine(JsonSerializer.Serialize(new { chosen, savedEntries = entries, same, wrongKey, changed }));
}
static void Require(bool condition, string message) { if (!condition) throw new InvalidOperationException(message); }
