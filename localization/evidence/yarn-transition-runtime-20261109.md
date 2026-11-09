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

The follow-up Windows repair also changes instruction 89 in
`Conrad_finished_mount_3` to the original macOS target `Conrad_Outro_3`.
The builder output completed that outro through stock input and
reached the exit button state in a background CrossOver copy.
The comparison, prior control and successful run are in
[the Conrad follow-up](background-performance-20261109.md).

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

## Equipment setup and background input

The pinned Windows level and managed assembly bind the phone instruction to
the real equipment path. `InteractableCrate.CanInteract` requires an equipped
`Crowbar`. The level's `MountFrame_Socket (1)` (component `4046`) accepts the
frame and sets `HasMountFrame` and `PlacedMount`. The other socket
(component `4221`) requires `HasMountFrame`, sets `PlacedMountForUse`, and
has the performance trigger. Both serialized components round-tripped exactly.
The order matters for replay. `Conrad_finished_jerkoff_3` stores
`$conrad_jerked_off_3` and, if the mount was already used, selects
`Conrad_Outro_3`. `Conrad_finished_mount_3` stores
`$conrad_used_mount_3` and, with the earlier activity completed, selects
`Conrad_Outro` on Windows. Its `DONE` branch selects the restored
`Conrad_OutroDone`. These are original instruction bindings, with actual
player reachability still pending.

The repair-only copy was reopened from the disposable slot. A guarded
Windows `SendInput` helper accepted relative pointer events while the game
owned foreground focus. Camera aim and mount placement were not established.
The game was then hidden and left running at the owner's request. In that
state the helper resolved foreground focus to the bottle's Explorer process
and refused to send input. The background test therefore establishes safe
refusal, while normal transition reachability remains open. Local logs and
helper source are in the `playthrough-20261109.f7XBcc` directory under the
builder-test work directory above.

The repair remains opt-in. The source, renderer, glossary, and
special-scene readiness gates remain open.

## Hidden player follow-up

The live repair-only process (macOS PID `16018`) was still hidden, inactive,
and without any on-screen window. Its existing log `normal.log` remained at
5,523 bytes with `Waiting for flag PlacedMount...False` as its last line.
The last write was 19:25:43 local time, before the input helper's recorded
refusal at 19:26:27. The application and bottle were left running.

Both original `globalgamemanagers` files matched the source-build hashes in
`compare_yarn_versions.py`. Their serialized `PlayerSettings#1` has
`runInBackground = false`. Each object decoded with the existing reader's
trailing-byte handling and round-tripped to its exact original 884 bytes.
The repaired Windows copy uses the same `globalgamemanagers` and
`Assembly-CSharp.dll` as the original Windows build.

An IL scan covered all 170 macOS and 172 Windows root managed DLLs. The only
direct reference to the background setter on each build is in the Unity
`Device.Application` wrapper. No application code directly calls either
setter. In the Windows `StartDragonWalkRoutine` coroutine, the wait message
goes to `Debug.Log` before a one-second `WaitForSeconds` yield. The hidden
run's stopped log is consistent with the configured focus behavior. This
observation does not measure native or reflection-based overrides, and it
does not establish what would happen with background execution enabled.
Addressing the old foreground guard alone would leave the simulation
boundary untested.

The existing Windows 11 VM reported `suspended` and the local CrossOver
installation supplied the Mac window driver only. No alternative running
Windows desktop was identified. Normal gameplay with background operation
still needs a private desktop that can supply ordinary input with the game
active inside it, or a separately validated background test route. Neither
the VM nor the hidden game was restarted.

Local source and receipts are in `localization/work/transition-background-20261109.VnR2nY/`:
`Program.cs`, `macos.il.txt`, `windows.il.txt`, `window-state.swift`, and
`window-state.txt`. The unchanged `normal.log` in the prior run directory
has SHA-256 `ed0b63da2f1f7b167df4a435f6752df3bb5d677507fa8f1a80d73a2635e11c83`.

