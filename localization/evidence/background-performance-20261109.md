# Conrad mount scene completion and Windows background startup

## macOS gameplay

The source-pinned repair copy used the same isolated `Conrad_3_8`
fixture and background route as
[the gate test](background-gate-20261109.md). Profile `B8P1` loaded the
slot through the game menu, assembled the mount, completed the intro,
admitted Conrad through the gate and installed the mount at its
performance socket. The observer read the original runner's events
and the original performance controller's state. All navigation,
interaction, line advancement and option selection used virtual
keyboard and mouse state through the game's input consumers.

After `Conrad_placed_mount_3` began, the probe advanced with
`Player/Plap` and selected the stock option view for `line:0372e0d1`.
The original runner reported node and dialogue completion. With
neutral input during the performance, the original coroutine started
`Conrad_finished_mount_3`. The probe selected, in order,
`line:82cf49aa`, `line:aeae4744`, `line:a983ffa3` and
`line:6a2e4e0d`. The runner reported both completion events, and
the original controller subsequently exited with the in-progress
flag false and the completed flag true.

The fixture begins before either activity. These option IDs bind
the observed finish to the branch before the other activity has
completed. No repaired destination was reached in this run.
The condition for the later combined branch and the platform
difference are recorded in
[the transition evidence](yarn-transition-runtime-20261109.md).

All 392 macOS desktop samples showed no on-screen window and no
foreground ownership. The four checked original profile roots
matched their baseline. The signed wrapper removed its generated
Steam file and verified the signature. The player was stopped after
the coroutine exited, with no teardown exception in the log.

Local source and receipts are in
`localization/work/background-performance-20261109.41uqFb/`.

| Artifact | SHA-256 |
| --- | --- |
| `B8P1` Unity log | `b99969ce07f4633ac4dd5f4463c8acca4f6e8d1e35e383244d26bb2790512b6d` |
| `B8P1` observer receipt | `19376e397f8f5b6ac14291a289fa71b62fa20c4d2b2a322bba916e48a01038d2` |
| `B8P1` runtime companion | `877caec6b8a8052795f7a67666042911bcb208237cb3504061329a967c5e1946` |

The tracked [gameplay companion](../tools/background-input-probe/gameplay-companion)
reproduced the instrumented macOS game DLL. The success markers are
`VN-BG-YARN-COMPLETE Conrad_finished_mount_3` and
`VN-BG-PERFORMANCE-FINAL choices=4 inProgress=False completed=True`,
with no `VN-BG-FAIL`.

## Windows startup and normal slot load

The installed Windows game was read as source. A separate copy passed
a 288-file hash comparison with four intentional differences. The
asset builder produced the same repaired `sharedassets1.assets`
recorded in the earlier Windows test. A test profile change in
`globalgamemanagers` changes only the two strings identifying the
company and product in `PlayerSettings#1`. Read-back compared all
19 serialized objects. The other two differences are the
instrumented game DLL and the companion. The patcher checked the
original instruction sequences and branch targets in 2,328 methods.

The launch used a fresh private CrossOver bottle and
`-batchmode -nographics`. The companion requires Windows batch mode,
the exact test company and product, the corresponding isolated
`Application.persistentDataPath`, and a test-only command-line flag.
The runtime reported `Codex Test Sandbox/ProbeW8P1`. Both attempts
ran outside the installed game, with no foreground ownership or
on-screen window in 23 and 41 samples respectively.

The first attempt seeded the default slot directories, but the
original menu kept `LoadGame` inactive. The second attempt read the
slot-one directory from the original `SaveManager.GetSteamAndSlotPath`
before the menu initialized. The result was a nondefault directory.
The guarded helper copied only the fingerprinted synthetic fixture to
that path inside the isolated profile. Stock mouse input clicked
`LoadGame` and `LoadSlot1`. The original game loaded `PlayGame`
and the companion recorded the initial mount flags as false. The
observer then stopped the verified test process. The tested installed
files and original save directory matched their prelaunch snapshots.
The pre-existing hidden Windows copy remained running.

