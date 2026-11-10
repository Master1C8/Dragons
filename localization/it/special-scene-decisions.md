# Italian special-scene decisions

Binding: paired English worklist SHA-256 `692c32667546db79d51cab95d4894bb97f7f78b4fda0756465f90c0a5e6319d2`; Italian glossary SHA-256 `d069f575030d7f60b63d91c6596a0cfafaab55f36b42728918633082f5fdc037`. Source registries and hashes are bound by the worklist special-scene index. These are author decisions and self-review, not the independent final game-text audit. Source IDs retain the prefix `yarn:line:`. Accepted wording here is preparatory and is not yet inserted into a package.

## Alexander's proletarian register

Source case `alexander-proletarian-register`, registry SHA-256 `72f5dfa5d8ba396d92c7bf67c6912d05022940f2197e073b0a651b5e7f5b0809`. Both builds have the same meaning despite the Windows spelling of “environment”. The elevated word and the interrupted attempt to repeat it must match; Alexander's apology moves to a plain compliment. Author self-review: the seven target lines preserve the class contrast, confused question, separate polite path and convergence.

| ID | Italian wording |
|---|---|
| `73e4789c` | Sai... Questo ambiente è piuttosto piacevole. Molto... proletario. |
| `e5d47feb` | prole- <i><size=70%>come? |
| `8512365e` | Grazie! |
| `74c9c07b` | Oh, cioè... della classe operaia? |
| `e2f9c70c` | Scusa, volevo dire che mi piace il tuo servizio di lavaggio. |
| `13223129` | Ma certo |
| `a97338b0` | Chi avrebbe mai detto che posti simili fossero così facilmente accessibili al pubblico! |

Use the original ID and stock dialogue mapping; the existing text path accepts the same ordered `<i><size=70%>` tags. Positive: choice `e5d47feb` goes to stock destination 11 and receives the class clarification and apology; `8512365e` goes to 15 and receives the public-access comment. Negative: a different interrupted root, swapped destinations, or removed markup fails. Editorial: author-reviewed. Adapter feasibility: bounded paired renderer and source mapping passed; implementation/structural validation against the authored package, runtime and final visual fit: pending.

## Conrad's scales aside

Source case `conrad-scales-aside`, registry SHA-256 `792cd452b62853213499c2d167254db77907f1de652cf7cba076f386653380c7`, row `6c193ba9` (same English on both builds):

> Scaglie diverse oggi? <size=70%><i>è possibile...? </i><size=100%>Oggi stai bene.

Author self-review: the smaller hesitant aside questions whether scales can change; the compliment returns to normal size. Preserve the exact tag order and three nonempty regions with the original source ID. Positive: the middle region alone uses the smaller italic source treatment, then the compliment returns to 100%; negative: an empty aside or moved size boundary fails. Editorial: author-reviewed. Adapter feasibility: existing TMP text path and structural guard; package implementation and validation, actual runtime and visual fit: pending.

## Ryan branch hesitation sizing

Source case `ryan-branch-hesitation-sizing`, same typography registry, row `9fd5b834` (same English on both builds):

> Sì. <size=90%>Oh- <size=80%>sai, io... <size=70%>Ahah. Sì. Mhm!

Author self-review: successive hesitant beats retain the increasingly small voice without assigning the player's gender. Keep the original choice identity, destination, and 90%, 80%, 70% order and nonempty stages. Positive: each beat remains in its original size stage; negative: an empty stage, reordered tags or changed choice destination fails. Editorial: author-reviewed. Adapter feasibility: existing TMP text path and structural guard; package implementation and validation, runtime and visual fit: pending.


## Alexander's teacher correction

Source case `alexander-teacher-professor-correction`, registry SHA-256 `72f5dfa5d8ba396d92c7bf67c6912d05022940f2197e073b0a651b5e7f5b0809`. Author self-review: the player calls Alexander a teacher, he corrects the title to professor, and the alternative opens the gate; both routes converge on his apology. Source IDs and target wording:

| ID | Italian wording |
|---|---|
| `9aa97614` | Dovremo fare in fretta, gli studenti non si istruiranno da soli. |
| `393c128a` | Non ho mai lavato un drago insegnante... wow. |
| `155d1c64` | Va bene, apro il cancello! |
| `af0c15fd` | Professore... ma sì. Di solito non vado nei lavaggi pubblici. |
| `836d1b13` | Grazie. |
| `1270a483` | Ah, e mi scuso per essere assolutamente lurido. |

Map the IDs to their existing dialogue entries, leaving controls intact. Positive: `393c128a` follows destination 25 to the correction and `155d1c64` follows destination 30 to thanks; both reach the apology. Negative: calling him a professor in the first choice or swapping the continuations defeats the joke. Editorial: author-reviewed; paired text-path feasibility: passed; implementation/structural check and runtime/visual fit: pending.

## Conrad's emphatic greetings

Source case `conrad-emphatic-greetings`, typography registry SHA-256 `792cd452b62853213499c2d167254db77907f1de652cf7cba076f386653380c7`. Author self-review: each sudden greeting remains emphatic and is followed by ordinary-sized speech.

| ID | Italian wording |
|---|---|
| `36073321` | <gradient="yellow - orange"><size=140%>EHI! </gradient><size=100%>È qui che si lava, no? |
| `f474ffa9` | <size=140%>EHI, <size=100%>vorrei una lavata. |

Retain both IDs and the exact ordered tags, with wording in both size regions. Positive: first greeting uses its gradient and 140% size, the later one uses 140%, and both requests return to 100%; negative: a missing greeting region or altered size/gradient order fails. Editorial: author-reviewed; existing TMP path and structural guard supply feasibility; package checks and runtime/visual fit remain pending.

## Editor route prompt

Source case `editor-route-prompt`, registry SHA-256 `6209639693f1c03ea71bd49a7da0e994ecd8262b04a0e26223f6320be1f8a14d`. This prompt is conditioned on `$isEditor`; its presence in released play is not assumed. The target nevertheless covers its three source IDs, without treating the meta choices as spoken player dialogue.

| ID | Italian wording |
|---|---|
| `dbab7a39` | <b><i><size=130%>Hai suggerito Ryan a Conrad? |
| `4ab6c5a9` | sì |
| `dc86c2de` | no |

Author self-review: the question asks about the same suggested pairing and the choices remain opposites. Keep condition, `$suggested_ryan_to_conrad`, original option IDs and state writes untouched; use only the paired display mapping. Positive: in a controlled editor-state check each selection writes its stock corresponding boolean; negative: swapped choices or modified variable/condition fails. Editorial: author-reviewed; paired source and text path establish feasible display replacement; package structural checks and controlled runtime/visual check remain pending.


## Alexander's number-seven answer

Source case `alexander-number-seven-taste`, registry SHA-256 `5efe4c18581eddd9929227750dfb34842142c172e3cb3bd18d36e58953aa5a51`. Both English bindings were read. Author self-review: the absurd sensory answer remains a yellow lime, distinct from a lemon; his confidence and the appeal-to-authority correction remain jokes rather than proof of a correct answer. Duplicate source replies retain distinct IDs.

| ID | Italian wording |
|---|---|
| `c2bdc402` | Che sapore ha il numero 7? |
| `78eccd9b` | Lime giallo. |
| `eedccaec` | Impossibile. |
| `db79a905` | Cioè... un limone? |
| `4d49ae72` | Possibilissimo. Non c'è nulla di cui io sia più certo. |
| `6128a09c` | No. Un lime di colore giallo. |
| `f718a7eb` | Qui il professore sei tu. Dev'essere giusto. |
| `f0351f0c` | Impossibile. |
| `6605187b` | È un appello all'autorità, un errore logico. Ma sì, ho ragione. |
| `15bcd86c` | Possibilissimo. Non c'è nulla di cui io sia più certo. |

Keep both identical response pairs distinct and preserve `$Yarn.Internal.Once.line:c2bdc402` and all source destinations. Positive: both first responses and nested responses lead to their original replies; 7, lime and lemon remain distinguishable. Negative: merging the duplicate IDs, changing 7, or making lime and lemon the same fruit fails. Editorial: author-reviewed; paired dialogue mapping and stock branching give feasible text substitution. Package validation, branch runtime and visual fit remain pending.

