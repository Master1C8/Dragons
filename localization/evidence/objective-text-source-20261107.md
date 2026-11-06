# Objective text in managed code

The pinned `Assembly-CSharp.dll` in each build contains four source strings returned by `Objective.GetName` and three direct overrides: `DEFAULT`, `DIRTY`, `SOAPY`, and `TOO BRIGHT`. `ObjectiveManager.Start` statically constructs the latter three objective types. `ObjectiveDisplay.SetObjective` calls `Objective.GetName` virtually and passes the result directly to `TMPro.TMP_Text.set_text`; its target field is declared as `TMPro.TextMeshPro`. This is a previously unclassified potential display-text path outside the Yarn and serialized UGUI text adapters. These four values are source candidates, not yet accepted visible-text or translation counts.

The 17 pinned serialized files per build contain no MonoBehaviour whose script identity is `ObjectiveDisplay`, `ObjectiveManager`, or `TMPro.TextMeshPro`; all MonoBehaviour script references in this scoped scan resolved. The absence is limited to those exact classes and files. It does not rule out dynamic object creation, other bundles, subclasses, code paths or runtime presentation. No conclusion about actual visibility or whether to exclude these strings is justified yet. A future code-localization adapter, if needed, must target the actual consumers and be checked on the delivered runtime; the current asset-only adapters do not translate these literals.

`tools/objective-source` verifies pinned assembly/Cecil hashes, exact constant-return methods, constructor identities, the target field type and the virtual getter-to-TMP setter chain for both builds. A mismatched build was rejected at the assembly hash guard. `inventory_objective_components.py` independently inventories the three exact serialized script identities against the pinned assets. Four machine-readable reports were reproduced byte-for-byte. Matching and nonmatching script identities and the real scoped sources are covered by tests; the complete suite passed 104 tests using `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. Runtime visibility was not tested.

Fingerprints: managed tool `56783d12d107bd5c6d4f1f010a9d98952533fe9eeb3c4aad4d2abe0ba9616c2d`; component scanner `0d4b6964423d9feb0f9ece2fda2705acb894275791f9c326a2e1f728a80c40ed`; code reports macOS `72ec67ad4136691a8fe1e60a32fcfaf03d73f97fdd98d476ccb2fe41bd74fce7`, Windows `f5b037d22d5963fc46922b39ba02e0e31c4927642b414d64145f124cdddda0fb`; component reports macOS `448e1b73f8cb1016b2ce3a55afdc93f0e2b50367c171dd623b1f6cc03a4a658a`, Windows `5f41cac8437f25dd119816887979ae3c59f6ed65efee41738987be58811298b2`.

Reproduce with pinned Python dependencies and .NET 8 / Mono.Cecil 0.11.6:

```sh
dotnet build localization/tools/objective-source/objective-source.csproj -p:BaseIntermediateOutputPath=NEW_OBJ_DIR/ -o NEW_BIN_DIR/
dotnet NEW_BIN_DIR/objective-source.dll macos ORIGINAL_MAC_DATA/Managed/Assembly-CSharp.dll
dotnet NEW_BIN_DIR/objective-source.dll windows ORIGINAL_WINDOWS_DATA/Managed/Assembly-CSharp.dll
python localization/inventory_objective_components.py macos ORIGINAL_MAC_DATA
python localization/inventory_objective_components.py windows ORIGINAL_WINDOWS_DATA
python -m unittest discover -s localization -p 'test_*.py'
```
