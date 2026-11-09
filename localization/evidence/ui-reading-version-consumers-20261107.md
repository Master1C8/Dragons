# UI source reading and version consumers

The coordinator read the 162 source-bearing Windows TMP fields identified by
`ui-source-roles-20261107.json`, together with their hierarchies and provisional
roles. The 138 paired macOS fields have matching exact source-text hashes; the
remaining 24 Windows pause fields have no mapped macOS counterparts. The reading
used `ui-windows-all.json` SHA-256
`598c2adb429385d9abc07c68a2ed7465bf2ae510ae70d5f5e5850c3b2c33efca` and
the previously pinned role report SHA-256
`6219fb3d833a85a61e92392fe7c002738d8b105db61f3f39d82f27153ecfefdc`.
The 19 macOS and 17 Windows known settings objects and their source fields were
also read from the previously pinned paired export SHA-256
`eda16ce679eedf3e5b76beb76c8e9bc49a62c974639ab6327ea6063c6ad5cf25`.
The 32 distinct legacy debug-template text values were read, but not every
one of their 149 individual hierarchies in this reading. These are bounded
source observations, not independent editorial acceptance or proof of
visibility, exhaustive text discovery or a translation denominator.

Potentially significant distinctions include: credits contributor names and
the `GDC Bundle Part 4` attribution title need careful preservation/translation
decisions; `Xbox` and `DualShock` are controller identifiers in indexed
settings options; resolution values and numeric slot counters carry structured
values; `LABEL`, `Option A`, dialogue presenter examples and `Version\n` are
serialized templates whose runtime visibility needs separate review. The two
settings `LookInvertY` and `SprayerReduceMotionSick` exist only on macOS within
the inspected source objects. These observations do not authorize omitting
any entry from the common inventory or changing existing protected identities.

`inventory_version_displays.py` adds a source-pinned component relationship:
each build has seven `VersionNumber` components in `level0`–`level6`, each on
the same serialized GameObject as exactly one `TextMeshProUGUI` text field.
All 14 fields match the seven corresponding paths and source-text hashes in
the paired UI-role report, and both component types pass byte-exact no-op
serialization. Source reports are `version-displays-macos-20261107.json`
SHA-256 `ee3cc9a1fa8d52872cab512e759f6800c0a60bd01a84152a37f08b424a09b60b`
and `version-displays-windows-20261107.json` SHA-256
`9cc843b00e6322bdcd2f012770539db6b0bf12b8fe601231aa821b231d429957`.

In each pinned game assembly, `VersionNumber.Start` has a direct instruction
sequence obtaining `GetComponent<TMP_Text>()`, reading `Application.version`,
and assigning that value through `TMP_Text.set_text`. The focused tests match
the exact source-to-component identities and this IL sequence on both builds.
That is strong static evidence that the seven placeholders are intended to be
replaced at startup. It does not prove `Start` actually runs in every scene,
which component Unity resolves at runtime, or whether the placeholder is
briefly visible. The initial source pass therefore retained these entries
as needs-review. The runtime follow-ups below resolve the shared
placeholder role. Other runtime mutations and component/text APIs remain
unclassified.

Run `inventory_version_displays.py macos|windows ORIGINAL_DATA` and
`python -m unittest discover -s localization -p 'test_version_displays.py'`
with pinned dependencies. The direct-code test also requires a built
`tools/text-setter-consumers` executable. These checks never modify the game.

## macOS scene activation probe, 2026-11-09

The two original `BuildSettings` scene lists match. Indices 0–6 load
`StartScene`, `PlayGame`, `EndScene`, `SexScene3`,
`SexSceneRyanConrad`, `SexScene2` and `SexScene1`, respectively.

An isolated macOS `V3A1` copy loaded the original start scene and
then each of the six other scenes by build index with Unity's scene
API. The probe read the sole scene-local `VersionNumber` and its
colocated TMP component on scene load and after input updates. It
did not modify text or activate any object. The start scene's
enabled, active field held the serialized `Version\n` at the
scene-loaded callback and the real `Application.version` value at
the later update. The other six components were enabled but their
GameObjects were inactive in hierarchy at both sample points. Those
fields retained the serialized template while inactive.

