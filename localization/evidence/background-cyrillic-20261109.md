# Russian glyphs in the original dialogue presenter

The macOS builder made isolated profile `R6M1` using the original
game and a one-line Russian test table. The sample for
`line:39fd52f1` was `Жёлтый ёж. Ъъ Ьь Щщ Йй.` The original Yarn
runner started `Conrad_Intro_3` after stock menu, movement and
interaction input loaded the synthetic `Conrad_3_8` fixture and
prepared the mount. The companion read the active dialogue text
and its TextMeshPro character info without writing either.

All 16 Cyrillic occurrences resolved to the matching character
in `LiberationSans SDF - Fallback` and had visible character
geometry on line zero. The Metal player reported a 640 × 480
viewport and one line of 23 visible characters. Unity's screen
capture failed in this batch-mode run and produced no image.
Pixel-level legibility and clipping in this viewport remain
unverified. The sample is diagnostic and supplies no accepted
translation.

All 174 desktop samples showed zero foreground ownership and
zero on-screen windows. The wrapper verified the signed copy
after exit and removed its generated Steam file. The four
checked original profile roots matched their snapshots.

Local source and receipts are under
`localization/work/background-cyrillic-20261109.hWyvEA/`.

| Artifact | SHA-256 |
| --- | --- |
| One-line test table | `57d5c409d1b558c4b8d49f94aef65ae9e9ddf2a66dec781d52274faf1ffb6635` |
| Builder asset | `820371cb7cf412747fed239fa8852224578dd2e1bb32dea253331489085d82b0` |
| Instrumented game DLL | `7d97754b9cff4f74090db3acce1c918a254472115786c181892f90ea0201a098` |
| Runtime companion | `35e1138d72f7e2e82d6e45fea361c14c3e18b9e14fe0ff1c85caf85b8bc4f3b7` |
| Unity log | `53568da020bd23ed8321154b08955ddd9b0cc4e1632d5dd4f393adb53c85c8f2` |
| Observer receipt | `04ccba35a5df8bc2506ce3361b5d2eff501e252c826432b60f0183076f808cd8` |

## Windows frame follow-up

The saved original `windows-dialogue-synthetic.png` from the
[CrossOver dialogue review](windows-dialogue-review-20261106.md)
matched its recorded SHA-256
`56cfe7d100f6cc33289414a2719e14886348bf8301ad7f38c0c4d9d5c90c4b80`.
The prepared 1280 × 995 WebP80 preview confirms the visible
paired-case Cyrillic characters and one line contained within
the speech bubble. The source-pixel crop at `(1410, 1415, 300, 82)`
shows a closing apostrophe after `223`, followed by three dots
and `123`, resolving the earlier punctuation uncertainty for
this frame. The original bytes were preserved.

The prepared preview SHA-256 is
`1a3297b79d3282af87e747183566a524990d9fe0b7491b853a4c2a3c1c7d21c5`
and the no-upscale crop SHA-256 is
`03f1cbe2645d2f7e895735fd1c2701179a9f229ceb257718603e7f545d4ef55f`.
This is a visual read of a prior synthetic dialogue frame from
the original presenter after test-bridge entry. Native Windows,
other text roles and smaller-viewport behavior remain open.

## Offscreen capture follow-up

Profile `R6M2` uses the same source-bound table and a byte-identical
dialogue asset. Its isolated companion requests an offscreen render
from the original gameplay camera after the same dialogue is
visible. The probe temporarily routes the existing presenter
canvas through that camera and restores its prior configuration
after readback. The follow-up source and receipts are under
`localization/work/background-cyrillic-offscreen-20261109.w6zvmR/`.

The original presenter again resolved all 16 Cyrillic
occurrences. The render request used the `PlayerFace` camera and
produced a 640 × 480 PNG. The observer verified that the isolated
process exited, all 163 desktop samples stayed hidden, the
checked original profile roots matched, and the wrapper removed
its Steam file. The temporary camera routing limits the visual
finding to this offscreen presentation path.

Local OCR recognized `Жёлтый ёж. Ъъ Бь Щщ Йй.` with confidence
0.5. It returned `Б` at the position where TextMeshPro reports
`U+042C`. The OCR result is a reason to inspect the prepared
source-pixel crop and does not establish the glyph's appearance.
Crop bounds are `(208, 413, 227, 49)` on the same PNG.

