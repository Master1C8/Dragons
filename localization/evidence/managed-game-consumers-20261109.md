# Managed game consumers in the v22 source inventory

The v22 recipe adds a consumer and role to 214 existing occurrences.
The stack check follows only known instruction shapes and exact call
signatures. It keeps a tracked value across a call when all consumed
values are above it, and stops at unsupported instructions and branches.
For the audited save path fragments, JSON syntax and reflected Yarn
registrations, the source binding uses the original method and literal.
The reflected registrations also check the literal ordinal because the
same string can name both the Yarn command and the reflected method.

| New role group | Occurrences | Evidence |
| --- | ---: | --- |
| Exact JSON keys and protocol | 59 | `FlagRegistry.ToJson` calls `JSONNode.set_Item`; SimpleJSON uses exact scalar tokens, escape sequences and structural values. |
| Exact file paths and fragments | 17 | Current and legacy slot directory construction, save and backup names, and the Steam App ID file path. |
| Exact command and reflection names | 16 | `RegisterActions` passes the command name to `AddCommandHandler` and the target member name to `Type.GetMethod`. |
| Exact state, animation, rendering and menu keys | 42 | Typed arguments for graph parameters, Yarn state, animation and VFX setters, and menu transition constructors. |
| Diagnostic visibility review | 52 | A Unity log or exception consumes the literal or a composed message. This includes 36 occurrences in Yarn Spinner Unity. |
| Bark visibility review | 28 | Twenty-four reasons reach `DragonBarkResponseTransition.reason`; four descriptions reach `DragonBarkAnimationToggleBool.description`. |

For example, the two `Player put egg` occurrences on each build have
distinct destinations. The description is passed to the oviposition
constructor, which forwards it to the base animation bark. The reason
is passed to the notification constructor, which forwards it to the
transition. A direct scan of each pinned game assembly found a store
but no direct read of the transition's `reason` field. Indirect
consumers and runtime visibility remain open.

The two pinned original DLLs were also executed under .NET 8 with
in-memory fixtures. SimpleJSON parsed and wrote quotes, backslashes,
control characters, a Cyrillic character, booleans and null. The
output round-tripped to the original value and honored the serializer's
ASCII escape switch. The isolated flag registry emitted `levelIndex`,
`id`, `type`, `boolValue` and `stringValue` in both builds, plus
`version` on macOS. These checks cover serialization with synthetic
values. The tests made no calls to read or write player saves.

Local IL, probe source and receipts are in
`localization/work/managed-game-roles-20261109.8LlHLN/`.

| Build | Consumer IL SHA-256 | In-memory receipt SHA-256 |
| --- | --- | --- |
| macOS | `d6482e62fdcfee0af4552d32d7de2114402938417fb4cbef9fedc51ae4363224` | `4c6042e83b0fa55b0659d311fb2a361fe03f6c80da13925bf405fd727a5d4da6` |
| Windows | `37cf463c37d02dd3e5d3dc1ae3cc27653b08ea69154f078cdcdbaabb5d160952` | `20618f52ac34b8ff8e522105273308dd5d742f1487a1c324156fd11a88752ec9` |

The remaining unclassified managed occurrences are 119 in
`Assembly-CSharp`, 314 in `YarnSpinner.Unity`, 276 in `UnityEngine.UI`,
226 in `Unity.TextMeshPro` and 2 in `UnityScriptableSettings`.
The full localization suite passed all 180 tests.

## v23 method-bound literals

Complete method IL from each original game DLL traces 32 occurrences
per build to exact-preserve roles. The recipe binds each literal to its
full method signature, so other occurrences of the same value keep
their own roles.

