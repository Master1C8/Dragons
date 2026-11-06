# Provisional shared source inventory

`assemble_source_inventory.py` combines previously extracted, fingerprinted
source exports for both supported builds into one local, reproducible working
inventory. It checks every input export hash, rejects duplicate identities,
checks paired UI and legacy text hashes, and retains each source occurrence
instead of deduplicating equal strings. Existing source game files are read only
by the earlier pinned extractors; this assembler reads their exports and writes
a new output with exclusive creation.

The current working output `localization/work/source-inventory-20261107/combined-provisional-v3-20261107.json`
has SHA-256 `02fb2a7f8a309023a37d80f9e41d50e289feceef899fa6dd826d90ab523c6e41`.
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
`input-action-preservation-20261107.md`. The earlier v2 output and its
byte-for-byte reproduction are historical under the prior recipe, SHA-256
`6fa14564a75d6e87ecadb700de4234b10e5ab1d1099d404760a5fe0c0e85fbea`.

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
