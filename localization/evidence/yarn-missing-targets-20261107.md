# Missing named Yarn targets: source finding

The source-bound audit `localization/audit_yarn_targets.py` SHA-256 `2dabc91fde7c4c8f67ac4f0ca18de7c1a09d3190843646edfc5de9a854c55a3a` inspects named `RunNode` and `DetourToNode` instructions in the one extracted, version-pinned Yarn project from each installed build. Its reproducible report `yarn-targets-20261107.json` SHA-256 `9cd529422340084c5dda98865ad485930d8a92fb6790c77c9a7c2e66a70068e4` records 89 named transfers per build, five of whose target names are not keys in that extracted program's 195-node map. The same five source locations and names appear in both builds:

| Source node, instruction | Absent target | Node containing matching title-like line |
| --- | --- | --- |
| `Alexander_Idle4`, 21 | `Alexander_Done` | `Alexander_Outro` |
| `ConradBeatup_Outro`, 21 | `ConradBeatup_OutroDone` | `ConradBeatup_Outro` |
| `Conrad_Outro`, 21 | `Conrad_OutroDone` | `Conrad_Outro` |
| `RyanDate_Outro`, 0 | `RyanDate_OutroDone` | `RyanDate_Outro` |
| `RyanExploded_Outro`, 21 | `RyanExploded_OutroDone` | `RyanExploded_Outro` |

Each target name also appears in a distinct `RunLine` value beginning `title: `, immediately between separate `==` and `---` RunLine values. These fifteen source IDs and their exact locations/hashes are captured in the report and in `special-scenes-missing-targets-20261107.json` SHA-256 `facfab83e94c85823786f1460d4e621f6a73352ba8f197a8148fa9707a18a6c9`. An embedded title-like line is not a compiled node map entry. No inference is made that it is intended to be shown or that its surrounding lines can safely become a new node.

Static inspection of the game's identical macOS and Windows `YarnSpinner.dll` SHA-256 `d10c640b1b0b3664241b19137d3f0c27ffa8ba75e0fcf5dac183bbcc89b78f7e` found that `VirtualMachine.RunInstruction` sends `RunNode` to `ExecuteJumpToNode`, which calls `SetNode`. In the inspected `SetNode` overload, a missing program-map key sets the execution state and throws `Yarn.DialogueException`. Thus, **if** one of these transfers executes against only the inspected program, the VM cannot enter the named target. This is a static inference, not a demonstrated gameplay failure: the actual runtime program might include merged nodes, the transfer may be unreachable, and game-level handling has not been checked. Do not silently repair or infer story behavior from this observation; investigate loaded program, reachability and intended continuations before deciding any fix and before claiming end-to-end progression.

Until the source role is resolved, `dialogue_locale.py` retains its existing exact rule for `title:` strings and additionally requires the ten specific adjacent `==` and `---` IDs to keep their original values in Yarn locale input. The new rule is ID-scoped and does not apply to UI/settings. Both pinned source tables accepted all ten original values and rejected a changed marker at the intended guard. Four audit tests cover missing/present nodes, marker association, unexpected transfer operands and unknown line IDs; the locale tests cover every new ID, unchanged positives, changed values, stale source and non-Yarn/other-ID controls. These checks are partial protection, not the complete preserve-exactly manifest or proof of runtime correctness.

Reproduce the static report with pinned Python dependencies and `audit_yarn_targets.py --macos-data <original macOS Data> --windows-data <original Windows Data>`; a second run matched the saved report byte-for-byte. No game files were modified.
