# Delete-save wording and transition reason

In each pinned build, `MenuSlotsNew.OnEvent` contains three `Delete Save?` literals. Each is passed as the second argument to `MenuResponseTransition`, alongside the destination identity `Menu_DeleteSave` and a `MenuTransitionDataLevelLoad` object. The constructor stores that second argument in its `reason` field. In the inspected `Assembly-CSharp.dll`, direct field references consist of the constructor store and `MenuResponseTransition.GetReason` load, and there are no direct method references named `GetReason`. These observations are static and scoped to this one assembly; reflection, other assemblies and runtime behavior are not ruled out. Conservatively preserve the code literals pending full consumer classification; do not infer from their English wording that they are labels.

Separately, the pinned scene assets contain a `TextMeshProUGUI` field with `Really Delete Save?`: macOS `level0#5208`, Windows `level0#5187`. The existing hierarchy comparison places it under `Menu/Menu_DeleteSave/Container/LoadSlotSelect/Question/Text (TMP)` and binds matching text hashes. The existing source-bound UI adapters can patch these serialized fields, but actual display, interaction, and safe save handling require runtime checks. The similarity of the two strings does not make them the same source occurrence.

`tools/menu-reason-source` checks the pinned assembly/Cecil hashes, all three literal-to-constructor argument sequences and the constructor's field assignment, then enumerates direct reason field accesses and `GetReason` method references. Both-build reports were reproduced byte-for-byte; the wrong-build assembly was rejected at the expected source guard. Tests cover the distinct serialized confirmation label in both builds and the managed report when the tool has been built. The complete suite passed 106 tests with `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. These controls do not prove no other consumer exists.

Fingerprints: tool `f05fd9555e958ff5903991199e2646b429260325d00ccb4be60f1151a00119a9`; tests `249c832fe86db3b13e63af3f4e0fbebef401b291163b9c796046bacc75e963cf`; macOS report `80c3cdd990c097e4c219daa3b852e90ba1bfcbfa00c259ec1ae0c06c1154be44`; Windows report `a4da3783605fc928e282dbeb28e9a4335efee9974c9b64d2a2e8305c79bc391a`.

Reproduce with pinned Python dependencies and .NET 8 / Mono.Cecil 0.11.6:

```sh
dotnet build localization/tools/menu-reason-source/menu-reason-source.csproj -p:BaseIntermediateOutputPath=NEW_OBJ_DIR/ -o NEW_BIN_DIR/
dotnet NEW_BIN_DIR/menu-reason-source.dll macos ORIGINAL_MAC_DATA/Managed/Assembly-CSharp.dll
dotnet NEW_BIN_DIR/menu-reason-source.dll windows ORIGINAL_WINDOWS_DATA/Managed/Assembly-CSharp.dll
python -m unittest discover -s localization -p 'test_*.py'
```
