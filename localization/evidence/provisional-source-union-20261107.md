# Provisional shared source inventory

`assemble_source_inventory.py` combines previously extracted, fingerprinted
source exports for both supported builds into one local, reproducible working
inventory. It checks every input export hash, rejects duplicate identities,
checks paired UI and legacy text hashes, and retains each source occurrence
instead of deduplicating equal strings. Existing source game files are read only
by the earlier pinned extractors; this assembler reads their exports and writes
a new output with exclusive creation.

The current working output `localization/work/source-inventory-20261107/combined-provisional-v15-20261109.json`
has SHA-256 `9e271efe1e795a2e86a413f732e2c65e0042f5dfd708572b320de59c80e6956d`.
Its 5,204 records comprise
1,839 Yarn line/option IDs, 162 paired or Windows-only known TMP UI fields,
80 paired or macOS-only known settings fields, 149 paired legacy UI fields,
and 2,974 literal-load occurrences from five inspected managed assemblies
across the two builds. Managed occurrences are deliberately **not paired**
across builds, because instruction ordinals can mean different things. The
counts are source records, not 5,204 visible phrases, completed translations,
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

The inventory is explicitly `provisional-not-translation-ready`: code literals
and many UI values remain unclassified, only five managed assemblies are
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
