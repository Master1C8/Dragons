# Ukrainian, Polish and Vietnamese text paths

The macOS `9/12/2026_a93aa21a` and Windows `9/9/2026_ee944596` builders
accepted five Yarn replacements and three settings labels per platform.
These inputs are script samples and use `uk` as the package locale.
They do not represent three complete translations.

The gameplay control loaded the isolated Conrad visit fixture through
the stock menu. Virtual input reached the dragon window and started
`Conrad_Intro_3`. The observer read the actual option text before each
click and required both the Yarn node-complete and dialogue-complete
events after the third click. The settings control opened Options
through the stock button and read the text components instantiated by
the settings spawner.

| Surface | Source binding | Paired runtime observation |
| --- | --- | --- |
| Choice | `line:83ac5b68`, `line:0b7589ff`, `line:4d692a01` | Ukrainian, Polish and Vietnamese samples each produced one line at 36 units. All three choices remained interactive and led to the expected Yarn completion. |
| Dialogue body | `line:9d458e88`, `line:78cc49e8` | Ukrainian and Vietnamese samples resolved on the active body component at 64 and 40 units, preserving the original 160% and 100% sizing. |
| Options | Ambience Volume, Anti-aliasing and Music Volume labels | All three samples resolved on active controls at 19.7 units on one line. The Vietnamese label retained U+01A1 followed by U+0301. |

Both Yarn paths emitted precomposed U+1EDB where the locale file
contained U+01A1 plus U+0301. The first dialogue observers treated
this as a mismatch. The second Windows attempt and the first macOS
attempt with the fixture demonstrated the same choice normalization.
The final observers required the exact NFC value in Yarn while the
settings observers still required the original decomposed sequence.
Game assets and input text were unchanged between those attempts.
The first Windows attempt had stopped before dialogue because the
test copy lacked the fixture JSON. The repeat used the established
fixture with its original checksum.

The eight glyph records match across macOS Metal and Windows
Direct3D 11 through CrossOver. Dialogue runs had 168 macOS and 286
Windows window and focus samples. Settings runs had 13 and 30.
Every sample was `0 0`. The original profiles and the checked
test fixtures matched their initial hashes. The owner game process
was outside the test copies.

This establishes observable glyph substitution behavior, point sizes
and one complete Yarn route for these samples. It leaves native
Windows, pixel-level mark placement, clipping, settings interaction,
the next gameplay state, and other scenes and locales unverified.

SiteForMods `29b0bb56` exposes 28 English glossary entries and 28
Ukrainian entries. The 29 non-Russian locale maps retain their 27
previously reviewed values by stable ID. Their new anonymous dragon
entry has the [separate affected editorial checks](generic-dragon-entries-20261110.md#canonical-integration-and-russian-scene-wording).

Local inputs, receipts, assets and logs are under
`localization/work/european-text-paths-20261110.QddlnY/`.

| Unity log | SHA-256 |
| --- | --- |
| macOS dialogue | `b59dcdc980c4a5ce3005e2e543b5eb5e4cb419eeac2ea4c1f978d64ede2ed4bc` |
| Windows dialogue | `563569b753ced8ae7cebd12d0005e61e4de6d9a50ac1289379f03082c667d05f` |
| macOS settings | `c777b043a36b4bbeed01e5f2b80cd63e9b76af7ad5174ada60b653adc9aaa538` |
| Windows settings | `dc9f8c1a31d57de96cd4800cdf3ae7604b9633b5507f33085e495fa3e8ca1811` |
