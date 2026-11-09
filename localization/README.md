# Drag'N Wash: dialogue locale asset builder

This is an experimental builder for the macOS build `9/12/2026_a93aa21a`. It
creates either one new `sharedassets1.assets` file or a separate `.app` copy
for a selected language. It does not modify the installed game, install a
translation, switch the game's locale, or translate textures or game code.
A new build is made from the original English asset for each locale; existing
output files are never overwritten.

The game uses Unity and Yarn Spinner. The pinned Yarn localization object is
MonoBehaviour path ID `10623`, with 1,839 ordered string IDs. The builder
changes its English text values, retaining the original locale identifier and
all remaining objects. This is a replacement of the English table for one
selected language, not a native multilingual in-game language picker.

## Prerequisites

- Python 3.9+ and `UnityPy==1.25.4` in an isolated environment. The local
  investigation environment used `/private/tmp/dragnwash-unitypy-venv/bin/python`;
  it is temporary and is not a durable project dependency.
- The canonical site locale catalog at
  `~/Desktop/SiteForMods/lib/language-data/site-locales.ts`. Builds reject an
  unsupported or missing locale instead of selecting a fallback language.
- Original, unmodified macOS `sharedassets1.assets` from the supported game.
  Its SHA-256 must be `f8c5c51ac1b0cf151177c05ee1805e032cf62baf384bb664337a71b923bee7b8`.

## Usage

Set `PYTHON` to a Python interpreter with the pinned UnityPy version and `ASSET`
to the original `sharedassets1.assets`. Use paths outside the installed game
for both outputs.

```sh
"$PYTHON" localization/dialogue_locale.py "$ASSET" --export source-lines.json
"$PYTHON" localization/dialogue_locale.py "$ASSET" --locale ru.json --output output/ru/sharedassets1.assets
```

To build a separate signed macOS app for a chosen language instead, use:

```sh
"$PYTHON" localization/build_game.py --source-app "/path/to/Drag'N Wash.app" \
  --locale-file ru.json --locale ru --output-app "/path/to/output/DragNWash-ru.app"
```

The selected locale must match the file exactly. The command copies the source
app, changes the dialogue asset and ad-hoc signs the copy. It does not launch
it. Without `--test-profile`, the output retains the game's original save and
preference identity; do not launch such a copy for isolated testing.

For a disposable test app, append `--test-profile G6P4`, substituting a fresh
four-character uppercase ASCII letter/digit code. The builder verifies the
pinned original, refuses a code with existing test data/preferences, assigns
a distinct test company, product and bundle identifier, checks each changed
object and plist field, and adds a `vn-test-profile.json` marker. Such a build
is **test-only**, not a player release. Its selected code may already have been
used on another machine; choose one that is fresh for the test environment.
The collision check is not an atomic reservation: do not build or run multiple
test apps with the same profile code concurrently.
The profile creates separate test data and preferences on launch. No automatic
copy, migration or restoration of the player's save is performed. A tested
launch reached the main menu with a distinct data directory/preferences and
left the existing original-profile file hashes unchanged; save creation,
normal exit, Steam integration and every possible save location are not proven.
The builder constructs and verifies the app in a private staging directory in
the output parent, then uses macOS exclusive rename to publish it without
replacing an existing destination. An ordinary exception before publication
removes that task-owned staging directory; abrupt termination may leave it for
inspection. Verification is repeated at the published path. If cleanup after
publication or that final verification fails, the published app may remain for
diagnosis and is not a successful build. Use a fresh destination after inspecting
any retained output.

The app builder pins the original `Managed` directory and compares every DLL
with the signed staging app before publication. The read-only verifier also
accepts a separate Windows game copy. See [the managed preservation
evidence](evidence/managed-assembly-preservation-20261109.md).
The game writes `steam_appid.txt` into the app-bundle root at startup, making the
ad-hoc signature invalid. Launch a generated copy through the wrapper:

```sh
"$PYTHON" localization/run_game.py "/path/to/output/DragNWash-ru.app"
```

The wrapper checks the signed build marker, verifies the signature, and removes
the generated root file after the game exits only when its hash matches the
preserved Steam identifier. It then verifies the signature again. It rejects an
existing root file, a concurrent wrapper and unexpected file contents. If the
wrapper is forcibly terminated or the machine loses power, cleanup may not run;
preserve the file and inspect the copy instead of deleting it blindly. Direct
Finder launch bypasses this protection and invalidates the signature. This is not
a release-ready installer, and Steam functionality itself remains unverified.