## Gate status

Nineteen of 27 cases have author-reviewed wording recorded in this file; the remaining 8 require complete contextual decisions. The Alexander once-state choices below are partial and are not included in the nineteen. Several cases overlap: when their complete groups are reviewed, reconcile any shared IDs with the accepted wording here and reopen affected decisions if wording must change. No ordinary translation has begun. Final implementation, package, runtime and visual checks remain separate.

## Alexander's family crest

Source case `alexander-family-crest`, node `Alexander_questions`, instructions 256–289; both stock English values match. Author self-review: the ornament around his head is a family crest, not simply a heraldic shield; the runaway explanation shrinks in seven stages, including the four-nations allusion. The player's request to repeat and Alexander's refusal stay separate. Wording:

| ID | Italian wording |
|---|---|
| `a5a8a9d5` | Bella la tua cresta. Che cos'è? |
| `1ff9a04c` | Oh, la cresta intorno alla mia testa? |
| `89c9a73b` | Molti pensano che faccia parte del mio corpo. |
| `18d418ab` | Invece è ornamentale! La mia cresta di famiglia. Vedi... |
| `8ee41fdc` | La storia dei draghi è complessa. Le creste ornamentali <size=85%> sono spesso <size=70%> indossate dai draghi per <size=55%>indicare a quale famiglia appartengono! <size=40%> Sono un segno interessante della loro eredità culturale <size=35%> e familiare. Mi sono spesso chiesto se dovrei continuare a portare la mia. <size=20%> Ma nella tradizione dei draghi i legami culturali e familiari sono considerati importanti! Perciò devo rispettarli. <size=10%> Acqua. Terra. Fuoco. Aria. Tanto tempo fa, le quattro nazioni vivevano insieme in armonia. Poi tutto cambiò quando la Nazione del Fuoco attaccò. |
| `e90fee8e` | Oh. |
| `535ee717` | Puoi ripetere? |
| `7f3fe9f9` | Ah, scusa, sono appassionato di queste cose. |
| `c56ee060` | Mi fa piacere che la mia cresta ti piaccia. |
| `f0cb8389` | ...No |

Keep all seven size tags in their original order and with nonempty successive regions, stock identities and controls. Positive: both response paths retain their own lines and the allusion is present at 10%; negative: a dropped size stage, missing allusion or replacement of the physical crest with a mere coat of arms fails. Paired text-path feasibility is established; authored-package validation, actual legibility and both branches in final runtime remain pending.

## Alexander's college introduction

Source case `alexander-college-self-introduction`, node `Alexander_2`, identical paired node SHA-256 `4518c325b247a32e3841ac1263ab1d060adb09074e167ee1e0d26bd8336afeae`. The glossary names the institution “College comunitario di taumaturgia di Burnswick”. The college question and “Okay” have distinct stock destinations 10 and 18; the boast and separate name are successive beats, not an actual new speaker identity. Author self-review of the full branch:

| ID | Italian wording |
|---|---|
| `7e9389a7` | Quale college? |
| `f64a5b30` | Va bene |
| `dd06ed39` | Il College comunitario di taumaturgia di Burnswick, naturalmente! |
| `4b36ea4e` | Il college più prestigioso, con professori prestigiosi come me: |
| `f167e3d7` | Alexander! |
| `6757e4a0` | ... |
| `607a5c47` | Bene, non posso permettere che il College comunitario di taumaturgia di Burnswick sappia che il suo miglior professore, Alexander, ha causato un altro incidente. |
| `85f39b27` | ... |
| `13c39c50` | Oh, accidenti, dimentica quello che ho detto! |

The exact source Yarn table value for `4b36ea4e` remains unchanged; its localized colon-ended sentence belongs in the speaker locale under the same ID, for the presenter to display in the body without a character annotation, as specified in `localization/evidence/alexander-colon-display-20261110.md`. Positive: the question leads to the college, full boast, separate name and pause in stock order; the other option follows its own continuation. Negative: treating the boast as a real speaker, changing its source prefix or swapping destinations fails. Existing paired adapter fixture and controlled VM evidence support feasibility; final authored-package and standalone-node presentation remain unverified.

