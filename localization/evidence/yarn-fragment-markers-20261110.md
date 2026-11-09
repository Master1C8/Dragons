# Embedded Yarn fragment delimiters

The [paired control-flow receipt](yarn-fragment-markers-20261110.json)
binds the 15 preserved delimiter IDs to five original host nodes and the
existing repaired programs. The audit loads the pinned original assets and
Yarn VM hashes for both platforms, reproduces the repair and verifies that
the original host nodes are byte-identical in the repaired program.

Each block begins after a non-fallthrough instruction. In
`Alexander_Outro` it is Yarn's stop at instruction 28. The other four
hosts transfer by name before their delimiters. The check bounds all
local jump, conditional and option targets before the first marker.
The one stack-based jump uses the checked `ShowOptions`, conditional
jump and pop sequence. Its selected target comes from the preceding
bounded option destinations. The audit rejects a jump into that
sequence after `ShowOptions`. It checks that each repaired node
starts at the exact suffix after the delimiters and that the only
marker references in the repaired program are the original
`RunLine` instructions in those five hosts.

The marker blocks cannot execute from a node entry through these
pinned programs. The conclusion concerns the 15 marker occurrences.
The dialogue suffixes still belong to the translation scope, including
ones with limited ordinary gameplay evidence. No game or texture
asset was changed by the audit.

The v42 source inventory assigns the 15 values the
`preserve-exactly-unreachable-yarn-fragment-marker` role and records the
exact source values. The paired scope retains 1,823 dialogue inputs,
one special display input and 15 exact-only IDs. No ordinary translation
is accepted by this audit.

| Artifact | SHA-256 |
| --- | --- |
| Marker receipt | `b7200b84ff6efe79bf44e64964ce4d39a60eec5a35a091287179a1c496643c1e` |
| `combined-provisional-v42-20261110.json` | `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d` |
| `yarn-scope-v42.json` | `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30` |

Reproduce with `audit_yarn_fragment_markers.py` using both original Data
directories, then use `assemble_source_inventory.py` and
`inventory_yarn_scope.py` with fresh outputs. The inventory is under
`localization/work/source-inventory-20261107/`. The scope and repeated
exports are under `localization/work/yarn-markers-20261110.ridbPA/`.
The paired proof and inventory reproduced byte-for-byte. A matching
positive control accepted a bounded local target. Pointing the same
jump at the first marker was rejected at the branch bound.

Both non-Yarn structural coverage controls matched their v41 results
after excluding the new inventory hash. Rebuilding the synthetic
Windows ZIP with the same locale inputs produced the same 12 payload
file hashes. Only the two scope hashes in its manifest changed. The
new archive SHA-256 is
`bc9c97240c805f589137182733b8418a74c937b87c4805e1ab35e9b5aa52f976`.
All 197 project tests passed with the paired build tools enabled.
