# Spanish (Spain) localization checkpoint

2026-11-10. Scope: standard localization, site/runtime `es`, English source, macOS `9/12/2026_a93aa21a` and Windows `9/9/2026_ee944596`. Assigned session: `gpt-6.1-terra`, reasoning `high`, verified from `localization/work/cli-terra-high-20261110.J0KLrx/es/worker.json` and matching thread ID in `events.jsonl`. No other model or translator used.

## Current stages

| Stage | Status and boundary |
| --- | --- |
| scope | Established for this lane; textures-with-text, installed games and saves excluded from modification. |
| probe | **Passed for the bounded Spanish renderer cases.** Both isolated builds passed dialogue and choice review at the tested sizes. The matched CrossOver scroll control resolved the initial partial stock row. The 1280×960 macOS Options frame and its source-pixel crops verified the complete Spanish labels and marks. See [the independent frame review](../evidence/es-it-renderer-frame-review-20261110.md). Final corpus and native Windows checks remain separate. |
| source | Worklist exported for 1,947 paired IDs from both installed stock data directories, without modifying them. Shared inventory and Yarn scope hashes match the pinned values below. The export indexes known special scenes; the fresh stock component check in [source-baseline.md](source-baseline.md) verifies 10,973 macOS and 10,936 Windows exact component fields. The check does not establish candidate preservation or adaptation. |
| glossary | **Author self-review closure completed, not independent.** Two distinct historical source and Spanish layers cover the 27 unchanged entries; their per-entry source and locale hashes match. The new anonymous role and affected context were read separately for each layer; detailed receipts and findings are in [glossary-review.md](glossary-review.md). Both earlier suspected defects were resolved against the English scenes without changing the glossary. The owner explicitly permitted these self-reviews in this task. |
| translate-edit | **In progress:** 1,279/1,947 authored; 27/27 special cases have author-reviewed decisions and context. The special-scene entry reconciliation is recorded below. |
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

## Historical resume (superseded by later updates)

Verify current inputs and locale-layer hash. Use the existing authorized bounded review context for the new 1280×960 macOS Options capture recorded in [visual-review-handoff.md](visual-review-handoff.md); preserve originals and resolve the macOS mark uncertainty. The isolated runtime test exited and released its lock. Use the completed author self-review closure in `glossary-review.md`, revalidate the bound hashes and owner permission on resume. Once these entry gates are actually resolved, prepare all 27 source-bound special groups with full reviewed Spanish wording and feasible adapter contracts before ordinary translation. Keep stage status distinct; do not treat a source-passthrough package or structural checks as translation or visual acceptance.

## Text-only resume reconciliation

[visual-review-handoff.md](visual-review-handoff.md) records original and preview hashes, image dimensions, source-pixel full-frame bounds, exact synthetic strings and pending mark/fit judgments. The capture code confirms that the saved body frame is the 64-point control only; the 40-point control was logged but has no dedicated capture. All 13 special-scene registries and their 13 English source files matched the worklist hashes on resume. No screenshot was opened in this already image-bearing review context. Visual acceptance remains open, so the 27 groups and 0/1,947 authoring status are unchanged.


## Resume update: imported review and pending evidence

The coordinator-owned ledger `localization/work/es-it-renderer-review-20261110.vDBLoY/es/packet-only-ledger.json` records visual passes for dialogue and choice orders 1–4 and for Spanish marks/fit in CrossOver Options order 5. That order fails layout for a partly clipped stock-English `Target Framerate` at the bottom; its stock scrolling behavior and complete reachable row have not been established. Order 6 passes layout but leaves `Pingüino ¿qué?` and `Año, sí` marks and content uncertain. Preserve these findings rather than converting them to passes. The 40-point `¿Qué año?` runtime log establishes progression and glyph records, but not legibility at its distinct size; capture and review on both players remain required.

Two exact source-bound crops for the order 6 findings were prepared without image input in this context, as detailed in [visual-review-handoff.md](visual-review-handoff.md). A task-owned draft ScrollRect probe is at `localization/work/cli-terra-high-20261110.J0KLrx/es/resume-01/scroll-preparation/Probe.cs`; it has not been compiled or run. It dispatches a scroll event and records viewport/label geometry before and after, with separate captures. Validate it on source-matched stock and localized isolated fixtures at the same resolution; establish fresh profile/bottle identifiers, guarded process exit and restoration. The runtime lock was held by live Polish owner PID 31176 at last check, so no test copies or game processes were started. Recheck live ownership, disk space and ledger before continuing. Imported review does not waive pending gates or authorize authoring prematurely.