| Artifact | SHA-256 |
| --- | --- |
| Repaired Windows asset | `62e922ea6ee759b0d083695aa24580061989166c942a042cec95992924333065` |
| Isolated Windows profile settings | `7ffd21631303e3e5c87464bccaf159832455ba63b137c1b1f276e4a643d49e2d` |
| First Windows Unity log | `b699446e83cbf944cf67c56d9f6f3c0b33a0887579056e939c6a0104c29e347d` |
| First Windows observer receipt | `9e099eb30abf2deb9d1aa861075581f350caebd0f7773b6bd26d5aa571f51b35` |
| Successful Windows Unity log | `2e17c421c6f1096162e2332df17dbbdf72409f8e9d582cc06532258598b0e9d2` |
| Successful Windows observer receipt | `ee7df87ef5a26fc81ef03115dd9db1d14e4823b5ce0c4c0fc53ddfa6e7c5c0fb` |
| Successful Windows companion | `322ccb8b03f31db4324b29d7da5020aec1661474878af02b63c4c6d2d8b9d760` |

The Windows test source, isolated copy, fixture and logs are in
`windows-preflight/` within the local work directory. The second
observer deliberately stopped at scene entry.

## Windows gameplay continuation

A third launch used the same guarded Windows copy and synthetic
fixture with the full observer enabled. The original menus loaded
the slot, and virtual input opened both crates, assembled the mount,
stored it, completed the intro with the same three choices, opened
the gate with a hand hit and moved the mount into the performance
socket. The original runner completed `Conrad_placed_mount_3` and
`Conrad_finished_mount_3` with the same one and four choice IDs as
the macOS run. The original coroutine exited with the in-progress
flag false and completed flag true. The test observed no repaired
destination on this branch.

All 635 desktop samples showed zero foreground ownership and zero
on-screen windows. The observer verified the test process exited.
The installed files and original save directory matched the
prelaunch snapshots, and the pre-existing hidden Windows copy
remained running. The Null graphics device run logged 3,286
`NullReferenceException` entries at the same
`FluidEmitter.Tick` instruction. The receipt covers the observed
gameplay and Yarn events. Rendering and the cause of that exception
remain unverified.

| Artifact | SHA-256 |
| --- | --- |
| Full Windows Unity log | `763e6fcb222d64594240073b5d3714253b1da71069e3dd3fa6fc9b3842bdf5a6` |
| Full Windows observer receipt | `1a685e667778f2ae7b8258dea11389ad4ea68a687753a7b067095c34b2e6bb59` |

The original Windows `Conrad_3_8` configuration uses evaluation
type `USE_MOUNT_AND_JERKOFF`. Its evaluator reads both activity
flags. Its highest-priority evaluation returns `DONE` when the
dragon is `WaitingOnExitButton` and `CONFUSED` otherwise. The
Windows-only combined branch from `Conrad_finished_mount_3` reaches
`Conrad_Outro`, where the repaired transfer requires
`$cleanEvaluation == DONE`. The route to the combined branch and the
evaluation at its actual arrival still require runtime evidence.

For reproduction, build the gameplay companion against the original
Windows Managed directory with `-p:WindowsGameplayProbe=true` and
pass `--windows` as the final menu patcher argument. Copy the tracked
`dragons-windows-conrad-fixture.json` next to the test executable.
Use `isolated_profile.prepare_windows_gameplay(original_windows_data)`
to produce the profile settings bytes for a fresh copy. Use the
existing Windows asset builder with `--restore-yarn-transitions`.
Launch in a private bottle with the test-only argument
`-dragons-background-fixture-w8p1` and the same batch flags. The
tracked source reproduced both game hook DLLs and the Windows profile
settings byte-for-byte. Both wrong-build patcher cases rejected the
input fingerprint before output. All 180 localization tests passed.

## Windows combined-branch approach

