# Brazilian Portuguese author audit handoff

Status as of 2026-11-10: the author has reviewed the 1,947 indexed source/target units in scene and interface batches, including choice routes, address and control text. The batch checkpoints record findings and evidence. This is an author semantic pass, not independent editorial acceptance. The 25 units with differing platform English were compared on both sides; their differences were spelling or punctuation variants with the same meaning. The fixed Yarn title is `Yip-Man - O Último Yip`. Texture content is outside this assignment; a complete text-bearing image-plan audit is not claimed.

## Bindings and verification

- Target: `localization/pt-BR/translation.json`, SHA-256 `b1e341f5338fc0c81e4af1e968a5b86acf3447330d726489cbc3ee89032b7311`; 1,947 authored IDs. Breakdown: 1,824 Yarn union IDs, 82 UI, 37 settings and 4 display IDs. Per-build Yarn binding count differs from the union.
- English v42 inventory SHA-256 `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`; Yarn scope SHA-256 `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30`. Source-readiness and preservation entry gate: `localization/evidence/source-readiness-v42-20261110.md` and its reconciliation receipt, bound to these inputs.
- SiteForMods English glossary semantic fingerprint `3d261921e114b6feab10f57ad54d43674a75e991d94937686155b92cce399dc3`; pt-BR compact stored-order map SHA-256 `6309cf331625336c510e6587ce3b35476301f242bfd63618ad01bfbd8b3966ad`. Two author self-review layers and their limits are in `glossary-review/`; they are not independent review.
- Final changed batch paired readback: `localization/work/cli-terra-high-20261110.J0KLrx/pt-BR/resume-10/ryan-rest-readback.json`, SHA-256 `52e312f6dce33bc4a02e945e8049630987dd79d355d88e41acd06f2dc34d7280`. It checked 1,947 source bindings on each stock build and the four changes of that batch. Complete Yarn reader receipt `ryan-rest-yarn-receipt.json` SHA-256 `072f3e02325c4e27a31e2f8d0303b5e26195f5a6bb13189e9fa620feaa0aba13`; temporary objects were reopened before removal. Individual earlier change receipts and reproducible commands are in `CHECKPOINT.md`. This is authoring-input readback, not final package readback.

## Effective correction cycle and next review

The baseline is the complete pre-audit draft from `git show a37584b:localization/pt-BR/translation.json`, SHA-256 `3b61a5413c81af7e9689a536d633f269846b45d31c44a5b3ab2cf2063c6d7d13`. The cumulative effective delta has 51 changed IDs and 947 selected closure IDs. Its component counts are 571 scene, 16 repetition, 0 explicit glossary/referent, 0 explicit runtime and 414 regression IDs, with overlaps; 55 protected context records are separate. Changed-ID list SHA-256 `8652fc71b8f98ab2036073284019f37b9f939329aba011009e24d16b5cb807bb`; closure-ID list SHA-256 `c37659516c0f1b70720e1c69b91819e692ec1eb913d2aafaaee25ab67cadd65b`. Lists and hashing conventions are recorded in the delta itself.

The committed candidate recipe `receipts/author-audit-recipe.json` has SHA-256 `84e2e698f372ff0102fbe59b76694b4d7a5a503e149be27da972b2734006e936`; its generated `receipts/author-audit-delta.json` has SHA-256 `8cbc0a7a8acaa4a13c9cb578be28bd2085638b2920f88237d9f3cc1463cb22fb`. The zero explicit glossary/referent and runtime components are not proof that no dependencies exist. Reconcile each effective edit against affected player-gender references, glossary concepts and actual consumer topology, including joined fragments and applicable image plans. Amend the selector/recipe and regenerate into a new immutable cycle if dependencies are missing; retain this candidate and its hashes. The reviewer must check the resulting full closure and mandatory regression catalog against English, glossary and actual context, then run the prescribed delta cycles until clean on unchanged hashes. The current author cannot supply the required distinct independent review under this assignment.

To reproduce this candidate in a fresh run-owned path, save the baseline with the `git show` command above, then run (the output path must not already exist):