The prepared full frame and source-pixel crop were visually
reviewed. The line reads `Жёлтый ёж. Ъъ Ьь Щщ Йй.`, including
the distinct paired-case signs. The capital soft sign has a
vertical stem and lower bowl without the upper arm of `Б`.
The single line fits within the speech bubble, with clear
separation from the border and no visible clipping.

| Follow-up artifact | SHA-256 |
| --- | --- |
| Unity log | `4a88d3353580eaa2400bd2850bb76f9a760807287991db7a97f882beeb608d84` |
| Observer receipt | `c6a793591c68b354d7f4b6b9f3f4eeffaf6d46fff7be5f08b68bf513eaa2f652` |
| Runtime companion | `0795a63ac99ec70e4679fb37f7fc0cd7a33b0f539f83c372d56b14625ae02c8b` |
| Original offscreen PNG | `d31abeab57803f96480f77de7e6d150dcede7050a465e3e211bbb71c02d5d1cb` |
| Prepared 640 × 480 WebP80 | `0a91ee0434a3a6b0e3684e8449286972f9e1d043347c39a52136d8be7ebbd679` |
| Prepared 227 × 49 dialogue crop | `109ac90ea55e0874b342d07b21c4ee23c7b36411c6d702180bac5c522f361976` |
| OCR receipt | `2a17c90afd3a12a17c0ef9c59787d32a5880a3b0927caf1a0163279b93b6aa50` |

## Matching Windows stock dialogue probe

The source-bound Windows builder produced a one-line table with
the same ID and sample and the current Yarn repair enabled. In
the isolated CrossOver copy, stock menu, movement and interaction
input reached `Conrad_Intro_3`. The original presenter resolved
the same 16 Cyrillic occurrences to matching characters in
`LiberationSans SDF - Fallback`. The Direct3D 11 player produced
a 1074 × 544 PNG using the same offscreen `PlayerFace` camera
request. The Windows viewport differs from the macOS viewport.

The observer sampled 274 times with zero foreground ownership
and zero on-screen windows. The test process exited, and the
checked original files and saves matched their snapshots.
Local OCR read `Жёлтый ёж. Ъъ bь Щщ Йй.` at 0.5 confidence.
The prepared full frame and source-pixel crop show the expected
`Жёлтый ёж. Ъъ Ьь Щщ Йй.`, including the case pairs and the
upright stem with a lower bowl of the capital soft sign.
The line stays within the speech bubble with clear padding.
Crop bounds are `(350, 443, 390, 55)` on the original PNG.
This verifies the representative one-line sample on the Windows
build under CrossOver and the comparable macOS Metal sample.
Both use the original presenter with temporary offscreen camera
routing. Other UI roles, long Russian lines and native Windows
remain separate checks.

Local source and receipts are under
`localization/work/windows-cyrillic-offscreen-20261109.eRMrOI/`.

| Artifact | SHA-256 |
| --- | --- |
| One-line test table | `db7214cd1ee224111da920f95ce58375c48ad15cdb62c184971f7ae9ce2fa116` |
| Builder asset | `946119a439fa0fe61423bb86aa7416fb1cc9a4502e554be3255ce2525ce2d9a1` |
| Runtime companion | `bc34fdb3ec1f62256e75063d55dd62b8163976e8af123f2e0f1d6465297f218f` |
| Unity log | `e0d3062bbf1f78ed1feb3ebb46c8623c42495ea3c6f657e98f356c55b1d94ce0` |
| Observer receipt | `28a138b9607c78038b1ba1a86c31145a4de3b67c94891e780d8dc8d1e35158f5` |
| Original offscreen PNG | `1e890958f2bbcd0f4b0af841404fedcd6fb8188ecdcc6b9c76b973d2f5039111` |
| Prepared 1074 × 544 WebP80 | `62eece0597d0ba628fd21665d788a24f0c40b313cca7db6ad945aca1b31a69d3` |
| Prepared 390 × 55 dialogue crop | `28694f32ae0a0a36cd984911bf36c578e6cbccad49ee6aa3edb9f2cb618db5fb` |
| OCR receipt | `52acaf2756baceeef505acfc55d05f4e6bbe7a761e403e7bb9cc61aae77479e9` |
