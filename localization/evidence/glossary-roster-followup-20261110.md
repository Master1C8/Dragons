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

## Paired runtime parser check

Desktop .NET ran the unmodified Yarn `LineParser` and
`LocalizedLine.CharacterName` getter from the original managed
assemblies. The probe pinned the core and per-platform Yarn Unity DLL
hashes and the paired scene export. It used the built-in provider's
empty substitution array, English locale and implicit-character
setting. All 1,261 lines and 578 options per platform have zero
compiled substitutions and were evaluated. Controls recovered an
unknown name both from a colon prefix and explicit character markup.
Disabling implicit extraction on the colon control and parsing plain
text both returned an empty name.

The results match across both builds and against every candidate ID in
the static speaker scan. The 18 known labels occur only in the three
Ryan–Conrad joint scenes. Ten return `Conrad` and eight return `Ryan`.
Five further values return `title` and are the unreachable fragment
markers. `line:4b36ea4e` returns the whole Alexander introduction
prefix and belongs to the separate body adapter. The remaining 1,815
strings return no character name, including all 578 choices. This
closes the source-table search for an additional parser-provided label.
It does not assign an actor to an unlabeled line or test the Unity
presenter.

Local probe source and outputs are in
`localization/work/yarn-speaker-roster-20261110.EZsFur/`.
The macOS receipt SHA-256 is
`894f8bd6248c4b2f058db5e211d9579b7ab3cb52277e9030dba9712f21b39217`.
The Windows receipt SHA-256 is
`c56f38137696c8ecfd37a3760152a2992e8806080eaf7b77653f145621f6a1dd`.

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
Their 20 IDs remain in scope. They comprise 12 unlabeled dragon lines
and eight player choices. The four contexts are asking for a second
cleanliness check, responding to buzzing, objecting to an early
dismissal and thanking the player after washing. None of their parsed
texts adds a named speaker. Neutral treatment without assigning a
named dragon has been presented to the owner for a decision. The
residual unprefixed `Mount_Alexander_2_6` belongs to the
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
| `dnw-franchise-representative` | The current meaning describes a communication where the source describes the caller role. | Term «Голос франшизы». Meaning «Голос за кадром в звонках от сети Drag'N Wash. Личность, число звонящих, пол и местоимения не установлены. Использовать нейтральные формулировки.» |
| `dnw-franchise-223` | «Франшиза Drag'n Wash № 223» assigns the number to the franchise. The English and Russian definitions both identify the player's location. | Term «Филиал № 223 сети Drag'N Wash». Keep the existing definition and the unnumbered `dnw-dragn-wash` brand entry. |
| `dnw-kobold` | The source defines a species. The Russian definition describes an individual of that species. | Keep «кобольд». Meaning «Вид, к которому принадлежит персонаж игрока.» |
| `dnw-dragon` | The source defines a species. The Russian definition describes an individual of that species. | Keep «дракон». Meaning «Вид, к которому относятся клиенты мойки.» |

Keep «фамильный гребень» for `dnw-family-crest`: the paired lines describe
a crest worn on the head and representing a family. For example,
`line:1ff9a04c` describes its placement and `line:8ee41fdc` establishes
the family association. Preserve the existing separation of Max and the
unresolved girlfriend reference. The source does not establish their
identity as the same person.

Preserve a second referent distinction in the explosion stories.
Alexander names Igwix in `line:9d7cc63c` and uses masculine pronouns
for the named colleague in `line:68ebf07b` and `line:8245fe2b`.
Ryan's parallel account in `RyanExploded_Intro` says “the alchemist”
and later “they” (`line:e02f464d`, `line:cc4e48a3`). Keep that
reference unnamed and neutral in Ryan's lines. Similar events do not
establish the alchemist's identity in that branch.

The owner selected «Большой К» for Conrad's `big C` on 2026-11-10.
The self-reference `line:0e1fd4b0` and the echoed choice
`line:982fd3c7` share that nickname with the Russian initial of
«Конрад». Inflect it where the sentence requires it. The other choice
`line:255362b9` uses his ordinary name. The nickname decision is
resolved. Review the complete Russian group after glossary readiness.

## Bound Russian correction draft

The [correction plan](glossary-ru-correction-20261110.json) records five
field changes across the four entries above. It pins the English source,
the current Russian map and the candidate map, and includes the exact
before and after values. The candidate retains all 27 IDs in source
order. All 27 original English entry receipts and 23 unchanged Russian
entry digests matched. A mechanical application in memory left the
other 29 locale maps identical. It rejected a changed Russian base
and a second application to the already patched map.

The coordinator compared all 27 English terms and definitions against
their Russian counterparts, then read the revised Russian fields with
the affected terms and usage rules. The bounded naturalness and
consistency recheck covered the player, Alexander, Conrad, Ryan, the
franchise caller, brand and branch, kobold, dragon, drake, washer, wash,
Yip, mount, special endings, family crest, Yip-Man and Dragons of the
Galaxy entries. It retains the neutral caller and player guidance,
keeps the brand spelling consistent, and distinguishes species from
the individual characters and the service. In the caller definition
«число звонящих» leaves the possible species and number open.
These are coordinator checks on the correction draft.

The compact candidate Russian map SHA-256 is
`e3165b854d1d9fe4a65968c3635d812994b2977a450ad0d1de8660a9c0d1e95a`.
The plan SHA-256 is
`cae7faca7bae621f25a62d2ba7dde6b61eadf747e39c5b18ed4613006cb7791b`.
The full candidate was generated locally at
`localization/work/ru-glossary-repair-20261110.4n94HG/glossary-ru-candidate-reviewed.json`.

## Canonical integration

At the owner's instruction, the unrelated review directory
`data/games/the-forest-of-love/glossary-review/finley-repair-20261027/`
was backed up locally and its 136 untracked Git files were saved to
SiteForMods stash `5124e04f8033faf03519f318436f5c343d3cc8f4`.
All 136 stashed byte hashes and the 51 ignored files left in place
matched their pre-stash values. The verified safety archive is
`.cache/dragons-glossary-safety.JgJNvF/forest-untracked.tar.gz` in
SiteForMods.

The exact four-entry correction is now on local and remote SiteForMods
main at `9cc4fd928769b1143eb0822fe6a61fc3fcaff89c`. The whole translation
file SHA-256 is
`c482427827a4b63eb5e5837998747f676ece82419a8aaaca8d488669170e7c84`.
The compact Russian digest matches the draft. English and the other
29 locale maps retain their exact data. The canonical CLI passed
structural checks and all 59 glossary tests passed. The previous
editorial receipts remain historical. The unresolved generic speaker
treatment leaves standard-localization readiness at `needs-review`.
