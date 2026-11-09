# Cyrillic staged typography in the game renderer

The stock menu loaded the isolated `Conrad_3_8` fixture. Virtual
input used the game's ordinary movement, equipment, window and
choice handlers to reach `Conrad_Intro_3`. The two tested line
IDs, `line:9d458e88` and `line:78cc49e8`, each use the same
synthetic Cyrillic sample, `ЖжЪъ`. The ordinary builder preserved
their respective source `<size=160%>` and `<size=100%>` tags.

In the original active presenter the four glyphs resolved to
matching characters in the stock Liberation Sans fallback, with
visible character geometry and sizes 64 and 40 respectively.
The tags did not appear in the character stream. The companion
read that component without replacing its text.

The companion then temporarily cloned the same TMP text
component. This second check bypasses Yarn and measures TMP's
local interpretation of the [two serialized gradient presets](staged-typography-20261110.md).
The plain control used size 40 and black vertex colors. A
mixed-size sample produced the following glyph data:

| Region | Point size | Vertex colors |
| --- | ---: | --- |
| Yellow-orange first pair | 56 | `FF2C00FF` to `FFBE00FF` |
| Following ordinary pair | 40 | Black |
| 80% pair | 32 | Black |
| 70% pair | 28 | Black |
| Gold first pair | 40 | `E9A317FF` to `E5CC57FF` |
| Caption after the gold pair | 28 | Black |

The companion destroyed the clone after sampling. This measures
glyph and mesh data in the real renderer. It does not inspect
pixels, certify readability or fit, or test those gradients on the
original special-scene choice prefab or the final Russian wording.
The body component's source style is bold, so the gold test does
not distinguish explicit bold markup from inherited bold styling.

The macOS player used Metal. All 172 desktop samples showed zero
foreground ownership and zero on-screen windows. The signed
wrapper cleaned the generated Steam file after exit. The four
checked original profile roots and the test slot fixture were
unchanged. The stopped synthetic app was removed after strict
signature verification and recording all 284 file hashes.

The first Windows CrossOver run stopped before the dialogue. The
test route reached 0.276 world units from its window waypoint and
overshot the 0.25-unit tolerance. The follow-up raised only that
test waypoint tolerance to 0.36 and used the same built dialogue
asset. The stock interaction selector and ordinary choices then
reached both sample lines. The player used Direct3D 11. All 285
desktop samples stayed hidden, the verified player exited, and
the checked installed files, original profile and test fixture
matched their prelaunch bytes. All 28 glyph records, including the
per-character sizes and four vertex colors, matched macOS exactly.
Native Windows and pixel inspection remain outside this check.

Local input, companions and logs are under
`localization/work/styled-cyrillic-runtime-20261110.yAjNaW/`.

| macOS artifact | SHA-256 |
| --- | --- |
| Locale control | `e375835727b77da6435732582bc44c2245782e153329461bcb6f9fe6ac0dd2c7` |
| Built Yarn asset | `b36f5efdd22cb253dcbbbaf48d564e4b972ffa56668fd2ba5edf43e2a3c1cf8d` |
| Companion DLL | `2f292ad1675fd29469466c09d8adfe303f022332b853ad21dc47f4dad26f681d` |
| Unity log | `e69d46447bb87d29678e14587aa4074d8acf0bcad8219f759f629d589688477a` |
| Observer receipt | `fae4e2d2e963346d538abf3156905f01dbdcab9bac471238dac5d2ac84ba719a` |
| Signed app file hashes | `2c4901eb1b440e3ed5f067a1d35dec94575ca3daf484266d72b4bc5ce25df46f` |

| Windows artifact | SHA-256 |
| --- | --- |
| Locale control | `8aa77e8f0689897886d2d85aa401aa1e4b6796b48092425e960724024841f5c5` |
| Built Yarn asset, both attempts | `573a61319c12b2528a547e4ac1be303ef9d43fe908b5baac24c1ed95ab656b83` |
| First observer receipt, waypoint timeout | `92b4a7080d092a3ae166193e5612d3dc55ff768869357617199ea1442563aeb8` |
| Follow-up companion DLL | `a99898ed63ffa43cf0c1b30f2f5ca9b24ba488e7924a3446f1c0b7bcb7189fc8` |
| Follow-up Unity log | `7f0f64f6de8740540e7f3478cfc941bf99d6f8d14bb5991daefe8d5094768b13` |
| Follow-up observer receipt | `2f3b52af1ebca02aba7d81df1bc4edaee0f738f533a195b2b3e8acb497d8d258` |
