# Provisional shared source inventory

`assemble_source_inventory.py` combines previously extracted, fingerprinted
source exports for both supported builds into one local, reproducible working
inventory. It checks every input export hash, rejects duplicate identities,
checks paired UI and legacy text hashes, and retains each source occurrence
instead of deduplicating equal strings. Existing source game files are read only
by the earlier pinned extractors; this assembler reads their exports and writes
a new output with exclusive creation.

The current working output `localization/work/source-inventory-20261107/combined-provisional-v31-20261109.json`
has SHA-256 `b8a635bab364087f078a6ff4b4a76a0441f9824cbe46c118ecfc373f692edb43`.
Its 27,113 records comprise
1,839 Yarn line/option IDs, 162 paired or Windows-only known TMP UI fields,
80 paired or macOS-only known settings fields, 149 paired legacy UI fields,
2,974 literal-load occurrences from five inspected managed assemblies,
and 21,909 serialized game component fields across the two builds. Code and
game component occurrences are kept separately per build because instruction
ordinals and object IDs can mean different things. The counts are source
records, not visible phrases, completed translations,
or a localization denominator. Each record retains its family, source values,
platform locations and current provisional role; Yarn records also retain
their node, instruction index and available option/substitution attributes.
The v3 recipe additionally pins input-action reports and identifies 56
source-bound input-control occurrences as preserve-exactly; see
`input-action-preservation-20261107.md`. The v4 recipe additionally binds 16
full-value protections and 18 separate speaker-prefix protections; see
`yarn-protection-inventory-20261107.md`. The earlier v2 output and its
byte-for-byte reproduction are historical under the prior recipe, SHA-256
`6fa14564a75d6e87ecadb700de4234b10e5ab1d1099d404760a5fe0c0e85fbea`.

The v5 recipe also binds the source-pinned credit-name manifest described in
`credit-name-preservation-20261107.md`. It verifies the complete candidate set,
both platform IDs, hierarchy, source hashes and Windows text against the
earlier UI export before marking those 34 paired records
`preserve-exactly-credit-name`. The description fields retain their original
candidate roles. The v5 output was independently reproduced byte-for-byte.
Comparing it with v4 (`dea3523b082ea0c1a1a87c25315b17fa049364d5e5c2f6bc28f3d1f1bb667bcf`)
verified that exactly those 34 roles changed and all other records remain
identical; the only additional top-level field pins the manifest hash. Focused
tests exercise the positive binding and reject changed source and hierarchy.
This classification does not establish visibility or completeness of the
remaining credits and other sources.

The v6 recipe adds all 1,156 literal-load occurrences from the two Unity UI
assemblies across the pinned builds, without pairing platforms or presuming
that a literal is visible. See `managed-engine-strings-20261107.md`. The output
was reproduced byte-for-byte; comparison to v5 SHA-256
`bb8216c3d1d88150afb0800110bb12a50642ac731b4e30c3985a94d33b04451e`
verified that all 4,048 pre-existing records remain exactly equal by ID.

The v8 recipe adds manually reviewed source-function roles for 79 IDs in six
opening/test and first-Ryan nodes, with full scoped ID/kind reconciliation; see
`opening-source-roles-20261107.md`. Both v8 runs were byte-identical. Against v6
(`7001b3a1e2da59b77758cb3e672943b120f46d9342d34933650932fdeda47a21`),
exactly these 79 roles changed and all other records remained identical. An
intermediate v7 covered only the first 39 and was superseded before handoff.

The v9 recipe adds 133 reviewed source roles across seven Ryan second/third
visit nodes; see `ryan23-source-roles-20261107.md`. Both v9 outputs were
byte-identical. Against v8
(`52103dbf23391d57a907b889e1d06056b1ac7ca0c7907d89c5269e5b4b40e5d0`),
exactly those 133 record roles changed; the other records stayed identical.

