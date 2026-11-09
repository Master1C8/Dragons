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
