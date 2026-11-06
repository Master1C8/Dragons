# Level configuration dialogue bindings

Both pinned builds contain 15 `LevelConfiguration` objects in `sharedassets1.assets`. Their serialized dialogue fields contain 93 nonempty references per build, covering 83 distinct Yarn node names; all 93 targets exist in the respective extracted program. `inventory_level_dialogues.py` binds each object, field and array index to source hashes and performs an exact no-op round trip of every configuration. Its per-build reports contain the complete selected references and a static closure over named `RunNode`/`DetourToNode` instructions.

The generator initially represented five `string[]` fields as scalar strings and could not decode the objects. The pinned `Assembly-CSharp.dll` metadata identifies `setFlags`, `endFlags`, `progressDialogs`, `idleDialogs` and `nagDialogs` as serialized `System.String[]` in both builds. The source-pinned Cecil check in `tools/level-schema` verifies those declarations; the extractor repairs only those five generated schema nodes and rejects unexpected field layouts or any object that fails exact byte round-trip. The wrong-build managed assembly was rejected at the expected hash guard. This validates the decoding boundary, not runtime behavior.

Following named transfers from the 83 configuration roots yields 108 nodes / 1,289 line IDs for macOS and 112 nodes / 1,303 line IDs for Windows. These are static graph closures that ignore branch conditions and include every mapped line in a reached node; they are not reachable-content counts. They omit entry points from other components, dynamic node names or program loading, and do not establish dead code or complete inventory. `Start` is absent from these particular closures, but five serialized dialogue runners have `startNode` set to `Start` with auto-start disabled; dynamic invocation remains possible. Do not exclude its test-looking lines on this evidence.

The Windows configuration `Conrad_3_8`, field `dragonFinishMountDialogue`, names `Conrad_finished_mount_3`. Its static named-transfer path includes `Conrad_Outro`, whose instruction 21 names the absent node `Conrad_OutroDone`. The macOS closure has no unresolved named target. This links one previously identified missing target to a configuration path; it does **not** establish that the game selects this configuration or executes those particular transfers. The runtime program may be merged or otherwise modified. Do not repair the original or assert a gameplay failure without the separate runtime investigation.

Reports `level-dialogues-macos-20261107.json` and `level-dialogues-windows-20261107.json` have SHA-256 `4a16420f2b028201e605466c66c103b367c0cc60e8fd04c684df82a0beaaf3bd` and `cb590fe02f13aa39e04b892d66f873850b6a798870d2dea0fff74c34ce70335b`; both were reproduced byte-for-byte. Extractor SHA-256 `8545aaa56dbbb2854d2e839f03f86d8a272fd7dfb8a47303023d88f1a22737b0`; schema metadata tool SHA-256 `a575e9024e566d87905a565a0e8e967af6eb2cf8e0901f43b60de4977c1fdbe8`. Tests cover both real builds, exact decoding, a cyclic graph with a missing target and rejection of an unknown generated schema. The complete suite passed 102 tests with `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`.

Reproduce with the pinned dependencies and .NET 8 / Mono.Cecil 0.11.6:

```sh
python localization/inventory_level_dialogues.py macos ORIGINAL_MAC_DATA
python localization/inventory_level_dialogues.py windows ORIGINAL_WINDOWS_DATA
dotnet build localization/tools/level-schema/level-schema.csproj -p:BaseIntermediateOutputPath=NEW_OBJ_DIR/ -o NEW_BIN_DIR/
dotnet NEW_BIN_DIR/level-schema.dll macos ORIGINAL_MAC_DATA/Managed/Assembly-CSharp.dll
dotnet NEW_BIN_DIR/level-schema.dll windows ORIGINAL_WINDOWS_DATA/Managed/Assembly-CSharp.dll
python -m unittest discover -s localization -p 'test_*.py'
```
