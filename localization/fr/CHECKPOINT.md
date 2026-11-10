# French localization checkpoint

Updated 2026-11-10. Status: **glossary author layers reconciled; bounded renderer probe complete; special-scene preparation started**. See [glossary review](glossary-review.md) and [renderer probe](renderer-probe.md) for the current resumption; historical notes below retain the earlier checkpoint context. The requested standard locale is `fr`; source is English. Session `01a1c394-a809-7812-9570-df379360d954` turn context and process arguments record `gpt-6.1-terra`, reasoning `high`. No other model or agent was used.

## Bound inputs

- Canonical Dragons checkout: `main`, initial HEAD `8f800bca8620dc7a4430e5882c95f005cca0a08a`. Preserve the untracked owner directory `textures-with-text/` and installed games/saves.
- macOS `9/12/2026_a93aa21a`, Windows `9/9/2026_ee944596`; source Data paths are in the task prompt and `localization/README.md`.
- Source inventory `localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json`: SHA-256 `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`. Yarn scope `localization/work/yarn-markers-20261110.ridbPA/yarn-scope-v42.json`: `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30`.
- SiteForMods read-only checkout `29b0bb56b3ce71a1d5a700c840b050af7333084d`. English glossary raw SHA-256 `24f51ad99f3b78ef06e1ba8ebefb2ab9072c866f4860fe9839055b504ead8baf`, canonical semantic fingerprint `3d261921e114b6feab10f57ad54d43674a75e991d94937686155b92cce399dc3`. Whole translation file raw SHA-256 `b49c48fb84eae01921070c11267706a3bd036f1d9b13a4f57e1a87a7144b672e`. French map SHA-256 `2980e0d03da5759766e13a252ac6061c5e7aa1045016b204861b567891717852`, computed as UTF-8 JSON with sorted keys, `ensure_ascii=False`, separators `(',', ':')`, no trailing newline.
- Paired English worklist, regenerated from both actual stock Data directories with `export_locale_worklist.py`: `localization/work/cli-terra-high-20261110.J0KLrx/fr/worklist.json`, SHA-256 `ef9d5709b061ea426c2e113373fdbfde547c6518f6394a4afc325204dea89cf8`; 1,947 authoring IDs and embedded 27-case index. Ignored run artifacts are not durable archival evidence: regenerate using the documented README command if missing. At that earlier worklist checkpoint no wording had yet been authored.

## Feasibility

The bounded French synthetic renderer controls now cover slot, dialogue, choices and settings on the pinned macOS and Windows builds, the latter through CrossOver. Both live routes progressed, original profile checks matched, and offscreen sample frames were reviewed. See [renderer-probe.md](renderer-probe.md) for hashes, the failed isolation-guard attempt and exact limitations. Native Windows, final corpus glyph coverage and visual fit remain unverified. The runtime lock was released after test exit.

## Glossary readiness

CLI preflight reports 28/28 IDs structurally complete, not editorial acceptance. Historical French `glossary-reviews/fr/layer-1.md` and `layer-2.md` are two author self-reads of the earlier 27-entry hashes; the new anonymous-dragon entry was subsequently reviewed by the coordinator, without an independent reviewer (`localization/evidence/generic-dragon-entries-20261110.md`). Source historical reviews were also self-reviews. Reconcile exact affected evidence and current hashes before crediting any unchanged receipts. The owner later explicitly allowed the two glossary author self-reviews without a distinct reviewer; see glossary-review.md. This does not waive independent game-text review.

A preliminary direct comparison of all 28 current English/French entries found an objective candidate issue: `dnw-family-crest` translates the ornamental family emblem as “crête familiale”, which normally denotes a physical crest; “blason familial” is a candidate for adjudication against the actual source context. The later scene-bound review withdrew this finding: the crest is worn around the head. See glossary-review.md. No SiteForMods file was changed.

## Stage status

