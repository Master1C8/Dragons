# Settings option semantics

The pinned `Naelstrof.UnityScriptableSettings.dll` files have identical instruction lists for the seven selected methods in the accompanying reports. `SettingDropdown.GetLocalizedDropdowns` returns its `dropdownOptions` array. Its `SetValue(int)` uses the array length to clamp the numeric argument and forwards it to `SettingInt.SetValue`; this inspected method does not compare option text. `SettingFullscreenMode.SetValue` dispatches a four-way switch on the numeric input to `Screen.fullScreenMode`, then delegates the value to the base dropdown setter. `SettingVSync.SetValue` sends a numeric value to `QualitySettings.vSyncCount` and the base setter. Preserve option order, count, indices and unrelated fields: changing only visible wording is a separate operation, not permission to alter those identities.

`SettingResolution.GetLocalizedDropdowns` obtains current values from `Screen.resolutions`, constructs `ScriptableSettingString` values and, on one branch, formats width and height; the selected method does not read the serialized `dropdownOptions` field. `SettingResolution.SetValue` also reads `Screen.resolutions`. This clarifies that the actual displayed resolution list can be generated at runtime and the 42 serialized fallback values are not a complete list of runtime choices. The current adapters conservatively preserve all 42 serialized values exactly; no localization of generated resolution strings is claimed. `ScriptableSettingString.GetLocalizedString` contains both localized-reference and backup-string paths; the existing source scans reject active serialized references before allowing changes.

Source-bound controls check the three indexed `CrouchControl` options, four `WindowMode` options, the 42 protected resolution fields and empty `MasterVolume` label in both builds. `tools/settings-semantics` verifies pinned assembly and Cecil hashes, selected method identities and key IL relationships before exporting complete selected instruction lists. Both reports reproduced byte-for-byte, and a wrong-build settings assembly was rejected at the source-hash guard. The complete suite passed 113 tests using `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. These are static checks of selected methods and serialized inputs; other callers may use strings differently, and actual UI, option display, applied values, persistence and platform behavior still need runtime verification. The prior synthetic Windows Off selection is documented separately in `windows-ui-settings-composition-20261107.md`; it does not establish all options or relaunch persistence.

Fingerprints: tool `a2c57022c98fc2049bb982f27b3a97c8bfb7cce9c8697ecb987ea5444a7d2b98`; tests `7e406d88ae7f8b40a8f6c10d29c63a327488a74d19d2128d380be71a5a287bb8`; macOS report `52e0d3235da84fd9702fbe33c51c800fa42f91767a4c3cc87cfec81326f3a8d5`; Windows report `0430ab56414728bd8ae895b37e33455e99a9b6aa60f0a857fea53602f57030ae`.

Reproduce with pinned Python dependencies and .NET 8 / Mono.Cecil 0.11.6:

```sh
dotnet build localization/tools/settings-semantics/settings-semantics.csproj -p:BaseIntermediateOutputPath=NEW_OBJ_DIR/ -o NEW_BIN_DIR/
dotnet NEW_BIN_DIR/settings-semantics.dll macos ORIGINAL_MAC_DATA/Managed/Naelstrof.UnityScriptableSettings.dll
dotnet NEW_BIN_DIR/settings-semantics.dll windows ORIGINAL_WINDOWS_DATA/Managed/Naelstrof.UnityScriptableSettings.dll
python -m unittest discover -s localization -p 'test_*.py'
```

## v35 settings prefab templates

The source-pinned component scan found one settings spawner in each
of the seven levels on each build. The spawners in each build use the
same four prefab references. The byte-verified manager in `level0`
lists 16 macOS settings and 14 Windows settings. All map to the
dropdown or clamped slider branches of the stock spawner. There is
no registered free-text, unclamped integer or unclamped float
setting in either inspected menu. Its three group headings are
separate from the manager's settings list.

The inspected spawner assigns labels from the settings data and
slider bounds from the setting values. It populates the dropdown
option list from the setting and selects the saved index. The stock
TMP item clone replaces `Option A` with that item's option data
before returning to the list builder. The text-input placeholder
and its zero-width text belong to the unused input branch for these
builds.

The isolated players opened Options with the original button using
a virtual pointer. macOS created eight dropdowns, eight sliders and
three titles. Windows under CrossOver created six dropdowns, eight
sliders and three titles. Neither created a text input. The complete
runtime registry matched the two serialized manager lists. Read-back
confirmed actual labels, captions and numeric bounds. Some slider
amount components still contained the numeric prefab value `32`;
others held real values. The observer did not establish the pixel
visibility or semantic correctness of the stale amount. These
numeric values are preserved exactly. The run did not expand an
option list, change settings or exercise persistence.

All 15 macOS and 29 Windows samples showed no on-screen window or
foreground ownership. Both test processes exited and the checked
original profiles remained unchanged. The Windows copy used
Direct3D 11 under CrossOver. The runtime check used existing source
settings wording, not a Russian settings build.

The source recipe now preserves 11 paired settings prefab fields,
while retaining the separate translatable setting values. Two v35
exports matched byte-for-byte. Only these 11 roles differ from v34.

Static artifacts are under `localization/work/settings-prefab-flow-20261109.v8WmsL/`.
Runtime artifacts are under `localization/work/settings-stock-runtime-20261109.pOHuxf/`.

| Artifact | SHA-256 |
| --- | --- |
| macOS manager source scan | `5824c77f5083216e17f0e893a9e359e52e3dcd32b4ff63b4e0db7477ad83b319` |
| Windows manager source scan | `bf2a57407083eb2f21377a561534ea15807ad2e82ff07db964beec776e58357e` |
| macOS managed flow | `491d5d86b0aa34f54f187f29295421918b8a4f610da0a011506f1d31a8742e51` |
| Windows managed flow | `b8f5579676966b2473d2c24efc9d78141d2eb271db453ee63370beeafc3ce877` |
| Runtime companion source | `8c1ed835d78f9a2e02757a0ed84cdfbf37ec2ddbe708642e85ed558f208d652d` |
| macOS player log | `6baf0e3a5e9e5e089157b42394348c23dc5b3fff37eb6161a3b310449c6c9534` |
| macOS observer receipt | `2e9a48efe8a9813710f853c7498e394df75f2f8f568a600ed130a41b2dcf003c` |
| Windows player log | `97c130bc0d4115d7aa139fb1b9667b7996314f7a0d357717d8dc1a299aec5b74` |
| Windows observer receipt | `a82916f24976b0113b7c9b7491dda80d078f94c7a38ff3392fddc7445bddb10e` |
