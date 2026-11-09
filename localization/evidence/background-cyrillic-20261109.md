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
after readback. The result remains pending. The follow-up source
and receipts are under
`localization/work/background-cyrillic-offscreen-20261109.w6zvmR/`.