## Ryan's mouth-full speech

Source case `mouth-full-speech`, node `Ryan_4_intro`; both English bindings agree. Author self-review: Ryan's basket is identifiable, his difficulty speaking and thanks carry a consistent, intelligible impediment, and the two opening choices and two gate choices remain distinct. The basket/pose are stock scene dependencies, not edited textures.

| ID | Italian wording |
|---|---|
| `390f05be` | Accidenti... cos'hai in bocca? |
| `af3f02c9` | Ehi Ryan, cos'hai lì? |
| `156e0b50` | Cethtino da picnic- |
| `835e0c27` | Non riethco a parlare bene. |
| `20cb68b9` | mi fai entrare? |
| `b6fb6fce` | Oh! Va bene. Apro il cancello! |
| `0caa6657` | Certo, te lo apro subito. |
| `9a9a6120` | Grathie! |

Keep the original choice IDs, controls and order; do not invent a speaker for another line. Positive: either opening reaches the basket explanation and either gate reply reaches the impeded thanks; negative: intelligibility lost, basket omitted or a choice redirected fails. Paired dialogue and choice renderer feasibility is bounded; authored-package checks, pose, actual runtime and fit remain pending.

## New-save slot display

Source case `new-slot-display`, `localization/evidence/non-yarn-translation-scope-20261110.md`, SHA-256 `c3df834a09a5e9855912953cf9257302781cbe33388f23e0638115dc761415f1`. Author self-review: distinguish the three serialized `New` button labels from the runtime-populated `NEW` progress label. The button IDs `ui:3944a555d130038af2323d988762ab1967719d178270e20fc65cd74b7c5efd27`, `ui:4cbc97aea69bccfd4defdb896f11600bdcc0964b970916200b59966d037b24e5`, and `ui:1f92f7d859adfd67efa3a3f37608780f984d3d2e55b5a74774f0dfa70d9d4f86` each use **Nuova** (a new game). The paired managed `display:slot-new` row uses **NUOVA**, covering three `MenuSlotsNew::OnShow` literal occurrences per build. Preserve the numeric progress formats, greyed-slot values and identities exactly. Positive: an empty new-game slot displays both localized labels and an occupied slot retains numeric progress; negative: translating the progress format, overwriting the greyed template or omitting the managed write fails. Existing stock menu observation and paired adapter establish bounded feasibility; actual Italian occupied-state behavior and fit remain pending.

## Missing-line fallback

Source case `missing-yarn-line-display`, same source evidence. The paired `display:yarn-missing-line` row maps both `LocalizedLine::.cctor` source literals per build, English `!! ERROR: Missing line!`, to **!! ERRORE: Battuta mancante!**. Author self-review: the diagnostic remains visibly an error for a missing dialogue line, rather than becoming normal dialogue. Preserve the unrelated provider fallback and choice prefab template. Positive: the missing-line fallback presents the same Italian diagnostic on both paths; negative: leaving one mapped literal in English or changing the unrelated provider/template fails. The existing paired managed-adapter checks establish feasibility; actual Italian package validation and runtime display remain pending.

## Alexander question once-state: partial wording

Source case `yarn-alexander-question-once-state`; the seven paired choice sources agree. The two previously reviewed choices `c2bdc402` and `a5a8a9d5` retain their existing wording above. The other target choices are `fc7aaaa0` **Com'è insegnare?**, `daa040eb` **Ti piace il viola?**, `21c0526b` **Ti piace essere grande?**, `838cdf1b` **Cosa pensi di me?**, and `72a9b5bb` **Sei felice?**. Preserve each exact `$Yarn.Internal.Once.line:<ID>` key, choice ID and listed destination in the source registry; do not merge similar questions. Positive: a fresh state offers the stock-permitted questions and selecting each sets only its original once-state; negative: changed state key, swapped destination or repeated completed option fails. These seven choice wordings are preparatory only: the full associated response scope and final state behavior have not yet been target-reviewed for this case, so it remains open.

