# Glossary scope and speaker follow-up

## Source reading coverage

The four `source-reading-*-20261107.json` receipts passed
`verify_source_reading.py` against the paired scene export, SHA-256
`52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995`.
Their union covers all 184 line-bearing nodes. All 1,839 distinct
`(node, line ID)` pairs match the v41 Yarn scope, SHA-256
`5e14d25cc87714b705680667eab6fad4c60f67f7efa530f37106904cd1400bd6`.
There are no duplicate or missing nodes or pairs. Adding a trailing byte to
the paired export was rejected at the source fingerprint check. This
verifies historical source reading coverage for both builds. Roster and
editorial acceptance still require separate evidence.

## Ryan's cold-water bark

All 14 `DragonColdBalls` references in the shared inventory, SHA-256
`74113db1932d1da69c93b053bf5fb0a79750e7e9753c58b9fffef42f790cf711`,
are `DragonBarkFeaturePlapResponse` fields ending in `dialogueTitle`.
The read-only check verified the build and asset hashes with
`compare_yarn_versions.BUILDS`, `ui_locale.ASSETS` and
`map_ui_hierarchy.WINDOWS_ASSETS` before loading each affected original
asset with UnityPy 1.25.4. For each reference, the exact component bytes
matched the inventory digest. Its MonoBehaviour owner listed that
component and one local Transform. Following the local Transform parent
references yielded the same asset and hierarchy combinations in both builds.

| Asset | macOS PathID | Windows PathID | GameObject ancestry from root |
| --- | ---: | ---: | --- |
| `level4` | 2172 | 2118 | `Pair / DragonRyanSexWithConrad / DragonBallsScrunch` |
| `level6` | 1701 | 1647 | `DragonRyanA / DragonBallsScrunch` |
| `sharedassets1.assets` | 11014 | 11002 | `DragonRyan3_7 / DragonBallsScrunch` |
| `sharedassets1.assets` | 11015 | 11003 | `DragonRyan5_13 / DragonBallsScrunch` |
| `sharedassets1.assets` | 11016 | 11004 | `DragonRyan2_4 / DragonBallsScrunch` |
| `sharedassets1.assets` | 11123 | 11111 | `DragonRyanA / DragonBallsScrunch` |
| `sharedassets1.assets` | 11307 | 11295 | `DragonRyanDate / DragonBallsScrunch` |

Use Ryan as the source character for these seven serialized callers of
`line:4d3233a1`, `line:eea7573f`, `line:78975048` and `line:c2c659d1`.
There is no additional speaking character in these known uses. Which bark
branch plays in a stock run and whether it displays a speaker label remain
unverified. The four other generic nodes still lack verified callers.
Their 20 IDs remain in scope with generic dragon dialogue and player
choices. The residual unprefixed `Mount_Alexander_2_6` belongs to the
Alexander route. `Start` contains a Yarn demonstration and
`ErrorHasOccurred` contains a diagnostic message that mentions Nael.
Neither introduces a story speaker. The full semantic roster remains open.

## Russian glossary repairs proposed for review

The two franchise scenes contain 21 IDs, including seven player options.
`line:a99c515c` and `line:4183ca7e` address the location numbered 223.
`line:b83ec453` uses institutional “we”. The two calls leave the number
of speakers and their gender unresolved. Their closing lines
`line:d7b3cd09`, `line:3517b28e` and `line:5a9abbd4` support a
consistent register across both scenes. Preserve both neutral-address
decisions when reviewing caller text and player responses.

| ID | Finding | Proposed Russian entry change |
| --- | --- | --- |
| `dnw-franchise-representative` | The current meaning describes a communication where the source describes the caller role. | Term «Голос франшизы». Meaning «Голос за кадром в звонках от сети Drag'N Wash. Кто звонит и один ли это человек, неизвестно. Пол и местоимения не установлены. Использовать нейтральные формулировки.» |
| `dnw-franchise-223` | «Франшиза Drag'n Wash № 223» assigns the number to the franchise. The English and Russian definitions both identify the player's location. | Term «Филиал № 223 сети Drag'N Wash». Keep the existing definition and the unnumbered `dnw-dragn-wash` brand entry. |

Keep «фамильный гребень» for `dnw-family-crest`: the paired lines describe
a crest worn on the head and representing a family. For example,
`line:1ff9a04c` describes its placement and `line:8ee41fdc` establishes
the family association. Preserve the existing separation of Max and the
unresolved girlfriend reference. The source does not establish their
identity as the same person.

Conrad's `big C` remains a pending owner decision. The self-reference
`line:0e1fd4b0` and the echoed choice `line:982fd3c7` must share the
same nickname with the Russian initial of «Конрад». The other choice
`line:255362b9` uses his ordinary name. The alternatives presented for
review are «Большой К» and «Крутой К».

The proposals are recorded in Dragons. Integration remains pending in
the canonical SiteForMods checkout, which still contains unrelated
untracked work under
`data/games/the-forest-of-love/glossary-review/finley-repair-20261027/`.
The canonical English and Russian glossary files and their historical
review receipts were left intact. Both glossary layers remain
`needs-review`.
