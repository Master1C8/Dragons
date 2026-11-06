# Synthetic speaker-color comparison

The pinned macOS `level1` dialogue body `TextMeshProUGUI#3899` has black
`m_fontColor`, while the speaker-name `TextMeshProUGUI#3900` has white
`m_fontColor`; both have alpha 1 in the serialized source. This is static
component data, not a measurement of the runtime material or background.

`experimental_speaker_color.py` builds a test-only hypothesis in a separate
copy of `level1`, changing only the name component's `m_fontColor` and
`m_fontColor32` to the original dialogue body's black values. It validates the
original asset, schema, target object inventory and old colors; checks a
byte-identical schema round trip; and compares every saved object and the full
updated tree before replacement. It is not connected to the player builder.
Two focused tests passed: the positive checks only the two intended fields
changed and the negative controls reject an unsupported locale, original target,
and repeated application. This is a test candidate, not a production style change.

Two separate signed test apps used fresh profiles `Q9R7` and `Q9R8` and the
same synthetic source, bridge, ID-bound helper and forced line described in
`alexander-colon-runtime-20261107.md`. The white control retained original
`level1` SHA-256 `6af2815f16cba00e935fe110023ec91421c7d4107c5d8d31f55b70039b17d618`;
the black candidate used SHA-256
`91ca8ca2efbe236ccd7b0e2db65c243f9a0e3aa36cae991c3f1a8b8ebb8febd6`.
Each entered the forced test node, logged the same helper marker and was
captured at a 1024 × 768 game viewport at least two seconds after the marker.
The window captures were 1024 × 824, including native window chrome.

| Candidate | Original PNG SHA-256 | Prepared WebP80 SHA-256 |
| --- | --- | --- |
| White control | `a8bed0f0c374bfebc259cdc4fe561d504b12bdf14a7cbf4892ae6462bca3511f` | `cc4a8acc6a8a84bcfe42fdfa197c956aed2e69b32118364f49683e08d9447cfe` |
| Black candidate | `494b9c5fa663b57cb77a4c5723d9a029d864f92f2d915a0007b3f000840000af` | `a63df73278341a9142842e24abdfaa5d255a3c352e1aa05ada0ab6b76b86962f` |

The originals are `work/alexander-white-stable-20261107.png` and
`work/alexander-black-stable-20261107.png`; prepared, not-upscaled review
copies are in `work/alexander-color-review-20261107/`. An authorized
independent reviewer `alexander_color_review` (`gpt-6.1-terra`, high) observed
much stronger contrast in black; the white label was too faint to verify its
individual glyphs. The black label's small italic middle glyphs and their case
also remained uncertain on the full frame. Neither had obvious clipping,
overlap or contamination, though the white label's faintness limited inspection.
Both are **needs-review**; this synthetic comparison is not final font or
Russian-language acceptance.

Both verified test processes were terminated by PID, their launchers removed
generated Steam files and verified app signatures, and the four checked original
profile roots matched the earlier baseline. Runtime logs: white SHA-256
`e1c1fbd6ec10a1480a7f01752f863a0cd3db350f0a6331e5b3c91ab330b89e30`, black
`c7626e185f67125e1523c9675e627627bf8d587a26ad4c0ff8eb2a213ae6ae14`.
This does not prove natural entry, normal exit, all save locations, Windows
behavior or a finished translation. Source script SHA-256
`39f202d280f2633d886cf0e21df55c1727002dcddf464d55f4eae62dae327afc`;
tests SHA-256 `fb49444e6ba2302229f3c993431b124b23110bd890f98382d06f2f8f7acbb599`.

```sh
python -m unittest discover -s localization -p test_experimental_speaker_color.py -v
```
