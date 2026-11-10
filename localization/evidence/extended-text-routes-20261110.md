# Extended managed and serialized text routes

The optional `--extended` mode of `text-setter-consumers` checks
selected TMP text methods, direct text field writes, legacy text
generation, IMGUI, UI Toolkit and Unity Localization references across
the same 170 macOS and 172 Windows assemblies. It also inventories
parameterless instance `OnGUI` definitions. The original one-string
setter report still reproduces byte-for-byte on both builds.

Both extended outputs contain the same 1,024 references and writes.
There is no `OnGUI` definition or extended hit in the game assembly.
Ten additional TMP calls are settings input-field setters. They take
numeric or string values from the settings input path. The pinned
stock menus register dropdowns and sliders, so this path adds no
player-facing wording to the known scope. The remaining hits are
in Unity UI, rendering and localization libraries. They include
library-internal work such as binding error objects and schema names,
so the total counts references and writes.

| Category | References per build |
| --- | ---: |
| UI Toolkit text-related references | 554 |
| IMGUI text-related references | 342 |
| Direct text field writes | 48 |
| TMP text methods | 25 |
| Unity string-localization API | 20 |
| UI Toolkit tree operations | 15 |
| Unity missing-translation configuration and reads | 11 |
| Legacy text-generator calls | 9 |

