# Yarn source instruction export

`export_yarn_instructions.py` makes a source-bound, node-ordered review export for each pinned build. It includes all compiled node bytes, every instruction's original encoded bytes and individual protobuf wire operands, and source text attached to each verified `RunLine` or `AddOption` ID. Non-node program fields are represented with their wire values. The pinned game build, project, localization table and Yarn runtime hashes are checked first; line IDs must exactly match the source table and verified node/index mapping. The exporter creates only a new output file.

Each build has 195 nodes and 8,393 instructions, including 1,261 line and 578 option instructions. All 1,839 text IDs are bound exactly once. The instruction type counts match across builds; the encoded bytes differ in three nodes: `Alexander_2_intro`, `Conrad_finished_mount_3`, and `Ryan_3_required`. Equal counts do not mean equal behavior. Earlier source comparison found 25 English value differences; review the matching platform export rather than silently substituting another build's wording.

The exports retain exact control bytes and expose printable UTF-8 operands for human investigation, but numeric fields are not a complete semantic disassembly. A text ID's presence is not proof of reachability or display. Conditions, stack semantics, dynamic substitutions, command consumers, special scenes and non-Yarn sources still need review. This is not the complete shared inventory, a preserve-exactly validator, or a translated corpus.

Source-bearing outputs stay in `localization/work/source-inventory-20261107/`: `yarn-instructions-macos.json` SHA-256 `3e0acd1a2f25811e380de5743e0913535470d931301cc9bc40f5a3c897d73e18` and `yarn-instructions-windows.json` SHA-256 `13d34e111e48fcd80105f419f1072717ddc11659300474410f52e7839b88522b`. Both were regenerated and compared byte-for-byte. Tool SHA-256 `14cd9d797dfaac90919edc5028053e5d0b764a4263c6a3c9a9d90b529d46987b`; test SHA-256 `89a7fb6bd0b280a86003924e443205836de59ec82709126c99868604b1b336c0`.

Reproduce with the pinned dependencies and fresh output paths:

```sh
python localization/export_yarn_instructions.py macos ORIGINAL_MAC_DATA --output NEW_MAC_JSON
python localization/export_yarn_instructions.py windows ORIGINAL_WINDOWS_DATA --output NEW_WINDOWS_JSON
python -m unittest discover -s localization -p 'test_*.py'
```

Tests compare every exported node byte and instruction byte against both actual pinned programs and every attached text value against its source table. Operand tests cover UTF-8, non-UTF-8 and unsigned numeric representations. The complete suite passed 95 tests with `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. The output is a review aid; no semantic or runtime test is implied.
