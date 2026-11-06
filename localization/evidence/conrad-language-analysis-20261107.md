# Conrad language-dependent source groups

A coordinator reading of Conrad-named macOS Yarn text identified three groups requiring coordinated target wording: the physical/sexual senses of “dirty” with progressively shrinking markup, a professional/expertise exchange with a delayed sexual punchline, and a self-invented nickname based on Conrad's initial. The full affected node IDs, branch controls, invariants, dependencies, acceptance scenarios and pending status are recorded in `special-scenes-conrad-language-20261107.json` SHA-256 `17f03f837652ee7e0fb110dc5b23155a8c833e1b779934fbc9dfe2b7d2b732fc`. No Russian wording or independent editorial acceptance is claimed. The owner-selected neutral player wording applies; the approved Russian character name needs to be considered when deciding the nickname.

`inventory_conrad_language.py` pins both source programs and runtime schema, extracts all 41 line/option IDs from the three complete nodes, checks 11 exact option destinations and binds a previous-activity variable read and write. The node bytes and all selected source hashes match between builds. `conrad-language-groups-20261107.json` SHA-256 `54743814ab62a4f140db3ad3bfb93415dd0efe2084cdd98dc7f29844b2ea8770` reproduced byte-for-byte; the registry's lists and source inventory fingerprint were checked against both build records. Tool SHA-256 `fe7826c0be27badb899049eb6a72451faad535c7ac51d449e4c18b0146b41b60`; test SHA-256 `5fc5fe18824772b8297c8566eadee3e259ef5af5b89f47541dcaac46c13aa6cb`.

The focused tests verify both real source groups and reject an altered option destination with a matching positive control. The complete suite passed 115 tests with `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. They do not execute a game branch or certify visibility, rendering, all state combinations, the whole source inventory, or an exhaustive search for linguistic cases. Conditions and commands remain source controls; texture text is outside this localization. The complete glossary and source gates and special-scene decisions remain open.

Reproduce using pinned dependencies:

```sh
python localization/inventory_conrad_language.py --macos-data ORIGINAL_MAC_DATA --windows-data ORIGINAL_WINDOWS_DATA
python -m unittest discover -s localization -p 'test_*.py'
```