## Resume update: scroll and 40-point captures

The previous paragraph's draft/unrun statement is superseded. The task-owned probe compiled and ran on Windows through CrossOver against source-matched stock and synthetic Spanish settings at the same resolution. The initial Target Framerate label crosses a real vertical ScrollRect Mask boundary in both. Dispatching the Unity scroll handler moved the complete label geometry inside the viewport in both; this tests the handler, not a physical wheel. Stock and localized post-scroll originals and WebP80 previews, exact hashes, receipts and asset hashes are in [visual-review-handoff.md](visual-review-handoff.md). They have not been visually inspected in this context; coordinator review of the complete row and control remains pending. The logged 40-point `¿Qué año?` is a distinct body size and merits separate representative evidence; dedicated captures on both builds were produced and bound there, but still require visual review. All four isolated test runs exited, verified owner profile unchanged, remained in the background and released the Spanish runtime lock. No installed game or texture was modified.

The coordinator ledger was rechecked after these tests and still records order 5 layout failed and order 6 glyphs/content needs-review. Submit the new prepared previews and the two previously prepared macOS accent crops to the existing authorized bounded review context; do not duplicate its work. After the actual judgments resolve, reassess the probe gate. Until then, do not author special-scene or ordinary translation. Translation remains 0/1,947 and 27 special groups remain unreviewed; packaging, final runtime and independent game-text audit remain unrun.

At this checkpoint the new Spanish evidence updates remain uncommitted: `.git/codex-canonical-commit.lock` is held by live `pt-BR` owner PID 48328. Do not take over the lock. Once released, acquire it and verify `main`, an empty index and the complete Spanish-only staged diff before committing these two checkpoint files and verifying the committed tree.

## Resume update: imported passes and higher-resolution macOS capture

The coordinator's `scroll-ledger.json` SHA-256 `a119b2ba91d630df459f5e38c726fc02a87eb0bcb4027110f2d61c093d9c13da` passes both stock and synthetic Spanish CrossOver post-scroll frames, including the complete Target Framerate label and control. `body40-ledger.json` SHA-256 `c7cec02c5827e31bf303826536348c0dcf7de8424d07ee769cf4bede7610d071` passes both 40-point body frames. These visual results supersede earlier pending statements, but do not establish hardware wheel interaction or native Windows. `accent-ledger.json` SHA-256 `ab40c6dc9ecae06655e8c61a8f9a942de1156f5ee32eccc51b3fb31e17e5ac8d` leaves both 640×480 macOS accent crops needs-review.

A new isolated background macOS capture used an actual 1280×960 Unity render target and the same source-bound synthetic settings labels. The frame and no-upscale WebP80 preview, exact hashes, test identity and receipt are in [visual-review-handoff.md](visual-review-handoff.md). The test player exited, the original profile was unchanged and the runtime lock was released. Its pixels have not been reviewed here; send the prepared frame to the existing authorized bounded review context. Do not mark the remaining macOS mark findings passed before its actual judgment.

The broader source gate remains open even if the renderer clears: the shared paired-package resource audit identifies indirect runtime text consumers and additional resources still to reconcile, and incomplete field-level preservation inside 11 changed files. Reuse its bound findings; do not modify shared files. The 27 special scenes remain unreviewed and translation remains 0/1,947.

On this resume, the inventory, Yarn-scope and Spanish worklist SHA-256s were recomputed and still match the bindings above; the Spanish `rows` array contains 1,947 entries. This input check does not close the broader source gate.

## Resume update: accepted source and first special group

The shared source and exact-preservation authoring gate passed at canonical ancestor `15c330ef17ca031b547dae23af30f7315faa6d3e`, for the unchanged v42 fingerprints. See `localization/evidence/source-readiness-v42-20261110.md` and its reconciliation JSON (SHA-256 `c4a2587e6fa57ca27fef6e9244665340a848fb7ec5b4efd87a5dede88f85d7a7`). This supersedes all older source-pending statements above. The renderer pass and two author glossary self-review layers recorded above remain valid; self-review is not independent acceptance.

Created the paired `translation.json` from the pinned inventory and scope. The 20 direct IDs in `anonymous-dragon-address` have authored and self-reviewed Spanish wording; [special-anonymous-dragon.md](special-anonymous-dragon.md) records its decision, technical contract, scenarios and both stock object read-backs. Thus 20/1,947 entries have authored values (including one intentionally unchanged silence), and 1/27 special groups has a recorded author-reviewed decision. The remaining 26 groups must be fully authored and reviewed before ordinary scene translation; do not count blank template entries as translation. The structural object checks are not final artifacts.

