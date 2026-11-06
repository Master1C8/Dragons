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
briefly visible. Retain these entries as needs-review rather than excluding
them or changing the shared classification automatically. Other runtime
mutations and component/text APIs remain unclassified.

Run `inventory_version_displays.py macos|windows ORIGINAL_DATA` and
`python -m unittest discover -s localization -p 'test_version_displays.py'`
with pinned dependencies. The direct-code test also requires a built
`tools/text-setter-consumers` executable. These checks never modify the game.
