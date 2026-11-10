# French localization checkpoint

Updated 2026-11-10. Status: **glossary author layers reconciled; bounded renderer probe complete; all special-scene decisions prepared; reconciled source gate passed; ordinary authoring in progress**. See [glossary review](glossary-review.md) and [renderer probe](renderer-probe.md) for the current resumption; historical notes below retain the earlier checkpoint context. The requested standard locale is `fr`; source is English. Session `01a1c394-a809-7812-9570-df379360d954` turn context and process arguments record `gpt-6.1-terra`, reasoning `high`. No other model or agent was used.

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
| source | Passed for the pinned v42 inputs at `15c330ef17ca031b547dae23af30f7315faa6d3e`; see `localization/evidence/source-readiness-v42-20261110.md` and its reconciliation receipt. Earlier provisional assessments are superseded for those exact fingerprints. |
| glossary | Two author self-review layers reconciled on current hashes under the owner exception; the earlier crest finding was withdrawn after scene review. Independent review was not claimed. See glossary-review.md. |
| special-scene decisions | 27/27 groups have author-reviewed draft wording and feasible technical candidates. The anonymous group retains a direct-entry fixture boundary. The reconciled source gate now permits ordinary authoring. See special-scenes.md. |
| translate-edit | 278/1,947 authored: 258 special-scene and display IDs plus 20 ordinary Alexander first-visit IDs, including intentional exact vocalizations and ellipses. Paired diagnostic assets verified; author self-review only. |
| editorial | Not run; full semantic audit, independent delta and regression catalog pending. |
| fonts | Slot and bounded live text samples resolved; full corpus coverage and typography remain unverified. |
| textures | Textures with text excluded and preserved. |
| package | macOS and Windows deliverables not built or verified. English passthrough is not a completed translation. |
| runtime / visual | Bounded synthetic French controls run and reviewed; actual authored scenes and exact display strings remain unrun / unreviewed. |
| screenshot upload / review | Not requested / not run. |
| release / archival | Not complete; no publication, push or deployment authorized. |

Next: continue ordinary translation by coherent English-source scenes from the paired worklist, self-edit and validate both builds per batch. The source gate passed for the exact fingerprints above; do not generalize that receipt to changed source inputs. The buzzing failure remains an English direct-entry fixture limitation, not a passed natural-play test. Keep game runtime and visuals, full-corpus audit and delivery gates separate. Use the cooperative commit lock and locale-only scope.

## Source gate and first ordinary batch, 2026-11-10

The shared source readiness receipt at `localization/evidence/source-readiness-v42-20261110.md` and its JSON reconciliation receipt SHA-256 `c4a2587e6fa57ca27fef6e9244665340a848fb7ec5b4efd87a5dede88f85d7a7` bind the unchanged inventory, Yarn scope and French worklist hashes above and supersede the earlier open gate for these exact inputs. Canonical commit `15c330ef17ca031b547dae23af30f7315faa6d3e` is an ancestor of the current main. The 27 indexed groups were checked: all direct IDs in the authoring worklist are authored; the remaining direct IDs identify protected exact markers and underlying display occurrences represented by paired package IDs. Existing scene decisions retain their documented technical candidates and runtime limitations.

The first ordinary batch adds 20 IDs across `Alexander_1_intro`, `Alexander_1` and `Alexander_1_Outro`, completing the available worklist entries in these nodes while preserving previously reviewed lines. The author compared the paired English values, both choices and the professor correction, read the French in scene order, and explicitly shared one punctuation/spelling-only source variant. This is self-editing, not an independent audit. Both paired readers accepted all 278 IDs, including 270 Yarn values. Reopened partial assets match all 1,839 ordered Yarn values and metadata: 270 authored and 1,569 untouched for each build. macOS asset SHA-256 `afa75d489f12c189c0fc5354db7839263b902e72bac1559fa3096b25a092b517`; Windows `2f7d22e8a738048b12d3c7be05998ef2bf9d43d9007b940849e9cd2e065f4ee2`. Scratch scripts, paired locale files and partial assets are under `localization/work/cli-terra-high-20261110.J0KLrx/fr/resume-03/`. These are diagnostic readbacks, not deliverables. Translation SHA-256 `6097c4a230af0bd197fa8b2b4935d6556cb098d3fe07cf91afda660f56c20a38`. Actual French playback, branches, fit, final packages and independent audit remain pending.


The Alexander register/professor batch has author-reviewed wording and paired 43-entry macOS/Windows partial asset readbacks; see special-scenes.md for hashes and limits. At that checkpoint the buzzing finish-command boundary awaited an unmodified-English comparison; the later macOS control below classifies the direct-entry fixture limitation, while natural entry remains unverified. CrossOver is not native Windows evidence.

The college self-introduction batch adds nine scene IDs and two speaker-name IDs, with 51-entry paired Yarn readbacks and separately built speaker adapters; see special-scenes.md for exact hashes, the protected colon line and unrun scene checks. The overall translation hash is `f80b8eea2113edee81ec7340a05fa5fb9209798000bf42400001570a46b32efc`.

The family-crest draft adds ten scene IDs and preserves the seven source size tags; paired partial readbacks cover 61 Yarn entries. Its long, progressively shrinking line still requires actual French scene and visual review. Current translation SHA-256: `2420c6a0260f3fc3e8144b7ae5319f21b3108b94e83f30c321ba61da8cc06df6`.

