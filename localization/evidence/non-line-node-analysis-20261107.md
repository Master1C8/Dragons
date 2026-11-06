# Compiled Yarn nodes without line instructions

`inventory_non_line_nodes.py` parses both original, source-pinned compiled
programs and inventories nodes containing neither `RunLine` nor `AddOption`.
Each build has 11 of these nodes among 195, with identical node hashes,
instruction counts and named-transfer records between the builds. They are
listed with exact node hashes, opcode counts and 25 transfer sites in
`non-line-nodes-20261107.json`, SHA-256
`b2d4683b8eb05bcfcbc425cfc7c6f2589c7abeeb190240172c8776ff736ba703`.

The coordinator read the decoded instruction listings for these 11 nodes.
Four food nodes increment `$food_number`, use `AttachItem` and transfer to
their corresponding food-dialogue nodes. Four relationship-routing nodes
inspect the three romance variables and transfer to different dialogue nodes.
Two cleanliness-routing nodes compare `$cleanEvaluation` to source values;
one of their transfers names `Alexander_Done`, which is absent from the
extracted node map and was already recorded in
`yarn-missing-targets-20261107.md`. `Declarations` contains no line or option
instruction. These values and node names are program controls, not phrases to
translate; the exact program bytes are already compared by the separate
Yarn-only preservation check. None of this establishes runtime reachability,
correct behavior, in-game failure, all dynamic targets, or loaded programs.

The name "without line instructions" applies only inside each individual
compiled node: named transfers can and do lead to nodes containing player-facing
text. Excluding these nodes from a text-string count must not remove their
dependencies or treat their behavior as irrelevant. The 11-node inventory
does not close the complete preserve-exactly contract across other assets and
code, the classification of 1,839 Yarn source values, or editorial decisions.

Focused tests use a matching positive source graph, a missing target, a changed
transfer operand rejected at the relevant parsing boundary, and both actual
source builds. The check does not execute the Yarn VM. Reproduce with
`inventory_non_line_nodes.py --macos-data ORIGINAL_MAC_DATA --windows-data ORIGINAL_WINDOWS_DATA`
and `python -m unittest discover -s localization -p 'test_inventory_non_line_nodes.py'`.
