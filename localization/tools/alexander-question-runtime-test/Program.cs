using System.Security.Cryptography;
using System.Text.Json;
using Yarn;

const string questionNode = "Alexander_questions";
const string exitId = "line:66fb84fe";
const string exitNode = "Alexander_3_required_end";
const string hasAsked = "$has_asked_question";
const string yarnHash = "d10c640b1b0b3664241b19137d3f0c27ffa8ba75e0fcf5dac183bbcc89b78f7e";

if (args.Length != 2 || args[0] is not ("macos" or "windows"))
    throw new ArgumentException("Usage: alexander-question-runtime-test macos|windows ORIGINAL_PROGRAM");
string Sha(byte[] data) => Convert.ToHexString(SHA256.HashData(data)).ToLowerInvariant();
var programBytes = File.ReadAllBytes(args[1]);
var programHash = Sha(programBytes);
var expectedHash = args[0] == "macos"
    ? "a67bbfc37dca0b29b1be740e36b570e9d524a46ef2fdf5574e0f58278c0ff1e6"
    : "cbaaba712e0cc699d0cdf98f4b8b86060c666d6196fa91cd0a9d9a237c104466";
Require(programHash == expectedHash, "unsupported original program");
Require(Sha(File.ReadAllBytes(typeof(Dialogue).Assembly.Location)) == yarnHash, "unsupported Yarn VM");
var program = Yarn.Program.Parser.ParseFrom(programBytes);

string[] questions = ["line:fc7aaaa0", "line:daa040eb", "line:21c0526b", "line:c2bdc402",
    "line:838cdf1b", "line:72a9b5bb", "line:a5a8a9d5"];
var cases = new (string Name, string[] Questions, string[] Replies, string[] ExpectedBody)[] {
    ("all-once", questions, [], []),
    ("seven-doubt", ["line:c2bdc402"], ["line:eedccaec"], ["line:78eccd9b", "line:4d49ae72"]),
    ("seven-lemon-authority", ["line:c2bdc402"], ["line:db79a905", "line:f718a7eb"],
        ["line:78eccd9b", "line:6128a09c", "line:6605187b"]),
    ("seven-lemon-doubt", ["line:c2bdc402"], ["line:db79a905", "line:f0351f0c"],
        ["line:78eccd9b", "line:6128a09c", "line:15bcd86c"]),
    ("crest-acknowledge", ["line:a5a8a9d5"], ["line:e90fee8e"],
        ["line:1ff9a04c", "line:89c9a73b", "line:18d418ab", "line:8ee41fdc", "line:7f3fe9f9", "line:c56ee060"]),
    ("crest-repeat", ["line:a5a8a9d5"], ["line:535ee717"],
        ["line:1ff9a04c", "line:89c9a73b", "line:18d418ab", "line:8ee41fdc", "line:f0cb8389"]),
};

foreach (var scenario in cases) {
    var store = new MemoryVariableStore();
    var dialogue = new Dialogue(store);
    var remaining = new Queue<string>(scenario.Questions);
    var replies = new Queue<string>(scenario.Replies);
    var asked = new List<string>();
    var body = new List<string>();
    var nested = new List<string>();
    var menus = new List<string[]>();
    bool reachedExit = false;
    bool reentered = false;

    dialogue.SetProgram(program);
    store.SetValue("$dragonHead", "test-head");
    dialogue.LogDebugMessage = _ => {};
    dialogue.LogErrorMessage = message => throw new InvalidOperationException(message);
    dialogue.CommandHandler = _ => {};
    dialogue.LineHandler = line => {
        if (dialogue.CurrentNode == questionNode) body.Add(line.ID);
        if (dialogue.CurrentNode == exitNode) {
            Require(line.ID == "line:3027bcf7", "unexpected exit dialogue");
            Require(store.TryGetValue<bool>(hasAsked, out bool value) && !value, "exit flag was not reset");
            reachedExit = true;
        }
    };
    dialogue.OptionsHandler = options => {
        var available = options.Options.Where(option => option.IsAvailable).ToArray();
        string[] ids = available.Select(option => option.Line.ID).ToArray();
        bool rootMenu = options.Options.Any(option => option.Line.ID == exitId);
        if (!rootMenu) {
            var chosen = scenario.Name == "all-once" ? available[0]
                : available.Single(option => replies.Count > 0 && option.Line.ID == replies.Peek());
            if (scenario.Name != "all-once") replies.Dequeue();
            nested.Add(chosen.Line.ID);
            dialogue.SetSelectedOption(chosen.ID);
            return;
        }

        var expected = questions.Except(asked);
        if (!reentered && asked.Count > 0) expected = expected.Append(exitId);
        Require(ids.SequenceEqual(expected), "incorrect root option availability or order");
        menus.Add(ids);
        foreach (var id in asked) {
            Require(store.TryGetValue<bool>("$Yarn.Internal.Once." + id, out bool once) && once,
                $"selected question did not write its original once flag: {id}");
        }
        if (reentered) return;
        string next = remaining.Count > 0 ? remaining.Dequeue() : exitId;
        if (next != exitId) asked.Add(next);
        dialogue.SetSelectedOption(available.Single(option => option.Line.ID == next).ID);
    };

    dialogue.SetNode(questionNode);
    for (int step = 0; step < 150 && !reachedExit && (step == 0 || dialogue.IsActive); step++)
        dialogue.Continue();
    Require(reachedExit && remaining.Count == 0 && replies.Count == 0, "scenario did not reach exit");
    if (scenario.ExpectedBody.Length > 0)
        Require(body.SequenceEqual(scenario.ExpectedBody), $"wrong line sequence for {scenario.Name}");

    reentered = true;
    int priorMenus = menus.Count;
    dialogue.SetNode(questionNode);
    dialogue.Continue();
    Require(menus.Count == priorMenus + 1, "reentry menu was not reached");

    Console.WriteLine(JsonSerializer.Serialize(new {
        scenario = scenario.Name, asked, nested, body, menus, exitNode, reachedExit,
        reentryWithSameStore = reentered, programSha256 = programHash, yarnSha256 = yarnHash
    }));
}

static void Require(bool condition, string message) {
    if (!condition) throw new InvalidOperationException(message);
}