| Stage | Status |
| --- | --- |
| probe | Bounded French synthetic paths observed on macOS and CrossOver, including body/choice/settings frames and progression; native Windows and corpus-specific fit pending. See renderer-probe.md. |
| source | Pinned worklist generated; verify source/preserve-exact gate and current shared receipts before translation. |
| glossary | Two author self-review layers reconciled on current hashes under the owner exception; the earlier crest finding was withdrawn after scene review. Independent review was not claimed. See glossary-review.md. |
| special-scene decisions | 16/27 groups have author-reviewed draft wording; the anonymous group retains a source buzzing-command boundary, and 11 groups remain unreviewed. Ordinary translation remains gated. See special-scenes.md. |
| translate-edit | 120/1,947 authored as special-scene preparation, including intentional exact vocalizations and ellipses; no ordinary batch started. Paired diagnostic assets verified. |
| editorial | Not run; full semantic audit, independent delta and regression catalog pending. |
| fonts | Slot and bounded live text samples resolved; full corpus coverage and typography remain unverified. |
| textures | Textures with text excluded and preserved. |
| package | macOS and Windows deliverables not built or verified. English passthrough is not a completed translation. |
| runtime / visual | French not run / not reviewed. |
| screenshot upload / review | Not requested / not run. |
| release / archival | Not complete; no publication, push or deployment authorized. |

Next: complete and review the remaining 11 special-scene groups, resolve or explicitly classify the anonymous-scene technical boundary before ordinary text; use the exact paired English worklist and preserve source-bound handling. If the shared glossary or probe needs changes outside `localization/fr/` and this run directory, report the exact boundary instead of modifying shared files. A verified locale-only commit requires the specified `.git/codex-canonical-commit.lock`, empty pre-existing index, complete staged review and committed-tree verification; do not reset, amend or interfere with other lanes.

The Alexander register/professor batch has author-reviewed wording and paired 43-entry macOS/Windows partial asset readbacks; see special-scenes.md for hashes and limits. The buzzing finish-command boundary remains open pending a same-fixture, unmodified-English runtime comparison. CrossOver is not native Windows evidence.

The college self-introduction batch adds nine scene IDs and two speaker-name IDs, with 51-entry paired Yarn readbacks and separately built speaker adapters; see special-scenes.md for exact hashes, the protected colon line and unrun scene checks. The overall translation hash is `f80b8eea2113edee81ec7340a05fa5fb9209798000bf42400001570a46b32efc`.

The family-crest draft adds ten scene IDs and preserves the seven source size tags; paired partial readbacks cover 61 Yarn entries. Its long, progressively shrinking line still requires actual French scene and visual review. Current translation SHA-256: `2420c6a0260f3fc3e8144b7ae5319f21b3108b94e83f30c321ba61da8cc06df6`.

Three typography groups add four scene IDs; both partial readbacks check 65 Yarn values with untouched tags and metadata. Scene-specific typography, fit and runtime remain open. Current translation SHA-256: `64c9f686b397a7d253eb64e3ac7408e83ee2b477cf96418bca635b303e47732d`.

The relationship and editor-question groups add ten scene IDs and paired 75-Yarn-entry readbacks. Source route reachability and scene-specific outcomes and fit remain unverified. Current translation SHA-256: `3abdf969d15f8cccab3d6a4607d6613959fb4056e11489ba5dff73366acecfa8`.

The Yip speech and film-title batch adds 20 IDs, including intentional exact vocalizations, and paired 95-Yarn-entry readbacks. A dash preserves the approved film title without triggering implicit-speaker parsing. Scene playback, audio and fit remain unverified. Current translation SHA-256: `765e4d612dbb1cfd427501f7a0e5580b780b25b016968b0f0749039e5c81a2b4`.

The full-mouth and nickname groups add 22 IDs; paired asset readbacks cover 117 Yarn values. Branches, character presentation and visual fit still need actual scene checks. Current translation SHA-256: `6049fd5a18d7394b35199337ef6d215f543a89c58327a8fa6ea178c1c7f4f0fd`.