Separate status: editorial authoring in progress; independent game-text audit not run; packages not built; final localized runtime and visual QA not run; delivery pending. Textures and owner saves remain untouched. The active session is `gpt-6.1-terra` with high reasoning, verified from the running Codex CLI arguments. Next, continue with another complete source-bound special group, preserving exact cases and using per-platform adapter validation and read-back. The Polish lane owns the cooperative runtime lock; inspect ownership before any game work and never take it over.

### Typography batch

Three further cases are author self-reviewed with exact target wording, adaptation contracts and positive/negative acceptance scenarios in [special-typography.md](special-typography.md). Four additional IDs passed per-platform source and object encode/parse checks; negative staged-region checks rejected the intended defects. Current total: 24/1,947 authored IDs and 4/27 recorded special decisions. The 23 remaining cases still block ordinary batches. Package, final runtime/visual and independent editorial audit remain pending.

### Alexander dialogue batch

Four more special decisions and 33 direct IDs are author self-reviewed in [special-alexander-dialogue.md](special-alexander-dialogue.md), with both stock-source object read-backs and their hashes. The build-specific typo is bound to separate platform fields. Current total: 57/1,947 authored IDs and 8/27 special decisions; the remaining 19 decisions precede ordinary batches. This is not an independent audit, a finished package, or final runtime/visual acceptance.

### Ryan and Alexander choice batch

Three additional special decisions and 13 IDs were author self-reviewed and checked against both stock objects in [special-ryan-and-alexander-choices.md](special-ryan-and-alexander-choices.md). One authored `no` is intentionally identical to its English source. Current total: 70/1,947 authored IDs and 11/27 special decisions. The remaining 16 decisions precede ordinary text. Final packages, exact-string visual and runtime checks, and the independent game-text audit remain pending.

### Ryan relationship batch

Two additional special decisions and 28 IDs are author self-reviewed in [special-ryan-relationships.md](special-ryan-relationships.md), with separate stock-source object read-backs. One pause is intentionally unchanged. Current total: 98/1,947 authored IDs and 13/27 special decisions. Fourteen special decisions remain before ordinary translation; final package, runtime/visual and independent editorial audit remain pending.

### Alexander question-state batch

The seven question labels and their once-state contract are author self-reviewed in [special-alexander-question-state.md](special-alexander-question-state.md), with both stock-source object read-backs and a source-mismatch negative check per build. Five labels are newly authored; two were already counted in previous groups. Current total: 103/1,947 authored IDs and 14/27 special decisions. Thirteen special decisions remain before ordinary text. Independent game-text audit, final packages and final runtime/visual checks remain pending.

### Alexander college introduction batch

The college introduction's nine direct IDs, two contextual lines and two unchanged speaker display names are author self-reviewed in [special-alexander-college.md](special-alexander-college.md). Both source-bound readers and dialogue object read-backs passed on both builds; a missing-colon negative control was rejected. Current total: 116/1,947 authored IDs and 15/27 special decisions. Twelve special decisions precede ordinary text. Independent game-text audit, final packages and final runtime/visual checks remain pending.

### Conrad wordplay batch

The dirty double meaning, professional double meaning and big-C nickname cases are author self-reviewed in [special-conrad-wordplay.md](special-conrad-wordplay.md). All 41 direct IDs passed source-bound readers and object read-back on both builds; an emptied progressive markup region failed the intended guard on each. Current total: 157/1,947 authored IDs and 18/27 special decisions. Nine special decisions precede ordinary text. Independent game-text audit, final packages and final runtime/visual checks remain pending.

### Ryan date and yip batch

The date wordplay, film choices, kobold vocalization and related film title are author self-reviewed in [special-date-yip.md](special-date-yip.md). Their 48 direct IDs and one earlier glossary-spelling correction passed both source-bound readers and object read-backs; an introduced film-title colon was rejected at the intended delimiter guard on both builds. Current total: 205/1,947 authored IDs and 22/27 special decisions. Five decisions precede ordinary text. Independent game-text audit, final packages and final runtime/visual checks remain pending.

### Conrad euphemisms batch