The export contains English source values keyed by line ID. A locale JSON
contains only entries to replace; missing IDs retain English:

```json
{
  "schema": 1,
  "locale": "ru",
  "sourceObjectSha256": "9baafe5b3c36e63042cc0d02b2c755580e142447cea13f946d485a342c269853",
  "lines": {
    "line:12345678": {"source": "Exact original text", "text": "Replacement text"}
  }
}
```

The example ID and wording are illustrative, not game data. Copy real IDs and
exact `source` values from the export. Markup, placeholders and initial labels
must be preserved; unknown IDs, duplicate JSON keys, changed source text and
unsupported source versions are rejected. Entries beginning with `title:` must
remain completely unchanged. Ten specifically identified `==` and `---` source
markers adjacent to title-like lines must also remain exact in Yarn translations
while their role is unresolved; this ID-scoped rule does not apply to UI/settings.
See `evidence/yarn-missing-targets-20261107.md`. Only one locale is built per run.
This validation is conservative and does **not** prove all game-specific
controls or speaker-label semantics have been identified. Source line presence
does not prove visibility or runtime reachability.

The game's Yarn provider recognizes an implicit speaker before a colon. Until
the source cases are classified, dialogue validation rejects adding or removing
colon presence, preserves existing short ASCII prefixes exactly, and requires
an unclassified long colon-bearing line to remain unchanged. These deliberately
conservative guards can block a legitimate translation, including localized
speaker names; do not weaken them without an explicit per-ID speaker/control
contract and runtime verification. The colon rule does not apply to UI and
settings strings. Dynamically substituted values and all markup cases remain to
be classified.

## Windows TextMeshPro asset adapter

`windows_ui_locale.py` builds a separate, source-pinned Windows asset. It can
combine UI with a Yarn locale in `sharedassets1.assets`, or UI with a settings
locale in `sharedassets0.assets`; any one of these locale inputs may also be
used alone. See `evidence/windows-ui-dialogue-composition-20261107.md` and
`evidence/windows-ui-settings-composition-20261107.md`. These are individual
asset operations; source classification, a complete Windows package and final
runtime checks remain required.

## Restoring missing Yarn transitions

Pass `--restore-yarn-transitions` to `build_game.py` or to
`windows_ui_locale.py` when building `sharedassets1.assets`. Both paths
regenerate the exact five previously tested continuation nodes from the pinned
source and verify the serialized output. The original program bytes, all
existing nodes and translation IDs are preserved. The flag composes with
dialogue and UI locale files. Pass the same flag to
`verify_combined_yarn_ui.py` to include the repaired YarnProject in its exact
object comparison.

The flag is opt-in while normal gameplay verification is pending. Use a fresh
macOS test profile or an isolated Windows game and save directory for runtime
checks. See [the transition evidence](evidence/yarn-transition-runtime-20261109.md).

## Optional TextMeshPro interface strings

For `level2`, both platform adapters preserve the 34 source-bound contributor
name fields exactly. They verify the complete manifest against the original UI
strings and reject an attempted name change before writing an output. Credit
descriptions are separate fields and remain eligible for translation. This
guard covers only the pinned name fields, not every credit or text source; see
`evidence/credit-name-preservation-20261107.md`.

For supported serialized assets, export the TextMeshPro UI objects separately:

```sh
"$PYTHON" localization/ui_locale.py "/path/to/Drag'N Wash.app/Contents/Resources/Data" level0 --export ui-level0-source.json
```

Supported names are `level0` through `level6`, `sharedassets0.assets` and
`sharedassets1.assets`. For each asset to change, prepare a JSON file named
`<asset>.json` in a UI locale directory. Its shape is the dialogue locale format
above, except `sourceObjectSha256` is the **asset hash** from that asset's UI
export and IDs are keys such as `level0#5201`. Then append
`--ui-dir /path/to/ui-locale-directory` to `build_game.py`. Every file must
identify the same requested locale. Assets not supplied stay unchanged, and
dialogue and UI changes to `sharedassets1.assets` are merged.

The export includes dynamic placeholders, numbers and names as well as text.
It is an inventory, not a classified translation list. Review each candidate
and preserve runtime values and proper names. Settings, code-generated text,
other UI types and texture lettering are not covered by this mechanism.

Both UI builders read the same source-pinned preservation roles as the shared
inventory. Leave protected fields out of the locale input or supply the exact
source value. The current checks cover contributor names, version placeholders,
dialogue presenter templates, settings prefabs and development-menu labels.
The combined-asset verifiers apply the same rules.

