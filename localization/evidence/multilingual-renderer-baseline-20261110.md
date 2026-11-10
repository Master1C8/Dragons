# Multilingual renderer baseline

The local game manifest lists English as the sole official locale.
The SiteForMods glossary catalog and the 30 non-English site codes
matched the script sample set. The samples contain independent script
strings and are separate from the game translation corpus.

The read-only audit used stock `sharedassets0.assets` on macOS
`9/12/2026_a93aa21a` and Windows `9/9/2026_ee944596`, Unity
`6000.3.14f1`. It verified byte-identical serialization of the three
font objects per build, the static primary and dynamic fallback links,
and the identical embedded Liberation Sans font bytes. The prior
[font-role inventory](font-role-coverage-20261110.md) binds this chain
to 98 macOS and 122 Windows TMP components.

Both Unity runs reached New Game through a virtual mouse in an
isolated profile. A probe wrote each sample to the active slot-progress
component and asked TMP to regenerate its mesh, then read the resolved
glyphs and positions. The component was restored after sampling. The
macOS control used the delivered Russian app as its base. The Windows
control used a stock game clone through CrossOver. Both retained the
same stock TMP engine and font chain. Original profile hashes matched.
All 13 macOS and 25 CrossOver window checks reported no window or
focus. The observer changed two menu methods in each test copy and
verified the remaining instruction sequences.

| Locales | Stock font and observed runtime result on both builds | Next check |
| --- | --- | --- |
| `zh`, `zh-TW`, `ja`, `ko` | TMP substituted U+25A1 for 13, 13, 15 and 10 unique sample code points respectively. | Test script-specific fallback coverage and dense glyph atlas capacity, then inspect narrow UI and dialogue. |
| `th`, `hi` | TMP substituted U+25A1 for 13 and 17 sample code points respectively. | Test fallback glyphs and complex shaping separately, including Thai marks and Devanagari clusters. |
| `ar`, `fa` | TMP substituted U+25A1 for 15 and 13 sample code points respectively. | Test fallback glyphs, Arabic-script joining, and mixed-direction layout independently. |
| `he` | All sampled code points resolved. The field had RTL mode disabled. The first three base letters appeared at increasing horizontal positions on one line, from −36.1 to −7.0. | Verify bidi ordering, mark positioning, and punctuation and numeric runs on all affected surfaces. |
| `ru`, `uk`, `bg`, `sr`, `el` | Sample glyphs resolved without substitution. | Check representative dialogue, choices and settings, then verify the corpus and visual fit. |
| `es`, `es-419`, `pt-BR`, `de`, `fr`, `tr`, `pl`, `it`, `vi`, `id`, `cs`, `hu`, `nl`, `ro`, `fil`, `sw` | Sample glyphs resolved without substitution, including the Vietnamese decomposed acute sample. | Check placement of combining marks, representative dialogue and choice progression, and visual fit. |

On both platforms, every substitution matched the corresponding
static font gap. Mesh glyph identity and positions are not pixel
review. This control covers one active stock text component and leaves
dialogue animation, choice and settings behavior, full alphabets and
final corpus coverage, typography, line wrapping and clipping open.
It establishes a concrete stock-renderer blocker for nine locales.

Artifacts are under `localization/work/multilingual-feasibility-20261110.L1v5Yf/`.

| Evidence | SHA-256 |
| --- | --- |
| Embedded stock font | `e5b0af421ea2bfbc1ac8d251d647268087ae82786234c57f757d1f0b90fa8b49` |
| `samples.json` | `7d7592270011b1560785e6d5b98a3a7c08bde3499e80b91f39a0f4e558e75391` |
| `coverage.json` | `729b17a0743be3a62792e7728b49d3b45fde5819ca7baec44b5fb09d26457c30` |
| `runtime-glyph-check.json` | `00fa6389dedc6236117640461b8b0700777db09b2379cea9998c92d41cb1a614` |
| macOS Unity log | `badd146b3a98a76f05d579944da1ed6be460c91048fd581f0dffe5ed050df389` |
| Windows Unity log | `8ef46bc2c443bb3e27a3a655cee240fd93ba047df34d827906661cfbe0476f97` |