The special endings and height euphemism cases are author self-reviewed in [special-conrad-endings-height.md](special-conrad-endings-height.md). Their 42 direct IDs passed both source-bound readers and object read-backs, and an empty progressive region failed the intended guard on each build. Current total: 247/1,947 authored IDs and 24/27 special decisions. Three decisions precede ordinary text. Independent game-text audit, final packages and final runtime/visual checks remain pending.

### Transition and display batch

The final three indexed cases have author decisions and source-bound checks in [special-transitions-displays.md](special-transitions-displays.md). Five display/UI IDs and eight continuation dialogue IDs were authored and read back on both builds. Current total: 260/1,947 authored IDs and 27/27 indexed cases with author decisions. Reconcile the full special-scene dependency groups before declaring the locale entry gate passed: direct-ID coverage alone does not establish that every clue, answer, feedback and related wording is authored. Ordinary translation has not started. Independent game-text audit, final packages, normal-play transition completion and final runtime/visual checks remain pending.

### Alexander question-branch dependency closure

Completed 52 additional authored IDs, bringing the locale to 312/1,947. All 77 source-bound IDs in the Alexander question groups and shared exit now have self-edited wording, including all nested choices and outcomes; see [the decision and paired read-back receipt](special-alexander-question-state.md). The 27 indexed decisions are recorded, but broader special-case dependency review remains in progress before the ordinary translation gate. Independent game-text audit, final localized runtime/visual QA and final packages remain pending.

### Ryan date dependency closure

Completed 15 remaining date-node IDs: all four date options and their continuations now have self-edited wording. The locale contains 327/1,947 authored IDs. Both-platform source-bound object read-back and negative-source controls are recorded in [the date decision](special-date-yip.md). The wider special-case dependency review continues before ordinary batches; the independent game-text audit, final packages and final runtime/visual QA remain pending.

### Alexander romance dependency closure

Completed 39 additional context IDs for the invitation, choices and outcomes; all 41 indexed IDs in that group have self-edited wording and paired source-bound object checks. See [the decision and receipt](special-ryan-and-alexander-choices.md). Current authored total: 366/1,947. The broader special-case dependency review continues before ordinary batches; independent audit, packaging and final localized runtime/visual QA remain pending.

### Continuation: Alexander gate and Conrad route closure

Authored 54 additional stable IDs in the complete `Alexander_4_intro` and `Conrad_Outro_3` scenes; total **420/1,947**. All 27 special decisions remain author-reviewed, while their remaining dependent wording still needs reconciliation before ordinary batches. The gate exchange, three Yip meanings, both Conrad route outcomes and follow-ups are now complete. Both stock platform readers accepted all 63 IDs in these two scenes; object encoding/parse and negative English-source mismatch checks passed. Receipt and object hashes are in `special-date-yip.md`; scripts and partials are under `work/cli-terra-high-20261110.J0KLrx/es/resume-09/branch-closure/`. Translation SHA-256 at this checkpoint: `4bba5cd525eea554d02c36e8f2f80d826a312ad49e90622f6011eb8dca2e7015`. These checks are author self-review and in-memory read-back, not the independent game-text audit or final package/runtime/visual QA.

### Continuation: professor correction context

Added 13 stable IDs to complete all 19 entries of `Alexander_1_intro`; **433/1,947** stable IDs are authored, counting a platform-specific entry only when both targets are nonempty. Both stock dialogue readers, object encode/parse and altered-English negative guards passed. One source line differs by the English spelling `regrettable`/`regretable`, with explicitly paired targets. See `special-alexander-dialogue.md`; task-owned evidence is in `work/cli-terra-high-20261110.J0KLrx/es/resume-09/professor/`. Translation SHA-256: `8c97d1514a075f809dac7fd06a673400c78cd35098a3fc4fb334f06e85e292f6`. The special-scene dependency reconciliation, independent audit, package and final runtime/visual checks remain open.

### Continuation: Conrad greeting context

Added 16 stable IDs to complete both emphatic-greeting scenes, `Conrad_Intro_1` and `Conrad_5_intro_ryan_romanced`. Current authored total: **449/1,947**. Both platform source readers and object encode/parse passed for all 18 IDs, and altered-English negative checks were rejected on each build. The source-bound platform-specific apostrophe variant is retained. Receipt: `special-typography.md`; task-owned evidence: `work/cli-terra-high-20261110.J0KLrx/es/resume-09/greetings/`. Translation SHA-256 `acd01b7730c7f34d9fdad0bfaf622df3ad46148956afc2f2bb6d182e9731bfd4`. Further special-scene dependencies, independent editorial audit, packaging and final localized runtime/visual QA remain open.