Three typography groups add four scene IDs; both partial readbacks check 65 Yarn values with untouched tags and metadata. Scene-specific typography, fit and runtime remain open. Current translation SHA-256: `64c9f686b397a7d253eb64e3ac7408e83ee2b477cf96418bca635b303e47732d`.

The relationship and editor-question groups add ten scene IDs and paired 75-Yarn-entry readbacks. Source route reachability and scene-specific outcomes and fit remain unverified. Current translation SHA-256: `3abdf969d15f8cccab3d6a4607d6613959fb4056e11489ba5dff73366acecfa8`.

The Yip speech and film-title batch adds 20 IDs, including intentional exact vocalizations, and paired 95-Yarn-entry readbacks. A dash preserves the approved film title without triggering implicit-speaker parsing. Scene playback, audio and fit remain unverified. Current translation SHA-256: `765e4d612dbb1cfd427501f7a0e5580b780b25b016968b0f0749039e5c81a2b4`.

The full-mouth and nickname groups add 22 IDs; paired asset readbacks cover 117 Yarn values. Branches, character presentation and visual fit still need actual scene checks. Current translation SHA-256: `6049fd5a18d7394b35199337ef6d215f543a89c58327a8fa6ea178c1c7f4f0fd`.

The overlapping salmon and movie-choice groups add 28 IDs; paired partial readbacks cover 145 Yarn values. Scene branches and French fit remain unverified. Current translation SHA-256: `9747f6b49e356d098b022ff5b27f8522db23592e40bdec7afaa4a7f6dd919168`.

The macOS unmodified-English direct-entry control now reproduces the buzzing finish failure after choosing `line:2f55b3aa`: `FinishDialogue $dragonName` is passed literally and cannot resolve its component. The control used the same historical direct-entry companion and active-dragon fixture route, with English expected text, a fresh `FRE3` profile, and the stock `sharedassets1.assets` SHA-256 `f8c5c51ac1b0cf151177c05ee1805e032cf62baf384bb664337a71b923bee7b8`. Receipt `resume-02/english-control/run3/result.json` SHA-256 `8704d02f3371bb9a3d91970720f785bc6282b3ef434e908f7eb35fc5f3af3e5e`, Unity log SHA-256 `7f8101ede79e5756d69b94efc93b87d3d79938d1687fff256ae2fde4ca964c09`. The isolated process exited, the original-profile comparison matched, the generated root Steam file was absent, all 71 sampled window states were `0 0`, and the signature verified before releasing the runtime lock. This is a reproducible English **direct-entry fixture limitation**, not proof of a natural-play source bug or successful French scene completion. The first attempt lacked a Unity library in the historical stripped copy; the second failed the launcher guard due to a missing copied Steam reference. Both exited before gameplay and are retained in `run` and `run2`; the third used a stock app clone and repaired those specific boundaries. No Windows English control or natural-entry check was run.

The Conrad height-euphemism batch adds 18 IDs and paired 163-Yarn-entry readbacks; both route playback and fit remain open. Current translation SHA-256: `0aa11944f37c39444b7352606ee16600ad4681880891fd3af149035e9dc9c69c`.

The Ryan relationship-question group adds 23 IDs, including its opening joke and distinct later replies. Paired readbacks cover 186 Yarn values on each build; scene playback and fit remain pending. Current translation SHA-256: `f8f23fd9ca0a3c2a9c12927cd76dd7a2abace7926c59b18489d4f00d45ee5329`.

The Alexander question-state group adds five labels to the two previously authored labels; paired readbacks cover 191 Yarn values. Source VM/save controls do not establish French gameplay or visual fit. Current translation SHA-256: `66835f1116c9fa892b8a40f4430f5cb211a459eea4100456435c05c4d63fa4c1`.

The Conrad dirty/professional wordplay groups add 27 IDs. Both partial readbacks cover 218 authored Yarn values; scene playback, fit and independent audit remain open. Current translation SHA-256: `dd438d8d6f119f3e149ea113aea3a585778fcc521ec3a4bf0f8bb4a19bf15515`.

Conrad’s special-endings group adds 24 IDs. Both partial readbacks cover 242 authored Yarn values; playback and fit remain pending. Current translation SHA-256: `aeb92f076d7c740f9c28d9a40bb1dfe0d90a718b8b67d907d316c7078fe16ab0`.

The missing-destination group adds eight continuation IDs and preserves all 15 exact markers. Existing controlled repair evidence establishes a feasible route but not ordinary-play completion. Both partial readbacks cover 250 Yarn values. Current translation SHA-256: `d153aa24bb50ec84c01ed9c55f43bf23d3ddd6d40b8f2f56499e1412a4118290`.

The two final special-scene groups add five paired IDs for new slots and missing-line fallback. Managed method-body checks and separate UI asset readbacks passed for both pinned builds; exact evidence and limits are in special-scenes.md. Current translation SHA-256: `d62cc7de3c68353e3416091ef9df05e6ddafb23243244d1dd64c321c0b7e9e92`. At that historical checkpoint the complete source preservation gate was still open; it has since passed for the reconciled fingerprints as recorded above.
