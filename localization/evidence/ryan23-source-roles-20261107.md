# Ryan's second and third visit source roles

The coordinator read the paired-build source lines and choices in
`Ryan_2_Outro` (38 IDs), `Ryan_2_intro` (20), `Ryan_2_required` (23),
`Ryan_3_Outro` (16), `Ryan_3_intro` (17), `Ryan_3_required` (17), and
`Ryan_3_wont_use_mount` (2). The 133 IDs and source-function roles are stored
in `localization/yarn_roles_ryan23.json`, SHA-256
`82f0dd640b385abeb4a06cec54cc267c61ac60d790035d55a72a3b4a0b7669e1`,
bound to paired source export SHA-256
`52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995`.

The manifest distinguishes dialogue, player choices and two standalone
ellipsis beats. It records contextual reminders for the question-about-a-
question exchange, relationship discussion, separate choices and replies,
Yip callback and markup. The source's references to a girlfriend and a partner
must not be merged into a confidently named identity without evidence. The
known grammatical and address decisions in the glossary still govern Russian
wording. These roles are preliminary: they do not establish runtime visibility,
final translation choices, independent editorial acceptance or a full source
denominator. The related special-scene and route registries remain open.

The v9 union checks the exact ID/kind set for these nodes, requires each
punctuation role to match the source ellipsis in both builds, and keeps them
disjoint from earlier source-control bindings. Five focused tests passed,
including a punctuation-misclassification control. Two generated v9 inventories
were byte-identical; comparing all records to v8 found only the 133 intended
role changes. No actual game-text translation or source game modification was
performed.

```sh
python -m unittest discover -s localization -p test_assemble_source_inventory.py -v
python localization/assemble_source_inventory.py --work localization/work/source-inventory-20261107 --ui-roles localization/evidence/ui-source-roles-20261107.json --output FRESH_WORK_OUTPUT.json
```
