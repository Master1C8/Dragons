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
observer deliberately stops at scene entry. Equipment input, Yarn
completion, repaired transfers and visible Russian on Windows remain
open.