The v10 recipe classifies 319 more Ryan IDs in commit `3727bf3`. The v11 recipe
adds all 112 IDs in the nine dialogue targets named directly by
`Conrad_3_8` in the pinned Windows level configuration. Both source columns
were read, and the manifest separates 72 dialogue lines, 37 options and
three standalone dialogue beats. It keeps the platform text variants and
the wording of route-unlock labels bound to their own IDs. Comparing v11 with
v10 changed exactly those 112 roles and retained the rest of the records
byte-for-byte at the JSON value level. Two v11 runs were byte-identical.
There are 1,180 Yarn IDs still awaiting classification. These are source
roles, with runtime reachability and editorial decisions tracked separately.

The v12 recipe adds 170 IDs across the 17 distinct line-bearing targets
named directly by `Conrad_1_2`, `Conrad_2_5` and `Conrad_4_11`. It separates
98 dialogue lines, 62 regular options, five standalone dialogue beats, two
recovery prompts and three recovery options. The recovery branch in
`Conrad_Intro_4` is guarded by the three relationship flags being false and
the three options write different flag combinations. Regular route-specific
options retain distinct IDs even when the displayed text repeats. The
shared refusal node `conrad_mount_no` is counted once. Two v12 builds matched
byte-for-byte and the v11 comparison changed exactly those 170 roles.
There are 1,010 unclassified Yarn IDs.

The v13 recipe assigns all 111 IDs of `ryan_food_dialogue` to 68 dialogue
lines and 43 options. The paired source and original instructions bind
the food counter and the three route-choice destinations. The three
relationship choices remain distinct, including conditional availability
and visible route hints. Two v13 builds matched byte-for-byte and the
v12 comparison changed exactly those 111 roles. There are 899 unclassified
Yarn IDs.

The v14 recipe adds 302 IDs from the 27 line-bearing targets named directly
by the five Alexander level configurations and 77 from `Alexander_questions`.
The question roles reconcile against all seven source-bound question groups
and the shared exit, including source hashes and instruction locations. The
standalone ellipses, regular options and the all-false recovery choices in
`Alexander_5_intro` retain separate roles. The number-seven and family-crest
groups still require Russian adaptation decisions. Two v14 builds matched
byte-for-byte and the v13 comparison changed exactly those 379 roles. There
are 520 unclassified Yarn IDs.

The v15 recipe assigns the remaining 520 Yarn IDs across 87 nodes. It
separates 361 dialogue lines, 141 ordinary options, ten standalone dialogue
beats, three diagnostic lines, two recovery prompts and three recovery
choices. `ErrorHasOccurred` is a target of five named transfers in each
pinned program. The all-false relationship recovery in `Conrad_Intro_5`
retains its own options. The five mixed nodes retain their prior full-value
protections. Two v15 builds matched byte-for-byte, and comparison with
v14 changed exactly the 520 intended roles. All 1,839 Yarn IDs now have
either a provisional source function or an existing exact-value protection.
The protected records still retain their pending source-role designation.
This closes the unclassified Yarn count and leaves runtime visibility,
complete preservation and the other source families open.

The v16 recipe assigns consumer-backed roles to 919 previously unclassified
managed occurrences. For direct calls, an allowlisted consumer must be the
very next IL instruction after the five-byte `ldstr`. This binds the literal
to that call's last argument and leaves ambiguous concatenations, assignments
and later calls unclassified. Separate pinned reports bind the save-slot
literals and formats, menu transition reasons, and the four objective names
per build. The combined delta includes 595 exact-preserve roles for keys,
comparisons, formats, paths, empty defaults and transition reasons. UI
defaults, diagnostic strings and objective names retain visibility review.
The source role of `NEW` is distinct from the serialized new-slot label.
The v16 outputs reproduced byte-for-byte, and comparison with v15 changed
only the 919 managed records and the associated consumer report hash block.
The v16 SHA-256 is `f51247f170094f3d9f63e8fe85a3ae6f36b84cdd87fb715af1559538b057a31a`.
At that checkpoint 1,999 managed occurrences awaited classification, with
runtime visibility and complete preservation separate from this count.

