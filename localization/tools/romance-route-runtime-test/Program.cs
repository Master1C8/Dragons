using System.Security.Cryptography;
using System.Text.Json;
using Yarn;

const string alexander = "$alexander_romanced";
const string suggested = "$suggested_ryan_to_conrad";
const string together = "$ryan_conrad_romanced";
const string ryan = "$ryan_romanced";
const string conrad = "$conrad_romanced";
const string food = "$food_number";
const string accept = "line:a0e49f02";
const string decline = "line:0371fb9c";
const string suggest = "line:36ff6bd9";
const string invite = "line:7e9d40e6";
const string chooseTogether = "line:bedc761d";
const string chooseRyan = "line:e104b8e4";
const string chooseConrad = "line:f5a81524";
const string alexanderNode = "Alexander_5_romance_route";
const string conradNode = "Conrad_Outro_3";
const string foodNode = "ryan_food_dialogue";

if (args.Length != 2 || args[0] is not ("macos" or "windows"))
    throw new ArgumentException("Usage: romance-route-runtime-test macos|windows ORIGINAL_PROGRAM");
string Sha(byte[] data) => Convert.ToHexString(SHA256.HashData(data)).ToLowerInvariant();
var bytes = File.ReadAllBytes(args[1]);
var programHash = Sha(bytes);
var expectedHash = args[0] == "macos"
    ? "a67bbfc37dca0b29b1be740e36b570e9d524a46ef2fdf5574e0f58278c0ff1e6"
    : "cbaaba712e0cc699d0cdf98f4b8b86060c666d6196fa91cd0a9d9a237c104466";
Require(programHash == expectedHash, "unsupported original program");
Require(Sha(File.ReadAllBytes(typeof(Dialogue).Assembly.Location)) ==
    "d10c640b1b0b3664241b19137d3f0c27ffa8ba75e0fcf5dac183bbcc89b78f7e", "unsupported Yarn VM");
var program = Yarn.Program.Parser.ParseFrom(bytes);
string[] flags = [alexander, suggested, together, ryan, conrad];

void Check(string name, string node, string selected, string[] expectedMenu,
           string[] initialFlags, string[] expectedFlags, string? expectedReply = null,
           string? expectedFollowUp = null) {
    var store = new MemoryVariableStore();
    var dialogue = new Dialogue(store);
    dialogue.SetProgram(program);
    store.SetValue("$dragonModel", "test-model");
    store.SetValue("$dragonHead", "test-head");
    store.SetValue(food, 3f);
    foreach (string flag in flags) store.SetValue(flag, initialFlags.Contains(flag));
    var branch = Run(dialogue, node, expectedMenu, selected);
    Require(StateMatches(store, flags, expectedFlags), $"{name}: unexpected outcome flags");
    if (expectedReply is not null)
        Require(branch.Lines.Contains(expectedReply), $"{name}: expected reply missing");
    Trace? followUp = null;
    if (expectedFollowUp is not null) {
        store.SetValue(food, 4f);
        followUp = Run(dialogue, foodNode, [expectedFollowUp], expectedFollowUp);
        Require(StateMatches(store, flags, expectedFlags), $"{name}: follow-up changed outcome flags");
        Require(followUp.Commands.Contains("SetDragonState \"WaitingOnExitButton\""), $"{name}: follow-up missed exit state command");
    }
    Console.WriteLine(JsonSerializer.Serialize(new { name, node, initialFlags, expectedFlags,
        selected, branch, followUp, programSha256 = programHash }));
}

Check("alexander-accept", alexanderNode, accept, [accept, decline], [], [alexander], "line:36d49875");
Check("alexander-decline-fresh", alexanderNode, decline, [accept, decline], [], [], "line:b920f205");
Check("alexander-decline-existing", alexanderNode, decline, [accept, decline], [alexander], [alexander], "line:b920f205");
Check("conrad-suggest", conradNode, suggest, [suggest, invite], [], [suggested]);
Check("conrad-invite", conradNode, invite, [suggest, invite], [suggested], []);
Check("food-together-after-suggestion", foodNode, chooseTogether, [chooseTogether, chooseRyan],
    [suggested], [suggested, together], expectedFollowUp: "line:1a9a36e1");
Check("food-ryan-after-suggestion", foodNode, chooseRyan, [chooseTogether, chooseRyan],
    [suggested], [suggested, ryan], expectedFollowUp: "line:cd9b2a8f");
Check("food-ryan-without-suggestion", foodNode, chooseRyan, [chooseRyan, chooseConrad],
    [], [ryan], expectedFollowUp: "line:cd9b2a8f");
Check("food-conrad-without-suggestion", foodNode, chooseConrad, [chooseRyan, chooseConrad],
    [], [conrad], expectedFollowUp: "line:0d20d327");

static Trace Run(Dialogue dialogue, string node, string[] expectedMenu, string selected) {
    var lines = new List<string>();
    var choices = new List<string>();
    var commands = new List<string>();
    bool completed = false;
    string[]? menu = null;
    int emptyMenus = 0;
    dialogue.LogDebugMessage = _ => {};
    dialogue.LogErrorMessage = message => throw new InvalidOperationException(message);
    dialogue.CommandHandler = command => commands.Add(command.Text);
    dialogue.LineHandler = line => lines.Add(line.ID);
    dialogue.DialogueCompleteHandler = () => completed = true;
    dialogue.OptionsHandler = options => {
        var available = options.Options.Where(option => option.IsAvailable).ToArray();
        var match = available.Where(option => option.Line.ID == selected).ToArray();
        if (match.Length != 0) {
            Require(menu is null && match.Length == 1, $"duplicated selected option: {selected}");
            menu = available.Select(option => option.Line.ID).ToArray();
            Require(menu.SequenceEqual(expectedMenu), $"wrong available options for {selected}");
            choices.Add(selected);
            dialogue.SetSelectedOption(match[0].ID);
        } else if (available.Length == 0) {
            emptyMenus++;
            dialogue.SetSelectedOption(-1);
        } else {
            choices.Add(available[0].Line.ID);
            dialogue.SetSelectedOption(available[0].ID);
        }
    };
    dialogue.SetNode(node);
    for (int step = 0; step < 200 && !completed && (step == 0 || dialogue.IsActive); step++)
        dialogue.Continue();
    Require(completed && menu is not null, $"incomplete dialogue or missing option: {node}/{selected}");
    Require(commands.LastOrDefault() == "FinishDialogue test-model", $"missing finish command: {node}");
    return new Trace(menu!, choices, lines, commands, emptyMenus);
}

static bool StateMatches(MemoryVariableStore store, IEnumerable<string> flags, string[] expected) =>
    flags.All(flag => store.TryGetValue<bool>(flag, out bool value) && value == expected.Contains(flag));

static void Require(bool condition, string message) {
    if (!condition) throw new InvalidOperationException(message);
}

record Trace(string[] AvailableAtDecision, List<string> Selected, List<string> Lines, List<string> Commands, int EmptyMenus);