A separate guarded repair copy loaded the same fixture, completed
the stock intro and opened the gate. After Conrad reached
`WaitingOnBeingWashed`, the probe used the original movement, look
and hand actions to approach the other activity before placing the
mount at the performance socket. The probe read the trigger center,
hand position and activity progress. It set no gameplay flags or
scene state.

The hand action fired, but the ray intersected `WalkableDragon`
about 0.60 world units from its origin. With the camera about 1.27
horizontal units from the trigger center, the settled hand was
about 0.81 world units from the trigger center. The original
activity response and progress remained zero, and the probe stopped
at its hand-contact deadline. The runner never reached the combined
finish or its outro in this attempt.

The observer verified that the copy stayed hidden in all 727
desktop samples and exited. The checked installed game files and
original save directory matched their prelaunch snapshots. Local
logs and probe source are under
`localization/work/background-combined-20261109.yMvcOH/`.

| Artifact | SHA-256 |
| --- | --- |
| Unity log | `68cd4060781bac142540e4048c3c805e8dfbf11c32e48bfcbb5ce1f757dc5bc8` |
| Observer receipt | `50f1f78875ac222b11c03ea47fd453af8c4bb118294093561b0416b37f08f82b` |

A second copy sampled eight approach points around the primary
trigger after the same gate opening. Every sampled direct ray
intersected `WalkableDragon`. The smallest predicted separation
from the trigger center was 0.500 world units. The stock movement
probe timed out before arriving at its chosen point, so this run
did not measure settled hand distance at that point. All 729
desktop samples showed no foreground ownership or on-screen
window. The copy exited and the checked original files and
profile matched their snapshots.

Original Windows IL also shows `WalkNWashDragonBoner.OnEnable`
registers the same hit callback with both its primary trigger and
`WalkNWashPenetratorPhysicsApprox`. The latter forwards events
from layer-six hitboxes in its 16 generated collider prefabs.
`PlapperHand.UpdatePlapper` only issues the overlap query after
the hand approaches the raycast target and the ray has a valid
surface collider. The next probe uses the original crouch binding
and tests geometry against both groups of hitboxes.

Local source and receipts for the second approach are under
`localization/work/background-contact-20261109.JXkGpp/`.

| Artifact | SHA-256 |
| --- | --- |
| Unity log | `316a70e4d3a40e986cf6c0a4148836c28597ab20a06a3d1ad4bd938761319997` |
| Observer receipt | `f952c81a621666843f4182fae842a4295eaa96518342f2af45896d8bbfa764de` |
| Original Windows interaction IL | `6fec704c1d973b8f006ac19ad0628f9dc49517da5be7687eb9a7279e1d7b7290` |

The first crouch probe counted 17 active hitbox candidates and
measured a primary sphere extent of 0.400 world units. After the
stock approach reached 1.271 horizontal units from the center, the
companion stopped on a null reference while obtaining the crouch
mode before pressing the key. The following probe reads the setting
from the active `PlayerController` instance. The failed run stayed
hidden in all 418 samples, exited, and matched the checked original
files and profile snapshots.

The local failed run is under
`localization/work/background-crouch-20261109.6ZBUGv/`.

| Artifact | SHA-256 |
| --- | --- |
| Unity log | `a9c82a686fd64ec89c4a9d55953448cb3baaa3bb37150677644dfa8602f44c19` |
| Observer receipt | `742ad793323c5dc2a3595365440fbe034fcd50075cddda2887caba684b4b5341` |

The corrected companion read crouch mode zero and activated it
through the original `C` input. The look origin lowered from
1.914 to 1.414 world units on the vertical axis. A sampled ray
predicted a gap of 0.074 to the nearest collider, while the settled
hand measured 0.330 away and both original activity counters
stayed zero. The observer reached its contact deadline, verified
that the copy exited and matched the original file and profile
snapshots. All 724 desktop samples showed zero foreground
ownership and zero on-screen windows.

