# Alexander: number seven and taste

Source: `alexander-number-seven-taste` in `localization/work/cli-terra-high-20261110.J0KLrx/pt-BR/special-scenes-index.json`, inventory SHA-256 `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`; English paired worklist SHA-256 `4b161f5aa3c93d1023fa5cad77324dfa4907370713a7986f7528add12378dff1`. Both builds have the same English text for these IDs. The source registry identifies `Alexander_questions`, instructions 140–181, once variable `$Yarn.Internal.Once.line:c2bdc402` and face commands. Source classification remains `needs-review`; this is a draft decision and author self-review, not independent acceptance.

| Stable ID | English source | Proposed pt-BR |
|---|---|---|
| `yarn:line:c2bdc402` | What does the number 7 taste like? | Qual é o gosto do número 7? |
| `yarn:line:78eccd9b` | Yellow lime. | Limão-taiti amarelo. |
| `yarn:line:eedccaec` | No way. | Não pode ser. |
| `yarn:line:db79a905` | Like... a lemon? | Tipo... um limão-siciliano? |
| `yarn:line:4d49ae72` | 'Yes way', There is nothing I am more certain of. | Pode, sim. Não há nada de que eu tenha mais certeza. |
| `yarn:line:6128a09c` | No. A lime that is yellow. | Não. Um limão-taiti que é amarelo. |
| `yarn:line:f718a7eb` | You're the professor here. Must be correct. | O professor aqui é você. Deve estar certo. |
| `yarn:line:f0351f0c` | No way. | Não pode ser. |
| `yarn:line:6605187b` | That's an appeal to authority fallacy. But, yes. I'm correct. | Isso é uma falácia de apelo à autoridade. Mas, sim. Estou certo. |
| `yarn:line:15bcd86c` | 'Yes way', There is nothing I am more certain of. | Pode, sim. Não há nada de que eu tenha mais certeza. |

Author self-review: `limão-taiti` versus `limão-siciliano` makes the intended lime/lemon distinction explicit to Brazilian readers while retaining the unexpected yellow lime and number 7; it specifies common varieties rather than asserting the fruits are identical. The repeated denial and rejoinder stay consistent across both IDs. No answer is added or identified as correct by the translation.

Technical plan: use the existing per-ID paired Yarn mapping and preserve the once variable, all option IDs, destinations and face commands. Confirm both initial choices and both nested choices reach their original branches; negative controls must reject a changed number or merged citrus terms. Structural mapping and localized runtime/visual checks are **not run**; source classification and any effect of the variety specification require review before treating this group as settled. Texture content is excluded.

## Source control reconciliation

The pinned `localization/evidence/alexander-question-analysis-20261107.md` records paired original-Yarn VM runs of all three relevant paths, with explicit option IDs and body sequences. Rechecked SHA-256 of `localization/work/alexander-question-runtime-20261110.aCqz9A/macos.jsonl` is `67c5f247551df049f94171487e13dd3cdd86c694dfdc6110b2ca96ffe35b6cd7`, and of `windows.jsonl` is `c73d17296db2ed747563edd206c25f2ff50756f1433f7d94cd96e2b7bf3e040a`. The observed paths are `eedccaec` → `4d49ae72`, `db79a905` → `f718a7eb` → `6605187b`, and `db79a905` → `f0351f0c` → `15bcd86c`, with `78eccd9b` in all three and `6128a09c` in the latter two. The original question once state and exits are covered by the same traces. This accepts the local source control-path analysis, not the provisional completeness of the overall source inventory. The traces use original English and do not prove that this wording was packaged or rendered; final target mapping, translated choices, presentation and fit remain untested. The existing per-ID mapping is a feasible route, conditional on successful paired read-back and unchanged controls.

## Author decision after source-gate reconciliation

The author accepts the ten values above for the locale pretranslation decision. In context, Brazilian Portuguese ordinarily calls both citrus fruits `limão`; specifying the familiar varieties preserves the source contrast and the intentionally surprising yellow lime. This is an explicit localization choice, not a claim that the English specifies varieties. The number, the initial alternatives, both nested replies and the repeated rejoinder stay distinct. The previous concerns about the wording and source classification are resolved for this entry gate; this is not independent editorial review.

The unchanged 248-input paired readback, SHA-256 `d001d31ddfc21bcce77a022123cda4abccb2b19881fbd12dec1e5815f9ad7b04`, contains all ten IDs with identical authored values on both builds; a fresh comparison of each source, target and ordered tag sequence passed. The original-Yarn traces cited above supply the feasible per-ID/once-state contract. Positive acceptance scenarios are the three recorded paths and the correctly yellow lime; negative scenarios are a changed 7, a lemon in Alexander's answer, merged options, or a repeated question after its once flag is set. Actual pt-BR package application, flags, typography and visual fit remain pending.
