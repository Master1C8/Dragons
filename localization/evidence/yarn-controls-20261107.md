# Yarn substitutions and digit preservation

`inventory_yarn_controls.py` scans the source-pinned Yarn tables and instruction bindings in both builds. Each of the 1,839 line and option instructions reports a substitution count of zero. This describes the inspected compiled operands only; it does not prove that runtime markup, commands, dynamic strings or other resources have no substitutions. The two machine-readable reports bind each result to source and program fingerprints and reproduced byte-for-byte.

There are 22 source IDs per build containing ASCII digit runs outside recognized markup. Eighteen are numbered `Start` test lines; the other four include Alexander's question about 7, two occurrences of franchise number 223 and a title containing 2. These are source occurrences, not proof of reachability or translation scope. Digits inside `<size=70%>` and other recognized tags remain part of the separately protected markup and are not treated as visible numeric runs.

`dialogue_locale.py` now compares the multiset of visible ASCII digit runs in each supplied Russian Yarn entry with its exact source. It rejects additions, omissions or changes, including spelling a source digit out; retaining the digit passes. The check is scoped to Russian Yarn entries, not settings or other locales. It is intentionally conservative and does not prove semantic correctness, preserve spelled-out numbers, decimal relationships, numeric meaning, source classification, or a complete preserve-exactly contract. A legitimate case needing a different representation requires an explicit reviewed mapping rather than silently bypassing the check.

The initial full-suite run exposed four Windows probe failures: their synthetic Yarn fixture appended `123` to a source line containing only `223`. The fixtures were changed to retain `223` without the extra number, preserving the original purpose of their asset and failure-boundary checks. Historical synthetic locale files that add digits may likewise be rejected by the new guard; existing evidence and originals were not rewritten.

Focused tests cover matching digits, changed, omitted and added digits, unchanged markup and the non-Yarn boundary. Real-source controls check the zero-substitution counts and important source IDs in both builds. The corrected full suite passed 97 tests with `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. Reproduce with the pinned dependencies:

```sh
python localization/inventory_yarn_controls.py macos ORIGINAL_MAC_DATA
python localization/inventory_yarn_controls.py windows ORIGINAL_WINDOWS_DATA
python -m unittest discover -s localization -p 'test_*.py'
```

Fingerprints: adapter `7e53430f6d5325315dc357ed7e659bd2ac1870472e8a0a7163998e0437e116b0`; inventory `22b88cfa3741b3eda98a239a7eaee475175b617dc3ee952fe1f46c745e2fe387`; macOS report `01a0c5d01c2cdc2af9440fccf94a2cf71bfbffeadb5a28fc6f254ebf1406acca`; Windows report `3e4af4ac77b68d520d959da698cff28acf4487a07436362cf7cf71db3fe7ebc7`.