The Windows `PlapperHand.UseContinuous` IL scales both stored
look-offset components by 0.1 before the surface raycast and
applies mouse look input while the hand action is held. The
corrected aiming probe in
`localization/work/background-hand-aim-20261109.Fo5uLh/`
uses the Windows scaling and adjusts aim through the held
stock input.

| Artifact in `background-crouch-20261109.ky4HUP/` | SHA-256 |
| --- | --- |
| Unity log | `e21c896135f3226251eb2a76f429167adcfba5db5c7d6cb43efbafc34bcabcd1` |
| Observer receipt | `232c38691573d343deff421515e6772631b688482f7d7629f59fe782c545997f` |

## Windows combined branch through stock input

The corrected aim reached zero measured collider separation
through held mouse and keyboard input. The original activity
counter rose and the original Yarn runner started and completed
`Conrad_started_jerkoff_3`, then started and completed
`Conrad_finished_jerkoff_3` with `line:5788e15c` and
`line:05c673e7`. The game set `DragonFinishedFromHandJob=True`.

The probe returned to the mount, installed it through the stock
selector and completed `Conrad_placed_mount_3` with
`line:0372e0d1`. The original performance then set its completed
flag and cleared its in-progress flag. The runner completed the
single-choice combined branch of `Conrad_finished_mount_3`
with `line:82cf49aa` and transferred to `Conrad_Outro`. The
original evaluation at entry was `CONFUSED` with dragon state 5
(`WaitingOnBeingWashed`). Yarn completed that routing node and
entered the existing `Conrad_OutroDirty` destination. The
observer stopped after that entry.

All 870 desktop samples confirmed the copy stayed hidden. The
observer verified it exited and the checked installed files and
original saves matched their prelaunch snapshots. Null graphics
again logged repeated `FluidEmitter.Tick` exceptions. This run
records gameplay events and supplies no visual acceptance.

| Artifact in `background-hand-aim-20261109.Fo5uLh/` | SHA-256 |
| --- | --- |
| Unity log | `ba2fcf4f4415fb30e1565ee878bac3bd23b0d8cfb1d6c8e7500dfedd50a94237` |
| Observer receipt | `e7636191a7dd99aabd00cb819862f94e43aaef72fca873d3d123a4ae29eed532` |
| Companion | `e69ff5b87909781bb1fcf0ff7a08dc51d86fc4d3750b78bc767c4cfb47227524` |

## Windows mount-last target candidate

In the original Windows code, `CanDoPerformance` requires state 5
and rejects a completed mount performance. The combined evaluation
returns `DONE` only in state 6. The original Windows state setter
and its direct callers were checked against the pinned assembly.
The exit button accepts state 6 and advances to state 7. It does
not change state 5 to state 6. The source `Conrad_OutroDirty` and
`Conrad_OutroSoapy` do not set state 6. The original
`Conrad_Outro_3` issues `SetDragonState "WaitingOnExitButton"`
at instruction 151. The source-pinned Windows state IL has SHA-256
`0b606db98b8c7cf9ace931a9f0067e1b3066ad2c1c64dd93da0195d47a60c695`.

In both builds, finishing the other activity last selects
`Conrad_Outro_3`. When the mount finishes last, the Windows node
`Conrad_finished_mount_3` selects `Conrad_Outro` while the macOS
node selects `Conrad_Outro_3`. That destination at instruction 89
is the only instruction difference between the two nodes.

The isolated Windows candidate replaces that single instruction.
The resulting node is byte-identical to the original macOS node.
Every other node, including the five appended repair nodes, and
all other protobuf fields compare equal to the previous Windows
repair. The candidate uses the original English table and is
under `localization/work/windows-conrad-done-20261109.PredoR/`.
The program SHA-256 is
`e4e29b20afff9ba3306431ed316cbbb327c06e535ebcc2200b2f20bc06c00d8d`
and the Windows asset SHA-256 is
`59ccbdabf4579e47f0e7f8c353b7f697fcd54368423484c341c4f13803a5d335`.
The isolated runtime probe checks the mount-last destination, four
stock option clicks, dialogue completion and state 6.