## Conrad's dirty double meaning

Source case `dirty-double-meaning`, node `Conrad_placed_mount_3`; both source bindings agree. Author self-review: **sporco** describes both physical dirt and sexual raunchiness, and the drawn-out opening shrinks as in the source. The support is the adult device, not a riding animal. The alternative activity orders and their `$conrad_jerked_off_3` condition remain stock program behavior.

| ID | Italian wording |
|---|---|
| `cc6e7856` | Ah! Ecco il supporto! |
| `5a5e7f21` | Allo<size=90%>o<size=80%>o<size=70%>o<size=60%>ora... <size=100%>Non sono sporco. Ma sono <i>~sporco~</i>, capisci? |
| `31fa3bdf` | Quindi sei venuto solo per... |
| `0372e0d1` | Già. Non costava troppo. |
| `a7ca3ca8` | Scopare qualcosa e poi, spero, farmi fare una sega. |
| `1d9b3531` | Farmi fare una sega e scopare questo supporto. |
| `8bab3246` | Sei... molto diretto. |
| `283e56d8` | Certo che lo sono! So di essere molto... |
| `be0e51af` | Figo. |
| `045f5836` | ... |
| `926f5f41` | Comunque. Ora userò questo coso! |
| `9542e7a6` | Ah, bene. Inauguriamolo! |

Positive: both replies and each prior-activity state retain their source continuations, and both senses remain clear; negative: collapsed meanings, changed condition or altered tag sequence fails. Bounded text-path feasibility is established; package validation, both runtime states and final fit remain pending.

## Conrad's professional double meaning

Source case `professional-double-meaning`, node `Conrad_finished_jerkoff_3`; paired sources agree. Author self-review: **professionista** avoids assigning the player's gender and lets Conrad echo the profession claim before the separate punchline; duplicate source lines remain distinct IDs.

| ID | Italian wording |
|---|---|
| `496134bc` | ...! |
| `eaf45022` | Accidenti, sai usare bene le mani. |
| `7cc45755` | ...! |
| `c6955ecc` | Accidenti, sai usare bene le mani. |
| `50a559bb` | Ah... <size=70%> già. |
| `5788e15c` | Certo. Lavoro da <i>professionista</i>. |
| `c1b8e62b` | Fa sempre piacere quando un coboldo sa cosa gli piace. |
| `3063100e` | Anch'io. |
| `a6531779` | ... |
| `1c021ee0` | A farmi fare le seghe. |
| `8a321997` | Ora sto puntando quel supporto... |
| `29a77d09` | Fammi provare! |
| `bf977a7e` | Ah, va bene. Vado a prenderlo. |
| `05c673e7` | Certo! |
| `93f67490` | Cazzo, sì |

The phrasing avoids an article that could suggest player gender; Conrad's **Anch'io** still echoes the professional claim. Keep the duplicate IDs, italic and size tags, option routes and `$conrad_jerked_off_3` behavior. Positive: the professional route holds the delayed punchline while the alternative receives its own continuation; negative: adding player gender or merging continuations fails. Bounded text-path feasibility is established; package validation, state execution and fit remain pending.

## Conrad's self-invented nickname

Source case `big-c-nickname`, node `Conrad_5_outro_ryan_romanced`; both source bindings agree. Author self-review: **il Grande C** remains tied to Conrad's initial, and the player's questioning echo prompts him to discard it. His separate named reply remains distinct; Ryan is the other character referenced.

| ID | Italian wording |
|---|---|
| `f57fc630` | Tutto fatto! |
| `f2527ed7` | Sei <i>splendente. |
| `646279a0` | Pare di sì. |
| `17dbb9b7` | Cazzo, sì. |
| `81ebbec0` | Grazie per il lavaggio a quest'ora della notte. |
| `3bbab759` | Devi tenermi aggiornato su te e Ryan, va bene? |
| `ad8ab02e` | Comunque... |
| `0e1fd4b0` | Fate uscire il <i>Grande C</i> da qui! |
| `982fd3c7` | Grande C...? |
| `255362b9` | Va bene, Conrad. |
| `227eda5e` | ... |
| `b44edd29` | Sììì, meglio non usare quel soprannome. |
| `b36365ce` | Ah... Già... |
| `d04df8f8` | Bene, ci si vede! |

