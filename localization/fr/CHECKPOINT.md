# French localization checkpoint

Updated 2026-11-10. Status: **probe and glossary gates open; translation not started**. The requested standard locale is `fr`; source is English. Session `01a1c394-a809-7812-9570-df379360d954` turn context and process arguments record `gpt-6.1-terra`, reasoning `high`. No other model or agent was used.

## Bound inputs

- Canonical Dragons checkout: `main`, initial HEAD `8f800bca8620dc7a4430e5882c95f005cca0a08a`. Preserve the untracked owner directory `textures-with-text/` and installed games/saves.
- macOS `9/12/2026_a93aa21a`, Windows `9/9/2026_ee944596`; source Data paths are in the task prompt and `localization/README.md`.
- Source inventory `localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json`: SHA-256 `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`. Yarn scope `localization/work/yarn-markers-20261110.ridbPA/yarn-scope-v42.json`: `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30`.
- SiteForMods read-only checkout `29b0bb56b3ce71a1d5a700c840b050af7333084d`. English glossary raw SHA-256 `24f51ad99f3b78ef06e1ba8ebefb2ab9072c866f4860fe9839055b504ead8baf`, canonical semantic fingerprint `3d261921e114b6feab10f57ad54d43674a75e991d94937686155b92cce399dc3`. Whole translation file raw SHA-256 `b49c48fb84eae01921070c11267706a3bd036f1d9b13a4f57e1a87a7144b672e`. French map SHA-256 `2980e0d03da5759766e13a252ac6061c5e7aa1045016b204861b567891717852`, computed as UTF-8 JSON with sorted keys, `ensure_ascii=False`, separators `(',', ':')`, no trailing newline.
- Paired English worklist, regenerated from both actual stock Data directories with `export_locale_worklist.py`: `localization/work/cli-terra-high-20261110.J0KLrx/fr/worklist.json`, SHA-256 `ef9d5709b061ea426c2e113373fdbfde547c6518f6394a4afc325204dea89cf8`; 1,947 authoring IDs and embedded 27-case index. Ignored run artifacts are not durable archival evidence: regenerate using the documented README command if missing. No wording was authored.

## Feasibility

`localization/evidence/multilingual-renderer-baseline-20261110.md` reports the French synthetic sample resolving without substitution in a live save-slot component on both pinned builds, with the stock font chain. This is not a dialogue, choice, settings, full-corpus or visual pass. `localization/evidence/european-text-paths-20261110.md` exercises those paths using Ukrainian, Polish and Vietnamese, not French. The corresponding settings frames are offscreen controls, not French visual evidence; dialogue and choice pixels were not inspected. French rendering feasibility remains **unverified**. Native Windows remains separately unverified; prior Windows evidence uses CrossOver.

Next: use the existing paired sample/observer recipe and a French-specific synthetic set on both builds, covering accents and ligatures, dialogue reveal and progression, choices, settings, dynamic/narrow layout, and actual visual fit. Preserve original frames and inspect only policy-compliant WebP80 copies or source-bound crops. Acquire `localization/work/.dragons-cli-runtime.lock` via mkdir for the entire runtime test, do not remove another owner's lock or operate an owner process. Disk check showed 18 GiB available on the project volume; serialize large package work with that lock. The existing paired probe source and receipts are under `localization/work/european-text-paths-20261110.QddlnY/`; determine exact invocation and profile isolation before launching. Do not treat another script sample as French proof.

## Glossary readiness

CLI preflight reports 28/28 IDs structurally complete, not editorial acceptance. Historical French `glossary-reviews/fr/layer-1.md` and `layer-2.md` are two author self-reads of the earlier 27-entry hashes; the new anonymous-dragon entry was subsequently reviewed by the coordinator, without an independent reviewer (`localization/evidence/generic-dragon-entries-20261110.md`). Source historical reviews were also self-reviews. Reconcile exact affected evidence and current hashes before crediting any unchanged receipts. Independent editorial acceptance is **pending**: the user prohibits agents and no distinct authorized reviewer is available.

A preliminary direct comparison of all 28 current English/French entries found an objective candidate issue: `dnw-family-crest` translates the ornamental family emblem as “crête familiale”, which normally denotes a physical crest; “blason familial” is a candidate for adjudication against the actual source context. No SiteForMods file was changed and this is not an accepted glossary correction. Review source context, complete the source and French fidelity and separate native-language layers, record all findings and dependency closures, and obtain an authorized independent review. The current preliminary read is not a clean layer or a substitute for the full evidence-bound process. SiteForMods is read-only under this assignment; do not silently alter or approve the canonical glossary.

## Stage status

| Stage | Status |
| --- | --- |
| probe | Open: French dialogue, choices, settings, visual fit and progression lack matching evidence. |
| source | Pinned worklist generated; verify source/preserve-exact gate and current shared receipts before translation. |
| glossary | Open: identified candidate defect, source/target editorial reconciliation and independent acceptance pending. |
| special-scene decisions | 0/27 reviewed French decisions; begin only after applicable source and glossary gates. |
| translate-edit | 0/1,947 authored; `translation.json` does not exist. |
| editorial | Not run; full semantic audit, independent delta and regression catalog pending. |
| fonts | Slot sample only; full corpus and applicable real text paths unverified. |
| textures | Textures with text excluded and preserved. |
| package | macOS and Windows deliverables not built or verified. English passthrough is not a completed translation. |
| runtime / visual | French not run / not reviewed. |
| screenshot upload / review | Not requested / not run. |
| release / archival | Not complete; no publication, push or deployment authorized. |

Next work must respect fixed gates. If the shared glossary or probe needs changes outside `localization/fr/` and this run directory, report the exact boundary instead of modifying shared files. A verified locale-only commit requires the specified `.git/codex-canonical-commit.lock`, empty pre-existing index, complete staged review and committed-tree verification; do not reset, amend or interfere with other lanes.
