# Drag'N Wash Russian localization — current state

Updated 2026-11-06. Canonical checkout: `/Users/antonkrutov/Desktop/Dragons`, branch `main`. Goal: complete standard Russian localization of the verified supported builds, excluding all text baked into textures, with a reproducible package and verified runtime, installation and restoration. Do not modify the installed game or its saves during tests. Publication and deployment are separate decisions.

## Scope and process binding

Source language English; requested locale `ru` → runtime `ru` selected at build time, replacing the English Yarn table in a separate build. This prototype is not an in-game language selector. Owner decisions: player and franchise contact use neutral wording; Alexander uses masculine forms; Igwyx is referred to with masculine forms without asserting gender; Max uses neutral forms without asserting gender. These rules do not establish other characters' gender or complete roster coverage.

All locales use the shared fixed stages in `~/.codex/skills/vn-localization/references/ROUTING.md` (SHA-256 `75fac761503c8cfdeee6281629fa158ce6661f8acaf02e225cee4a66861aa093`) and the state and feasibility contracts `CHECKPOINT.md` (`de6fcd0119aceda9edeed0850eaa659b10aaf8e7cfc7e7c22ce7c627c9849b25`) and `EARLY-PROBE.md` (`834ea4fe965447f00c59680d149fc1445fe08b8f042f30c99a0504354c9bc237`). Universal translation prompt SHA-256 `68acfd48b4408a53af62bc0b021f355f25d089d784d417fe24f30fba3be935dd`; editorial workflow SHA-256 `37ff4269163b17cab4030c2d1c78651f7a79b9c8be3d569a2b9ea7f17748a5dc`. Paths: `~/.codex/instructions/game-localization-prompt.md` and `~/.codex/instructions/game-localization-audit-workflow.md`.

| Stage | Game binding / required evidence |
| --- | --- |
| `scope` | This file; validate version, permissions, type, locale and identity before changes. |
| `probe` | `localization/dialogue_locale.py`, `ui_locale.py`, `build_game.py`, isolated game copy; matrix below. No bulk translation before applicable paths pass or a specific risk decision. |
| `source` | Complete shared stable-ID inventory, classifications, preserve-exact contract and validator, special-scene discovery; assess effort after verification. Existing exports are incomplete candidates. |
| `glossary` | Verify standard source and Russian glossary evidence and pinned hashes below. Existing publication does not prove every editorial prerequisite. |
| `translate-edit` | Settle all in-scope special-scene solutions first; then directly translate, immediately edit and validate each batch against the shared inventory. |
| `editorial` | Full semantic audit, independent diff/delta review and regression closure on pinned artifacts; do not assert independence without evidence. |
| `resources` | Verify final font coverage and metrics against the finished corpus; textures not applicable by owner decision. |
| `package` | Build and read back complete locale artifact using documented adapter; validate install and recovery. |
| `runtime` | Test the delivered artifact in authorized isolated environments, including progression, clipping and saves. |
| `screenshot-upload`, `screenshot-review` | Not run: no game screenshot upload requested; if later authorized, pin and review every delivered slot. |
| `delivery` | Integrate verified source into canonical branch; publication/release requires separate authority. |

## Inputs and evidence

- macOS game bundle `9/12/2026_a93aa21a`, Unity `6000.3.14f1`, `/Users/antonkrutov/Documents/Drag'N Wash.app`; `sharedassets1.assets` SHA-256 `f8c5c51ac1b0cf151177c05ee1805e032cf62baf384bb664337a71b923bee7b8`. Yarn string object path ID `10623`, raw SHA-256 `9baafe5b3c36e63042cc0d02b2c755580e142447cea13f946d485a342c269853`; 1,839 source IDs are candidates, not the visible-text denominator. Yarn program path ID `10719`; 195 named nodes were examined. Dynamic settings, other UI types and code-generated text remain to be inventoried.
- Windows installation `.../Dragn.Wash/game/DragNWash_Data/sharedassets1.assets` SHA-256 `aff0c9a7b017a4b8cd5fa7ee069fa49331703c54bff9e7a2e398fa04b646d231`. It differs from macOS; version, compatibility and source correspondence are not established.
- Source glossary `/Users/antonkrutov/Desktop/SiteForMods/data/games/dragn-wash/glossary.json` SHA-256 `245b734e32bc70760e884ae16505e08c6571e5120c7053255fc7435d7905ac4d`; 27 entries. Russian glossary is in adjacent `glossary-translations.json`, whole-file SHA-256 `db410f7dd0d016973fc8372e65f2f24723dfdead95e03d2d9f44be4a746288`; compact Russian map SHA-256 `00560fed9bdc23ca10cc7a231c91f65f124ae7781ec6ce0a64f8067c6261234f`. Russian review receipts are in `glossary-reviews/ru/`; two self-review layers, no independent reviewer claimed. Readiness under standard-localization requirements remains needs-review.
- No complete shared inventory, preserve-exact manifest, special-scene registry, source estimate or character roster coverage has been verified. `/private/tmp/dragnwash-dialogue.json` is disposable research, not a source handoff. No source-bound Russian game-text corpus exists yet.
- Adapter source and instructions: `localization/README.md`. On 2026-11-06, `python3 -m unittest discover -s localization -p 'test_*.py' -v` passed 13 tests. They verify builder and wrapper guards, not complete game runtime.

## Shared feasibility matrix

| Requirement / surface | Pinned inputs and static evidence | Runtime / visual evidence | Status and next action |
| --- | --- | --- | --- |
| `ru`, Yarn narrative and choices | macOS Yarn object and adapter described above; no-op byte round trip and synthetic line readback documented in `localization/README.md` | Isolated game copy entered gameplay, but replacement line was not reached. `localization/work/probe-player-2.log`. | needs-review: reach the actual substituted line, inspect representative Cyrillic glyphs and wrapping, and advance dialogue. |
| `ru`, TextMeshPro UI / save-slot menu | macOS UI adapter and source hashes are validated by the builder; synthetic replacement readback documented in README | Isolated test copy produced `ЖЮЯ 427`, recognized by local OCR in `localization/work/ui-cyrillic-distinct.png` (SHA-256 `61c6a6ce8a1a2b70d33d829affd44f9dde8f3324a9d0bfe66a3342e20551d8ac`). OCR is not visual acceptance and covers only three distinct Cyrillic glyphs. | needs-review: inspect real-size representative samples, full Cyrillic repertoire and narrow layouts; identify all UI text paths. |
| Dynamic values, settings, other UI | No complete source/path contract | not-run | needs-review: discover paths, validate placeholders and exercise their runtime states. |
| Windows build | Asset hash differs from macOS | not-run | needs-review: identify version and compare actual source, renderer and safe copy behavior. |

The test copies have isolated Unity company/product identifiers; ordinary copies currently retain the original save identity. The Steam wrapper passed signature cleanup after targeted process termination; normal exit and Steam integration remain unverified. Original assets and saves must not be overwritten. `localization/work` is disposable test evidence retained while work is active, not a final deliverable.

## Locale status

| Locale | Phase | Translated / visible total | Glossary | Editorial | Fonts | Textures | Build | Runtime | Visual | Screenshot upload | Screenshot review | Release | Blocker / next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ru` | `probe` | 0 / unknown | needs-review | not-run | needs-review | not-applicable: excluded by owner | needs-review: prototype only | needs-review | needs-review | not-run: not requested | not-applicable: no upload | not-run | Establish real dialogue/UI rendering and progression, then finish and classify shared inventory; do not infer coverage from raw ID count. |