| Role | Occurrences across both builds | Consumer |
| --- | ---: | --- |
| Rig key | 18 | Foot arrays reach `AddFoot` and transform lookup. |
| Empty value | 14 | Failed idle and nag lookups return empty strings, and the flag constructor initializes its empty string field. |
| Animation key | 10 | The Animator plays a named state or sets named float and Boolean parameters. |
| State key | 6 | Yarn flag normalization strips the dollar prefix. The camera graph uses an exact parameter name. |
| Object name or lookup | 8 | Temporary visual effects use a named object. The auto library looks up exact dictionary keys. |
| Renderer key | 4 | `Material.SetVector` receives the two shader property names. |
| Command | 4 | The queued animation command parser recognizes `Wait` and an empty argument. |

`DragonBark.GetDescription` returns `Idle` in both builds. Its
visibility remains open. There are 871 managed occurrences still
unclassified, including 53 in game code.

The SHA-256-checked IL dumps are in
`localization/work/background-combined-20261109.yMvcOH/`.
`managed-macos.il` has SHA-256
`1e229bec1494ddc4371cb49c63f762e7e5d5e1befc142fb956d74402cb8c24b6`.
`managed-windows.il` has SHA-256
`e0c76f46a360ca66b6f653b2313dd7360e27c9662eae71376d908bbf384666ba`.
The full localization suite passed all 180 tests with v23.

## v24 remaining game assembly literals

The last 53 previously unclassified occurrences in the two inspected
`Assembly-CSharp` DLLs now have method-bound roles. Twenty-nine
must be preserved verbatim. These initialize the `None` line keys
or empty values, name hitbox objects and a bone format, or supply an
editor path or exception parameter name.

Four diagnostic occurrences feed the Unity log or warning methods.
Twenty more construct `ToString()` representations for flags, tickets,
barks and menu intents. Those representations remain under visibility
review. In particular, the flag representations are distinct from the
earlier, separately validated JSON save path. There are 818 occurrences
still unclassified across the other four managed assemblies.

The SHA-256-checked IL dumps are in
`localization/work/background-crouch-20261109.6ZBUGv/`.
`residual-macos.il` has SHA-256
`2bd2dd3f7e65f545f6dc9c625dfb47c29c9f45c3995e0cddb1d6deaab920de64`.
`residual-windows.il` has SHA-256
`ed0744bc1e90b6c3c0891f22e26999bfbd67451af1e4dff4f255e1133625f40a`.
The full localization suite passed all 180 tests with v24.

## v25 Unity UI and settings dependencies

Both `UnityEngine.UI.dll` fingerprints matched the pinned source
inventory. Full method IL binds 142 exact-preserve occurrences to
object names, shader keys, input normalization, empty values,
reflected method names and an exception parameter. Ten canvas
update strings are profiler labels. Thirty-six strings feed
diagnostics, and 88 construct string representations with pending
visibility review. The two `Toggle` occurrences in each
`DefaultControls.CreateToggle` demonstrate the distinction
between the object name and the existing candidate caption.

A method-reference scan read 170 macOS and 172 Windows managed
DLLs from their original player directories. All 58 references
to `DefaultControls` methods per build came from Unity UI itself.
This bounds direct managed use within those folders. Engine or
reflection entry points and runtime visibility remain open.

The generated `{0} x {1}` resolution format is preserved in each
build. It formats the width and height read from Unity's runtime
resolution list, as verified by the pinned
[settings method reports](settings-semantics-20261107.md).
The remaining 540 unclassified managed occurrences are in
Yarn Spinner Unity and TextMeshPro.

Full methods, caller inputs and references are under
`localization/work/dependency-roles-20261109.UZpgoE/`.
`macos.il` has SHA-256
`bbfe629b10b8fab0e993ed0e8a3fa1312e7c9022a4fe649acc45621bcef0b6b6`.
`windows.il` has SHA-256
`14d6debf0a39c09f7e7d934b2e8d1c2732a9a248b51980550cd3a8037b94eb06`.
The full localization suite passed all 180 tests with v25.

## v26 TextMeshPro and Yarn Spinner Unity

The emitted full instruction lists match byte-for-byte between macOS
and Windows for the 50 selected TextMeshPro methods and 47 selected
Yarn Spinner Unity methods. The enclosing DLLs and caller inputs are pinned
separately for each platform. The final export binds the remaining
literal loads to the method and consumer identified in those dumps.

