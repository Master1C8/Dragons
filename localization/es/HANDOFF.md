# Spanish (Spain) localization checkpoint

2026-11-10. Scope: standard localization, site/runtime `es`, English source, macOS `9/12/2026_a93aa21a` and Windows `9/9/2026_ee944596`. Assigned session: `gpt-6.1-terra`, reasoning `high`, verified from `localization/work/cli-terra-high-20261110.J0KLrx/es/worker.json` and matching thread ID in `events.jsonl`. No other model or translator used.

## Current stages

| Stage | Status and boundary |
| --- | --- |
| scope | Established for this lane; textures-with-text, installed games and saves excluded from modification. |
| probe | **Needs review.** Spanish sample glyphs resolved in the stock slot component on both players, per `localization/evidence/multilingual-renderer-baseline-20261110.md` (SHA-256 `50f9123194c565e9a91058a49344260d470c111d89c194abe86381c867375045`). This does not verify Spanish dialogue, choice, settings, visual fit or complete alphabet. The paired text-path and Options controls use Ukrainian, Polish and Vietnamese, not Spanish. Native Windows remains untested; Windows evidence uses CrossOver. No new runtime test was run. |
| source | Worklist exported for 1,947 paired IDs from both installed stock data directories, without modifying them. Shared inventory and Yarn scope hashes match the pinned values below. The export indexes known special scenes but does not prove the remaining source-classification/preservation gates or their adaptation. |
| glossary | **Needs review.** Structural CLI preflight says 28/28, no missing or empty entries; that is not editorial acceptance. Read all 28 English/Spanish entry pairs once for preliminary fidelity; this is not a complete clean coverage layer, does not review every concept use, and has no separate native-language pass. `dnw-family-crest`: `cresta familiar` risks a ridge/comb reading; source specifies an ornamental family emblem, for which `escudo familiar` is a candidate pending evidence and authorized glossary correction. Check `dnw-phoenix-feather`: `reconstrucción del cuerpo` adds body specificity absent from the glossary source; verify actual scene before adjudication. No shared glossary edits are authorized. Two complete clean source and target layers on current hashes, including independent acceptance by a distinct authorized reviewer, remain unverified. The latest anonymous-dragon entry's receipt explicitly says no independent reviewer participated. |
| translate-edit | **Not started:** 0/1,947 translated and edited. All 27 known special-scene groups need reviewed Spanish wording and feasible contracts after glossary readiness, before ordinary text. No `translation.json` exists. |
| editorial | Not run; independent reviewer unavailable under current no-agent instruction. |
| resources | Not run. Existing text-bearing textures are preserved; no texture production authorized in this lane. |
| package | Not run on either platform; no completed translated payload exists. |
| runtime / visual | Not run on either platform for Spanish deliverables. No owner game was operated or stopped. |
| screenshot-upload / screenshot-review | Not run; no upload authorized. |
| delivery | Pending all applicable gates and canonical integration of future verified work. No publication or deployment authorized. |

## Input bindings

- Shared v42 inventory `localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json`: SHA-256 `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`.
- Paired Yarn scope `localization/work/yarn-markers-20261110.ridbPA/yarn-scope-v42.json`: SHA-256 `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30`.
- Generated worklist `localization/work/cli-terra-high-20261110.J0KLrx/es/worklist.json`: SHA-256 `8d172ebe8165344df8e705ce041ee57ecba1fb6c9179bbead5fe3ee7975eb7ec`; includes source-bound special-scene index. Generated with pinned `localization/font_probe_requirements.txt` in this run's isolated venv; scripts do not generate wording.
- SiteForMods HEAD `29b0bb56b3ce71a1d5a700c840b050af7333084d`; previously recorded canonical English CLI parsed-source fingerprint `3d261921e114b6feab10f57ad54d43674a75e991d94937686155b92cce399dc3`. Raw English glossary SHA-256 `24f51ad99f3b78ef06e1ba8ebefb2ab9072c866f4860fe9839055b504ead8baf`; raw multi-locale file SHA-256 `b49c48fb84eae01921070c11267706a3bd036f1d9b13a4f57e1a87a7144b672e`. Spanish layer SHA-256 `3ddb6805226140429659f75367979afb69e06c55955dbe09c41a7b04bc3cf5cd`, computed over Python JSON `ensure_ascii=False, sort_keys=True, separators=(',', ':')`, UTF-8 without newline. Different serialization schemes yield different hashes.
- Process binding follows `localization/README.md` and `HANDOFF.md` shared fixed stage mapping. `ROUTING.md` SHA-256 `75fac761503c8cfdeee6281629fa158ce6661f8acaf02e225cee4a66861aa093`; `CHECKPOINT.md` `de6fcd0119aceda9edeed0850eaa659b10aaf8e7cfc7e7c22ce7c627c9849b25`; `EARLY-PROBE.md` `834ea4fe965447f00c59680d149fc1445fe08b8f042f30c99a0504354c9bc237`; localization prompt `68acfd48b4408a53af62bc0b021f355f25d089d784d417fe24f30fba3be935dd`; editorial protocol `37ff4269163b17cab4030c2d1c78651f7a79b9c8be3d569a2b9ea7f17748a5dc`.

## Resume

Verify current inputs and locale-layer hash. Establish Spanish-specific representative dialogue, choice, settings and visual feasibility using existing probes and the shared runtime lock, without affecting owner processes or saves. Reconcile complete source and Spanish glossary review evidence and the two findings above; correction of shared glossary and a distinct independent reviewer require authority unavailable in this assignment. Once these entry gates are actually resolved, prepare all 27 source-bound special groups with full reviewed Spanish wording and feasible adapter contracts before ordinary translation. Keep stage status distinct; do not treat a source-passthrough package or structural checks as translation or visual acceptance.
