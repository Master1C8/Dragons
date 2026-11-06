# Combined Yarn and UI asset preservation

`verify_combined_yarn_ui.py` independently inspects a supplied candidate
`sharedassets1.assets` against the pinned original build and exact source-bound
locale files. It reconstructs expected Yarn object bytes from the original
ordered IDs, localized values and metadata; it separately reconstructs expected
serialized UI objects. It checks locale identity, rejects overlapping object
identities, and compares the complete source and candidate object inventories
and each object's raw bytes. Every object not explicitly authorized by the
locale files, including the compiled Yarn project, must match the original.
Yarn-only and UI-only inputs are supported; at least one is required.

The verifier is separate from the builders and reads their output rather than
their internal changed-object maps. It deliberately reuses the project's pinned
UnityPy scanner and locale parser/encoder; it is not an independent parser
implementation or a comparison of every file-level header and metadata byte.
It covers this one shared asset, not settings in `sharedassets0.assets`, code,
other files, full source classification, translation meaning, runtime behavior,
player saves, installation or restoration.

Two focused tests passed against both original local builds. Each creates an
isolated synthetic candidate using the platform's existing asset operations,
then verifies one Yarn and one UI replacement. Negative controls omit the UI
authorization, provide different but structurally valid UI and Yarn values,
change the requested locale, and alter a byte of the compiled project object;
each is rejected at its intended boundary. An additional control rejects a
request with neither locale input. The temporary candidates are removed by the
test; no original game files are changed. The tests do not execute the game.

Verifier SHA-256 `617c6729c84986d55cb61161a5834b2e4083d82f1fe2c615315347e9afce8e37`;
test SHA-256 `5740655e78d760aeea56b10a6e28c052f07b688b2433675ee5cb65c41cf85b8f`.

```sh
python localization/verify_combined_yarn_ui.py macos ORIGINAL_DATA CANDIDATE --locale ru --yarn-locale YARN_JSON --ui-locale UI_JSON
python localization/verify_combined_yarn_ui.py windows ORIGINAL_DATA CANDIDATE --locale ru --yarn-locale YARN_JSON --ui-locale UI_JSON
python -m unittest discover -s localization -p test_verify_combined_yarn_ui.py -v
```

Omit one locale argument only if that family is unchanged in the candidate.
This extends, rather than retrospectively changing, the Yarn-only evidence in
`yarn-preservation-check-20261107.md`.