## Direct callers of the four other routing nodes

The original programs in both builds contain no exact operand
references to `Alexander_Idle4`, `ConradBeatup_Outro`,
`RyanDate_Outro` or `RyanExploded_Outro` from any instruction.
A direct scan of 170 macOS and 172 Windows managed DLLs found no
matching string literal. A separate raw-byte scan of 17 top-level
serialized game files per build found two occurrences of each name,
both inside the original YarnProject object. Their position and
protobuf decoding identify the map key and the node's own name.
The same scan finds the Windows `Conrad_Outro` instruction reference
and the `Conrad_Outro_3` level configuration field in each build.
These positive controls distinguish node definitions from callers.

The reports and per-file fingerprints are in
`localization/work/yarn-ordinary-callers-20261109.IIkjOt/`.
This covers exact managed literals, compiled operands and top-level
serialized byte matches. Dynamic name construction, reflection and
compressed or external resources need separate investigation before
claiming the four nodes cannot be reached through gameplay.

## Compiled transfer and entry-point follow-up

Reading both original YarnProject objects again found 195 nodes and
89 named transfers on each build. The decoded instruction lists
contain no dynamic run or detour opcodes. None of the 1,472 command
instructions in either program starts another Yarn node through
the game command handlers.

The whole managed reference scan matched the 170 macOS and 172
Windows DLLs in the pinned inventories. It found 26 methods per
build that call or reference the selected Yarn runner, node or
program APIs. The seven game-code callers cover the runner's
existing project, the shared start coroutine, the on-enable
dialogue component, the window and phone, and the dragon bark
path. The start methods pass the selected name through unchanged.
The traced name sources are serialized component fields and
level dialogue fields, including the progress, idle, nag, intro,
phone, mount and finish dialogue paths. The five serialized
runners have auto-start disabled and share the same Yarn project.

All 31 pinned local StreamingAssets files per build were checked
for the four routing names in UTF-8 and both UTF-16 byte orders.
The three bundles were also decompressed and their 14 serialized
objects inspected. No matching name was found. The APV files were
checked for raw matches against the pinned bytes.

The conservative named closure starts with the 123 nonempty
serialized game dialogue references and adds the configured
`Start` node as a precaution. There are 95 distinct root names
per build. The graph follows every named transfer, including
conditional ones.

| Program | Reachable nodes | Missing named targets in this closure |
| --- | ---: | --- |
| Original macOS | 133 | None |
| Original Windows | 137 | `Conrad_OutroDone` |
| Current repaired macOS | 133 | None |
| Current repaired Windows | 133 | None |

The four legacy routing nodes are absent from each closure.
Adding those names as test roots made the graph include them,
confirming the reachability check distinguishes defined nodes
from rooted ones. The four individual transfers have controlled
VM evidence, while ordinary entry into those nodes has not been
observed. Reflection, external programs and uninspected entry
points remain outside this proof.

Reports are in `localization/work/yarn-dynamic-callers-20261109.MlBmaH/`.

| Report | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Managed caller IL | `f4c434ed2cf776a4ddb3699fd817b9f5f5d846d7b4d0f030b007c7864d6baa12` | `e9fc697da1764e01b6679f783f8f3bca3a839a774feac9968900404abe9cdbb7` |
| Game entry names and their sources | `465d353634c6efa3a900a0b14784feb4ab187bd1652445d8240a017a29b969dc` | `ca753042a710e19864a270087d3e1c13cefd61389cb3b4733f40ec5fcdb3bacb` |
| Program and streaming evidence | `9d25a71faf842a21b18afac070bfbee1d4e614292f7384082eda81fb0246f28a` | `3af798920446138b31d12508992f5a10e04e25f85cd64682a274f506a002f426` |
| Named closure | `ebc365f20e2733fd97f4152ea0b128fbb27008de9b1794ed071847d01751bccf` | `fdc4bd66ff7f42699a68dafab0d54ce9c80e48f7065e9add77a55f48ada178b7` |
