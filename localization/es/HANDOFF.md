# Spanish (Spain) localization checkpoint

2026-11-10. Scope: standard localization, site/runtime `es`, English source, macOS `9/12/2026_a93aa21a` and Windows `9/9/2026_ee944596`. Assigned session: `gpt-6.1-terra`, reasoning `high`, verified from `localization/work/cli-terra-high-20261110.J0KLrx/es/worker.json` and matching thread ID in `events.jsonl`. No other model or translator used.

## Current stages

| Stage | Status and boundary |
| --- | --- |
| scope | Established for this lane; textures-with-text, installed games and saves excluded from modification. |
| probe | **Passed for the bounded Spanish renderer cases.** Both isolated builds passed dialogue and choice review at the tested sizes. The matched CrossOver scroll control resolved the initial partial stock row. The 1280×960 macOS Options frame and its source-pixel crops verified the complete Spanish labels and marks. See [the independent frame review](../evidence/es-it-renderer-frame-review-20261110.md). Final corpus and native Windows checks remain separate. |
| source | Worklist exported for 1,947 paired IDs from both installed stock data directories, without modifying them. Shared inventory and Yarn scope hashes match the pinned values below. The export indexes known special scenes; the fresh stock component check in [source-baseline.md](source-baseline.md) verifies 10,973 macOS and 10,936 Windows exact component fields. The check does not establish candidate preservation or adaptation. |
| glossary | **Author self-review closure completed, not independent.** Two distinct historical source and Spanish layers cover the 27 unchanged entries; their per-entry source and locale hashes match. The new anonymous role and affected context were read separately for each layer; detailed receipts and findings are in [glossary-review.md](glossary-review.md). Both earlier suspected defects were resolved against the English scenes without changing the glossary. The owner explicitly permitted these self-reviews in this task. |
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
