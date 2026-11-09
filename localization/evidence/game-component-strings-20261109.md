# Strings in game-owned serialized components

The new read-only scanner uses the 17 pinned Unity asset files and managed
schemas on each build. It resolves every MonoBehaviour script reference to
select `Assembly-CSharp` components, then checks the common header and
requires a complete byte-identical decode and re-encode for each selected
object. Nested string fields retain the asset name, component PathID,
script identity, raw object digest and complete field path with array
indices. Unity base object names remain outside this string inventory.

The schema generator labelled a nested `string[] bones` as a scalar
string. The correction is confined to the four mesh-attachment component
classes and checks the precise generated array shape before replacing the
type. Three game component classes also needed inline managed-reference
schemas. The scanner supplies the missing trees for the pinned serializable
dragon-bark and game-event response types. It removes the synthetic
MonoBehaviour header from those generated inline layouts and uses a
per-object read context. Every selected component passed exact read-back.

| Build | Components | String fields | Needs consumer review | Nonempty Yarn references |
| --- | ---: | ---: | ---: | ---: |
| macOS | 1,331 | 10,973 | 826 | 123 |
| Windows | 1,299 | 10,936 | 824 | 123 |

Each build has 93 previously known level-configuration references and
30 further references from `DragonBarkFeaturePlapResponse`,
`DragonPerformanceTriggerEggAnimation`, `DragonPerformanceTriggerDragonBark`
and `YarnRunDialogOnEnable`. All 123 values point to existing nodes in the
pinned program. Seven bark references per build point to `DragonColdBalls`,
including `level4#2172` and `level6#1701` on macOS and `level4#2118` and
`level6#1647` on Windows. This adds an entry path that the earlier direct
level configuration, named Yarn transfer and managed-literal scans did
not cover. `DragonBarkDialogue.OnStart` reads `dialogueTitle` and sends it
to `StartDialogue` or `StartBark`. Player reachability still requires runtime
evidence. The other four generic `Dragon…` nodes remain unresolved.

The shared inventory adds 21,909 per-build fields, of which 20,259 have
exact-preserve roles. They include rig keys, Unity event bindings,
serialized managed types and Yarn node references. The unclassified fields
include bark descriptions and dragon descriptor names. A direct reference
scan found the bark description getter and the dragon name's descriptor
store, with no downstream direct consumer in the pinned game assembly.
These results leave runtime and indirect consumers open. The new fields
are source occurrences, with no implication that they are all visible or
that the two builds' object IDs pair.

Both exports reproduced byte-for-byte. Local evidence is in
`localization/work/game-component-fields-20261109.Ku7FyS/`. The two
`*-consumers.il` reports have the same SHA-256
`898c309aa46e3ea88a4f848967c66850d303742cd9bc695630297507aa874e58`.
The export hashes are pinned in the [shared inventory recipe](../assemble_source_inventory.py).
The full suite ran 179 tests with one optional catalog test skipped. That
test passed separately with the built catalog-options scanner supplied.

```sh
python3 localization/inventory_game_components.py macos ORIGINAL_MAC_DATA > game-components-macos.json
python3 localization/inventory_game_components.py windows ORIGINAL_WINDOWS_DATA > game-components-windows.json
python3 -m unittest discover -s localization -p 'test_inventory_game_components.py' -v
```