### Continuation: Conrad scales and relationship states

Added 53 stable IDs, completing all 54 `Conrad_Intro_4` entries and the three relationship-state alternatives surrounding the italic scales aside. Current authored total: **502/1,947**. Both platform source readers and object encode/parse passed; altered-English negative inputs were rejected at the source guard on each platform. Details and hashes: `special-typography.md`; task-owned evidence: `work/cli-terra-high-20261110.J0KLrx/es/resume-09/scales/`. Translation SHA-256 `199e05b156ac8109ce6b45f4a6d51fad438b4badead34e70bdbcf1332f984ac8`. Remaining special-scene dependencies must be reconciled before ordinary batches; independent editorial audit, packages and final localized runtime/visual QA remain open.

### Continuation: Ryan food and relationship context

Authored 89 additional IDs to complete all 111 entries of `ryan_food_dialogue`, including the relationship options, their follow-ups and Conrad's height euphemism. Current total: **591/1,947** authored IDs. Both stock platform source readers and in-memory object encode/parse passed; altered-English negative checks were rejected on both builds. Receipt and object hashes: `special-ryan-and-alexander-choices.md`; task-owned evidence: `work/cli-terra-high-20261110.J0KLrx/es/resume-09/food/`. Translation SHA-256 `5914a4ee636a3e2bda20d9f34c716b099aa052403605aa483e1e076c93f3ed96`. Reconcile remaining special-scene dependencies before ordinary batches. Independent editorial audit, final packages and localized runtime/visual QA remain open.

### Continuation: Yip scene contexts

Authored 109 additional IDs across eight complete Yip-related scenes; **700/1,947** IDs now have authored values. Both platform readers accepted all 119 scene IDs, object encode/parse passed, and altered-English negatives failed at the source guard on both platforms. Details and object hashes are in `special-date-yip.md`; task-owned evidence is under `work/cli-terra-high-20261110.J0KLrx/es/resume-09/yip/`. Translation SHA-256 `86d8c95880fb37a5d6ed3a2d9a98fa4ff387bb1e223168d1f40f0858f4aeb029`. Complete remaining special-scene dependency reconciliation before ordinary batches. Independent audit, final packages and localized runtime/visual QA remain pending.

### Continuation: Ryan introduction and remaining Yip context

Authored 48 IDs in `Ryan_5_intro` and the final Yip-associated exchange, bringing the locale to **748/1,947**. The full 49-ID set passed both platform source readers and in-memory object read-back; altered English was rejected for both. See `special-date-yip.md` and task scratch `work/cli-terra-high-20261110.J0KLrx/es/resume-09/ryan5/`. Translation SHA-256 `91c003bf232a5f65d9757e0c49a1dab08401c169044dac87f48a3e9c9dc89fe8`. All indexed Yip context has wording; remaining romance-routing contexts require reconciliation before ordinary batches. Independent audit, final packages and localized runtime/visual QA remain open.

### Continuation: Alexander relationship-state dialogue

Authored 47 IDs in `Alexander_5_intro` and `Alexander_5_required`, for **795/1,947**. Both platform source readers and in-memory object read-back passed; altered-source negatives were rejected on both. See `special-ryan-relationships.md` and `work/cli-terra-high-20261110.J0KLrx/es/resume-09/alex5/`. Translation SHA-256 `62013be64200d01d5904309019ed5137b2df42457649c3b8c68cc524cfcc93e1`. Remaining relationship-state context reconciliation precedes ordinary batches. Independent audit, packages and final runtime/visual QA remain pending.

### Continuation: Conrad fourth-visit relationship alternatives

Authored 65 IDs across four complete Conrad fourth-visit relationship scenes, for **860/1,947**. Both stock platform source readers and in-memory object read-back passed; altered English was rejected on both. See `special-ryan-relationships.md` and task scratch `work/cli-terra-high-20261110.J0KLrx/es/resume-09/conrad4/`. Translation SHA-256 `82a1c15d2ec5e019d1cf80552bcf7d7d76f956e5cbd8235f9e68408669e2a525`. Reconcile remaining relationship-state context before ordinary batches. Independent audit, packages and final runtime/visual QA remain pending.

### Continuation: Ryan fifth-visit relationship outcomes