Preserve both italic tag sequences, choice IDs and distinct continuations. Positive: the questioning choice produces the abandoned nickname and the named choice follows its own response; negative: losing the shared C or redirecting the branches fails. Paired renderer feasibility is bounded; actual route execution, authored-package validation and fit remain pending.

## Ryan's question about a question

Source case `ryan-question-about-a-question`, `Ryan_2_required`, paired node SHA-256 `91a8f75f2ef3f4c7cf82641fed9357693b163f539a77dfb5b5e765c958427697`. Author self-review: the first reply plays on the question already asked; the direct reply bypasses the acknowledgment. Ryan discusses an uncertain relationship without identifying its other party or the player. All eight choice destinations remain as registered.

| ID | Italian wording |
|---|---|
| `aa0dda7b` | Ehi. |
| `3c3ddd0c` | Mh? |
| `866cd495` | Che succede? |
| `105cd3e2` | Posso farti una domanda? |
| `81416c72` | Me ne stai già facendo una, dimmi. |
| `709a9a57` | Certo. |
| `17716b05` | Oh, giusto. Scusa. |
| `e6aa9d20` | Allora, riguardo alle... relazioni. |
| `5cfb94b9` | Se una relazione è <i>così</i> travagliata e sai che finirà. |
| `cacb93ce` | E hai provato di tutto. |
| `695ef750` | ... |
| `ff6ef027` | Quando decidi davvero di chiudere la relazione? |
| `453ff9be` | Oh- Ryan... |
| `d422462e` | Non... so se posso rispondere io per te. |
| `d30ffec9` | Lo so. Non dovrei scaricarti addosso tutto questo. |
| `42124159` | È solo che con te mi sento davvero a mio agio. |
| `31ab814e` | Hai ragione... Non potresti. |
| `a79b8639` | Sono solo felice di non sentirmi giudicato qui. |
| `1dca8fa0` | È solo che con te mi sento davvero a mio agio. |
| `8bfa88d7` | Grazie. Anche a me piace stare con te. |
| `be5feb3e` | Spero che le cose migliorino. |
| `286fec49` | Mi fa piacere. |
| `040ee2a7` | anche a me. |

Positive: `81416c72` reaches the acknowledgment and `709a9a57` bypasses it; both enter the relationship discussion and later choices keep their distinct responses. Negative: remove the question logic, merge choices, change a destination or attribute the other party without evidence. Existing paired text and choice paths establish feasibility; package validation and actual branch execution and fit remain pending.

## Conrad's height euphemism

Source case `conrad-height-euphemism`, two spans in `ryan_food_dialogue`. Author self-review: both contexts use **diversamente alto** for the same joke about Conrad's stature, while the surrounding reactions and relationship paths stay distinct. **Draco** follows the glossary; Ryan and Conrad remain different people.

| ID | Italian wording |
|---|---|
| `8b7915f4` | Chi è? |
| `31281c6d` | È un draco rosso DAVVERO carino che viene al centro di lavaggio! |
| `a7181b1a` | È un drago rosso. Credo che vi trovereste bene! |
| `3605a48a` | Oh! Credo di averlo visto. Quello piccolino, vero? |
| `a035a3fd` | Preferisce “diversamente alto”... Ma sì. |
| `69dd6a73` | Mhm! Sta cercando di conoscere nuove persone. |
| `45bc649d` | Oh... |
| `d38c63ea` | Che carino. |
| `ffed6d04` | Oh, fantastico. Sembra che ci somigliamo. |
| `d9c91bca` | E tu invece? Stai frequentando qualcuno? |
| `48d4a45a` | C'è questo drago rosso, Conrad. È... impulsivo, ma carino. |
| `dee4a32d` | Sì! Conrad è adorabile. Anche se odierebbe sentirmelo dire. |
| `b90f527f` | Oh, ma è quel draco piccolino che ho visto entrare poco fa, vero? |
| `2f3f5508` | Ehi! È solo... “diversamente alto”. |
| `a0cb3f78` | Mhm! È lui. |
| `956e5c91` | Oh, scusa. |
| `035e5be6` | Sembra carino! |
| `36fb380f` | Fantastico, è carino! |

