# Missing Yarn destinations in Unity

The five named transfers in the [static source finding](yarn-missing-targets-20261107.md)
were exercised in separate macOS test profiles. The base game asset and
`YarnSpinner.dll` matched the original byte-for-byte. A test bridge selected the
source node at `WalkingToWindow` and set `$cleanEvaluation` to `DONE`. The
instrumented Unity runner logged before its original `Dialogue.Continue` and
logged the original exception at its async catch site. Each failure came from
`VirtualMachine.ExecuteJumpToNode` and named the expected absent destination.

| Profile | Source | Absent destination |
| --- | --- | --- |
| QW31 | `RyanDate_Outro` | `RyanDate_OutroDone` |
| QW32 | `Conrad_Outro` | `Conrad_OutroDone` |
| QW33 | `ConradBeatup_Outro` | `ConradBeatup_OutroDone` |
| QW34 | `Alexander_Idle4` | `Alexander_Done` |
| QW35 | `RyanExploded_Outro` | `RyanExploded_OutroDone` |

A separate Windows 9/9/2026_ee944596 copy in a fresh CrossOver bottle reproduced
the same `Conrad_OutroDone` exception. Its YarnProject and core Yarn DLL matched
the pinned originals. The prior Windows probe copy retained its synthetic table
input. Both Unity tests used a forced scene entry. In desktop Yarn, a test
starting one node earlier at `Conrad_finished_mount_3` with the required
flags set and automated line/choice callbacks reached `Conrad_Outro_3` on macOS,
hit the missing-node exception on Windows, and reached `Conrad_OutroDone` in the
Windows repair candidate. This exercises the relevant script condition with
controlled inputs. Normal player reachability and native Windows remain unverified.

## Repair experiment

Each matching `==`, `title:`, `---` group is followed by a self-contained
block from the original compiled program. The candidate appends five named
nodes containing those existing instructions, starting after the marker and
ending at the original node's end. All 195 original serialized node bodies,
initial values and original program bytes were preserved. The asset read-back
found only the YarnProject object changed. The candidates preserve the existing
line IDs, table entries, and commands. The results establish a feasible repair
for these controlled cases. The inferred boundaries still need normal-scene
regressions before integration into a player build.

The original core Yarn VM executed all five restored nodes to completion in both
builds in desktop .NET, with line/command callbacks recording output in place of
Unity presenters and actual game commands. In Unity, macOS QW37 entered the
restored `RyanDate_OutroDone` and invoked the original line handler. A second
fresh CrossOver bottle entered the restored `Conrad_OutroDone` and invoked the
original line handler. Each of these two runs started at its source node under
the same controlled conditions as its failure case. Completion of the live
Unity dialogue, actual gate/dragon side effects, normal entry, and visible
readability are separate checks.

Local evidence and scripts are under `localization/work/transition-unity-20261109.G2AxDU/`.
The desktop prototype is `repair-probe.cs`, the ancestor route check is
`conrad-route-probe.cs`, and the Unity diagnostics are in `tools/Program.cs`.
The builder probes use `apply-candidate.py` and `observe.py`. Key result hashes:

| Artifact | SHA-256 |
| --- | --- |
| macOS candidate program | `7d4a0f1ecb58565a1fd1dc154d2ba3c4c9e4caf1832589da3a53f0e88b5768cc` |
| Windows candidate program | `6d2dfffecadd81cdeca8ff5e3781bb5ab7e36b7b603f3d6265a444959f73b3f0` |
| Desktop repair logs (same bytes for both builds) | `ab05246af70859376e12a8950f411f3a6fa7d4727da12ac0835c9183005764dc` |
| `conrad-script-route.jsonl` | `c45a6fc05c4f3c45416f96179a0a0b4f2b5741cc3229e8090ada59d0c9433ddc` |
| `QW37.unity.log` | `765ed8fbe0a4ad68b85f658c255cb93e295395ae21dcb9ac0c65ae83476389c8` |
| `win-conrad.unity.log` | `bb9da96b509031a269b82244822f52a549067b4ffc0189093c7116cd1dc64f8c` |
| `win-conrad-fixed.unity.log` | `45e6c358c8fc98090e7e8dda4e5d158bdd6163ec577bcd871d5a56cbc6683e7c` |

## Builder integration and normal input

Commit `1f28b03` adds `--restore-yarn-transitions` to the macOS app builder,
Windows asset builder and combined asset verifier. The outputs regenerate
the exact candidate program hashes above. A real-asset regression exercises
combined dialogue, UI and repair on both builds, checks each object, and
rejects corrupted project bytes and a repaired asset without the explicit
verification flag. All 170 localization tests passed.

A separate Windows CrossOver test used the original managed assemblies and
loaded a disposable slot through the game's normal menu. The pinned
`LevelFlow` object maps save index 7 to `Conrad_3_8`. The legacy slot included
the six unconditional start/end flags from the preceding levels, with
`PlacedMount` left unset. The fixture SHA-256 is
`f22430735fb7e3d69be1a525ba0eb6d2633d50af66ba243414bc67c4e7dbec09`.
The original and repair-only copies used the same isolated CrossOver
profile, fixture and viewport in successive runs. The candidate verified
exactly against the original with a no-op dialogue input and only the
YarnProject object changed.

Both runs rendered the scene and recorded `DeliveredMountFrame=True` and
`Waiting for flag PlacedMount...False`. An earlier blank frame was not
reproduced in this paired check. Guarded player movement and interaction
inputs were sent in the repaired build, but the flag remained false and
the restored transition was not reached. This proves ordinary menu loading
and entry into the scene before the transition, with no injected state or
dialogue call during play. Normal-play transition completion and its
side effects remain pending.

Artifacts are in `localization/work/transition-builder-20261109.8zft9T/`.
The Windows repair-only asset SHA-256 is
`62e922ea6ee759b0d083695aa24580061989166c942a042cec95992924333065`.
The two logs are `natural-original-control.log` and
`natural-repaired-control.log`. The game-window captures are
`control-world.png` and `repaired-control-world.png`. The latter was
prepared separately as a 1280 × 1013 WebP80 preview for visual inspection.
The original SHA-256 is
`d3db8e65da9f4dbb5067f266cd1601b5803c1aaa9574548a7b376442ce7ea4df`;
the preview SHA-256 is
`0dd6a37ef25cf861a5ce68de635dd7ffdbb7a37dad14f9fbce82fd7c97f88316`.

The repair remains opt-in. The source, renderer, glossary, and
special-scene readiness gates remain open.
