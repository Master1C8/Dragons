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

## v36 objective entry-path audit

The complete 170 macOS and 172 Windows root managed inventories
match the earlier caller fingerprints. The follow-up checked
subclasses, field types, direct methods, generic method operands,
type operands and exact class-name literals. The only instantiation
reference is `ObjectiveManager.AddObjective` cloning an
`ObjectiveDisplay` from its own serialized field. No stock managed
reference creates an `ObjectiveManager`, and neither build has a
subclass of the manager or display.

The earlier component scan found neither component in the 17
serialized assets. The follow-up rehashed all 31 pinned
`StreamingAssets` files per build and inspected the 14 decoded
objects in the three Unity bundles. The single MonoBehaviour is
an ordinary `UnityEngine.Localization.Locale`. There is no bundled
GameObject, scene or objective component.

The combined evidence establishes no stock entry to the inspected
objective display. The v36 recipe preserves the four literals on
each build, with their underlying setter consumers retained for
future review. Arbitrary reflection, external mods and a runtime
test of a deliberately created objective display are outside the
scope of this decision.

Scans are in `localization/work/objective-entry-flow-20261109.eF6gON/`.

| Artifact | SHA-256 |
| --- | --- |
| macOS managed flow | `2aefd3c10b23a319e9c1c8f7eb40e4415e3ae741efa725f59815e35f489a1056` |
| Windows managed flow | `ae129d40b7cd10ee99eda233743983184f7d6619955d067633cb87e03496b2d1` |
| macOS decoded bundle types | `fce5a8415eda83c50402c587a77ede2787857248cc3d66c0995a313772f96353` |
| Windows decoded bundle types | `454f86dea1484565cdbc71a59638b578bad1a80b0851c38139571391031350b3` |
