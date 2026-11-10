# Mixed direction and candidate fonts

These controls follow the [multilingual baseline](multilingual-renderer-baseline-20261110.md)
on macOS `9/12/2026_a93aa21a` and Windows `9/9/2026_ee944596`
through CrossOver. Each entered the stock New Game slots in a separate
profile using Unity's virtual mouse. All window and focus samples were
`0 0`, and the original profiles matched their pre-run hashes.

## Hebrew direction

The active slot-progress component was tested three ways. Stock TMP
received the logical text with RTL disabled, the toggle condition fed
it the same text with RTL enabled, and the prepared condition fed it
the ICU 78.1 visual order with RTL disabled. The reference used the first
strong direction, mirrored RTL punctuation and kept marks with their
base in the reference string. The probe disabled wrapping, used one
line and sorted visible glyphs by horizontal origin. [ICU bidi API](https://unicode-org.github.io/icu-docs/apidoc/released/icu4c/ubidi_8h.html)

Both players returned identical glyph sequences and positions.
With the toggle alone, the number run `12` appeared as `21`, the
Latin identifier `TMP-42` appeared as `24-PMT` and the bracketed run
appeared as `)21(`. The prepared condition matched the reference
for all four unmarked samples, including the pure LTR control.
The marked Hebrew sample still disagreed when ordered by origin.
TMP advanced the pen after each of the three observed marks, and
the holam origin fell beyond the next base letter's origin. This
separates bidirectional ordering from glyph positioning. The result
covers one active control and one line at a time. Mark placement,
wrapping, rich text, dynamic substitutions and Yarn advancement
remain open.

## Missing glyphs and Thai shaping

Seven regular Noto font files covered every code point missing in the
eight baseline samples. Every such point mapped to a glyph with a
nonempty outline. The audit checked font table checksums, recorded
face names, font hashes, license hashes, line metrics and space advance.
Four region-specific Noto Sans CJK 2.004 faces cover `zh`, `zh-TW`,
`ja` and `ko`. The other candidates are Noto Sans Arabic 2.013 for
`ar` and `fa`, Noto Sans Thai 2.002 for `th`, and Noto Sans
Devanagari 2.007 for `hi`. The preserved upstream licenses are SIL OFL
1.1. [CJK release](https://github.com/notofonts/noto-cjk/releases/tag/Sans2.004), [Arabic release](https://github.com/notofonts/arabic/releases/tag/NotoSansArabic-v2.013), [Thai release](https://github.com/notofonts/thai/releases/tag/NotoSansThai-v2.002), [Devanagari release](https://github.com/notofonts/devanagari/releases/tag/NotoSansDevanagari-v2.007)

The Thai runtime test temporarily substituted the hinted Regular
source font inside the existing dynamic fallback on private copies.
Exact Unity object comparison found a change in only the embedded
`Font` object per asset. TMP resolved all code points in `น้ำ` and
`กำลัง` through the candidate, and the `ABC` control continued to use
the original static primary font. For `น้ำ`, both players emitted
glyph IDs `71, 47, 90`. HarfBuzz 14.5.1 with the same font and Thai
script returned `71, 59, 49, 86`, including zero-advance marks. The
fallback can fill the glyph gap and still leaves the shaping gap.
The other six faces passed static sample coverage only. Full-corpus
coverage, an append-only fallback chain, atlas capacity, shaping,
pixel review and progression remain open.

Reproduction inputs, exact asset digests, font receipts, observers and
logs are under `localization/work/rtl-order-20261110.RoB8ak/`.

| Evidence | SHA-256 |
| --- | --- |
| ICU reference cases | `2eaa6c96380dd9d7246c53aa18980c14ac6d454ecdd93e2f11f3ab012ead50a5` |
| RTL macOS Unity log | `236f1f454f94418a66c89d797ebcf30377640d4baae14ca69e7a84a5bbd98b68` |
| RTL Windows Unity log | `e432aa383f9742160d694f9e339d6f4190d3072387f48293d6e05d2ed7aa7e9b` |
| Font audit | `9cf106d79332aa313e30ee6e06c821e618bbe917c0ed9531bb2469d33ece2b7` |
| Thai macOS Unity log | `320638109675d2ecb65aeba81ca7ea9160a74d3b2412fa550da54314a873b0a6` |
| Thai Windows Unity log | `e384d382693c37f9387ba222c758a9f370ab40986f09b42398daca45f69d5b41` |
