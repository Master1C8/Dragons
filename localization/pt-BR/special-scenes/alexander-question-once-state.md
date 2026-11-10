# Alexander: question availability

Source: `yarn-alexander-question-once-state`, `Alexander_questions`, in the pinned paired worklist and special-scene index. Both builds have the same English for the seven direct options. Two options overlap the number-seven and crest drafts; their wording below is identical to those drafts. The remaining five options are authored here. These are author-reviewed drafts, not independent editorial or localized runtime acceptance.

| Stable ID | English | Proposed pt-BR |
|---|---|---|
| `yarn:line:fc7aaaa0` | What's teaching like? | Como é dar aula? |
| `yarn:line:daa040eb` | Do you like purple? | Você gosta de roxo? |
| `yarn:line:21c0526b` | Do you like being big? | Você gosta de ser grande? |
| `yarn:line:838cdf1b` | What do you think of me? | O que você acha de mim? |
| `yarn:line:72a9b5bb` | Are you happy? | Você é feliz? |
| `yarn:line:a5a8a9d5` | Your crest is cool. What is it? | Sua crista é legal. O que é? |
| `yarn:line:c2bdc402` | What does the number 7 taste like? | Qual é o gosto do número 7? |

The wording keeps the questions distinct, including happiness as an ongoing state and size as a trait rather than an evaluation. Preserve all seven original IDs and their `$Yarn.Internal.Once.line:…` variables, the shared exit condition and destinations. The source-bound original Yarn VM and managed save controls in `localization/evidence/alexander-question-analysis-20261107.md` exercise each option's flag and exit path on both builds; the Unity save/reload control covers one flag variant per build under macOS and CrossOver. These controls use English source tables. The Portuguese choices, normal node entry, visual fit and live saved-state behavior in a localized package remain untested; the other question bodies are contextual dependencies and require translation in their own batches. Full game source discovery remains provisional.

## Author decision after source-gate reconciliation

The seven choices above are accepted by the author for the pretranslation decision, with the already accepted citrus and crest decisions reused rather than separately rewritten. The paired readback `localization/work/cli-terra-high-20261110.J0KLrx/pt-BR/resume-07/readback-alexander.json` (SHA-256 `b560f35989280468e0aa204cae773b7c29bed6a89c86d5bcf50337f544e9db40`) maps all seven inputs on both builds. The cited original VM and save controls make retaining the original IDs and once flags feasible. A positive scenario selects each option once and exits after the original conditions; negative scenarios repeat a previously consumed choice or substitute another option's flag or destination. Full question bodies will be translated with their own context. Actual Portuguese gameplay, saved-state behavior and visual fit remain pending; this author self-review is not independent.
