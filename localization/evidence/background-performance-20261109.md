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
