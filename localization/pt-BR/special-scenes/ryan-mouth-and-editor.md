# Ryan: editor route prompt and mouth-full exchange

Source: paired English worklist and `localization/evidence/special-scenes-ryan-language-20261107.json`, `Ryan_4_intro`. The prompt is conditional on `$isEditor`: its yes and no choices set opposite `$suggested_ryan_to_conrad` values; its visibility in a release is not established. Ryan carries the picnic basket in his mouth. Omitted consonants make his speech muffled while retaining an intelligible basket, request and thanks. Author self-reviewed drafts, not final acceptance.

| Stable ID | English | Proposed pt-BR |
|---|---|---|
| `yarn:line:dbab7a39` | <b><i><size=130%>Did you suggest Ryan to Conrad? | <b><i><size=130%>Você sugeriu o Ryan ao Conrad? |
| `yarn:line:4ab6c5a9` | yes | sim |
| `yarn:line:dc86c2de` | no | não |
| `yarn:line:390f05be` | Woah... What is that in your mouth? | Nossa... O que é isso na sua boca? |
| `yarn:line:af3f02c9` | Hey Ryan, what do you have there? | Oi, Ryan, o que você tem aí? |
| `yarn:line:156e0b50` | Picnic bathket- | Ceta de piquenique— |
| `yarn:line:835e0c27` | Can't sthpeak well. | Não conigo falar direito. |
| `yarn:line:20cb68b9` | lemme in? | me deixa entar? |
| `yarn:line:b6fb6fce` | Oh! Okay. I'll get the gate! | Ah! Tá bom. Vou abrir o portão! |
| `yarn:line:0caa6657` | Right, I'll get that for you ASAP. | Certo, já vou abrir pra você. |
| `yarn:line:9a9a6120` | Thankth! | Obigado! |

Preserve the editor guard and each yes/no state write without changing the program; retain both opening choices and both gate responses. Verify the two editor choices under a controlled editor-state probe, and both opening and gate alternatives in the localized scene, including presentation and any context needed for the speech effect. Runtime reachability, localized behavior and visual fit remain unverified. The source coverage and full preserve-exact contract remain provisional.

## Author decisions after source-gate reconciliation

The author accepts two linked pretranslation decisions. The editor prompt's `sim` and `não` retain the source labels and opposite state writes; visibility outside an editor-conditioned probe is not assumed. Ryan's `Ceta de piquenique`, `Não conigo`, `entar` and `Obigado` adapt the impeded speech while leaving the basket, request and thanks understandable. Ryan is the speaker of the gendered thanks; the player responses do not assign player gender. All 11 table IDs match both platform drafts in the paired readback recorded in the checkpoint, with macOS English and both builds' ordered markup checked.

`localization/evidence/special-scenes-ryan-language-20261107.json` records both opening and gate choices as well as `$isEditor` and the opposite suggestion-flag writes; `localization/evidence/romance-route-analysis-20261107.md` records the route dependency. The existing per-ID adapter preserves the program guard and state writes. Positive scenarios cover both editor answers in a controlled editor-state test and both opening and gate alternatives in the mouth-full exchange. Negative scenarios swap the state writes, claim normal release visibility, or make the basket and impaired speech unintelligible. Actual localized execution, articulation in context and visual fit remain pending. This is author self-review, not independent acceptance.
