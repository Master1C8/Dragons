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

## Field roles in the v2 exports

The pinned root Managed inventories (170 macOS and 172 Windows assemblies)
were scanned for direct field and getter references. The following table
accounts for all 1,650 formerly uncategorized fields.

| Role | macOS | Windows | Verified consumer |
| --- | ---: | ---: | --- |
| Exact animation keys | 401 | 399 | `DragonBarkAnimationToggleBool.OnStart` and `OnEnd` call `Animator.SetBool`; the egg trigger forwards its key through `DragonBarkOviposition` to the same base class. `CreditsIconAnimator`, `LocomotionAnimationBridge` and `IntermissionFade` pass parameters or state names to Animator setters, `Play` or `AnimatorStateInfo.IsName`. |
| Exact progression flags | 20 | 20 | `FlagDelivery.OnFlagChanged` compares the event's flag, `InteractableToolEquip` compares, reads and sets flags, and `WalkNWashDragonDescriptor.StartWithAuxMap` calls `Flags.IsSet`. |
| Exact menu intent keys | 24 | 24 | `MenuIntents` constructs `MenuEventUserIntent`; the six observed menu handlers compare the event key with `Cancel` or `Pause`. |
| Bark descriptions awaiting runtime review | 361 | 361 | `DragonBarkAnimationToggleBool.GetDescription` returns the field. The pinned assemblies contain no direct call to a dragon-bark `GetDescription`. |
| Dragon descriptor names awaiting runtime review | 20 | 20 | `WalkNWashDragonDescriptor.GetDescription` writes the name to `WalkNWashSceneState.DragonDescription.name`; the pinned assemblies contain no direct read of the destination field. |

The nested bark roles check the actual serialized type in each registry
entry. On each build 341 entries are `DragonBarkAnimationToggleBool` and
20 are its subclass `DragonBarkAnimationPlayVFX`. The two macOS-only
transition states pass through `IntermissionFade.RunTransition` to
`Animator.Play`. The distinct runtime-review roles leave indirect access
and visibility open. The source union now contains 21,147 exact-preserve
component occurrences and 762 with a specific runtime-review role.

The v2 export recipe below reproduced both files byte-for-byte. Comparing
the v20 and v21 unions confirmed that only the roles of these 1,650
occurrences changed. The direct reference reports are in
`localization/work/game-component-consumers-20261109.Crtz9a/`.
All 180 localization tests passed with the catalog-options tool supplied.

| Build | Direct references SHA-256 | Consumer follow-up SHA-256 |
| --- | --- | --- |
| macOS | `2096e0fd953fce00df8028eca8a898f0c76c3cbb01d30d152c873defda231c4d` | `77636b5332683cbe8bc43ee9a215ad56fbcbf62dc0cb29ec6b8d2d7f563cc083` |
| Windows | `586f5321a0ddc7c8818d8238dd9e243338dc2c620d2514d3367f729d970ea586` | `b1197bc905657428879b236e292e5bc5d50e3a6429b13ec217260ba888d8112a` |

```sh
python3 localization/inventory_game_components.py macos ORIGINAL_MAC_DATA > game-components-v2-macos.json
python3 localization/inventory_game_components.py windows ORIGINAL_WINDOWS_DATA > game-components-v2-windows.json
python3 -m unittest discover -s localization -p 'test_inventory_game_components.py' -v
```

## v29 metadata preservation

A follow-up scanned all 170 macOS and 172 Windows root managed DLLs.
The file digests match the earlier caller scan as a multiset. The earlier
probe reported the assembly names of 13 Yarn dependencies per build
without their on-disk `Yarn.` prefix.

- `DragonBark.GetDescription` introduces a virtual slot and
  `DragonBarkAnimationToggleBool` overrides it. There is no method
  reference to that slot in the scanned IL. The bark classes have no
  alternative interface mapping or `ToString` override. The machine's
  `ToString` formats the current bark object without reading its
  description. The description field is written by its constructor and
  read by its getter.
- `WalkNWashDragonDescriptor.GetDescription` copies the component's
  `name` into the value-type `DragonDescription.name`. The sole reference
  to that destination is the store. The other fields have ordinary
  consumers. In particular, `DialogCommands.StartDialogue` sets
  `$dragonModel`, `$dragonPrefab` and `$dragonFace` from the Animator,
  GameObject and head Transform names. Yarn's displayed character name
  comes from the `character` markup's `name` property.
- No exact `GetDescription` string literal occurs in the scanned DLLs
  or in the pinned component exports. The game assembly's four
  `Type.GetMethod` calls belong to generated Yarn action registration
  and do not bind the getter. The scan does not prove the behavior of
  native reflection or external mods.

The assembly recipe now keeps the 722 bark descriptions and 40 descriptor
names byte-for-byte as internal metadata for the verified builds. The pinned
component exports retain their original discovery roles. Two independent
v29 assembly invocations produced byte-identical output. Comparison against
v28 found only the 762 role changes, with every original ID, value, location
and raw object hash retained.

Local scanner source and reports are under
`localization/work/component-indirect-20261109.5gu524/`.

| Artifact | SHA-256 |
| --- | --- |
| Scanner source | `ebfddaceeb0e054994256c048c4d1b1d576b8b0c13cc5e5442512b95a758e628` |
| macOS report | `e968822ab39e82740ff4f991dc1532eb4b5cc0b88d4fd328a81f16b07acc2bfe` |
| Windows report | `e9e022948f2b16c72809f8f308329cf085343f2501674a596265ce280b6060fb` |

## v31 managed bark arguments

The managed constructor audit matched the complete assembly name and hash
inventory on both builds. `DragonBarkSexAct` and `DragonBarkOviposition`
forward their description arguments to `DragonBarkAnimationToggleBool`.
Its getter and the base getter that returns `Idle` use the virtual slot
examined above. The animation keys and Yarn destinations travel through
separate arguments.

`DragonBarkNotifyTransition` forwards its reason string to
`DragonBarkResponseTransition`. The sole IL reference to the latter's
string field is the constructor store, with no matching formatter. The
recipe preserves six managed bark descriptions and 24 transition reasons.
It retains their original method, offset, literal and constructor binding.
As with v29, arbitrary runtime reflection is outside the evidence.

Local reports are under `localization/work/bark-reason-consumers-20261109.2w9Bmk/`.

| Artifact | SHA-256 |
| --- | --- |
| Scanner source | `bf41bd7269a9f163c916013c0ecf89740c211318742b417540665e66d815ef82` |
| macOS report | `a2dd7aa2778862fcbfe1b94d2713b5249f55507cc18634bc19d44ebef3ad407f` |
| Windows report | `7464dbdbc8c5ef06354b1dd78fdc45f568ae33c2fed6d6dde5d6fd97bbfb07ba` |