Positive: each euphemism receives its own route-specific reaction and either alternative retains its source continuation; negative: different euphemisms or swapped route identities fail. Paired text-path feasibility is bounded; authored-package validation, branch execution and fit remain pending.

## Anonymous dragon replies

Source case `anonymous-dragon-address`, four separate nodes. Author self-review: do not identify the four dragons as one person or assign gender to either participant. Preserve the anonymous dragon's feeling of remaining dirt, the player's button admission, the distinct silence choice and the normal versus emphatic agreement.

| ID | Italian wording |
|---|---|
| `7d791906` | Oh, va meglio, ma sento ancora dello sporco addosso. |
| `ec64a696` | Puoi ricontrollare se ho ancora dello sporco addosso? |
| `7a54a1e1` | Va bene |
| `1dbf50b3` | Certo |
| `8b8f57c4` | Grazie! |
| `b965b4dd` | Smettila, non abbiamo ancora finito. Vero? |
| `2f55b3aa` | Eh eh |
| `9504ba33` | ... |
| `63926ecd` | Oh, abbiamo finito? |
| `f28fd15d` | Credo che manchino ancora alcuni punti... |
| `64bfd62a` | Ops, colpa mia. |
| `4116f001` | Non sapevo cosa facesse il pulsante. |
| `d726f776` | Nessun problema, |
| `fb47f998` | Sì, fa BRRT ahah. |
| `6d77feef` | Comunque, meno male che non hai finito, continuiamo! |
| `f1946aab` | Grazie per il lavaggio!! |
| `67a46ddc` | Magari possiamo passare del tempo insieme più tardi? |
| `c4310942` | Sì! |
| `52010e35` | SÌ! |
| `e85007ac` | Fantastico! Allora a dopo! |

Positive: each menu keeps its two IDs, order and corresponding follow-ups; the button still makes the sound and the emphatic agreement stays uppercase. Negative: unifying identities, assigning unsupported gender, swapping choices or losing silence fails. Bounded renderer feasibility is established; package validation and final runtime and fit remain pending.

## Ryan's salmon self-correction

Source case `salmon-guy-dragon`, node `Ryan_5_Required_ryan_romanced`. Author self-review: “tipo da salmone” sets up Ryan's correction that he is a dragon; the other seafood response goes elsewhere and no dietary restriction is invented. The date, alternative destinations and the equine-kin fusion restaurant remain distinct.

| ID | Italian wording |
|---|---|
| `d9652dff` | Allora. Il nostro appuntamento di stasera... |
| `7af04961` | Dove ti piacerebbe andare? |
| `ecc04e16` | Decidi tu! |
| `81905be1` | Mi piacerebbe andare a mangiare fuori. |
| `412ba249` | Conosci qualche bel bar? |
| `bd66082e` | E un film? |
| `108de471` | Sì, mi sembra una bella idea. |
| `86bde306` | Come te la cavi con pesce e frutti di mare? |
| `e5937e30` | Sì. Mi piace il pesce! |
| `fc571337` | Mmm, magari qualcos'altro? |
| `73a37947` | Oh, fantastico. Sono proprio un tipo da salmone. |
| `c9f270de` | Be', sono un drago... ma hai capito cosa intendo. |
| `5fc277a9` | Allora è un appuntamento! Pesce e frutti di mare, poi si vedrà. |
| `6a671440` | Conosco un buon locale di cucina equina vicino al molo. |
| `d0361dd9` | È una specie di cucina fusion equina... |
| `46061aae` | Mi piace! Credo che piacerebbe anche a te. |
| `d71ba53e` | Allora è un appuntamento! |

Positive: the fish choice reaches the salmon joke and the alternate food choice retains its own continuation. Negative: erasing the human-expression setup, inventing a food prohibition or changing option routes fails. Paired dialogue and choice paths establish bounded feasibility; package validation, route execution and fit remain pending.
