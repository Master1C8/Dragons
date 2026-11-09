# Pivotal relationship choices: source analysis

`localization/inventory_romance_routes.py` SHA-256 `2f79cc6eb87769b31ca1e10a265df22887041a8f94cf2c4a3126bc89299e7cef` traces seven player-facing choices in `Alexander_5_romance_route`, `Conrad_Outro_3` and `ryan_food_dialogue`, together with explicit reads and writes of five selected Yarn variables. Its output `romance-route-source-20261107.json` SHA-256 `c717112dec2ba06871a105aed62dfc61b9812120c9065f906edf9e76798a0753` pins both original programs, node bytes, exact control locations, source IDs and text fingerprints. In each build the five variables have false initial values, occur in 102 explicit read/write instructions across 16 directly related nodes, and their forward closure through named Yarn transfers covers 38 nodes and 708 line/option IDs. Those IDs and control references match across the two builds; ten source values within the closure differ. There are no missing named targets within this particular static closure. This is not a count of reachable or completed translations, nor a complete dependency graph: code-side state, reverse callers, dynamic behavior, external assets and other variables remain unreviewed.

The inspected source distinguishes these decisions:

- `Alexander_5_romance_route` presents choices described as accepting or declining an Alexander romance. The accepting path contains a write of true to `$alexander_romanced`; the source caption for the other choice describes no romance. The inspection does not establish that the declining path clears any earlier state.
- In `Conrad_Outro_3`, suggesting Ryan writes true to `$suggested_ryan_to_conrad`, while the other major choice writes false. In `ryan_food_dialogue`, conditional choices test this value and separate choices write true to `$ryan_conrad_romanced`, `$ryan_romanced` or `$conrad_romanced`. The source captions tell the player which relationship outcome each option enables or locks in. Later scenes read and also write these variables, so an isolated line-by-line translation is insufficient.
- `Ryan_4_intro` also contains a source branch guarded by `$isEditor` that writes the suggestion variable. Its presence in the compiled program does not establish that normal players can reach that branch.

`special-scenes-romance-20261107.json` SHA-256 `b8da7bd161086ad9cd4e1b8f858eaac78ff9cf7b634a118bcdbdcb8ec5857673` records two incomplete decision groups, exact pivotal IDs, state identities and conservative forward source scopes. The Alexander group has 41 IDs in two named-transfer nodes; the Ryan/Conrad group has 691 IDs in 37 nodes. The scopes overlap and are not additive. They are broader contexts for review, not a claim that every included line is a special case. Actual Russian wording, caption readability, all choice outcomes and runtime progression remain pending. Text on textures is excluded by the owner's decision.

Reproduce with pinned Python dependencies and `inventory_romance_routes.py --macos-data <original macOS Data> --windows-data <original Windows Data>`; a second run matched the saved JSON byte-for-byte. Three focused tests cover conditional choice destinations and true/false flag writes, full real-source closure, and all seven original choice-markup sequences. A matching positive control passed before a modified destination was injected while the preceding source-loader guard was deliberately replaced for the test; the intended control-instruction check rejected it. Reordering the same original markup tags was rejected at the markup-order check after the unchanged source passed. These checks do not prove translated wording, correct rendering, or natural gameplay.

## Controlled paired Yarn runs, 2026-11-10

The [desktop route test](../tools/romance-route-runtime-test/Program.cs)
starts the original nodes in the pinned Yarn VM with test state and
records available choices, lines and game commands. It checked nine
scenarios per build, covering all seven pivotal IDs:

| Entry and state | Observed outcome |
| --- | --- |
| Alexander accepts | The romance flag is set and the accepting reply appears. |
| Alexander declines with no prior romance | The flag stays false and the declining reply appears. |
| Alexander declines with the flag already true | The same declining reply appears and the earlier flag stays true. |
| Conrad receives the Ryan suggestion | The suggestion flag becomes true. |
| Conrad receives the direct invitation with suggestion already true | The suggestion flag becomes false. |
| Food stage 3, suggestion true | The player can choose the Ryan–Conrad match or Ryan romance. Both were exercised. |
| Food stage 3, suggestion false | The player can choose Ryan or Conrad romance. Both were exercised. |

Each food stage 3 selection set only its own romance flag in the
tested fresh state. Stage 4, using the same variable store, offered
the matching follow-up option. The IDs are `line:1a9a36e1` for the
match, `line:cd9b2a8f` for Ryan, and `line:0d20d327` for Conrad.
Each route issued the exit-state and finish commands. The choice
caption for declining Alexander describes the outcome of the new
choice. It does not imply that this choice clears an earlier flag.
The Ryan choice remains available on either side of the suggestion
condition, so the suggestion and invitation captions must preserve
the source's distinct claims without adding exclusivity.

For an empty available option set, the test uses `SetSelectedOption(-1)`.
All five original serialized dialogue runners per build have
`allowOptionFallthrough=true` and `runSelectedOptionAsLine=false`.
Both flags were read from byte-round-tripped runner objects. The
original Unity runner's no-selection path passes `-1` to Yarn when
fallthrough is enabled. The desktop harness supplies these callbacks.
It does not exercise Unity menu rendering, live game commands or saves.

Build the test with .NET 8 and
`-p:ManagedDir=<original Data/Managed>`. Invoke its DLL with
`macos|windows <original program.bin>`, extracted through
`compare_yarn_versions.load`. The wrong-platform program control
failed at the input hash guard. Both builds' traces matched except
for the program hash, and five focused source and index tests passed.
Local receipts are under
`localization/work/romance-route-runtime-20261110.XhiiQO/`.

| Receipt | SHA-256 |
| --- | --- |
| macOS trace | `f62b84d20741075d63e90664031b73c862cd3a6139663833594d629eeb3cac39` |
| Windows trace | `fd6a2640c2f0e35650b807318bc0f773676d99b998c9860a52cccc07f6b7a975` |
| Serialized runner options | `07eba14659ff7dd9e3c3eec85de70dd8f73e8fea4b2fa7d1c0fd356a8011ae3e` |
