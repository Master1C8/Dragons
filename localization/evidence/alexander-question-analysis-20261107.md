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
