# Provisional shared source inventory

`assemble_source_inventory.py` combines previously extracted, fingerprinted
source exports for both supported builds into one local, reproducible working
inventory. It checks every input export hash, rejects duplicate identities,
checks paired UI and legacy text hashes, and retains each source occurrence
instead of deduplicating equal strings. Existing source game files are read only
by the earlier pinned extractors; this assembler reads their exports and writes
a new output with exclusive creation.

The current working output `localization/work/source-inventory-20261107/combined-provisional-v11-20261109.json`
has SHA-256 `23cc5c0061bb9c83d6d62583924ccc6c334889dfab6f08f8707e3b87218cd838`.
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
