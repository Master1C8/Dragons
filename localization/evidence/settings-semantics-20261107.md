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