The v17 recipe adds a pinned instruction-window export for each of the ten
existing build and assembly combinations. Generate each input with
`dotnet <managed-strings.dll> <build-key> <original-dll> --context` and name it
`managed-context-<build-key>.json` in the inventory work directory. The assembler
checks the hash and matches the header, literal ID, method token, IL offset
and value against the corresponding v2 report. The old report remains
byte-identical with the default invocation. Both modes reproduced for all
ten inputs from the pinned original assemblies. Context mode rejected a
Windows game assembly under the macOS selector before writing report output.

Classification is limited to immediate stores into allowlisted fields, first
arguments of allowlisted two-argument calls with a single independent load
or known static getter for the other argument, and the direct Yarn delegate
registration sequence. Reflection-based registration and general dataflow
remain outside these rules. Two v17 builds matched byte-for-byte. The v16
comparison found only ten newly pinned inputs and 303 managed role changes,
comprising 279 exact-preserve roles and 24 profiler labels. All 5,204
identities and source values are unchanged. The v17 SHA-256 is
`62461ab1d2f9d76fd0110b784b206eced511c0dadb83c026a0d0d5d2a8538bd2`.
At that checkpoint 1,696 managed occurrences still needed classification.

The v18 recipe adds 290 diagnostic message roles from the same pinned IL
windows. It follows the literal or its formatted/concatenated result through
allowlisted contiguous instructions to the message argument of an exact
Unity `Debug.Log`, `LogWarning`, or `LogError` overload. The tracker stops at
unrecognized operations or an argument position that would place the value
outside the message. Negative controls reject a missing log context value, a
discarded result and an intervening branch. The Windows `PlacedMount` wait
format reaches its single-object log overload through this path. These roles
record an identified debug consumer while retaining visibility review. Two
v18 builds matched byte-for-byte. Comparison with v17 verified that only
those 290 records gained a role and consumer. All source IDs and values are
unchanged. The v18 SHA-256 is
`1dd1a48c1a7d1dadecb7df91eeef7cd8838a4a766017406b3d9c4552d12ed099`.
At that checkpoint 1,406 managed occurrences still needed classification.

The v19 recipe binds more literals to their exact argument positions and
preserves a distinction between two inputs to `MenuResponseTransition`.
The first is stored as `destination` and compared with the Unity menu
object name. The second is stored as `reason`. For a level-load transition
the tracker can step across creation of the separate payload, provided
the constructor consumes only values above the tracked literal. It stops
at unknown calls and never treats the third argument as a reason.
In the decal settings constructor the third argument flows to
`Shader.PropertyToID` and then the texture ID field. The two pinned game
DLLs and decal DLLs gave identical relevant IL. The local reports under
`localization/work/managed-argument-roles-20261109.AMaZb3/` share SHA-256
`8fa799516cb63ef168a7b5b36205f93ea4999ed382a310fc1b8dae35e9b6177a`.
The decal input DLL SHA-256 values are
`20552df9a1bf2c9aa0b43b16f14817efcd3a3a77f515ce0d9a1b7630a93f5188`
on macOS and
`fefa273174484c8f9cb49da83242019ad3aa94a08268e3d17aa7b1983370068c`
on Windows.

The missing-line path has two copies per build of the same error text,
one in `LocalizedLine.InvalidLine.RawText` and one in its parsed body.
These records retain runtime review. The `TextID` values are separately
protected. The v19 delta adds 251 exact-preserve roles and four fallback
roles. Two exports matched byte-for-byte, and comparison with v18 verified
that only these 255 records changed roles or gained consumers. All 5,204
source identities and values remain intact. At v19 there were 1,151
unclassified managed occurrences. Its SHA-256 is
`2e73b75c9d94da31b51974bd3ebac09c7c87eb4ccdbaf5450ecdcb4008e5ea73`.

The v20 export retains all 5,204 prior records exactly and appends the
two pinned serialized game component exports. It checks that both belong
to the same source builds and Yarn programs as the paired text inventory.
Of the 21,909 added fields, 20,259 have exact-preserve roles and 1,650
need consumer review. The added fields, missing-reference check and
byte-for-byte reproduction are documented in
[the component evidence](game-component-strings-20261109.md).