The copy used an English table and ran with Null graphics. The direct
scene loads do not demonstrate ordinary gameplay entry or menu activation.
All 22 samples showed no visible window or foreground ownership.
The process exited, the original profile snapshot matched and the
wrapper verified the signature and removed its Steam file.

Local evidence is under `localization/work/version-ui-runtime-20261109.vpXR5H/`.

| Artifact | SHA-256 |
| --- | --- |
| Player log | `8161c19f7c031175a854f6dcf32b0fd0021aa6caed633d961ed14854b0576eff` |
| Observer receipt | `cb659f979406091fada3589de4d9503dd13c4b9d26dd2f7f70bbe719ad6bba07` |
| Companion source | `9aff04d9da543117a9308552537bd58368ec4a9f34996d4e502a180c4bac7c2c` |
| Companion DLL | `46be5b64e719e99ef77e07ba6d8b5b9979aa6e89a894a8d24b531e58f7534f88` |

The `V3A2` follow-up ran with Metal. It kept natural activation in
`StartScene` and activated the hidden label branch explicitly in the
other six scenes after each direct scene load. As a control, the
inactive labels still contained `Version\n` at scene load and
immediately after activation. In all seven scenes the first sampled
`Canvas.willRenderCanvases` callback after scene load found the active,
enabled label already set to `9/12/2026_a93aa21a`. The later input
sample confirmed the same value. The observer checked the original
`VersionNumber` and TMP value without writing either.

All 22 desktop samples again showed no window or foreground ownership.
The copy exited cleanly, the original profiles matched the snapshot
and the wrapper removed its Steam file and verified the signature.
This verifies the string delivered to the macOS Canvas in the isolated
test. The six controlled activations do not exercise the ordinary
menu navigation path. The probe does not capture pixels.

Local evidence is under `localization/work/version-ui-activate-20261109.G47qP7/`.

| Artifact | SHA-256 |
| --- | --- |
| Player log | `87f29d07c3edb5b0bfbfdf10a68820dbb3500c62896032d3c21ff4b3311c4d65` |
| Observer receipt | `d4c8bbe419da4946e73e91b8a696764bf232a0f4de78a25bac47deba136718fd` |
| Companion source | `e0917dd0cd265e0d8463283bd3783260a94ab90d1acfb09e5f780910d71484c1` |
| Companion DLL | `0f1c9a488c0b118ac3637328ca750741166f68f139303da62969cd10e6c5a12f` |

## Windows CrossOver follow-up and v33

The Windows observer used the same scene sequence and sampling points
under Direct3D 11, with a test copy and the private CrossOver bottle.
An initial obsolete patcher rejected the Windows flag before launch.
The tracked Windows-capable patcher verified 2,328 method bodies,
with the two expected menu hooks and no change to `VersionNumber`.

The start scene activated the label normally. For each of the six
other scenes, the same controlled activation exposed the original
template immediately after activation. At the first sampled Canvas
callback and the subsequent input update, all seven enabled labels
contained `9/9/2026_ee944596`. All 43 window and focus samples were
`0 0`, the verified process exited and the original files and saves
matched the snapshots. This is CrossOver runtime timing evidence.
Native Windows, actual pixel visibility and ordinary menu navigation
in the six directly loaded scenes remain outside these checks.

The v33 shared recipe preserves the seven paired serialized
`Version\n` fields as placeholders. The two v33 outputs matched
byte-for-byte. Comparison with v32 changed only those seven roles.

Local evidence is under `localization/work/windows-version-ui-20261109.AaCv9x/`.

| Artifact | SHA-256 |
| --- | --- |
| Player log | `33a9193877f33106e5c895fc389ca4dcdfab59f1a475340593f3b2c12843e130` |
| Observer receipt | `4341bbf40c0f2b658426cf0dae2e6b8932453907fa3fabaadf8add98adbd9269` |
| Companion source | `8b4e036aeb16846962ff84c36f850c7455da68e16098fb88fe7957e20c58ab52` |
| Companion DLL | `1611136a2da26af74a676ef566ffa88d5d90c42750541e7734816861573b3df5` |
