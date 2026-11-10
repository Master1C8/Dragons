# Yip vocalization and film choices

Source: paired English worklist, `localization/evidence/special-scenes-yip-20261107.json`, and the bound pt-BR glossary. Keep Yip as the context-dependent kobold sound, including identical sounds paired with contrasting parenthesized meanings; keep the three film titles and Yip-Man reference consistent with the glossary. The long explanation is intentionally contrasted with “sei lá”. Existing date choices are reused. Author self-reviewed draft; actual reveal, fit, audio synchronization and branch behavior remain untested.

| Stable ID | English | Proposed pt-BR |
|---|---|---|
| `yarn:line:5efde4e2` | Yip! | Yip! |
| `yarn:line:c8cde395` | Haha, 'Yip' indeed. | Haha, 'Yip' mesmo. |
| `yarn:line:e662501c` | Yip! | Yip! |
| `yarn:line:5544e245` | Yip! | Yip! |
| `yarn:line:5e181cf4` | Yip! <size=70%>(Gate) | Yip! <size=70%>(Portão) |
| `yarn:line:5935a413` | Yip! <size=70%>(Yes) | Yip! <size=70%>(Sim) |
| `yarn:line:cf05a364` | I'm not certain why I suddenly understand your 'Yips' | Não sei por que de repente entendo seus 'Yips' |
| `yarn:line:a8ee5236` | Yip! <size=70%>(It's because the dormant part of your draconic mind is remembering the deep set language bridge between your kind and mine. Which carries the deep meaning and intention of kobold 'Yips' within it. This sudden understanding of yours is simply from our connection growing over time and activating that part of your mind.) | Yip! <size=70%>(É porque a parte adormecida da sua mente dracônica está se lembrando da profunda ligação linguística entre a sua espécie e a minha. Ela carrega o significado e a intenção profundos dos 'Yips' dos kobolds. Essa compreensão repentina surgiu porque nossa conexão cresceu com o tempo e ativou essa parte da sua mente.) |
| `yarn:line:b12a3f31` | Yip! <size=70%>(idk) | Yip! <size=70%>(sei lá) |
| `yarn:line:c3e1f198` | Yip! | Yip! |
| `yarn:line:266836f8` | That's... the first time you've yipped for me. | Essa é... a primeira vez que você dá um Yip para mim. |
| `yarn:line:52bf5ede` | I am THE kobold. Yip! | Eu sou O kobold. Yip! |
| `yarn:line:3d516ddb` | Yip! | Yip! |
| `yarn:line:9ec40945` | Haha. 'Yip' to you too. | Haha. 'Yip' para você também. |
| `yarn:line:14d2c62f` | Yip! | Yip! |
| `yarn:line:296ff3f4` | Yip! | Yip! |
| `yarn:line:d9652dff` | So. Our date tonight... | Então. Nosso encontro hoje à noite... |
| `yarn:line:7af04961` | Where would you like to go? | Onde você quer ir? |
| `yarn:line:ecc04e16` | You decide! | Você decide! |
| `yarn:line:81905be1` | I'd like to go out to eat. | Quero sair para comer. |
| `yarn:line:412ba249` | Do you know any good bars? | Você conhece algum bar legal? |
| `yarn:line:bd66082e` | What about a movie? | Que tal um filme? |
| `yarn:line:2b560f59` | Oh yeah? | É mesmo? |
| `yarn:line:910706c0` | I think a movie could be fun! | Acho que um filme seria divertido! |
| `yarn:line:073701b7` | What kind of movie are you thinking? | Que tipo de filme você quer ver? |
| `yarn:line:962abe27` | Project Scale mary | Projeto Escama Maria |
| `yarn:line:f1c14f75` | Yip-Man - The Final Yip | Yip-Man: O Último Yip |
| `yarn:line:7e352505` | Dragons of the galaxy 2 | Dragões da Galáxia 2 |
| `yarn:line:001ab950` | Oh I heard good things about that. | Ah, ouvi falar bem desse. |
| `yarn:line:67f14802` | Sure! | Claro! |
| `yarn:line:4b9046ec` | Yip-Man movies are real corny... | Os filmes do Yip-Man são bem cafonas... |
| `yarn:line:dda0419b` | But I'm sure I'd enjoy it with you! | Mas tenho certeza de que vou gostar de ver com você! |
| `yarn:line:e8052272` | Oh yeah I liked the first one. | Ah, sim, eu gostei do primeiro. |
| `yarn:line:52542beb` | Sure! | Claro! |
| `yarn:line:c4642c9c` | Sounds like a date then. I'm excited. | Então é um encontro. Mal posso esperar. |
| `yarn:line:9444cdba` | Yip | Yip |
| `yarn:line:3e870ad0` | Yip! | Yip! |

The source apostrophe-only variant for `yarn:line:266836f8` explicitly shares its target; IDs and choice destinations remain distinct. Preserve the exact `<size=70%>` tokens and existing `PlaySFX "yip"` commands without editing audio or texture assets. Verify all three movie branches, the repeated title, short and long interpretations, and actual presentation on both localized builds.

## Author decisions after source-gate reconciliation

The author accepts `movie-title-choices`, `kobold-yip-speech` and `kobold-yip-film-title` as pretranslation decisions. The three distinct title options retain the approved glossary titles, `2`, and their own reactions; `Yip-Man` is recognizable again in the series reference. The fixed vocalization `Yip` carries both the long explanation and the deliberately incongruous short `sei lá`. The player option `Eu sou O kobold` retains the source emphasis on the species noun without assigning a separate gendered player adjective. The exact `<size=70%>` tags and `PlaySFX "yip"` lookup remain source controls, not translated content. The source registrations `localization/evidence/special-scenes-yip-20261107.json` and `localization/evidence/special-scenes-ryan-language-20261107.json`, their linked context and the paired worklist bind the IDs and command occurrences; the existing per-ID Yarn adapter preserves them and the choice destinations. Positive scenarios cover the short and long interpretations, repeated sound, each film and its reaction, and the repeated series name. Negative scenarios remove or reorder the size tag, change the sound key, merge option identities, or break the title callback. Actual audio synchronization, localized branch execution and visual fit remain pending. These decisions are author self-reviews, not independent game-text acceptance.
