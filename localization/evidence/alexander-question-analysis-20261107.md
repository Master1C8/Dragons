# Alexander question groups

The source-bound extractor `localization/inventory_alexander_questions.py` SHA-256 `6fa5a853a355ac2fb4dd6d195d37c5c62e74d12768cc946418f76b3f645a2c2b` checks the pinned Yarn source objects and compiled control instructions for both installed builds. It produces `alexander-question-groups-20261107.json` SHA-256 `fd7f9cb5fd3e5e654ca07e4a84ad17aee2794b042765c6ae54c6c36a9bd824fc`, binding all 77 line/option IDs in `Alexander_questions` to seven complete instruction ranges plus the shared exit option. The two builds have the same bytecode for that node and the same English values for these IDs. The generated inventory lists source fingerprints, exact instruction positions, choice destinations, state variable names and command strings; source wording remains available in the local paired-scene export. This is static node-bound grouping, not proof of in-game reachability or complete game-source discovery.

The seven question options each read a distinct `$Yarn.Internal.Once.line:...` boolean, initially false in the extracted program, and use `Bool.Not` as the option condition. Entry to each chosen range stores true to the corresponding variable. After its branch, each range stores true to `$has_asked_question` and transfers back to `Alexander_questions`. The shared exit option is conditioned on that latter variable and transfers to `Alexander_3_required_end`, whose first instructions reset `$has_asked_question` to false. The once-state variables, branch destinations and identities must stay exact. This source inspection does not establish lifetime, persistence across saves, all external callers, or dynamic command behavior.

Two source groups require special locale decisions before ordinary translation, recorded in `special-scenes-alexander-20261107.json` SHA-256 `5efe4c18581eddd9929227750dfb34842142c172e3cb3bd18d36e58953aa5a51`:

- The number-seven question uses an unexpected taste, color and fruit association, then distinguishes two citrus fruits in nested choices. Review all ten question/response/choice IDs together and preserve the number, contrasts and branch identities.
- The family-crest explanation uses seven ordered `<size=...>` tags to progressively shrink a long line, includes a reference-like passage, and offers distinct replies. Review all ten IDs together and verify the rendered effect and readability. The owner's exclusion of text on textures remains in force; character visuals and their relation to the explanation remain unreviewed.

Neither case has accepted Russian wording, complete visual dependencies or an adaptation decision. The registry is partial; it does not establish the absence of other special scenes. Four focused tests verify boolean decoding, duplicate-key rejection, the real 77-ID group coverage, a changed control operand with the source hash guard deliberately satisfied, and exact size-tag order on the real crest line. For the tag negative control the unchanged source passed first and a reordered sequence with the same tags failed specifically at the markup-order guard. Reproduce the source inventory with pinned Python dependencies and `inventory_alexander_questions.py --macos-data <original macOS Data> --windows-data <original Windows Data>`; this does not modify either game.

## Paired desktop Yarn control, 2026-11-10

The [desktop probe](../tools/alexander-question-runtime-test/Program.cs)
executes the original Yarn VM and compiled program of each pinned build.
This supplies the observed control behavior for
`yarn-alexander-question-once-state` in the pinned
[source registry](special-scenes-pending-20261107.json).
Extract the program with `compare_yarn_versions.load(data, BUILDS[platform])[3]`.
Build `localization/tools/alexander-question-runtime-test` with .NET 8 and
`-p:ManagedDir=<that build's original Data/Managed>`. Run its DLL with
`macos|windows <original program.bin>`. The probe checks both the program
hash and the loaded `YarnSpinner.dll` before running. The Windows binary
rejects the macOS program at the program fingerprint check.

In a fresh in-memory variable store, all seven questions are available
and the exit is unavailable. After each of the seven selections, its
original once flag is true, its choice is unavailable, and the exit is
available. After the last question, the exit is the only available choice.
It reaches `Alexander_3_required_end`, resets `$has_asked_question` before
`line:3027bcf7` and leaves the seven once flags true. Reentry in that
same store finds zero available choices. Separate fresh runs take all
three number-seven reply paths and both crest reply paths. Each reaches
its distinct expected line sequence and can exit. After exit and reentry
in those five runs, the six unchosen questions remain available.

The six scenario traces match across builds after excluding the expected
program hash difference. Local output is in
`localization/work/alexander-question-runtime-20261110.aCqz9A/`.
The separate Python regression suite passed all 194 tests with the
paired build tools enabled.

| Trace | SHA-256 |
| --- | --- |
| `macos.jsonl` | `67c5f247551df049f94171487e13dd3cdd86c694dfdc6110b2ca96ffe35b6cd7` |
| `windows.jsonl` | `c73d17296db2ed747563edd206c25f2ff50756f1433f7d94cd96e2b7bf3e040a` |

The probe injects the entry node and uses line-ID selection callbacks.
The Unity presenter, game command effects, save serialization and reload,
visible choice interpretation and size-tag rendering are outside this
control. Russian wording and those checks remain open.

## Managed save round trip, 2026-11-10

In both pinned game assemblies, `WalkNWashSceneState.OnEnable` attaches
`OnYarnFlagSet` to the Yarn store's global change listener. The callback
passes boolean writes to the game's flag registry after removing `$`
from the ID. `FlagRegistry.ToJson` emits that ID and boolean as a
`BOOL` entry. `WalkNWashSceneState.NextLevel` calls `Flags.Save`;
`Awake` calls `Flags.Load`. `FlagRegistry.Load` clears the Yarn store
and, on successful slot read, calls `FromJson`. That method dispatches
the saved ID and boolean through `WalkNWashSceneState.SetFlag`.
The boolean setter adds the `$` prefix before calling the Yarn store.
The macOS save includes a version header and uses `SaveManagerV1`.
The Windows path uses `SaveManager`.

