# Opening and first-Ryan source roles

The coordinator read both-build source values and instruction kinds for six
nodes in the source-pinned paired Yarn export: `Start` (24 IDs),
`Ryan_1_PhoneTutorial` (15), `Ryan_1_intro` (17), `Ryan_1_required` (9),
`Ryan_1_nag` (2), and `Ryan_1_Outro` (12). The 79 IDs and their manually
assigned source-function roles are in `localization/yarn_roles_opening.json`,
SHA-256 `ad01a97ccffb6ea648bd5df90d42416e3c528f649f3fd4a5b5881a3c6a322025`.
The manifest binds paired export SHA-256
`52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995`.

The first group is test-script dialogue and choices, including numbered sample
lines; `Start` remains a configured runner node and is not assumed unreachable.
The phone and first-Ryan material is classified as dialogue, player choices,
or standalone punctuation beats. The classification retains distinct option
IDs, instruction indices, destination and condition data in the existing union;
it does not itself prove reachability, player visibility, finalized punctuation,
or which translated wording is appropriate. Both source builds are retained,
including their different spellings in several phone and introduction lines.
The franchise number, source markup, option branches and sound-linked Yip
callback remain subject to their existing source-bound controls and special-case
review. A source role is not an editorial or translation approval.

The v8 union reconciles the exact ID set and instruction kinds for all six nodes
and rejects duplicate IDs, incorrect kind, missing coverage, mismatched source
fingerprint and overlap with earlier protected Yarn bindings. Four focused tests
passed, including altered-kind and missing-ID controls. Two independent v8
assemblies were byte-identical; comparison with v6 verified exactly 79 intended
role changes and no other record changes. Overall source classification,
special-scene decisions, glossary readiness and ordinary game-text translation
remain incomplete. No source game file was modified.

```sh
python -m unittest discover -s localization -p test_assemble_source_inventory.py -v
python localization/assemble_source_inventory.py --work localization/work/source-inventory-20261107 --ui-roles localization/evidence/ui-source-roles-20261107.json --output FRESH_WORK_OUTPUT.json
```