```sh
base=localization/work/cli-terra-high-20261110.J0KLrx/pt-BR
PYTHONPATH="$base/deps" /private/tmp/dragnwash-unitypy-venv/bin/python localization/export_editorial_delta_with_regressions.py --locale pt-BR --inventory localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json --yarn-scope localization/work/yarn-markers-20261110.ridbPA/yarn-scope-v42.json --paired-scenes localization/work/source-inventory-20261107/yarn-paired-scenes.json --before "$base/resume-10/full-audit-before.json" --after localization/pt-BR/translation.json --recipe localization/pt-BR/receipts/author-audit-recipe.json --output "$base/resume-10/full-audit-delta-rebuilt.json"
```

## Separate outstanding gates

- Editorial: author text pass recorded; full independent dependency-aware diff/delta audit, complete dependency reconciliation and image-text inventory acceptance remain pending. A self-review is not independent acceptance.
- Artifacts: final macOS and Windows localized packages and their readbacks have not been built or accepted. Free space was 5.5 GiB at the last check and is shared; recheck capacity and cooperative runtime lock before any large build. Do not alter stock installations or textures.
- Runtime: prior synthetic pt-BR renderer feasibility passed for macOS and Windows under CrossOver, as documented in `renderer-evidence.md`; actual final localized packages and native Windows runtime have not passed. No game launch is authorized in this continuation.
- Visual: representative synthetic checks are not final translated-scene fit or full visual acceptance. Preserve screenshot originals and apply the workstation WebP80 preview policy when later authorized.
- Project delivery and source-only archival remain pending; no publication or deployment was authorized.

## Conservative dependency enumeration, subsequent author continuation

A new candidate retains the 51-change input and expands the explicit selector to the full 25 affected Yarn nodes and the IDs in special-scene decisions intersecting those nodes. This is intentionally conservative: membership does not assert that each scene line is a direct referent or consumer. It contains 571 scene, 16 exact-repetition, 571 explicit glossary/referent, 609 explicit runtime, and 414 regression target IDs; their union remains 947 target IDs, plus 55 protected context records. The lists and both platform source and target fields are in [the regenerated delta](receipts/author-audit-reconciled-delta.json). This candidate does **not** yet establish that cross-node implied referents and all downstream consumer dependencies are complete; it is not an independent audit.

The affected-node map is `localization/work/cli-terra-high-20261110.J0KLrx/pt-BR/resume-11/affected-node-map.json`, SHA-256 `fa05fdf1a278a9bd88e3c37d13fe974dff910e6a07bfdf252b365ed20873de42`. It records all source IDs in those nodes, the source-bound macOS and Windows instruction and node hashes, every option group including destination instructions, jump operands and intersections with special-scene documents. The map checks each visible instruction's ID, index, kind and English source against the pinned paired scenes on both platforms. The 27 changed options have matching option IDs, menu instruction positions and destination indices in these two extracted stock programs. This static comparison does not prove branch execution or translated visual fit. The affected nodes intersect the romance-route, Conrad height, Yip/film and typography decisions; the associated full decision ID sets are conservatively included. Ordinary unchanged node context and protected records remain marked as such.

Reconstruct in a clean task-owned scratch output. First run `python3 localization/pt-BR/receipts/reconcile-author-dependencies.py` from the checkout root, with its specified `resume-11/affected-node-map.json` output absent; this hashes and validates the pinned inputs before creating the map. Then run:

```sh
base=localization/work/cli-terra-high-20261110.J0KLrx/pt-BR
python3 localization/pt-BR/receipts/make-reconciled-recipe.py "$base/resume-11/affected-node-map.json" "$base/resume-11/rebuilt-recipe.json"
PYTHONPATH="$base/deps" /private/tmp/dragnwash-unitypy-venv/bin/python localization/export_editorial_delta_with_regressions.py --locale pt-BR --inventory localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json --yarn-scope localization/work/yarn-markers-20261110.ridbPA/yarn-scope-v42.json --paired-scenes localization/work/source-inventory-20261107/yarn-paired-scenes.json --before "$base/resume-10/full-audit-before.json" --after localization/pt-BR/translation.json --recipe "$base/resume-11/rebuilt-recipe.json" --output "$base/resume-11/rebuilt-delta.json"
```

The recipe SHA-256 is `17f709c4b2f2f6312cb630ace3b6bfbd0f0720c60f5fa5c57ffcd870c90ba021`; delta SHA-256 `566a9ea165d4f08a8ea87c9c5b8312c7e0b1aaaa4fb02ef93fb443c122ef27c6`. Both were regenerated byte-for-byte in the run directory. The map and exporter output require fresh paths and never overwrite existing evidence. Preserve the old candidate and its different recipe hash.

