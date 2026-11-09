# Paired Yarn translation scope

`inventory_yarn_scope.py` binds all 1,839 stable IDs in the v40 shared
inventory to both installed source tables and original instruction
positions. It checks the source wording, node, instruction, operand
attributes and compiled program pins. It then runs the existing
transition repair in memory and walks both repaired programs.

The scope uses the 123 nonempty serialized entry references per build
from the shared inventory. These include 93 level configuration fields,
21 bark responses, four egg animation triggers, one dragon bark trigger
and four on-enable dialogue components. They resolve to 94 distinct
entry names per build. The configured `Start` precaution brings the
root set to 95. Both root sets and all closure node names matched the
[earlier caller audit](yarn-transition-runtime-20261109.md#compiled-transfer-and-entry-point-follow-up).

| Program | Named-reachable nodes | Named-reachable text IDs | Unresolved named transfers anywhere |
| --- | ---: | ---: | ---: |
| Original macOS | 133 | 1,593 | 5 |
| Original Windows | 137 | 1,607 | 5 |
| Repaired macOS | 133 | 1,593 | 0 |
| Repaired Windows | 133 | 1,593 | 0 |

The repaired closure contains the same IDs on both builds. The 14 IDs
removed from the original Windows closure by the Conrad route alignment
remain in translation scope. Recomputing with every defined node as a
root checks the remaining transfer operands too, including the original
four unrooted routers. The repaired programs still refer to all 1,839
source table IDs. This is static reachability across named transfers,
including conditional paths.

## Locale inputs and exact values

| Disposition | IDs |
| --- | ---: |
| Dialogue locale | 1,823 |
| Alexander body in the speaker locale | 1 |
| Exact-only marker values | 15 |

The 1,824 translatable IDs include 231 outside the repaired closure.
This conservative scope retains fallback, editor, demo and other
unrooted text until evidence supports a narrower owner-approved scope.
It also retains all 18 exact speaker prefixes. The 15 exact-only values
are the five embedded titles and their ten punctuation markers.
Alexander's English table value is the sixteenth exact value. Its
translated body uses the same ID in the speaker locale. The two
displayed character names are separate speaker-locale inputs.

The 25 differing English source values include six options. The paired
review found spelling, contractions, grammar and brand styling
differences. All preserve the same markup, placeholders, digits and
instruction controls. The final locale files still carry their own
platform's exact English source value for those IDs.

## Coverage gate

Run the report against the two pinned source Data directories and the
current v40 working inventory:

```sh
"$PYTHON" localization/inventory_yarn_scope.py \
  --inventory localization/work/source-inventory-20261107/combined-provisional-v40-20261110.json \
  --macos-data "$macos_data" --windows-data "$windows_data" --output "$new_scope_report"
```

Add `--locale ru`, `--macos-dialogue`, `--macos-speakers`,
`--windows-dialogue` and `--windows-speakers` to require complete
inputs. The output binds both locale file hashes per platform. The
check requires every ordinary ID, including the unrooted dialogue,
and requires Alexander's display body and both names. It uses the
same source, markup and preservation guards as the builders.
This is structural coverage. The complete positive control uses
English passthrough dialogue and synthetic name and body values.
It establishes no accepted Russian translations. Both real Russian
draft files have 15 entries, 14 changed values and one unchanged
punctuation entry. The coverage gate rejected each for 1,808 missing
ordinary IDs. All 191 project tests passed with the paired tools enabled.

The two scope exports reproduced byte-for-byte. Local evidence is
in `localization/work/yarn-scope-20261110.YfzIDB/`.
The scope SHA-256 is
`ef9bcd136ec6b9c134c0d72e7e384096cf1170f06581a6ea36e8f0374b50ec3e`.
The structural control receipt SHA-256 is
`b5f1281879bf7cc7d05311bb518553a1b6d25bd831e4bbeca0ff395d3366d2c1`.
UI, settings, code-driven text, glossary, scene decisions and runtime
acceptance remain separate from this Yarn coverage gate.