The companion serialized scan resolves 3,498 macOS and 3,435 Windows
MonoBehaviour script references across the 17 pinned source assets.
It finds no stock TextMesh, UI Toolkit document, visual tree or
panel-settings object in those files. The local Addressables bundle
and catalog audit separately accounts for three containers and finds
no UI Toolkit or string-table location. IMGUI debug label references
in the render-pipeline libraries are consistent with the separate
[debugger activation audit](legacy-ui-inventory-20261107.md#runtime-debug-entry-points-in-the-two-pinned-builds).
The follow-up activation scan includes direct member references,
type tokens and generic type arguments for `CameraSwitcher`,
`DebugUpdater` and `UIDocument`. The camera switcher references
are all in its own implementation. None of the three component
types occurs in the 17 serialized assets.

## Unity localization fallback preservation

The serialized `LocalizationSettings` object in `globalgamemanagers.assets`
binds a managed `LocalizedStringDatabase` by reference ID. The
reader round-trips the outer settings fields and the selected
database payload as two byte-exact segments. The database has an empty
default table and enables `ShowMissingTranslationMessage`. Its
`m_NoTranslationFoundMessage` is
`No translation found for '{key}' in {table.TableCollectionName}`.
This wording also exists in the database constructor at `IL_0008`
and its fallback path at `IL_0080`. The pinned implementation of
`ProcessUntranslatedText` formats it and can return it to a
Unity table caller with that option enabled. It is distinct from
the built-in Yarn missing-line record.

The sole serialized `LocalizeStringEvent` in each scanned build is
disabled and has an empty table and entry reference. Its listener
targets the already protected `TextInput/Label` TMP template.
The stock settings use their verified backup-string inputs. All
five pinned dialogue runners leave their provider field empty and
select the built-in Yarn provider. The pinned local catalog contains
no string table. Together these bindings leave no observed stock
player path to the Unity database message.

Retain the serialized setting and both Unity assembly occurrences
exactly. The macOS app builder now verifies the entire pinned
`globalgamemanagers.assets` file after signing the staged output.
The existing Managed verification preserves the complete
`Unity.Localization.dll`. The Windows adapters publish the
selected assets and managed replacements separately from the
global settings file and Unity Localization assembly. Their final
package still needs its preservation verification.

## Reproduction

```sh
dotnet "$text_setter_tool" macos "$macos_data/Managed" --extended
dotnet "$text_setter_tool" windows "$windows_data/Managed" --extended
"$PYTHON" localization/inventory_serialized_text_bindings.py macos "$macos_data"
"$PYTHON" localization/inventory_serialized_text_bindings.py windows "$windows_data"
```

Receipts are in `localization/work/extended-text-sinks-20261110.ehYdQT/`.

| Evidence | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Extended managed references | `ae9bcfdd46aa60bff03eb41d333fe32ed5aaa10f64acac89481179fade3ffd81` | `0bba4448b8057d0a109a0748a55243acfdf9b5ed03b86f69987b0cf145782ec5` |
| Serialized text route bindings | `d001e6aebd98594628acffc722917e9217b9b3d8ed1932eed835ba7e176bace0` | `87ba3b8e67c71b2867277ee6061975b300c2a6b518f5c1d77c7e42506c479ea4` |
| Unity fallback flow | `83635240aa0d319a54eb5b5c4c7018da4c6e85f7c923a65bd1ef354b3260d65f` | `3f4763f723cb8daf218c20dbe3fdcc2865d3c8e29ce013c6a86c68a77a2798b7` |
| Selected activation references | `8e1a602640c8da830e5503cfcc7383017060ae82d0666751d6da31479e5d354c` | `74c7a74f2670f0ea643c50a45cdff2b88115bc3399ba02cc39b1a814c7bdd556` |

These are managed and serialized stock-source checks. Native code,
reflection, dynamically loaded resources and other uninspected output
APIs remain outside their coverage.
The extended reports and serialized bindings reproduced byte-for-byte.
All 194 project tests passed, including a wrong-build scanner control
and a staged global settings corruption rejected before publication.

## Managed resource reads and stock Yarn asset bindings

The separate `--resource-routes` mode finds 195 macOS and 193 Windows
references. It scans Unity resource, bundle, Addressables and TextAsset
API references in all pinned managed assemblies. File, stream, network
and reflection checks cover the game, Yarn Unity, settings, Addressables
and Unity Localization assemblies. Short IL windows identify local
call context.

- The game assembly loads a scene by its Addressables key and
  `SphereProjectorAlphaWrite` as a Material. Its direct JSON reader
  is called with `savegame.dgn` by the current save manager on both
  platforms and by the older save manager on macOS. The separate Yarn
  file reader reads persisted variables. Its load method has no direct
  managed caller in the scanned assemblies.
- The game's four selected reflection calls register Yarn command
  handlers. The ten direct TextAsset reads on each build belong to
  catalog loading, probe data, line-breaking rules, engine TextAsset
  accessors and UI Toolkit initialization.
- The built-in Yarn line provider has three references to
  `GetLocalizedObjectAsync` in each build. Full serialized reads of
  the pinned YarnProject and Localization objects reproduce their exact
  bytes. Each project uses the same English object for its base
  localization and its sole locale entry. All 1,839 localized strings
  match the extracted source in order, every object and Addressables
  reference is empty, and both localized-asset flags are zero. The
  compiled program matches the existing protobuf extraction. The 209
  metadata values are all `lastline` tags attached to known IDs.

These checks add no source IDs. They establish the serialized stock
Yarn bindings and the listed managed call sites. Native behavior,
indirect calls and runtime content injection remain outside this pass.

```sh
dotnet "$text_setter_tool" macos "$macos_data/Managed" --resource-routes
dotnet "$text_setter_tool" windows "$windows_data/Managed" --resource-routes
"$PYTHON" -B localization/verify_yarn_resource_bindings.py macos "$macos_data"
"$PYTHON" -B localization/verify_yarn_resource_bindings.py windows "$windows_data"
```

Receipts are in `localization/work/resource-route-audit-20261110.ffbSRj/`.

| Evidence | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Managed resource references | `9b8b418494a8d002c22da0b5a9bc3f4473f3e941753247da8236856b68cbc28a` | `a99cbb114b8c36c8017a60f3a86a41a83f2d4a399eaf64f7be8a19e4fbe3b4d3` |
| Yarn resource bindings | `ec42e53592453fba9d4140edcf9f185dcf16ffb7ceca7c3e6148fedf8891f7c9` | `aac6cdd1089feb88a19e38fa480f29e0af65cc601ba64cee8aaca66a92de87ca` |

Both reports reproduce byte-for-byte on a second run. Legacy and
extended scanner outputs still match the prior receipts. Each tool
rejects macOS inputs when run as Windows before producing a report.
With an otherwise valid text entry, either a populated local object
pointer or a populated Addressables GUID fails the entry check.
The project suite ran 208 tests with five skips and no failures.
