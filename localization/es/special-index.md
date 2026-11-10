# Special-scene source index — Spanish lane

Source-only preparation against `localization/work/cli-terra-high-20261110.J0KLrx/es/worklist.json`, SHA-256 `8d172ebe8165344df8e705ce041ee57ecba1fb6c9179bbead5fe3ee7975eb7ec`. It indexes 27 cases, with 271 distinct direct source identifiers and 1,126 distinct direct-plus-context identifiers. These are source references, not completed translation counts.

Of the 271 direct identifiers, 246 match authoring IDs directly; 15 are exact-only Yarn marker IDs and 10 are platform-specific managed literal occurrence IDs. The six `MenuSlotsNew` occurrences map to the paired `display:slot-new` input; the four `LocalizedLine` occurrences map to `display:yarn-missing-line`. They must not be invented as separate editable translation IDs. Their source roles and expected literal preservation remain governed by the shared inventory and package adapters.

Twenty-five worklist rows have differing English source between platforms; seven are direct IDs in these groups: `yarn:line:73e4789c`, `yarn:line:266836f8`, `yarn:line:43dd32f5`, `yarn:line:5a195ff2`, `yarn:line:d38c63ea`, `yarn:line:a0cb3f78`, `yarn:line:36fb380f`. These seven have spelling or punctuation differences, and their exact source bindings remain platform-specific. Shared wording requires contextual review, not automatic merging.

No target wording or decision is accepted here. All 27 complete groups still need Spanish wording, scene-specific review and a feasible technical contract after the renderer gate. Preserve branching, original IDs, markup and intentionally unlocalized exact markers.
