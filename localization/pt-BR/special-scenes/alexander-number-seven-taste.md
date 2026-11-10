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
