# Ukrainian special-scene wording

Authoring input is [translation.json](translation.json). The first
batch covers 46 of 1,947 package IDs in five of the 27 current
special-scene groups. It follows the common stage and review protocol
in [HANDOFF.md](../../HANDOFF.md). Ordinary translation remains gated
on the other cases and the applicable feasibility checks.

| Input | Identity |
| --- | --- |
| Shared v42 inventory | `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d` |
| Paired Yarn scope | `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30` |
| SiteForMods English glossary | `29b0bb56`, canonical fingerprint `3d261921e114b6feab10f57ad54d43674a75e991d94937686155b92cce399dc3` |
| SiteForMods Ukrainian ordered locale map | `4ff95ddd932acd5f990c8f8f11f76ecf372976200645872adc464a5b4842b4a0` |
| First authored batch | `c7c088e13254489bc23e4ad64a2c84361e320f8f0a1383c39291b82009fa210e` |

The author checked the Ukrainian wording against the paired English
source, the indexed choice groups and the glossary. The editor and
runtime columns below concern this batch only.

| Case | Wording decision and acceptance controls | State |
| --- | --- | --- |
| `anonymous-dragon-address` (20 IDs) | Keep both the unnamed dragon and player gender-neutral. The dragon asks about remaining dirt, and the player can apologize or explain unfamiliarity with the button. Retain the sound «БРРТ», silence option and «Так!» versus «ТАК!». Exercise both branches in all four groups and reject any choice-order change, added identity or shift in who acts. The source buzzing finish-command limitation remains as documented in the [source registry](../evidence/generic-dragon-entries-20261110.md). | Author checked. Ukrainian scene runs and visual review pending. |
| `big-c-nickname` (14 IDs) | Conrad calls himself «Великий К», tying the joke to Конрад. One reply echoes the nickname and he drops it. The other uses «Конраде». Retain both destinations, the Ryan relationship reference and the italic spans. Reject loss of the initial or inversion of the two replies. | Author checked. Both Ukrainian branches and visual review pending. |
| `alexander-proletarian-register` (7 IDs) | Keep «пролетарська» as the high-register descriptor, «проле-» as the false start and «робітничому класу» as the clarification. The alternative thanks him and leads to the public-access comment. The English spelling error in the Windows source does not affect the wording. Preserve the original tags and test each destination and convergence. | Author checked. Both Ukrainian branches and visual review pending. |
| `new-slot-display` (4 package IDs) | Use «НОВИЙ» for the runtime slot label and «Новий» for the three serialized labels. Both describe a new save slot. Exercise all three empty slots and reject changed progress formats or a change to an occupied slot's state. | Author checked. Empty-slot runtime result recorded below. Occupied-slot and visual checks pending. |
| `missing-yarn-line-display` (1 package ID) | Use «!! ПОМИЛКА: Репліку не знайдено!» for the existing error route. A missing line must still reach the fallback and a valid line must not. | Author checked. Managed bytes verified. Ukrainian runtime error control pending. |

Both complete builders passed a private structure control containing
the 46 authored values and original English for all remaining IDs.
Read-back matched the 41 authored Yarn values and all other Yarn
strings, key order and metadata. The two managed strings were present
in the built assemblies. The stock font contains all 58 display code
points in this batch. English control values stay outside the authoring
file and do not count as translated or reviewed.

The paired background New Game test saw three active «НОВИЙ» and
three active «Новий» labels on both builds. The initial observers
still expected the Russian spelling for the serialized labels.
The successful repeat changed that expectation alone. The macOS
and CrossOver observers recorded no foreground windows, and the
original profiles matched their pre-run hashes.

Local control assets and receipts are under
`localization/work/uk-special-scenes-20261110.pE2LiD/`.
