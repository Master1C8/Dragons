# Special-scene source index — Spanish lane

Source-only preparation against `localization/work/cli-terra-high-20261110.J0KLrx/es/worklist.json`, SHA-256 `8d172ebe8165344df8e705ce041ee57ecba1fb6c9179bbead5fe3ee7975eb7ec`. It indexes 27 cases, with 271 distinct direct source identifiers and 1,126 distinct direct-plus-context identifiers. These are source references, not completed translation counts.

Of the 271 direct identifiers, 246 match authoring IDs directly; 15 are exact-only Yarn marker IDs and 10 are platform-specific managed literal occurrence IDs. The six `MenuSlotsNew` occurrences map to the paired `display:slot-new` input; the four `LocalizedLine` occurrences map to `display:yarn-missing-line`. They must not be invented as separate editable translation IDs. Their source roles and expected literal preservation remain governed by the shared inventory and package adapters.

Twenty-five worklist rows have differing English source between platforms; seven are direct IDs in these groups: `yarn:line:73e4789c`, `yarn:line:266836f8`, `yarn:line:43dd32f5`, `yarn:line:5a195ff2`, `yarn:line:d38c63ea`, `yarn:line:a0cb3f78`, `yarn:line:36fb380f`. These seven have spelling or punctuation differences, and their exact source bindings remain platform-specific. Shared wording requires contextual review, not automatic merging.

At initial preparation no target wording or decision had been accepted here; the subsequent author reconciliation below supersedes that status. Preserve branching, original IDs, markup and intentionally unlocalized exact markers.

## Registry integrity on resume

All 27 named case indexes and all 13 referenced registries and their 13 referenced English source evidence files match the SHA-256 values embedded in the bound worklist. This read-only check establishes provenance, not target wording or technical acceptance. At this historical checkpoint the two captures per platform covered one selected choice and the 64-point body; subsequent reviewed 40-point captures are recorded in the handoff. See [visual-review-handoff.md](visual-review-handoff.md).

## Author reconciliation of all 27 cases

All 27 indexed cases have author-reviewed wording, context and feasible technical decisions in the linked `special-*.md` receipts. The bound scan `work/cli-terra-high-20261110.J0KLrx/es/resume-09/reconcile/receipt.json` (SHA-256 `e15c3d958c5f509be00f88884e63d02ffc1f59ad11c0bd489bf06b1a723b9855`) found no empty in-scope direct or context target and identifies the decision file for each case. The scan is a coverage check, not editorial acceptance by itself; scene decisions and paired positive and negative checks are recorded in the individual receipts.

The outside-worklist references are deliberately classified: 15 exact-only Yarn markers, 18 managed slot references and six protected UI context references, plus six managed fallback references and one protected UI context reference. The editable managed outputs are `display:slot-new` and `display:yarn-missing-line`; the three source-bound serialized slot labels have separate target IDs. The [transition and display receipt](special-transitions-displays.md) records the preservation and patch contracts. No marker or protected context is silently treated as a translated value.

The special-scene authoring entry gate is satisfied for ordinary scene work, subject to the documented source-bound transition adapter in packaging. Author self-review does not replace the independent game-text audit, actual package read-back, ordinary-play transition checks or final localized runtime and visual QA.