| Assembly | Exact-preserve | Pending visibility or runtime review |
| --- | ---: | ---: |
| Unity.TextMeshPro | 90 | 136 |
| YarnSpinner.Unity | 98 | 216 |

TextMeshPro exact values include ASCII lookup tables, input control
characters, style names and asset versions. Yarn exact values
include markup, CSV headers, metadata separators, resource keys
and the default node name. The command usage text, debugger
representations, diagnostics and localization failure fallback
carry separate review roles. The visible `...` prefix in the
options presenter is a preserved format value.

Every literal load has an assigned role within the five inspected
assemblies. The provisional inventory still has 1,076 managed
occurrences with open review roles, plus 762 component fields,
149 legacy UI fields and 39 other UI fields with open review roles.
Other source assets, runtime-generated text and semantic coverage
still require work.

The complete reports are under
`localization/work/remaining-dependency-roles-20261109.2CuNHX/`.

| Report | SHA-256 |
| --- | --- |
| macOS TextMeshPro | `6b393242aeea4b018bdae8d6eed9b630466616e8961400f1b40e478c63bfcae7` |
| Windows TextMeshPro | `4fe3b041d11ac1f4a40b4d0a1c38e90d6616ac7a84fcc5fbbbd2dabda7951ba9` |
| macOS Yarn Spinner Unity | `7944ffd0ef69f9ab0db302d286d70929e33bb2bd6ec8e00488f9c4ff0c808098` |
| Windows Yarn Spinner Unity | `644280e3d46783f05dbb88ffcbd98500bc14ccdd8e5ab392b059dc7b51b774b1` |

The full localization suite passed all 180 tests with v26.

## v28 player log sinks

The direct callback and logger-setter scan matched the earlier full
managed DLL inventory, including 170 macOS and 172 Windows files.
Both builds reference the searched log callback and setter methods
only in Unity CoreModule. The matches are Unity's compatibility
wrappers and its own logger constructor. The scan found no game
subscriber or game replacement logger through those entry points.
The pinned Unity UI stencil warning wrapper either returns in batch
mode or forwards to `Debug.LogWarning`.

The source recipe preserves 582 occurrences whose traced consumers
are these Unity log methods or the stencil warning wrapper. The
Windows wait-for-equipment log supplies a positive runtime control.
Throw messages, generated error result text and possible visible
fallbacks retain their existing review roles. There are 494 managed
occurrences still under review, including 190 diagnostics with
other consumers. The scan establishes the inspected managed log
routes in the original builds. Native logging and dynamically
constructed reflection calls are outside its scope.

The local logs are in
`localization/work/managed-log-visibility-20261109.dnQGdg/`.

| Report | SHA-256 |
| --- | --- |
| macOS managed callers | `e3afa39a759c519aa17b79a9bca55687e59a70e6271547289800651a6af159df` |
| Windows managed callers | `9004566b0a48d9f171733e7e2487a9eb1cfa01deedbd44a3461d8030582080a5` |
| macOS stencil wrapper | `4e0dfee65e0a3ef199e4e38ae43b992c701177bfa78f463ef8ecf8568f24e37a` |
| Windows stencil wrapper | `f7a52d245e07c1fd9291605b99400e33336dd9d36ce29120fc82d37c0c57b447` |

## v32 Yarn command help and error flow

The follow-up scanned method and field operands and exact reflection
literals across the same 170 macOS and 172 Windows root assemblies.
The two command-registration constructors initialize
`TypeFriendlyNames`. Its sole read is in `get_UsageString`, for which
there is no method reference or matching reflection literal in the
scanned inputs. The recipe preserves the 36 help-template occurrences
across the two builds.

