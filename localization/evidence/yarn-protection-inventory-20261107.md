# Partial Yarn protection inventory

`inventory_yarn_protected.py` derives a source-bound provisional protection set
from the pinned paired Yarn export and the earlier named-target audit. It binds
16 complete source values in both builds: ten adjacent `==`/`---` markers,
five `title:`-like lines, and `line:4b36ea4e`, whose long colon prefix requires
an unresolved presentation solution. It also binds 18 `Ryan: ` or `Conrad: `
prefixes separately from their dialogue bodies. The manifest
`yarn-protected-partial-20261107.json` SHA-256
`bff5f4ce3b270dedf77f31518a3bb75efe72d93617796baeff71cbebb5872be3`
records exact per-build expected values or prefixes, source hashes, IDs and
nodes. It is conservative: whole-value protection does not establish that a
source line is invisible, untranslatable, or irrelevant to the player.

The current provisional source-union recipe binds those manifest rows back to
the source values, marks the 16 whole records
`preserve-exactly-pending-source-role`, and records exact prefixes for the
other 18 without treating their entire dialogue bodies as protected. The v4
working union has SHA-256
`dea3523b082ea0c1a1a87c25315b17fa049364d5e5c2f6bc28f3d1f1bb667bcf`.
The existing locale adapter already enforces the corresponding conservative
guards; this manifest does not relax them or implement a release adapter.

Focused tests compare both-build counts and binding, reject a changed actual
long-colon source after a matching positive, and verify the union's 16 and 18
protected identities. This is not the complete exact-preservation set:
compiled instructions, metadata, other assets and code, markup, substitutions,
runtime identity and player-visible behavior still need their own contracts
and end-to-end verification. A tested text guard cannot establish that the
unresolved long sentence is translated or rendered correctly.

```sh
python localization/inventory_yarn_protected.py \
  localization/work/source-inventory-20261107/yarn-paired-scenes.json \
  localization/evidence/yarn-targets-20261107.json
python -m unittest discover -s localization -p 'test_inventory_yarn_protected.py'
python -m unittest discover -s localization -p 'test_assemble_source_inventory.py'
```
