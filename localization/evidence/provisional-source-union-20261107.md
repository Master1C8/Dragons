# Provisional shared source inventory

`assemble_source_inventory.py` combines previously extracted, fingerprinted
source exports for both supported builds into one local, reproducible working
inventory. It checks every input export hash, rejects duplicate identities,
checks paired UI and legacy text hashes, and retains each source occurrence
instead of deduplicating equal strings. Existing source game files are read only
by the earlier pinned extractors; this assembler reads their exports and writes
a new output with exclusive creation.

The current working output `localization/work/source-inventory-20261107/combined-provisional-v5-20261107.json`
has SHA-256 `bb8216c3d1d88150afb0800110bb12a50642ac731b4e30c3985a94d33b04451e`.
Its 4,048 records comprise
1,839 Yarn line/option IDs, 162 paired or Windows-only known TMP UI fields,
80 paired or macOS-only known settings fields, 149 paired legacy UI fields,
and 1,818 literal-load occurrences from three inspected managed assemblies
across the two builds. Managed occurrences are deliberately **not paired**
across builds, because instruction ordinals can mean different things. The
counts are source records, not 4,048 visible phrases, completed translations,
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

The inventory is explicitly `provisional-not-translation-ready`: code literals
and many UI values remain unclassified, only three managed assemblies are
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