### Yarn missing-line fallback

The stock built-in line provider can show a missing-line message in dialogue
or a choice. It uses two copies of the same string in `YarnSpinner.Unity.dll`.
The optional managed fallback input changes both from one locale record.
Use the normal locale JSON shape with the source DLL SHA-256 as
`sourceObjectSha256`, the ID `yarn-missing-line`, and the exact source
`!! ERROR: Missing line!`. The replacement must be a single plain-text line.

Build the pinned patcher with .NET 8:

```sh
dotnet build localization/tools/managed-fallback/managed-fallback.csproj \
  -p:BaseIntermediateOutputPath=ABSOLUTE_WORK_OBJ/ -o ABSOLUTE_WORK_BIN/
```

Pass `--fallback-locale FALLBACK.json --fallback-tool ABSOLUTE_WORK_BIN/managed-fallback.dll`
to `build_game.py`. The app builder verifies the full Managed directory after
signing, allowing only the exact replacement DLL digest reported by the patcher.
On Windows, build the DLL as a separate artifact:

```sh
"$PYTHON" localization/managed_fallback.py windows --source ORIGINAL_MANAGED/YarnSpinner.Unity.dll \
  --locale-file FALLBACK.json --locale ru --tool ABSOLUTE_WORK_BIN/managed-fallback.dll \
  --output NEW_OUTPUT/YarnSpinner.Unity.dll
```

This Windows command writes a verified DLL to a fresh path. The Windows asset
builder still produces its Unity assets separately.

### Runtime new-slot label

The same patcher can change the three stock `NEW` assignments in
`Assembly-CSharp.dll`. Use the locale JSON shape above with the original
`Assembly-CSharp.dll` SHA-256 as `sourceObjectSha256`, ID `slot-new`, and
source `NEW`. Pass `--slot-new-locale SLOT.json` with
`--managed-text-tool ABSOLUTE_WORK_BIN/managed-fallback.dll` to the macOS
builder. It can build both managed text inputs in one app.

For Windows use `managed_fallback.py windows --slot-new` with the original
`Assembly-CSharp.dll` as `--source` and a fresh DLL path as `--output`.
The serialized `New` fields in `level0` remain separate UI locale inputs
on both platforms. Localize both groups when preparing the complete slot
menu. The numeric save-progress formats are preserved.

### Yarn speaker display names

The speaker locale uses the same JSON shape. Set `sourceObjectSha256` to
the original platform's `YarnSpinner.Unity.dll` SHA-256 and include
`speaker-ryan` with source `Ryan` and `speaker-conrad` with source
`Conrad`. Both display values must be single words of at most 40 BMP
letters. Dialogue locale files still keep the exact English prefixes
`Ryan: ` and `Conrad: ` including their whitespace.

For the Alexander introduction, the speaker locale can also carry
`line:4b36ea4e` with the exact English source
`The most prestigious college hosting prestigious professors like me:`.
Supply its translated sentence as plain text ending with a colon. The
player adapter shows it in the dialogue body, with the name field hidden.
Keep the original line in the Yarn table so the source ID and parsed
identity remain available to the game. This record needs the final
editorial decision for the whole introduction.

Build the patcher and the player runtime from the same checkout. Use fresh
absolute output directories and the original platform's Managed directory.

```sh
dotnet build localization/tools/speaker-display-probe/speaker-display-probe.csproj \
  -p:BaseIntermediateOutputPath=ABSOLUTE_TOOL_OBJ/ -o ABSOLUTE_TOOL_BIN/
dotnet build localization/tools/speaker-inline-runtime/speaker-inline-runtime.csproj \
  -p:SpeakerLocale=true "-p:GameManaged=$original_managed" \
  -p:BaseIntermediateOutputPath=ABSOLUTE_RUNTIME_OBJ/ -o ABSOLUTE_RUNTIME_BIN/
```

Pass `--speaker-locale NAMES.json --speaker-tool ABSOLUTE_TOOL_BIN/speaker-display-probe.dll`,
`--speaker-runtime ABSOLUTE_RUNTIME_BIN/Dragons.SpeakerPresentation.dll` and
`--speaker-runtime-sha SHA256` to `build_game.py`. If given, the missing-line
locale is applied in the same Yarn DLL pass. The managed text tool is still
required when a new-slot locale is supplied. The app builder verifies both
speaker DLLs in the final signed bundle.

