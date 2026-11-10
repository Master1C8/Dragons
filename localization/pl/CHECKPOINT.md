# Polish localization checkpoint

2026-11-10. Standard localization, `pl`; supported macOS `9/12/2026_a93aa21a` and Windows `9/9/2026_ee944596`. Session metadata and run `worker.json` report `gpt-6.1-terra`, reasoning `high`. No delegated reviewer was authorized.

## Current gate and coverage

First unpassed stage: shared/locale renderer feasibility and standard glossary editorial readiness. Do not start special-scene wording or ordinary translation until their prerequisites are established. No Polish game translation has been authored: **0 / 1,947 package IDs**. No `translation.json` exists. The 27 special groups have **0 / 27 Polish wording decisions reviewed**. Independent glossary and game-text editorial acceptance is pending; self-review is not independent.

The stock font sample resolved Polish glyphs on both builds. The paired European text-path evidence exercised Polish choice samples and settings labels on both players; its dialogue-body samples were Ukrainian and Vietnamese, not Polish. The offscreen settings frames show Polish fit, but the macOS final accent was too small to certify; Windows was legible. Polish dialogue, choice pixel inspection and the unresolved macOS setting mark remain open, as do corpus-bound fit, native Windows and final visual checks. See `localization/evidence/multilingual-renderer-baseline-20261110.md`, `european-text-paths-20261110.md` and `european-settings-visual-20261110.md`. No runtime was launched in this session.

## Bound inputs

- Dragons starting HEAD `8f800bca8620dc7a4430e5882c95f005cca0a08a`; other authorized workers may advance main.
- Source inventory SHA-256 `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`; Yarn scope `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30`.
- SiteForMods HEAD `29b0bb56b3ce71a1d5a700c840b050af7333084d`; canonical parsed English fingerprint `3d261921e114b6feab10f57ad54d43674a75e991d94937686155b92cce399dc3`; source JSON bytes `24f51ad99f3b78ef06e1ba8ebefb2ab9072c866f4860fe9839055b504ead8baf`.
- Entire translations file bytes `b49c48fb84eae01921070c11267706a3bd036f1d9b13a4f57e1a87a7144b672e`; Polish map SHA-256 `1ab12ce29b28b65231fd03959fa51a32a8d81d3ac3e92a17e78794640b49d56a`, UTF-8 `json.dumps(map, ensure_ascii=False, sort_keys=True, separators=(',', ':'))`, no newline.
- Paired source-only worklist `localization/work/cli-terra-high-20261110.J0KLrx/pl/worklist.json`, SHA-256 `867bd3ee2e086876c1089576f966df8c548915bcd2a68dc35f87852dce960f87`, exported against both stock Data directories. No source passthrough is counted as translated.
- Special index `localization/work/cli-terra-high-20261110.J0KLrx/pl/special-index.json`, SHA-256 `ff3ea673c4f6bba76ffd98cdc695156312da224b265ae18efc4d2e9e9a452d2b`; 27 cases, 271 distinct direct IDs, 1,126 direct/context IDs. Recreate with `python3 -B localization/index_special_scenes.py --inventory localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json --output <new path>`.

## Glossary review status

CLI preflight found 28 matching, nonempty IDs; this is structural only. One initial comparison read all 28 English and Polish term/meaning pairs; it is not a complete clean editorial layer. Source evidence, all scene dependencies, separate complete native-language read, repair closures and the required clean layers remain to be completed. The latest anonymous-dragon addition's recorded affected read had no independent reviewer (`localization/evidence/generic-dragon-entries-20261110.md`). The English and Polish layers are not independently accepted on these hashes.

Concrete questions to resolve against English scenes and the technical consumer: `dnw-family-crest` Polish term `rodowy grzebień` may suggest a physical comb/crest instead of the source's ornamental family emblem; check the exact scene before proposing wording. `dnw-yip-man` contains a colon in the Polish film title; the Yarn speaker parser uses colon syntax, so assess the actual title's choice/dialogue consumers and choose a technically safe rendering through the authorized glossary process. These are findings for review, not accepted corrections. SiteForMods is read-only for this task; no shared glossary was changed.

## Next actions and separate status

1. Recheck the source and glossary hashes, evidence and universal stage contract. Complete source and Polish glossary editorial reads and source-bound findings; retain independent acceptance as pending unless a distinct reviewer is authorized. Do not mutate the shared glossary in this lane.
2. Run applicable Polish dialogue and choice probes and inspect compliant previews, including the source-pixel macOS settings crop as needed. Use the shared runtime mkdir lock for the entire isolated test; preserve owner games, installations and saves. Distinguish CrossOver from native Windows.
3. Once prerequisite gates permit, make and review all 27 source-bound special-scene decisions, preserve syntax, then translate complete contextual batches from the English worklist. Checkpoint and commit only locale-owned files under the canonical Git lock.
4. Editorial: pending. Packaging: not built on either platform. Runtime: Polish final payload untested on both platforms. Visual: pending. Installation/restoration: pending. No publication/deployment authorized.

Export prerequisite note: system Python lacked UnityPy; the existing `/private/tmp/dragnwash-unitypy-venv/bin/python` lacked fontTools and TypeTreeGeneratorAPI. Cached `fonttools 4.60.2` and `TypeTreeGeneratorAPI 0.0.10` were installed only under this lane's ignored `python-deps` directory, and the exporter succeeded using `PYTHONPATH` pointed there. No shared environment was changed. Available disk at preflight was 18 GiB; serialize large package work as instructed.
