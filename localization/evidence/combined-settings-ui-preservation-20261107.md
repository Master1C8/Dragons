# Combined settings and UI asset preservation

`verify_combined_settings_ui.py` compares a candidate `sharedassets0.assets`
to either pinned original build and the exact supplied settings and UI locale
files. It checks the build identity, source asset, scripts and schema inputs;
reconstructs every authorized setting tree and UI text object; and compares
the complete candidate Unity object inventory and raw object bytes with those
expected values. Changed setting trees are also decoded and compared in full.
Protected empty fields and serialized resolution options cannot be submitted
as translation keys. Other fields in changed settings objects, including option
order and indices, must remain exact. Settings-only and UI-only checks are
supported; an input for at least one family is required.

The verification is separate from the asset builders' in-memory change maps,
but reuses their pinned UnityPy schema and locale parsing/serialization logic.
It checks raw Unity objects, not every file-level header byte, and does not
establish runtime visibility, the dynamically generated resolution list,
applied setting behavior, semantic correctness or a full installation. Numeric
index handling and the scope of static findings are documented separately in
`settings-semantics-20261107.md`.

Two focused tests passed on both locally available original builds. Each built
a separate synthetic asset with a changed option and UI field and then checked
it. Negative controls rejected missing UI authorization, different UI and
settings text, a mismatched locale, an attempted protected resolution change,
and one corrupted unrelated object. A separate control rejects no inputs.
The test outputs are temporary; original assets are read only. Neither game
was launched for these tests.

Verifier SHA-256 `6f6987f59b4a9fdbced546e80bb995419b0ce02074e12234ccefdb0a076a847b`;
test SHA-256 `ed17ed324423ecb15d142ae97059da030dd3b509417953a6f88065d6698f83a8`.

```sh
python localization/verify_combined_settings_ui.py macos ORIGINAL_DATA CANDIDATE --locale ru --settings-locale SETTINGS_JSON --ui-locale UI_JSON
python localization/verify_combined_settings_ui.py windows ORIGINAL_DATA CANDIDATE --locale ru --settings-locale SETTINGS_JSON --ui-locale UI_JSON
python -m unittest discover -s localization -p test_verify_combined_settings_ui.py -v
```
