# Legacy Unity UI text inventory

`inventory_legacy_ui.py` scans the 17 pinned serialized assets per supported build for the `UnityEngine.UI.Text` component, resolves its GameObject ancestry, and exports source text, object identities and hashes. Each decoded component is checked against its original serialized bytes by a no-op schema round trip. It reports unresolved script references rather than treating them as absence. It uses the existing pinned UnityPy and managed schema inputs and does not modify the game.

Both builds yielded 149 entries, all in `resources.assets`, with no unresolved MonoBehaviour script references in the scanned assets. Every entry has a `DebugUI*` root; its object ID, GameObject ID, complete name ancestry, raw object hash and text match between the two builds. All 149 serialized strings are nonempty, with 32 unique values; 74 are `New Text`. Other examples are `0`, `Foldout` and `Reset`. This supports classifying these as debug UI template candidates, **not** excluding them from the inventory: actual reachability, code replacements, display behavior and translation scope remain unresolved. The scan does not cover other text classes, dynamic strings, Addressables or image text; image text is excluded by the owner's decision.

The full source-bearing exports stay in `localization/work/source-inventory-20261107/`: macOS `legacy-ui-macos.json` SHA-256 `7633ab7cf7622438d7f0ab17c2f58a8ad6190bef255bfb2c177738a2687970c8`, Windows `legacy-ui-windows.json` SHA-256 `ff233b106664f8de1fd9f73123dfad1c43babd037ad16f2721d0e915d83b24db`. A second independent export for each platform matched its first export byte-for-byte. Script SHA-256 `6405f872a9724e9de9a1545606521f8d47917c0ebcc4cf8ab4198c492150675b`; test SHA-256 `9d131b528b5a025589f3d7c0dc725b69dc291481f48393a48bfb9e98229c4d79`.

Reproduce with the pinned dependencies and a new output path:

```sh
python localization/inventory_legacy_ui.py macos ORIGINAL_MAC_DATA --output NEW_MAC_JSON
python localization/inventory_legacy_ui.py windows ORIGINAL_WINDOWS_DATA --output NEW_WINDOWS_JSON
python -m unittest discover -s localization -p 'test_*.py'
```

The tests check hierarchy ordering and malformed hierarchy rejection, matching real source entries and source-byte round trips on both builds, and a deliberately modified macOS resource rejected at its source-hash guard. The complete suite passed 91 tests using `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. Source classification, complete protected-value coverage, estimate, and Russian translation remain pending. The small-window Cyrillic readability risk remains open.

## Runtime debug entry points in the two pinned builds

`DebugUpdater.RuntimeInit` contains only `ret` in both original
render-pipeline libraries. `DebugManager.set_displayRuntimeUI`
can load and instantiate `DebugUICanvas`, and
`DebugUpdater.EnableRuntime` can create the updater and enable
its input actions. The direct managed reference scan over 170
macOS and 172 Windows DLLs found callers only within the same
debug library. It found no direct call to the no-op initializer.

The 17 pinned top-level serialized files in each build were also
checked. All 3,498 macOS and 3,435 Windows MonoBehaviour script
references resolved, and none pointed to `DebugUpdater`. The same
files contained none of the searched exact activation method names.
The 149 legacy UI records remain in the inventory while other
entry points and runtime visibility are assessed.

The source-pinned scans are under
`localization/work/debug-ui-reachability-20261109.1GiwmL/`.

| Report | SHA-256 |
| --- | --- |
| macOS managed callers | `fc1ab9a2ab1352403fb92bafa361f07525a7a33db48a4054e5015efc1bf9a7ef` |
| Windows managed callers | `187ae448bc0ed2795de3c28381a2a8174e4ef3706c08ce37014196ce1991981d` |
| macOS serialized references | `0c671b9b5165d3586338cc68fcb3c29e915b385ed5ee687c48942e5d810a1a68` |
| Windows serialized references | `90c92f7798ace85c57cb2feb04651cacb12ee5f20389203e7a14a32af47cdc3e` |
