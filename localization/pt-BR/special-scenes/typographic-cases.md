# Sized greetings, aside, and hesitation

Sources: the paired English worklist and `localization/evidence/special-scenes-typography-20261110.json`. Conrad calls out for a wash in two introductions; his quieter aside questions whether different scales are even possible before complimenting the addressee. Ryan’s hesitant response shrinks progressively. Author self-reviewed drafts; actual localized presentation and path coverage remain pending.

| Stable ID | English | Proposed pt-BR |
|---|---|---|
| `yarn:line:f474ffa9` | <size=140%>HEY, <size=100%>lookin' for a wash. | <size=140%>EI, <size=100%>tô querendo uma lavagem. |
| `yarn:line:36073321` | <gradient="yellow - orange"><size=140%>HEY! </gradient><size=100%>This is the cleaning place, ya? | <gradient="yellow - orange"><size=140%>EI! </gradient><size=100%>Aqui é o lugar da lavagem, né? |
| `yarn:line:6c193ba9` | Scales different today? <size=70%><i>is that a thing...? </i><size=100%>You look good today. | Suas escamas estão diferentes hoje? <size=70%><i>isso existe...? </i><size=100%>Você está com uma aparência ótima hoje. |
| `yarn:line:9fd5b834` | Yeah. <size=90%>Oh- <size=80%>you know. I'm like... <size=70%>Haha. Yeah. Mhm! | Sim. <size=90%>Ah- <size=80%>você sabe. Eu fico... <size=70%>Haha. É. Uhum! |

Retain the original tag sequence, gradient, size transitions, italic span and ID routing. The typography registry describes source behavior; its evidence does not prove locale-specific scene rendering. Verify both greetings, the aside and the increasingly small choice text in the localized builds, including fit and readability. The source coverage and full preserve-exact contract remain provisional.

## Author decisions after source-gate reconciliation

The author accepts all three pretranslation decisions: each `EI` remains an enlarged greeting followed by normal speech, the scales aside remains a hesitant aside before a compliment, and Ryan's player response retains its successive hesitation beats without gendering the player. The four IDs and drafts match both stock-build entries in the paired readback recorded in the checkpoint; macOS source and both ordered tag sequences were checked. `localization/evidence/special-scenes-typography-20261110.json` records the source-bound regions and verified structural guards, making the existing tag-preserving adapter feasible. Positive scenarios render both greetings, the aside, and all four successive stages of the player choice. Negative scenarios empty a marked region, move the aside out of italics, drop the gradient or reorder the sizes. Actual localized legibility, fit and runtime presentation remain pending; this is author self-review.