The normal `TryParseArgs` error paths return a status and an error
string through the out argument. `Invoke` stores that string and
three target-validation errors in `CommandDispatchResult.Message`.
Its sole IL read in the inspected assemblies is in
`DialogueRunner.OnCommandReceivedAsync`, where the value reaches
`Debug.LogError`. The unhandled-command event is a separate branch.
The recipe preserves 30 occurrences on these log-bound paths.

The exception texts remain under review. In particular, the
`TryParseArgs` literal at `IL_02ae` reaches an
`InvalidOperationException` constructor and is thrown. Its consumer
was corrected on both builds. Two v32 outputs matched byte-for-byte.
Compared with v31, 66 roles and those two consumers changed. All IDs
and source values remain intact. Native code, external mods and
dynamically constructed reflection are outside the scan's scope.

Local reports and scanner source are under
`localization/work/yarn-command-flow-20261109.a0NpyF/`.

| Artifact | SHA-256 |
| --- | --- |
| Scanner source | `8407ea9f4a586165edd17ab421ec06325336c09d5244af083f9338e0554685d4` |
| macOS managed flow | `38a58968f3b938e82ee4a4d1b57e9db2cea6c2ea4d9b08def35da14581705141` |
| Windows managed flow | `eaa727fd40f63d0341250e8cb275f05cb235c340f0a9843811962940ba8be6e5` |

## v37 diagnostic representations, 2026-11-10

The original managed inventories still match all 170 macOS and 172
Windows assembly hashes. The follow-up read the bodies of all 21
formatter methods in the v36 review group and checked direct
references, typed boxing and constrained calls, immediate subclasses,
selected generic formatting calls and exact non-`ToString` reflection
literals. It traced the following paths.

| Family | Occurrences | Evidence |
| --- | ---: | --- |
| Game state | 20 | `ToString` formats for menu intent, current bark, ticket lock and flag values. No direct or typed formatting reference in the pinned scan. |
| Yarn Spinner | 40 | The pluralizers are called only by `TryParseArgs`, whose error result goes to the player log. The string and metadata table structs' diagnostic formats have no direct or typed formatting reference. The debug-list renderer has no assigned view on either build. |
| TextMeshPro | 36 | Bounds and texture-packer metadata formats have no direct or typed formatting reference. `TextProcessingElement.DebuggerDisplay` is named by `DebuggerDisplayAttribute`. |
| Unity UI | 88 | Event and raycast state dumps. The direct `PointerEventData.ToString` caller is the extended input event's formatter. Its two constrained raycast conversions remain within the input dump. |

The debug-list formatter does have a real TMP setter through
`InMemoryVariableStorage.Update`. The guard checks the view reference
before formatting. All five pinned serialized storage components on
each build round-tripped exactly and have a null `debugTextView`.
The managed scan found only the three reads inside that method and
no direct writes. This excludes the optional view for the verified
source scope, while retaining its format byte-for-byte.

The recipe preserves all 184 diagnostic representation literals.
Two independent v37 invocations produced identical output. Relative
to v36 only those 184 roles changed. This is a stock-build source
classification. It does not model arbitrary reflection, every
erased `Object.ToString` flow, external mods or an explicitly
configured debug view.

Local evidence is under `localization/work/diagnostic-format-expanded-20261109.lYwrKq/`
and `localization/work/diagnostic-format-flow-20261109.dsyWKm/`.

| Artifact | SHA-256 |
| --- | --- |
| Expanded scanner source | `db7801199769629ab28d1ea47f2b967a42e8e3759c4b694068339ae3de3e118f` |
| macOS formatter scan | `7f5246370b6ac42d6377146c5886f81ef9510914a29b0f14820a70294931f9f5` |
| Windows formatter scan | `ac4576fdfabd53f68b4413e0169c539f971e914288ebdec09e458f815b00c27e` |
| macOS debug-view bindings | `de038d2486c697bb09f23a408ba96a2e7884073b7cdea8858e53e99aed64f535` |
| Windows debug-view bindings | `e0712e83a843f36dc068145196842d482e1a5ee3ebc51a7a04779c04afd42636` |

The full localization suite passed all 180 tests with v28.