The v21 export changes only those 1,650 roles. The pinned managed
consumers support exact preservation for 800 animation keys, 40 state
keys and 48 menu intent keys. The remaining 722 bark descriptions and 40
dragon descriptor names have specific runtime-review roles. Two v21
exports matched byte-for-byte and every source value, ID and location
matches v20.

The v22 export assigns roles to 214 previously unclassified managed
occurrences, 178 in game code and 36 in Yarn Spinner Unity. Two v22
exports matched byte-for-byte. Comparing against v21 verified that all
source identities and values match, and the only changes are the new
roles and consumer bindings. See
[managed game consumers](managed-game-consumers-20261109.md).

The v23 export resolves 64 more managed occurrences to exact-preserve
roles and sends both `DragonBark.GetDescription` occurrences of `Idle`
to runtime visibility review. Both v23 exports match byte-for-byte.
Against v22, all source identities, values and locations match. Only
roles and consumers changed. See
[the v23 IL review](managed-game-consumers-20261109.md#v23-method-bound-literals).

The v24 export binds all 53 remaining unclassified game assembly
occurrences to an exact-preserve or explicit review role. Independent
exports match byte-for-byte, and comparison with v23 verifies that
only roles and consumers changed. See
[the v24 IL review](managed-game-consumers-20261109.md#v24-remaining-game-assembly-literals).

The v25 export assigns roles to all 276 remaining Unity UI occurrences
and the two generated resolution format occurrences. Two separate
exports matched byte-for-byte, and comparison against v24 verifies
that only the 278 roles and their consumer bindings changed.
See [the dependency IL review](managed-game-consumers-20261109.md#v25-unity-ui-and-settings-dependencies).

The v26 export assigns roles to the last 540 unclassified literal
loads across the five inspected managed assemblies. Two separate
exports match byte-for-byte. The v25 comparison verifies that only
roles and consumer bindings changed. A visibility-review role is a
provisional classification.
See [the final managed pass](managed-game-consumers-20261109.md#v26-textmeshpro-and-yarn-spinner-unity).

The v27 export preserves all 149 render debugger template records.
The v28 export preserves 582 managed log occurrences based on their
exact sink. Each export reproduced byte-for-byte. Comparison with its
immediate predecessor verified that only the stated roles changed.
See [the debugger binding](legacy-ui-inventory-20261107.md#runtime-debug-entry-points-in-the-two-pinned-builds)
and [the log sink audit](managed-game-consumers-20261109.md#v28-player-log-sinks).

The v29 export preserves 762 internal dragon component fields. The v30
export preserves 28 engine factory template occurrences. The v31 export
preserves six managed bark descriptions and 24 transition reasons. Each
export reproduced byte-for-byte and differs from its predecessor only in
the stated roles. See [the component audit](game-component-strings-20261109.md#v29-metadata-preservation),
[the factory audit](managed-text-sinks-20261107.md#v30-factory-template-follow-up)
and [the bark constructor audit](game-component-strings-20261109.md#v31-managed-bark-arguments).

The inventory is explicitly `provisional-not-translation-ready`: code literals
and many UI values still require visibility review, only five managed assemblies are
included, and runtime-generated text, other resources, exact-preservation
coverage, branch context, special-case decisions and independent review remain
incomplete. Source entries may be internal keys or debug data; no entry was
automatically marked translatable merely because it contains words. Text
baked into textures is excluded by the owner's instruction. The output is
local work containing game source text, not a published deliverable.

Focused tests check both real input families and representative paired/unpaired
records, the macOS-only setting, unique identities, and intended rejection of a
changed pinned input. They do not establish semantic correctness or completeness.
The initial assembly attempt rejected a mistyped expected hash before output;
the corrected hash matched the actual previous source export, and the successful
v2 output above was independently reproduced.

```sh
python localization/assemble_source_inventory.py \
  --work localization/work/source-inventory-20261107 \
  --ui-roles localization/evidence/ui-source-roles-20261107.json \
  --output NEW_WORK_OUTPUT.json
python -m unittest discover -s localization -p 'test_assemble_source_inventory.py'
```