For a Windows staging directory, call `speaker_locale.prepare('windows', ...)`
with that build's original Yarn Unity DLL, names, runtime and runtime SHA-256.
Place both returned files in the staged Managed directory together. The
returned receipt records the patched Yarn Unity and companion fingerprints.
Windows installation and restoration are still separate from this preparation
step. See the [paired speaker build evidence](evidence/speaker-locale-build-20261110.md).

The optional `--speaker-contrast` flag uses the stock black text color for
the originally white speaker-name fields in `level1`, `level3`, `level5`
and `level6`. The macOS builder updates all four assets in the app. On
Windows use the same flag with `windows_ui_locale.py` for each of those
assets, with or without a separate UI locale for that asset:

```sh
"$PYTHON" localization/windows_ui_locale.py ORIGINAL_DATA level1 \
  --requested-locale ru --speaker-contrast --output NEW_OUTPUT/level1
```

The adapter changes only the name component's packed and floating-point
colors. `level4` already uses black. The scene files can contain localized
UI strings from the same build step. See the
[contrast verification](evidence/speaker-contrast-build-20261110.md).

## Optional settings labels and choices

Settings labels and dropdown choices are stored in separate scriptable objects;
the TextMeshPro UI exporter above does not cover them. Install the pinned
`localization/font_probe_requirements.txt` dependencies and use the original
game data directory to export their fields:

```sh
"$PYTHON" localization/settings_locale.py "/path/to/Drag'N Wash.app/Contents/Resources/Data" \
  --export settings-source.json
```

The export lists candidate `lines` and `preserveExactly` fields. It is not a
classified translation inventory. Resolution option values and empty fallback
labels are protected. Do not change option order, runtime values, IDs, other
fields or active localization references. Construct a locale file with the same
schema as the dialogue example, the settings export's `sourceObjectSha256`, and
keys such as `sharedassets0.assets#606:label` or
`sharedassets0.assets#606:option:0`. To include it in a copied application, pass
`--settings-locale /path/to/settings-ru.json` to `build_game.py`; it can be
combined with `--ui-dir`. The builder verifies the exact preceding UI changes,
then verifies the merged settings asset before replacing that one file. The
whole app remains in staging until all supplied steps and signing succeed.

The settings adapter accepts only the pinned macOS source and managed schema
inputs, round-trips each supported settings object, preserves every unrelated
serialized object and re-reads changed fields. It is still a prototype: runtime
testing used an isolated, instrumented app with one artificial settings label,
and full menu coverage, choices and translated text remain unverified.

For isolated tests only, `--test-settings-caption-layout` may be combined with
`--test-profile`. It applies the reviewed caption-height experiment to the
copied `sharedassets0.assets`, verifies prior UI/settings edits and preserves
all other object bytes. It is forbidden without a test profile, adds a signed
`vn-test-layout.json` marker and remains disabled for normal builds. One
synthetic value became legible in a controlled comparison; long values,
scrolling, normal input and final localized content remain unverified.

For isolated tests only, `--test-slot-font` with `--test-profile` changes the
three new-slot label font sizes from 20 to 18 in the copied `level0`, after
validating any supplied `level0` UI locale file and every unrelated object.
It requires the font-probe dependencies in `font_probe_requirements.txt`,
adds a signed `vn-test-slot-font.json` marker, and is disabled for normal
builds. The five-character synthetic sample has more room in one comparison,
but exact glyph details and real translated labels remain unverified; this is
not an accepted release setting. It is applied inside the unpublished staged app.

## Evidence and limitations

- `windows_dialogue_probe.py` produces a **test-only** Windows Yarn asset in
  `localization/work/` from the separately pinned Windows build and a
  Windows-source-bound synthetic locale file. It validates the game version,
  source asset and Yarn object, rechecks the bytes consumed, and compares all
  saved serialized objects after replacement. Existing outputs are never
  overwritten. It is a probe, not an installer or a Windows release builder;
  Windows UI/settings, safe packaging, full gameplay and restoration still
  require separate validation.
- `windows_slot_ui_probe.py` is likewise restricted to fresh test assets in
  `localization/work/` and the three source-pinned Windows new-slot labels.
  It checks their hierarchy and preserves all other serialized objects; it is
  not a general Windows UI adapter or a player installer.
- `windows_settings_probe.py` handles only the pinned Windows anti-aliasing
  label and one option in a fresh test asset. It validates the managed schemas,
  unbound text references and every saved object. It is not a general settings
  adapter; final strings, all other settings and release installation remain
  unverified.