Authored 81 IDs across five complete Ryan relationship-state scenes, for **941/1,947**. Both stock platform readers and in-memory object read-back passed; altered-English inputs were rejected on both. See `special-ryan-relationships.md` and task scratch `work/cli-terra-high-20261110.J0KLrx/es/resume-09/ryanroutes/`. Translation SHA-256 `435f904515780984c3fbd3c562831a7fd66815bd535c83b77198652ac4d832d3`. Reconcile remaining relationship-state context before ordinary batches. Independent audit, packages and final runtime/visual QA remain pending.

### Continuation: Conrad fifth-visit relationship dialogue

Authored 75 IDs across five complete Conrad relationship-state scenes, for **1,016/1,947**. Both stock platform readers and in-memory object read-back passed; altered-English inputs were rejected on both. See `special-ryan-relationships.md` and task scratch `work/cli-terra-high-20261110.J0KLrx/es/resume-09/conrad5/`. Translation SHA-256 `eefa4a9cfb6055f3935ddab4cf53cfeb5e8cb8cfa0afe39e54854299a42facf8`. Reconcile remaining relationship-state context before ordinary batches. Independent audit, packages and final runtime/visual QA remain pending.

### Continuation: remaining indexed relationship context

Authored the remaining 68 indexed relationship-context IDs across eight scenes, for **1,084/1,947**. Both stock platform readers and in-memory object read-back passed; altered-English inputs were rejected on both. See `special-ryan-relationships.md` and task scratch `work/cli-terra-high-20261110.J0KLrx/es/resume-09/relationship-last/`. Translation SHA-256 `7f7e9f40854a4d6c63812a3e44706386cd7b909ff09b8cbc11425b9d90b1393d`. A worklist scan finds no empty in-scope direct/context targets for the 27 special cases; reconcile the marker and managed-code exclusions and decision receipts before declaring the editorial entry gate passed. Independent audit, packages and final runtime/visual QA remain pending.

### Special-scene entry reconciliation

All 27 decision receipts and all editable direct/context IDs were reconciled against the pinned worklist; the exact marker, managed-code and protected UI exclusions are classified in [special-index.md](special-index.md). The authoring entry gate is satisfied; ordinary scene batches may proceed. This is author self-review and source-bound feasibility, not independent editorial acceptance. Current total remains **1,084/1,947**; translation SHA-256 `7f7e9f40854a4d6c63812a3e44706386cd7b909ff09b8cbc11425b9d90b1393d`. Independent game-text audit, final packages, normal-play transition verification and final localized runtime/visual QA remain pending.

### Ordinary scenes: Alexander and Ryan

Authored 41 IDs in the complete `Alexander_2_intro` and `Ryan_1_PhoneTutorial` scenes, bringing the total to **1,125/1,947**. Both stock source readers, in-memory object read-backs and altered-English negative checks passed; hashes and author decisions are in [ordinary-scenes.md](ordinary-scenes.md). Translation SHA-256 `f6e8bca50f1912bf7e261de968f5b5bcc204f68393055bf997e9047e25cb3a26`. Independent audit, final packages and final localized runtime/visual QA remain pending.

### Ordinary scenes: Alexander departure and return

Authored 54 IDs in `Alexander_2_Outro` and `Alexander_3_intro`; **1,179/1,947** are authored. Both platform source readers, object read-backs and altered-English negative guards passed; see [ordinary-scenes.md](ordinary-scenes.md). Translation SHA-256 `61f8f2046cfd6e32cdaf8d4cecfe907d0297759329c8b75cb1fef3554c941083`. Independent audit, final packages and localized runtime/visual QA remain pending.

### Ordinary scenes: Alexander fourth visit

Authored 47 IDs in `Alexander_4_required` and `Alexander_4_Outro`; **1,226/1,947** are authored. Both platform source readers, object read-backs and altered-English negative guards passed; see [ordinary-scenes.md](ordinary-scenes.md). Translation SHA-256 `24b58c8e41d2697c4d8d6858f6743b860d80ec885786d766131a0c6f741079f2`. Independent audit, final packages and localized runtime/visual QA remain pending.

### Ordinary scenes: Conrad equipment and injury

Authored 53 IDs in `Conrad_Intro_3` and `Conrad_required_2`; **1,279/1,947** are authored. Both platform source readers, object read-backs and altered-English negative guards passed; see [ordinary-scenes.md](ordinary-scenes.md). Translation SHA-256 `fbeb0a2123c745fb9260fc14dcf90fafdf137f46de654f152b4f4430d8136559`. Independent audit, final packages and localized runtime/visual QA remain pending.
