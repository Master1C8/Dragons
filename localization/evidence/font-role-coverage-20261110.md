# Paired source font-role coverage

The read-only probe binds v42 UI entries to the original serialized
objects, checks the source string, and decodes each TMP component
using the pinned managed schemas. It also verifies the stored object
hashes of all five body and speaker-name targets and all five
last-line targets per build from the existing presenter inventory.
The inspected components and font objects all serialize back to
their exact original bytes.

| TMP component scope | macOS | Windows |
| --- | ---: | ---: |
| Translatable UI fields | 58 | 82 |
| Settings prefab text components | 11 | 11 |
| Slot progress and version templates | 13 | 13 |
| Yarn body, speaker name, last-line and option targets | 16 | 16 |
| Total | 98 | 122 |

All 220 targets hold explicit references to the original Liberation
Sans SDF font. The observed base font sizes range from 16 to about
61.35 Unity units. Yarn body components use 40, last-line components
use 32, and the choice prefab uses 36, all with autosizing disabled.
The 16-unit targets include the six gameplay indicators and two
settings components on each build. These are serialized font sizes,
before scaling and rich-text overrides.

| Asset in `sharedassets0.assets` | macOS PathID | Windows PathID |
| --- | ---: | ---: |
| LiberationSans SDF, static primary | 627 | 622 |
| LiberationSans SDF - Fallback, dynamic | 626 | 621 |
| Embedded fallback source font | 300 | 299 |

The TMP default equals the primary font. There is no configured
global fallback list or alternate regular/italic typeface in the
two font assets' weight tables. The primary atlas contains none of
the 66 Russian letters. The local dynamic fallback has an initially
empty character table and uses identical embedded font bytes on
both builds. The source font has 2,048 units per em, horizontal
ascent 1,854, descent -434 and U+0020 advance 569 font units.

The 95-code-point sample covers the 66 Russian letters, all ten
digits, common punctuation including `№`, guillemets and dashes,
and regular, nonbreaking and narrow nonbreaking spaces. The
embedded face has a mapped glyph and positive advance for every
sample code point and a nonempty outline for every non-space
sample. The 28 relevant entries present in the primary atlas
resolve to glyph records with positive advance and nonzero
rectangles for non-space characters. The same local chain covers
all 95 sample code points at every checked target.

This establishes source bindings and font data coverage. It
does not exercise the engine's dynamic glyph insertion, final
font styling, text fit, atlas capacity or native readability.
Recheck the final corpus including any combining marks and
retained names, then exercise the actual tight roles and staged
typography on both delivered builds. No asset, texture, game
installation or save was changed.

Both reports reproduced byte-for-byte. Local probe and output
are under `localization/work/font-role-coverage-20261110.1O5tSJ/`.

| Input or output | SHA-256 |
| --- | --- |
| v42 shared inventory | `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d` |
| Embedded font bytes, both builds | `e5b0af421ea2bfbc1ac8d251d647268087ae82786234c57f757d1f0b90fa8b49` |
| `inspect-font-roles.py` | `c247904a4915e6ade8f7a7d90f733ce1be645d13d13981b2ffb5e46d62414045` |
| `font-role-coverage.json` | `eeab1e4557a5298bf10fdc1719b9aef31c468da1b5444c705a195688a71f2dd7` |