Remaining author work: adjudicate cross-node implied speaker/referent and glossary dependencies beyond the conservative node sets, walk the recorded branch jumps and downstream special consumers against the earlier source-bound controls, and amend the selector again if they add dependencies. The independent coordinator should receive a final bounded cycle only after that reconciliation. No translation text changed in this continuation, so the prior pinned dual-stock readback and Yarn verification remain applicable. Full localized artifact, actual runtime, visual and independent audit states remain open.

## Targeted player-choice referent check

A further author check searched both pinned source variants and the current target for a bounded list of masculine-looking terms in Yarn options: `obrigado`, `animado`, `ansioso`, `preparado`, `pronto`, `pequeno`, `fofo`, `gostoso`, `lindo`, and `certificado`. The seven matching IDs and both platform sources are recorded in `receipts/choice-referents.json` (SHA-256 `f0f440e72f7102248f78cbfad480980fb1aff9ed4cc0d69b5c71b44045dac54d`). `animado`, `gostoso` and `fofo` refer to male dragons; `Pronto!` and `Tudo pronto!` are impersonal completion expressions. No text correction was demonstrated. This literal search is not an exhaustive search for all gendered or implicit referents.

Three IDs outside the previous closure (`yarn:line:b2fe309b`, `yarn:line:4766af08`, `yarn:line:c13d4e24`) are included as explicit referent context in `receipts/author-audit-referent-recipe.json` (SHA-256 `9e1ba9b0b54d73b83be4e36c215283b3679819ad56f10d652ed21cceac5328a9`). The resulting `receipts/author-audit-referent-delta.json` has SHA-256 `e6a02080b993b8f69c03c6098fe26f8bc332451b90619367b535f4cec876ce28`: 51 changed IDs, 950 closure IDs, and the same 55 protected records. Closure-ID hash is `0a745e882c828fd8652baaa5137d26bda00e2ab2f72803d8062863cf0b0fa4da`; the changed-ID hash remains `8652fc71b8f98ab2036073284019f37b9f939329aba011009e24d16b5cb807bb`. Both files were reproduced byte-for-byte.

Reproduce with fresh output names in task-owned scratch:

```sh
base=localization/work/cli-terra-high-20261110.J0KLrx/pt-BR
python3 localization/pt-BR/receipts/check-choice-referents.py "$base/resume-11/choice-referents-rebuilt.json" "$base/resume-11/referent-recipe-rebuilt.json"
PYTHONPATH="$base/deps" /private/tmp/dragnwash-unitypy-venv/bin/python localization/export_editorial_delta_with_regressions.py --locale pt-BR --inventory localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json --yarn-scope localization/work/yarn-markers-20261110.ridbPA/yarn-scope-v42.json --paired-scenes localization/work/source-inventory-20261107/yarn-paired-scenes.json --before "$base/resume-10/full-audit-before.json" --after localization/pt-BR/translation.json --recipe "$base/resume-11/referent-recipe-rebuilt.json" --output "$base/resume-11/referent-delta-rebuilt.json"
```

Do not infer an executed branch from the next visible instruction: destinations can lead through further jumps. The earlier paired stock instruction map provides the operands, and applicable source-bound scene controls must be used when adjudicating actual downstream consumers. Cross-node implicit referents, the recorded branch jumps and downstream special consumers still need bounded reconciliation. Independent audit remains pending.

## Changed choice entry paths

`receipts/changed-choice-entry-traces.json` (SHA-256 `960e2b95e061d4a03539bf4bd4506bba99af9ab6f1324c3612f36d1d5360da9f`) traces the first static path from each of the 27 changed option destinations in both extracted stock programs. The deterministic `receipts/trace-changed-choice-entry.py` checks all bound input hashes, follows unconditional local jumps, and stops at the first visible line or unproved control boundary. It reproduced byte-for-byte using a fresh scratch output. Each of the 25 line boundaries is already in the 950-ID candidate closure. The two platform differences are English `your`/`you` typos for `a1f9de62` and `71d57aeb`; IDs, paths and Portuguese targets match.

