# Ryan language-dependent source groups

A coordinator reading of Ryan-named macOS Yarn scenes identified four groups requiring coordinated wording: his intentionally distorted speech while carrying a basket, a salmon preference followed by a dragon self-correction, three movie-title choices with separate reactions, and a repeated euphemism about Conrad's height across two relationship paths. A fifth registered source finding is an `$isEditor`-conditioned prompt whose yes/no choices write opposite values to `$suggested_ryan_to_conrad`. It is not excluded from the shared source inventory merely because it appears to be an editor-oriented prompt. The registry `special-scenes-ryan-language-20261107.json` SHA-256 `6209639693f1c03ea71bd49a7da0e994ecd8262b04a0e26223f6320be1f8a14d` records exact source IDs, grouped context, invariants, candidate adaptation routes and outstanding checks.

The three movie titles and Yip concept already have source glossary entries; their existing publication is not proof of standard-localization editorial readiness. The two height spans intersect the existing romance-route registry. Choose any Russian wording only after the source and glossary gates and review all related uses together. This checkpoint contains no approved target wording and no independent editorial review. Actual branch reachability, presentation, basket visuals and dynamically changed state remain unverified.

`inventory_ryan_language.py` binds five selected groups to both source builds and exact node hashes. It verifies 21 option destinations and the editor-prompt condition and opposite state writes. The groups contain 65 line/option occurrences, including six shared context IDs counted in two overlapping groups. All selected IDs and controls match across builds; three height-span source strings differ in apostrophe spelling. The per-build source hashes preserve those differences. `ryan-language-groups-20261107.json` SHA-256 `cf1f5a203bfa2f6e41357dbb2799fee702e3494412ba53a598d5eae6181b0891` reproduced byte-for-byte, and registry ID lists and source-report fingerprint were checked against both builds. Tool SHA-256 `76f026b250ecf1c4423404c5dfb161bc52ce1d8c60289396b7d0bd5f70fd60d9`; tests `8973626974ffa28d97fc19bf6cd28283d0625b98b6a1e09a9ba023f8dc55296a`.

Focused tests check both pinned sources, expected differences and a changed destination with a matching positive control. The complete suite passed 117 tests with `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. They do not execute the game or establish full discovery. Other nodes, resource types, source controls, runtime checks and localization decisions remain open. Texture text is excluded by the owner's instruction.

Reproduce using pinned dependencies:

```sh
python localization/inventory_ryan_language.py --macos-data ORIGINAL_MAC_DATA --windows-data ORIGINAL_WINDOWS_DATA
python -m unittest discover -s localization -p 'test_*.py'
```
