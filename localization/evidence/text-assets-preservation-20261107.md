# TextAsset inventory and preservation

The source-pinned inventory scans 17 serialized files per build. Each contains four TextAsset objects, all in `resources.assets`: `PerformanceTestRunSettings` (#19), `LineBreaking Leading Characters` (#20), `PerformanceTestRunInfo` (#21), and `LineBreaking Following Characters` (#22). Their individual hashes and provisional roles are recorded in `text-assets-macos-20261107.json` and `text-assets-windows-20261107.json`. The payloads match between builds except for `PerformanceTestRunInfo`. All four are conservatively marked preserve-exactly; diagnostic consumers have not been fully traced.

The serialized TMP Settings object (#1388) points to #20 and #22 for leading and following characters, respectively, and its modern Hangul line-breaking mode is disabled in both builds. Its source schema round-trips byte-for-byte. These references do not establish runtime use or rendered behavior.

`verify_text_assets.py` compares the identity and raw bytes of every TextAsset found in those 17 source and output assets, and checks the two TMP references and line-breaking mode. It verifies the source build and asset hashes first and requires a separate output directory. It does not verify every TMP setting, other protected values, dynamic or managed text, all possible resources, rendering, runtime behavior, or packaging.

The check passed on the existing synthetic macOS `DragNWash-MissingTargetBackgroundProbe` copy and Windows `WindowsSettingsCombinedGame` copy: four exact objects, unchanged references and mode in each. These are diagnostic copies, not finished localization packages. No game was launched or original modified for this check.

Three inventory parsing tests and five verifier tests cover positive controls and altered payload, reference, and mode rejection against real pinned sources. The complete suite passed 88 tests with the existing `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python` environment. An attempt with `/private/tmp/dragnwash-unitypy-venv/bin/python` could not run the suite because that environment lacks `fontTools`; it is not a product failure.

Reproduce using an environment with the dependencies in `localization/font_probe_requirements.txt`:

```sh
python localization/inventory_text_assets.py PLATFORM ORIGINAL_DATA
python localization/verify_text_assets.py PLATFORM ORIGINAL_DATA SEPARATE_COPY_DATA
python -m unittest discover -s localization -p 'test_*.py'
```

`PLATFORM` is `macos` or `windows`. Inventory script SHA-256: `bb1449e99bed20c7cd344df11b4401d6cfd9f67f59e25f7a28174fc5b7294c11`; verifier SHA-256: `f10f6546bcaf5447e4fc18c8fcbf8e0a783f435571c4f1ecb8ad95de592c6016`. The inventory remains incomplete and ordinary Russian translation has not started.
