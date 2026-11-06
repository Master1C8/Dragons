# Local Addressables inventory

`inventory_addressables.py` validates the exact seven-file local `StreamingAssets/aa` inventory and file hashes for each pinned build, along with existing build and schema fingerprints. It opens all three bundles, records object types and AssetBundle container entries, resolves the Locale script using the monoscripts bundle, and round-trips the Locale object exactly with the installed managed schema. The reports `addressables-macos-20261107.json` and `addressables-windows-20261107.json` contain the full scoped evidence and settings. Both were reproduced byte-for-byte.

Each build's three bundles contain respectively one AssetBundle and one MonoScript, one AssetBundle and one MonoBehaviour, and one AssetBundle and nine ComputeShaders. The sole MonoBehaviour is `UnityEngine.Localization.Locale`, container `Assets/Localization/English (en).asset`, object ID `-1847119570001700535`. Its serialized object is byte-identical between builds (SHA-256 `95e47be3836063187e102508ca4a77d886d480f5b2ab083060a03e9496542949`). Its fields identify `en`, display name `English (en)`, empty metadata and no custom formatter; it is locale configuration, not a string table. No separate string table object occurs in these three inspected bundles. This is a static observation, not proof of runtime lookup behavior or absence of dynamically loaded translations.

The binary catalog and its hash are fingerprinted, but the catalog has **not** been decoded. Remote catalogs, runtime discovery, other StreamingAssets including APV `.bytes`, other resource families and dynamically created content remain outside this check. Do not infer complete source coverage or lack of other strings from this result. Image text remains excluded at the owner's instruction.

Reproduce with the pinned dependencies:

```sh
python localization/inventory_addressables.py macos ORIGINAL_MAC_DATA
python localization/inventory_addressables.py windows ORIGINAL_WINDOWS_DATA
python -m unittest discover -s localization -p 'test_*.py'
```

The two real-source controls verify the matching locale and bundle inventories. A separate copied test tree passes first, then a changed catalog byte is rejected at the specific catalog hash guard. The full suite passed 93 tests in `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. Script SHA-256: `24e17ddf53fdefe1c2168615fa1fe84b5cb9a90dfc0ce76752f640a1273cf2cf`; test SHA-256: `2e9c538d952e7f3db23bcbaa07ef53aae495d4994c845590545c9c4e2af70f2c`. Report SHA-256: macOS `7df536ec5440a979052289861ea5ded8cd434ad7735daf2265c97418b442c990`, Windows `1630df87d98e0c977bff38605bb0d34e0cefdea356701432d70f30cbbe02f3f6`.
