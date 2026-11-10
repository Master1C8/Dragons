# CJK fallback runtime and atlas pressure

The four region-specific Noto Sans CJK 2.004 faces from the
[font audit](rtl-and-font-candidates-20261110.md#missing-glyphs-and-thai-shaping)
were tested on Unity `6000.3.14f1` in macOS `9/12/2026_a93aa21a`
and Windows `9/9/2026_ee944596` through CrossOver.

The macOS test copies used the delivered Russian app as their base and
the Windows copies used the stock game. The setup replaced the embedded
source font inside the existing TMP fallback on each isolated copy.
Unity object read-back confirmed that only the embedded `Font`
object changed within each asset. The background probe opened New
Game through the stock button, inserted one CJK sample into the live
slot-progress component, and read the visible glyph records. Every
previously missing code point resolved to its expected glyph ID in
the regional face. The `ABC` control still used the stock primary.

The stress test then called the real TMP atlas insertion method with
1,536 distinct characters absent from the visible control. It sampled
evenly across each face's mapped Han or Hangul block. The serialized
fallback has multi-atlas enabled, padding 9, sampling point size 86,
and a 512 × 512 page size on both builds.

| Locale | Previously missing sample code points resolved | macOS pages | CrossOver pages |
| --- | --- | --- | --- |
| `zh` | 13 | 63 | 63 |
| `zh-TW` | 13 | 63 | 63 |
| `ja` | 15 | 63 | 63 |
| `ko` | 10 | 64 | 63 |

All 1,536 characters per run were admitted. The recorded page totals
include the first page, which already contained the visible control.
The test exercises atlas growth and glyph identity. It does not
measure rendering time, memory use, or the full game corpus.

The paired Japanese follow-up changed only the serialized atlas width,
height, and empty free rectangle in the TMP fallback object. The
same font, control glyphs and byte-identical 1,536-character input
admitted all characters again. The 1024 × 1024 case used 17 pages on
macOS and 16 through CrossOver. Fewer pages do not imply lower memory
use. The total nominal page area was slightly larger on both builds.
Both paths still require a corpus-bound layout and performance check.

All ten runtime receipts showed zero on-screen windows and zero
foreground ownership. Test players exited and original profiles
matched their initial hashes. Stock texture objects were unchanged.
The temporary substitution does not test appending a fallback
alongside the existing dynamic face, nor does it certify punctuation,
CJK line breaks, glyph appearance, or dialogue and choice progression.

Local recipes, assets and receipts are under
`localization/work/cjk-fallback-20261110.BAc1J4/`.

| Artifact | SHA-256 |
| --- | --- |
| Font and stress inputs | `f89864466dd8889231099c34f9b5d8a66bb575a075c460cb5aded8643997da9f` |
| Eight stock-atlas runtime checks | `6abb0706511f0f55ec58ab84a962ab62b0ffc228888b65929bd9cb029fcbf336` |
| Japanese 1024 macOS Unity log | `7e726171737a4e1b8ef5158bc672cc45c9ab87596a10145a89b9428a981b9589` |
| Japanese 1024 Windows Unity log | `221c6b42a30d839260fb3101e7bb39f7ff962cd3c976ed822df643c037223921` |