- The installed Windows copy investigated separately reports build
  `9/9/2026_ee944596`, while the macOS build reports `9/12/2026_a93aa21a`.
  Their Yarn tables have the same 1,839 ordered IDs but 25 source text values
  differ; three compiled Yarn nodes also differ. Reproduce the bounded,
  read-only comparison with:

  ```sh
  "$PYTHON" localization/compare_yarn_versions.py --macos-data /path/to/mac/Data \
    --windows-data /path/to/windows/DragNWash_Data
  ```

  The pinned result is `localization/evidence/yarn-versions-20261106.json`.
  Matching IDs do not prove equivalent narrative meaning, runtime, UI, font,
  save behavior or package compatibility. The macOS builder does not support
  the Windows asset, and this comparison does not modify either installation.
- A read-only, source-pinned font-role probe can be run with a Python environment
  containing `localization/font_probe_requirements.txt`:

  ```sh
  "$PYTHON" localization/probe_font_roles.py "/path/to/Drag'N Wash.app/Contents/Resources/Data"
  ```

  It reports the managed files used to generate schemas, selected dialogue and
  menu component pointers, fallback chain and source-font cmap. The saved result
  for the pinned macOS build, including choice and settings text, is
  `localization/evidence/font-roles-settings-20261106.json`.
  Static font metadata and cmap coverage do not establish in-game readability,
  clipping or glyph rendering. The tool reads the installed source and does not
  extract or redistribute its font file.
- `localization/probe_text_surfaces.py /path/to/Data`
  counts selected component types in the pinned serialized assets without
  exporting their text. The saved result is
  `localization/evidence/text-surfaces-20261106.json`. It is a bounded discovery
  aid, not a complete inventory or evidence that a component is reachable.
- The original Yarn object was decoded and re-encoded byte for byte. A one-line
  synthetic replacement was built and read back; all 11,392 other Unity objects
  retained identical raw bytes in the saved asset.
- Dialogue and TextMeshPro changes in `sharedassets1.assets` were built together
  and independently read back without one overwriting the other.
- The installed game was not modified. A separately signed test copy, with
  different Unity company/product identifiers, launched to the main menu and
  entered a new game. The log confirms Yarn created its built-in localized line
  provider, but the synthetic replacement line was not reached. A second test
  copy displayed the synthetic UI value `TEST 427` on the save-slot screen,
  detected through on-device OCR. A separate Cyrillic probe `ЖЮЯ 427` was also
  recognized by OCR at that screen. OCR is not a visual acceptance check;
  font completeness, clipping and other scripts remain unverified. The two
  screenshot originals have SHA-256 `1d75c9c3d460b4df86c1dc4f0f145058427d82b73a7c1abf3c40cfba3c6a04fa`
  and `61c6a6ce8a1a2b70d33d829affd44f9dde8f3324a9d0bfe66a3342e20551d8ac`.
  Loading the replacement during dialogue,
  complete UI and settings coverage, save behavior, fonts,
  glyph coverage, shaping, bidirectional text and layout remain **unverified**.
  Do not treat the output as a finished
  localization or install it over a real game without an independently verified
  integration and recovery path.
- An isolated copy launched twice through the wrapper. Each run produced the
  root Steam file; after exit the wrapper removed the matching file and
  `codesign --verify --deep --strict` succeeded. The first run was terminated
  by a targeted test signal; the second used `-batchmode -quit` and was also
  stopped by a targeted signal after Unity did not exit on its own. Steam API
  initialization failed because no Steam client was running, so this proves
  signature cleanup only, not Steam support or normal player exit.
- Embedded texture text is outside scope and is not modified.
- This prototype does not prove compatibility with Windows, other game versions,
  different UnityPy versions or arbitrary scripts. Verify these separately.

Run the validation tests with `python3 -m unittest discover -s localization -p 'test_*.py'`.

### Speaker display investigation

`tools/speaker-display-probe` and `tools/speaker-display-runtime-test` are
source-pinned **synthetic test tools**, not part of the player builder. They
investigate translating a displayed speaker label without changing the Yarn
character identity. See `evidence/speaker-display-synthetic-20261107.md` for
test scope, exact build fingerprints, and the unresolved in-game result. The
tool does not implement a release-ready locale selector or translation package.

`tools/speaker-inline-probe` exercises the distinct inline-name path using
the original Yarn parser on both builds. For the optional synthetic presenter
patch, build the `tools/speaker-inline-runtime` companion and supply its DLL
and SHA-256 to `speaker-display-probe`. The desktop harness and limits are
recorded in [the inline-view evidence](evidence/speaker-inline-view-20261109.md).