The [save probe](../tools/alexander-question-save-test/runtime/Program.cs)
runs each question and the shared exit in the original Yarn VM, using the
original managed Unity Yarn store. In a fresh test for each question,
the real callback and serializer produced exactly two flag entries.
The selected `Yarn.Internal.Once.line:…` was true and
`has_asked_question` was false after exit. The probe then cleared a
separate store, parsed the synthetic save through stock SimpleJSON, and
ran the game's `FromJson`. On reentry the six unchosen questions were
available in their original order, while the chosen question and exit
were unavailable. For each matching negative control, changing one
character in the selected once key restored the seven original choices,
with the exit still unavailable.

For reproduction, build the [patcher](../tools/alexander-question-save-test/patcher/Program.cs)
with .NET 8 and invoke its DLL with
`macos|windows ORIGINAL_GAME_DLL NEW_PROBE_DLL`. It fingerprints the
input and only creates a new file. Build the probe runtime project
with `-p:ManagedDir=<that build's original Data/Managed>` and invoke
its DLL with
`macos|windows ORIGINAL_PROGRAM ORIGINAL_MANAGED PROBE_DLL PROBE_SHA256`.
The wrong-platform patcher control rejected the input and created no
DLL. The probe traces for both platforms are byte-identical. Output is in
`localization/work/yarn-save-boundary-20261110.bDCIbl/`.

| Artifact | SHA-256 |
| --- | --- |
| Both seven-scenario traces | `df5cd13895fb503e19cf9ae2b4dcb65f7c19d199917dae83260424fdd6219e7b` |
| macOS probe DLL | `cdcb7abccf4cac12acd09e22046e55fa1a64c6391979990c5ca2171b791019f0` |
| Windows probe DLL | `2c7e77dd4aa300411bc26363e9b42afe379d8a4328aaba2cc2f9b11a4eb88c5c` |

The probe substitutes Unity's native object lookup and debug logging
in the scratch game DLL, initializes the managed store and scene without
native constructors, and explicitly attaches the stock listener. It
invokes the save serializer and loader in memory. It does not call
stock slot I/O, trigger a real level transition, launch either game or
read or write player saves. Unity gameplay reload and visible choice
presentation remain to be checked on delivered artifacts. Preserve the
seven variable names and choice IDs from the
[question-group inventory](alexander-question-groups-20261107.json)
through packaging.

## Stock slot disk control, 2026-11-10

The desktop probe extends the in-memory control to real disposable
files. It executes the original Yarn routes, flag callbacks and
`FlagRegistry.Save` / `Load`. The macOS registry delegates to
`SaveManagerV1`; the Windows registry uses `SaveManager`. Their
original `FileManager` calls create directories, write JSON, copy
the backup and read the save from disk.

The source-pinned scratch assembly replaces Unity's persistent
data root with a new project scratch directory and forces the
non-Steam path branch. It supplies the managed Yarn store in place
of the native object lookups and suppresses native debug calls.
The probe initializes the managers' `FileManager` fields using
their original indexed slot path methods. Unity PlayerPrefs and
Steam user selection are outside the probe.

Each of the seven original question choices passed on both builds:

1. Selecting the question and exiting writes its exact once key
   and a false exit flag through the stock registry. The first
   file matches the registry's JSON for level index 6.
2. Saving index 7 to the same slot replaces the main file. The
   generated `savegame_backup.dgn` matches the first file byte-for-byte.
3. Loading into a fresh store restores index 7, the chosen once
   flag and the false exit flag. Only the six unchosen questions
   are available in the original Yarn VM.
4. Loading a separate empty slot leaves all seven questions
   available, creates no slot files and leaves the first backup
   byte-identical.

The macOS control used `defaultUser/slot1` and wrote the version-1
header. The Windows control used `defaultUser_slot1` and wrote the
legacy payload. The resulting choice lists match across platforms.
The probe does not execute a native Unity scene reload, press
Conrad's exit button, or exercise crash or backup recovery. No
installed game or player save was written.

The two source files extend the existing save-probe recipe and are
under `localization/work/stock-save-boundary-20261110.1eWIVW/`.
Build the patcher and runtime as in the previous section and
append a new scratch-directory argument to the runtime command.
The two traces record the first, backup and overwritten file
hashes for all seven paths.

| Artifact | SHA-256 |
| --- | --- |
| `patcher/Program.cs` | `082f37124d5c26ec204f71d6b095171369da35de10e817f3aabc4418afb23b52` |
| `runtime/Program.cs` | `65c2a62589d43dd8ba07b158a673ca861a7192859a0f3d89441dacb4f366c66d` |
| macOS scratch assembly | `7c7773cd46c1befffa33e9cf820a7c4d5f9e5dda458a83d1355fe35554567412` |
| Windows scratch assembly | `db2a2e98b500c92a36947ffb43b869224ca1e11b2bc15a593bb43135a9821f20` |
| macOS disk trace | `5b053e93ed62070c91e40d2311bbe9799bba0d9666d8bef109533dda5c386d6f` |
| Windows disk trace | `9e5ff6822f335fd4813fc8f9beccad2ef291cfa0c1302bc3dbe42a66cf22c312` |
