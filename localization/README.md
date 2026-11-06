# Drag'N Wash: dialogue locale asset builder

This is an offline prototype for the macOS build `9/12/2026_a93aa21a`. It
creates one new `sharedassets1.assets` file for a selected language. It does
not modify the installed game, install a translation, switch the game's locale,
or translate UI, textures or game code. A new build is made from the original
English asset for each locale; existing output files are never overwritten.

The game uses Unity and Yarn Spinner. The pinned Yarn localization object is
MonoBehaviour path ID `10623`, with 1,839 ordered string IDs. The builder
changes its English text values, retaining the original locale identifier and
all remaining objects. This is a replacement of the English table for one
selected language, not a native multilingual in-game language picker.

## Prerequisites

- Python 3.9+ and `UnityPy==1.25.4` in an isolated environment. The local
  investigation environment used `/private/tmp/dragnwash-unitypy-venv/bin/python`;
  it is temporary and is not a durable project dependency.
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

## Evidence and limitations

- The original Yarn object was decoded and re-encoded byte for byte. A one-line
  synthetic replacement was built and read back; all 11,392 other Unity objects
  retained identical raw bytes in the saved asset.
- The installed game was not modified or launched. In-game loading, all UI and
  settings text, save behavior, fonts, glyph coverage, shaping, bidirectional
  text and layout are **unverified**. Do not treat the output as a finished
  localization or install it over a real game without an independently verified
  integration and recovery path.
- Embedded texture text is outside scope and is not modified.
- This prototype does not prove compatibility with Windows, other game versions,
  different UnityPy versions or arbitrary scripts. Verify these separately.

Run the validation tests with `python3 -m unittest discover -s localization -p 'test_*.py'`.
