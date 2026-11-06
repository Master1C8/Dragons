# Speaker identity and presentation sources

The source-bound Yarn tables contain 24 colon-prefix candidates per build under the inspected implicit-speaker pattern: 18 begin with the known character labels `Ryan:` or `Conrad:`, five are embedded `title:`-like source markers, and `line:4b36ea4e` is a nonstandard full sentence ending in a colon with no remaining body under that pattern. The latter and title-like values are not ordinary character names; their intent and presentation remain unverified. The existing locale adapter protects the 18 English prefixes and holds the nonstandard and title-like source values unchanged. Consequently it does **not** yet provide a complete Russian speaker-name solution.

The 17 pinned serialized assets in each build contain five `Yarn.Unity.LinePresenter` and five `Yarn.Unity.OptionsPresenter` objects; no script references were unresolved in this scan. All five line presenters have `showCharacterNameInLine` set and non-null `characterNameText` references to source-verified `TMPro.TextMeshProUGUI` objects, while their container references are serialized null. All five option presenters have `showsLastLine` disabled and null last-line character-name text references. Their complete selected fields, target hashes and object-level no-op round trips are recorded in the presenter reports. These are serialized initial values, not proof that runtime code cannot change them.

Static inspection of the pinned `YarnSpinner.Unity.dll` shows `LinePresenter.Awake` sets a missing name container from a non-null name text component's GameObject. Across the complete pinned root `Managed/*.dll` sets (170 macOS and 172 Windows assemblies), the scanner found four direct IL references to `LocalizedLine.get_CharacterName`, all in Yarn Unity: one whitespace check and one immediately followed by a TMP text setter in each of `LinePresenter` and `OptionsPresenter`. The direct reference scan does not cover reflection, dynamically loaded assemblies, other uses of parsed text or runtime mutation. It does not establish that display-only mapping is sufficient across all execution paths.

Any future speaker adaptation needs to preserve the original identity and branching controls, handle both presenter configurations and name/inline fallbacks, separately address the nonstandard colon-bearing sentence and title-like markers, and be verified in both actual target runtimes with the finished font. Do not weaken the existing generic delimiter checks or translate source control names based solely on this static finding. No speaker patch or Russian target wording is produced here.

The source scans and direct-reference reports reproduced byte-for-byte. Tests cover source candidate counts, the nonstandard zero-body case, all ten presenter configurations and exact referenced script types in both builds, the four getter use sites and the expected rejection of a wrong-build managed directory. The complete suite passed 119 tests with `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. Tool hashes: presenter scanner `294781477816882e152ea5c3626e9a9b48fe4d5c209616f2a3f0a1f06295d765`; line scanner `2c16afab7bb9316858f822190584688aeb8c5327e741feff3722f21551d21ca5`; managed scanner `e30ae8c331ca375b754721cacb26a1e7a713d0fc6b13f58a35a07d58c25bafad`; tests `87765ee7ce95dec21a164f916cee06c2b291f7ad70b71a3f95b989d69b809df3`.

Reproduce with the pinned Python dependencies and .NET 8 / Mono.Cecil 0.11.6:

```sh
dotnet build localization/tools/speaker-consumers/speaker-consumers.csproj -p:BaseIntermediateOutputPath=NEW_OBJ_DIR/ -o NEW_BIN_DIR/
dotnet NEW_BIN_DIR/speaker-consumers.dll macos ORIGINAL_MAC_DATA/Managed
dotnet NEW_BIN_DIR/speaker-consumers.dll windows ORIGINAL_WINDOWS_DATA/Managed
python localization/inventory_speaker_presenters.py macos ORIGINAL_MAC_DATA
python localization/inventory_speaker_presenters.py windows ORIGINAL_WINDOWS_DATA
python localization/inventory_speaker_lines.py macos ORIGINAL_MAC_DATA
python localization/inventory_speaker_lines.py windows ORIGINAL_WINDOWS_DATA
python -m unittest discover -s localization -p 'test_*.py'
```