Two paths stop at conditional jumps and require further branch adjudication: `yarn:line:9addfb4a` reaches `Conrad_SexScene_Cum` instruction 33, conditional destination 55; `yarn:line:77ca2316` reaches `ryan_food_dialogue` instruction 448, conditional destination 451, after an unconditional jump to 444. Do not associate the latter with the next line in linear instruction order. This is static source analysis; it does not establish command side effects, state feasibility, later consumers or executed Portuguese gameplay. Prior romance-route VM controls are documented in `special-scenes/romance-route-choices.md` and the paired source evidence it cites; they do not replace the remaining checks for these changed paths.

Reproduce with `python3 localization/pt-BR/receipts/trace-changed-choice-entry.py <fresh-task-owned-output.json>`, then compare its bytes with the committed trace. Complete the conditional and cross-node consumer reconciliation before calling the 950-ID candidate a final dependency closure.

The paired static excerpts for those two conditionals are retained in `resume-11/choice-conditional-excerpts.json` (SHA-256 `b858a63f02ebd4be8b84a68351adf3d3269f420dc7baf95c57c148bfec077621`), extracted from the bound instruction JSONs at `Conrad_SexScene_Cum` indices 29–56 and `ryan_food_dialogue` indices 444–458. Their encoded instructions match across the two builds. Conrad's true fallthrough displays `yarn:line:7f543c2a` and options `yarn:line:e9643b5d`/`yarn:line:c50535b3`; one response transfers to `Conrad_SexScene_Loop`. The false path skips that menu. Ryan's conditional selects whether to issue `SetDragonState "WaitingOnExitButton"` before the shared finish commands. The excerpts establish alternatives, not which state applies or whether later consumers are fully enumerated.

## Conrad loop consumer correction

The static conditional follow-up exposed a missing consumer: `Conrad_SexScene_Cum` instruction 50 transfers to `Conrad_SexScene_Loop`, whose instruction 27 returns to the Cum node. Both pinned instruction programs contain these transfers. The loop has four source IDs previously absent from the candidate closure: `yarn:line:1a3e2a73`, `yarn:line:2f9b499a`, `yarn:line:8c0e2d04`, and `yarn:line:b9ab4eed`. Their paired English and current targets are in `receipts/conrad-loop-consumers.json` (SHA-256 `f2ec6be248b5c962de44d63c09528ed5b9242b8741a643cd776d4aca9d37be97`); author comparison found no demonstrated text defect. The loop is included as conservative consumer context for `yarn:line:9addfb4a`, without claiming that the guarded branch executes in every state.

The current candidate `receipts/author-audit-loop-recipe.json` has SHA-256 `e5364975b33ca75c6f02423c1feff58b46d4d3ca29641929a90af0140df47021`; its delta `receipts/author-audit-loop-delta.json` has SHA-256 `61a905e357abc3fcf99c064b9308db4053116505a371711085e165106cb7ec15`. It has 51 changed IDs, 954 closure IDs and 55 protected context records; closure-ID hash `78b4a70b8609e2a9315ada3fc261285b47bac86eb23ee64775acbeed1e32f837`. All three generated files reproduced byte-for-byte. Reconstruct with fresh scratch paths:

```sh
base=localization/work/cli-terra-high-20261110.J0KLrx/pt-BR
python3 localization/pt-BR/receipts/reconcile-conrad-loop.py "$base/resume-11/conrad-loop-rebuilt.json" "$base/resume-11/loop-recipe-rebuilt.json"
PYTHONPATH="$base/deps" /private/tmp/dragnwash-unitypy-venv/bin/python localization/export_editorial_delta_with_regressions.py --locale pt-BR --inventory localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json --yarn-scope localization/work/yarn-markers-20261110.ridbPA/yarn-scope-v42.json --paired-scenes localization/work/source-inventory-20261107/yarn-paired-scenes.json --before "$base/resume-10/full-audit-before.json" --after localization/pt-BR/translation.json --recipe "$base/resume-11/loop-recipe-rebuilt.json" --output "$base/resume-11/loop-delta-rebuilt.json"
```

This is still a candidate: other named transfers, variable readers and code-side consumers of all changed scenes need equivalent bounded reconciliation, and cross-node implied glossary/referent coverage is not yet demonstrated. The independent coordinator must not treat this author check as independent approval.
