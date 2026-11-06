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
app, changes the dialogue asset and ad-hoc signs the copy. It does not
launch it. The output uses the game's original save and preference identity if
run; only the separate test probe described below used isolated identifiers.
An error during copy or signing may leave a partial destination for inspection;
remove it only after verifying its contents. A new run requires a new destination.
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
remain completely unchanged. Only one locale is built per run.
This validation is conservative and does **not** prove all game-specific
controls or speaker-label semantics have been identified. Source line presence
does not prove visibility or runtime reachability.

## Optional TextMeshPro interface strings

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

## Evidence and limitations

- A read-only, source-pinned font-role probe can be run with a Python environment
  containing `localization/font_probe_requirements.txt`:

  ```sh
  "$PYTHON" localization/probe_font_roles.py "/path/to/Drag'N Wash.app/Contents/Resources/Data"
  ```

  It reports the managed files used to generate schemas, selected dialogue and
  menu component pointers, fallback chain and source-font cmap. The saved result
  for the pinned macOS build is `localization/evidence/font-roles-20261106.json`.
  Static font metadata and cmap coverage do not establish in-game readability,
  clipping or glyph rendering. The tool reads the installed source and does not
  extract or redistribute its font file.
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
