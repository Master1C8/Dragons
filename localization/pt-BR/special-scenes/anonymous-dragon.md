# Anonymous dragon scene wording

Source: paired English worklist, `localization/evidence/generic-dragon-entries-20261110.md` and the bound glossary author reviews. These four scenes do not establish a shared identity or the speakers’ gender. Wording avoids gendering each unidentified speaker and the player, while retaining the cleaning, buzzing and invitation choices. Author self-reviewed drafts; actual localized routes and presentation remain unverified.

| Stable ID | English | Proposed pt-BR |
|---|---|---|
| `yarn:line:7d791906` | Oh this is better, but I still feel dirty. | Ah, melhorou, mas ainda sinto sujeira. |
| `yarn:line:ec64a696` | Do you mind double checking if I'm clean? | Pode conferir mais uma vez se ficou tudo limpo? |
| `yarn:line:7a54a1e1` | Okay | Tá bom |
| `yarn:line:1dbf50b3` | Sure | Claro |
| `yarn:line:8b8f57c4` | Thanks! | Valeu! |
| `yarn:line:b965b4dd` | Knock that off, we're not done yet. Right? | Para com isso, ainda não terminamos. Né? |
| `yarn:line:2f55b3aa` | Hehe | Hehe |
| `yarn:line:9504ba33` | ... | ... |
| `yarn:line:63926ecd` | Oh we're done? | Ah, já terminamos? |
| `yarn:line:f28fd15d` | I think you missed a few spots still... | Acho que ainda faltaram alguns pontos... |
| `yarn:line:64bfd62a` | Oops, my bad. | Opa, foi mal. |
| `yarn:line:4116f001` | I didn't know what the button did. | Eu não sabia o que o botão fazia. |
| `yarn:line:d726f776` | No worries, | Sem problema, |
| `yarn:line:fb47f998` | Yeah it go BRRT haha. | É, ele faz BRRT haha. |
| `yarn:line:6d77feef` | Anyway glad you're not finished, lets keep at it! | Enfim, que bom que ainda falta! Vamos continuar! |
| `yarn:line:f1946aab` | Thank you for cleaning me!! | Valeu pela lavagem!! |
| `yarn:line:67a46ddc` | Maybe we can hang out later? | Quem sabe a gente pode sair depois? |
| `yarn:line:c4310942` | Yes! | Sim! |
| `yarn:line:52010e35` | YES! | SIM! |
| `yarn:line:e85007ac` | Awesome! See you later then! | Ótimo! Até mais, então! |

Preserve the four scene identities, separate choices and original command routing; do not infer that the same dragon speaks across scenes. Verify the buzzing reaction, accidental dismissal, cleaning continuation and both differently emphasized invitation answers on the localized builds. Runtime paths and fit remain untested, and source coverage remains provisional.

## Author decision after source-gate reconciliation

The author accepts the pretranslation wording under the anonymous-speaker and player glossary roles: the four speakers are not equated or assigned gender, the player is likewise neutral, and silence, button sound and ordinary versus emphatic agreement remain distinct. The 20 IDs and target drafts match both stock-build entries in the paired readback recorded in the checkpoint. The direct-entry original Yarn VM traces in `localization/evidence/generic-dragon-entries-20261110.md` cover the four nodes and original choice branches on both builds; the existing per-ID adapter is feasible without modifying these controls. Positive scenarios exercise both replies in each node, including the separate button explanation and invitation emphasis. Negative scenarios merge identities, assign an unsupported gender, remove silence or swap the two choice IDs. Localized package branches and visual presentation remain pending; this is author self-review.
