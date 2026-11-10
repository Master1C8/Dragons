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

Twenty-six of 27 cases have author-reviewed wording recorded in this file; the remaining 1 requires complete contextual decisions. The Alexander once-state response closure below completes the earlier choice-only section. Several cases overlap: when their complete groups are reviewed, reconcile any shared IDs with the accepted wording here and reopen affected decisions if wording must change. No ordinary translation has begun. Final implementation, package, runtime and visual checks remain separate.

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

Source case `yarn-alexander-question-once-state`; the seven paired choice sources agree. The two previously reviewed choices `c2bdc402` and `a5a8a9d5` retain their existing wording above. The other target choices are `fc7aaaa0` **Com'è insegnare?**, `daa040eb` **Ti piace il viola?**, `21c0526b` **Ti piace essere grande?**, `838cdf1b` **Cosa pensi di me?**, and `72a9b5bb` **Sei felice?**. Preserve each exact `$Yarn.Internal.Once.line:<ID>` key, choice ID and listed destination in the source registry; do not merge similar questions. Positive: a fresh state offers the stock-permitted questions and selecting each sets only its original once-state; negative: changed state key, swapped destination or repeated completed option fails. The response wording has since been reviewed in the response-closure section below; final state behavior remains untested.

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
| `6a671440` | Conosco un buon locale degli equini vicino al molo. |
| `d0361dd9` | È una specie di cucina fusion equina... |
| `46061aae` | Mi piace! Credo che piacerebbe anche a te. |
| `d71ba53e` | Allora è un appuntamento! |

Positive: the fish choice reaches the salmon joke and the alternate food choice retains its own continuation. Negative: erasing the human-expression setup, inventing a food prohibition or changing option routes fails. Paired dialogue and choice paths establish bounded feasibility; package validation, route execution and fit remain pending.

## Conrad's special endings

Source case `conrad-special-endings`, nodes `Conrad_1` and `Conrad_required_1`. Author self-review: **finali speciali** is the glossary euphemism; the literal reply uses the same noun so Conrad's correction remains intelligible. The direct sexual question stays explicit, and **supporto** means the device. Conrad's informal speech does not assign gender to the player. The paired values differ only in source apostrophes at `43dd32f5` and `5a195ff2`; both use the same target wording.

| ID | Italian wording |
|---|---|
| `9ab6ddfb` | Fate anche i “finali speciali” qui? |
| `f99840cd` | Che cosa sono? |
| `d5f94e23` | Sì! |
| `e05c2dca` | No |
| `6fa847ba` | Eh, no. Dai, dovresti offrirli. Ti pagherei bene! |
| `43c94954` | Fantastico! Non vedo l'ora di vederti all'opera! |
| `766c2abd` | Come? Li fanno in tutti i posti migliori! |
| `8a35fb7b` | Allo<size=90%>o<size=80%>o<size=70%>o<size=60%>ora... <size=100%>mi chiedevo |
| `6fbc3c1b` | Fate anche i <i>finali speciali</i> qui, vero? |
| `f98c3b6c` | Qui ogni finale è speciale! |
| `a0a0a49c` | Intendi... cose sessuali? |
| `43dd32f5` | Ehm... Non intendevo- |
| `d5ed3582` | Fate venire i draghi grossi, <size=60%>come me, <size=100%>qui? |
| `7678511c` | Ma- eh- <size=80%>oh. <size=60%>non facciamo- |
| `e048566b` | Oh, no. |
| `5a195ff2` | Cosa!? È terribile! Non avete nemmeno un supporto...? |
| `cc295885` | Ehm... <size=60%>no? |
| `5d34e715` | Be', allora fareste meglio a procurarvene uno! |
| `cb04e062` | Almeno puoi sempre usare le mani. Eh eh. |
| `3690a3eb` | Ah sì? Non vedo nemmeno un supporto. |
| `8cc1aa72` | Oh... sì, non ne abbiamo uno. |
| `1af1ad05` | No, qui non offriamo servizi del genere. |
| `b964c99b` | Peccato davvero. Dovreste rimediare. |
| `2f54ceec` | Almeno puoi sempre usare le mani. Eh eh. |

Positive: the literal option receives a correction and explicit explanation; the direct option follows its separate responses. `Conrad_1`'s three choices retain destinations 10, 13 and 16; `Conrad_required_1` retains all recorded separate destinations. Negative: disclose sexual meaning in the first question, make the literal reply unrelated, collapse the two nodes or route an option to a different response. Preserve size and italic tags exactly. Source routing and bounded text paths establish preparation feasibility, not actual branch execution or final fit.

## Three film choices and Yip-Man reference

Source cases `movie-title-choices` and `kobold-yip-film-title`, node `Ryan_5_Required_ryan_romanced`. Author self-review: the three approved glossary titles retain their separate choices; **Yip-Man** is repeated in the series reaction and the title keeps the vocalization-shaped pun. The separate Yip speech decision below preserves the same form. The numbered sequel's reaction refers to its first film, not the Yip-Man series. The first six rows are shared with the already reviewed salmon case and retain exactly that wording.

| ID | Italian wording |
|---|---|
| `d9652dff` | Allora. Il nostro appuntamento di stasera... |
| `7af04961` | Dove ti piacerebbe andare? |
| `ecc04e16` | Decidi tu! |
| `81905be1` | Mi piacerebbe andare a mangiare fuori. |
| `412ba249` | Conosci qualche bel bar? |
| `bd66082e` | E un film? |
| `2b560f59` | Ah sì? |
| `910706c0` | Un film potrebbe essere divertente! |
| `073701b7` | Che genere di film avevi in mente? |
| `962abe27` | Progetto Squama Mary |
| `f1c14f75` | Yip-Man - L'ultimo Yip |
| `7e352505` | Draghi della Galassia 2 |
| `001ab950` | Oh, ne ho sentito parlare bene. |
| `67f14802` | Certo! |
| `4b9046ec` | I film di Yip-Man sono proprio sdolcinati... |
| `dda0419b` | Ma sono sicuro che mi piacerebbe guardarlo con te! |
| `e8052272` | Oh sì, il primo mi è piaciuto. |
| `52542beb` | Certo! |
| `c4642c9c` | Allora è un appuntamento. Non vedo l'ora. |

Positive: each title retains its source option and reaction, Yip-Man is recognizable in both rows and the sequel retains numeral 2. Negative: cross the reactions, change the numeral or translate the series reference as the kobold speaking. Existing paired choice/text rendering is bounded feasibility only; final authored package, route execution and fit remain untested.

## Recurring kobold Yip

Source case `kobold-yip-speech`. Author self-review: retain **Yip** as the audible vocalization and title component; it is not a fixed word with one universal meaning. Alexander's gate/yes and long/short explanation branches express different contextual meanings; the long explanation is a character's playful claim. Preserve `PlaySFX "yip"`, the lookup key, ordered size tags and each distinct destination. The film entries below exactly match the separate movie decision. `9444cdba` is the player option to stock destination 9, not assigned to another speaker.

| ID | Italian wording |
|---|---|
| `5efde4e2` | Yip! |
| `c8cde395` | Ah ah, proprio un “Yip”. |
| `e662501c` | Yip! |
| `5544e245` | Yip! |
| `5e181cf4` | Yip! <size=70%>(Cancello) |
| `5935a413` | Yip! <size=70%>(Sì) |
| `cf05a364` | Non so perché all'improvviso capisca i tuoi “Yip”. |
| `a8ee5236` | Yip! <size=70%>(È perché la parte sopita della tua mente draconica sta ricordando il profondo legame linguistico tra la tua specie e la mia. Al suo interno racchiude il significato e l'intenzione profondi degli “Yip” dei coboldi. Questa tua improvvisa comprensione deriva semplicemente dal legame che è cresciuto tra noi nel tempo, attivando quella parte della tua mente.) |
| `b12a3f31` | Yip! <size=70%>(Boh) |
| `c3e1f198` | Yip! |
| `266836f8` | È... la prima volta che mi fai uno Yip. |
| `52bf5ede` | Sono IL coboldo. Yip! |
| `3d516ddb` | Yip! |
| `9ec40945` | Ah ah. “Yip” anche a te. |
| `14d2c62f` | Yip! |
| `296ff3f4` | Yip! |
| `f1c14f75` | Yip-Man - L'ultimo Yip |
| `4b9046ec` | I film di Yip-Man sono proprio sdolcinati... |
| `9444cdba` | Yip |
| `3e870ad0` | Yip! |

Key contextual callbacks: `c374e532` **In qualche modo mi sembra più sincero di qualsiasi cosa dica chiunque altro.**; `c8281b83` **Mmm, devo intendere che aprirai il cancello?**; `b058318f` **In coboldo significa che stai facendo un buon lavoro.**; `38b3c8c1` **Oh- volevo dire: vado ad aprire il cancello!**; `b8724c64` **Ah... ti piace proprio quel verso.**; `a8b70da7` **Allora dev'essere così! Mi fa piacere.** Preserve each callback's own context and don't promote its interpretation to a universal definition.

Positive: the same sound remains recognizable in distinct scenes, Alexander's two explanatory choices stay different and the film reference remains a film. Negative: change the audio key, merge meanings or choices, change destinations, omit the parenthetical size tag or assign unsupported speaker identity. Both builds' paired source and existing bounded dialogue/choice renderer support this preparation; actual sound playback, branch execution and final fit remain pending.

## Alexander's date decision and outcomes

Source case `alexander-romance-route`, `Alexander_5_romance_route` and `Alexander_5_Outro`. Author self-review: the affirmative and declined options state their respective outcomes explicitly; the refusal does not assert that an earlier state is cleared. Alexander asks about attractiveness before proposing a date at the college library. Keep the alternatives and their corresponding reactions distinct, the library's dragon entrance and Alexander's formal voice. Target wording uses no gender assignment for the player. Preserve the exact gradient, bold and size tag order and `$alexander_romanced` control identity.

| ID | Italian wording |
|---|---|
| `1b6c7f75` | Salve. |
| `8d5c7802` | Che c'è? |
| `370d719b` | Mh? |
| `a13d76ec` | Stavo pensando... |
| `3020c97c` | Mi trovi attraente? |
| `a610ce0b` | SÌ. |
| `f9c800f2` | Sì! |
| `763c6a82` | Penso che tu sia bello. |
| `4399096b` | Oh. |
| `d5a90e1c` | Mi fa piacere! |
| `6ff80785` | Questo... mi fa sentire molto più sicuro di me. |
| `5a5d646c` | Davvero? |
| `cc6d631b` | Questo... mi fa sentire molto più sicuro di me. |
| `e00c6df5` | Grazie. |
| `7111d265` | Questo mi fa sentire molto più sicuro di me. |
| `e721d512` | Il che mi porta alla prossima domanda... |
| `8c8591ec` | Ti andrebbe di raggiungermi alla biblioteca del college questa sera...? |
| `1ab5969b` | Sarebbe un... appuntamento. Come direbbero molti. |
| `a0e49f02` | <gradient="gold"><b> Non mi dispiacerebbe! </b></gradient><size=70%> (Porterà a una storia con Alexander!) |
| `0371fb9c` | <gradient="gold"><b> Stasera avrò da fare. Mi dispiace. </b></gradient><size=70%> (Non porterà a una storia!) |
| `36d49875` | Magnifico! |
| `9541fceb` | Da un po' di tempo meditavo di chiedertelo. |
| `b920f205` | Ah. Non preoccuparti. |
| `2f10f572` | Molto bene. Non ti interrompo oltre mentre lavori, allora! |
| `505e150f` | Grazie per il lavaggio. |
| `c66e1278` | Questa sera, nel campus. La biblioteca è l'edificio con la grande guglia blu. |
| `23e7d518` | Avvicinati all'ingresso per i draghi e ti farò entrare. |
| `b5d7d26f` | Non vedo l'ora. |
| `0f86dbf6` | Anch'io! |
| `3a23b81f` | Sembra davvero bello. |
| `99b6dc81` | Mi fa piacere. |
| `ac13bf68` | È davvero notevole. |
| `1642b6f1` | Ora mi tolgo dalle tue squame. Grazie per il lavaggio. |
| `8072b186` | A stasera. |
| `116f0e16` | Dovrei aver pulito tutti i punti. |
| `875f0961` | Grazie per il lavaggio! |
| `5d36d5c8` | Sono felice di averti conosciuto. |
| `cb06d2bf` | Anch'io. |
| `7157db26` | Oh, grazie Alexander. |
| `e767dc51` | Ad ogni modo, ora mi tolgo dalle tue squame. |
| `44f2b8cf` | Arrivederci! |

Positive: acceptance explicitly leads to Alexander romance and its date continuation; decline explicitly states no romance and retains its own response. Negative: reverse captions, change control identity, imply declining clears an earlier state, or route either response into the other. Both stock strings and tags are source-bound; actual state progression and final layout remain separate runtime checks.

## Restored destination suffixes and exact markers

Source case `yarn-missing-named-destinations`, `localization/evidence/yarn-fragment-markers-20261110.md` and `localization/evidence/yarn-transition-runtime-20261109.md`. Both source bindings agree on the eight suffix lines below. The 15 `==`, `title: ...` and `---` marker IDs remain exact-only, byte-for-byte, and are not dialogue translation targets. The existing opt-in transition adapter reconstructs five named nodes from original suffix instructions without changing original host bodies or IDs; the bounded VM and controlled Unity evidence supports feasibility, not an assertion of ordinary gameplay completion. Preserve the exact marker IDs and values, named destinations, commands and source routing.

| ID | Italian wording |
|---|---|
| `ddab3d34` | Sono molto soddisfatto di questi risultati.. |
| `4d6b365e` | Ahh, tutto pulito e con un peso in meno. |
| `f73a3fc7` | Grazie, ci vediamo domani allora. |
| `019b83df` | È stato meraviglioso! Adesso gli appuntamenti mi preoccupano molto meno. |
| `bbca8a46` | Grazie! |
| `b3c35166` | Accidenti, temevo di combinare un altro pasticcio. |
| `564a9606` | Ora non dovranno mai saperlo! |
| `c07a9171` | Grazie! |

Author self-review: the lighter load retains its double sense; Ryan's worry and unnamed plural referents remain open to source context. Positive: the repaired target emits its own suffix and original command sequence; negative: translating any marker, crossing destinations, or dropping a suffix fails. Authored-package structural validation, normal-play progression, side effects and final visual fit remain pending.

## Alexander question once-state: response closure

Source case `yarn-alexander-question-once-state`, node `Alexander_questions`. The seven choices in the earlier partial section are retained. The number-seven and crest responses are in their complete sections above. The remaining paired responses follow; distinct repeated IDs remain distinct. Author self-review: Alexander's pride and anxiety about teaching, his response about lavender, the burden of being large, and his trust in the player remain separate. The player is not assigned a gender. The two questions about how to interpret “an anomaly” have distinct replies.

| ID | Italian wording |
|---|---|
| `66fb84fe` | È tutto quello che volevo chiedere. |
| `19f36dc0` | È il mio sogno. |
| `8fc36ab7` | Mi piace avere un ruolo positivo nella vita di tante persone. |
| `3592632e` | ...È intimidatorio sapere quanto mi ammirino. |
| `a3a26459` | E non soltanto per la mia altezza. |
| `003700c7` | Che materie insegni? |
| `ba66095e` | Sei un buon esempio. |
| `960707b0` | Principalmente alchimia. A volte storia del mondo. |
| `2c560e29` | Sto cercando di avvicinarmi anche alle scienze sociali. |
| `2b7bb6ce` | È proprio questo che mi spaventa. |
| `bd4bb1b9` | Mi piace non temere il fallimento quando sono con te. |
| `4c90479c` | Me lo chiedi perché sono color lavanda? |
| `f6c14e05` | Già. |
| `c3642dec` | No. |
| `60f14972` | Be', il colore mi piace. Ma credo non abbia a che fare con la mia tonalità. |
| `55542a9b` | Il colore mi piace. Anche se credo non abbia a che fare con la mia tonalità. |
| `ef052302` | Ti piace il viola? |
| `79352475` | Già. |
| `9b915bf2` | No. |
| `e8289be5` | Oh. Bene. |
| `7e189c92` | ... |
| `0da15c85` | Oh. Va bene. |
| `b7f0551c` | ... |
| `825536f5` | È una domanda difficile. |
| `14653182` | Ci sono aspetti che mi piacciono. Il rispetto è piacevole... |
| `ae34381b` | Però quel rispetto porta con sé l'aspettativa che io mi comporti secondo il mio aspetto. È incredibilmente stressante. |
| `38043f6c` | Con me puoi comportarti come vuoi. |
| `a91980fc` | Mi piaci per quello che sei. |
| `3f29878b` | È molto gentile da parte tua. |
| `548dc375` | Voglio aprirmi di più. Mi fa stare bene. |
| `39ddd682` | Sei... |
| `afedd1f5` | Un'anomalia. |
| `0c78b56b` | Eh? |
| `6b6dd8bc` | È una cosa buona...? |
| `9a48b21c` | Nel senso che sei una persona unica. |
| `2019bb85` | In senso buono? |
| `27340362` | In senso cattivo? |
| `b629bcf2` | Certo! Sei una persona meravigliosa. |
| `b1040415` | Per le stelle! No, no. Sei una persona eccellente. |
| `fd5ddfcb` | Proprio così. La tua compagnia è eccellente. |
| `470cd652` | Sei la prima persona che incontro la cui unica aspettativa è che io sia... |
| `d13cd125` | Me stesso. |
| `e499b2cc` | Lo sono. |
| `5ec8bb55` | Credo che in parte sia merito tuo. |
| `c8f8bc22` | Ma io ti lavo e basta, no? |
| `2a5cc3a5` | È molto dolce da parte tua. |
| `59e503b2` | Lo so. Ma potersi aprire con qualcuno, anche solo ogni tanto- |
| `cfd504c5` | Fa miracoli. |
| `bc6cc4d2` | Sei molto dolce. |
| `063dcd4b` | Potersi aprire con qualcuno, anche solo ogni tanto... |
| `900dca3c` | Fa miracoli. |
| `3398aea2` | Grazie per questo. |

Preserve all seven `$Yarn.Internal.Once.line:<ID>` values, original option IDs, destinations and writes from `special-scenes-pending-20261107.json`; the fresh-state and repeated-selection checks in the earlier section apply. Positive: each permitted option follows its matching response and disappears only according to its own stock once-state. Negative: merge repeated IDs, swap responses or alter a flag or destination. Both paired source bindings were checked; existing text and choice adapters supply bounded feasibility. Actual state execution, package validation and visual fit are pending.

### `ryan-conrad-romance-routing` — Conrad entry scene (partial; case remains open)

The `Conrad_Outro_3` entry and its two distinct branches are prepared below. Ryan's introduction **unlocks** the Conrad/Ryan encounter or Ryan romance; the other choice **unlocks** Conrad romance. These labels do not promise a lock-in yet. The source's gold-gradient, bold and size tags remain in the same order, including the unclosed size tag where present. Gender-neutral player wording avoids inventing the player's gender. IDs are `yarn:line:` suffixes; the paired English differs only in the apostrophe in “That’s”/“Thats” at `266836f8`, without a meaning change. This is one bounded unit, not closure of the 686-ID conservative downstream reachability set.

| ID | Italian target |
|---|---|
| `d376acb9` | Ehi, senti. Stavo pensando... |
| `4546abce` | Forse è un po' strano chiederlo adesso. Peròòò... |
| `a0cf6cae` | Conosci qualche bel posto o qualche persona in gamba con cui potrei passare del tempo? |
| `36ff6bd9` | <gradient="gold"><b> Conosco un drago, Ryan. Potrei mettervi in contatto? </b></gradient><size=70%>(Sblocca l'incontro tra Conrad e Ryan OPPURE la storia con Ryan) |
| `7e9d40e6` | <gradient="gold"><b> A me piacerebbe passare del tempo con te... </b></gradient><size=70%> (Sblocca la storia con Conrad) |
| `8cae6240` | Un altro drago? Di solito non vado molto d'accordo... |
| `1a9e6537` | Oh, no. Ryan è un tesoro. |
| `b90b01a9` | Non preoccuparti, è davvero simpatico. |
| `2f3b06de` | Va bene. Allora credo che mi piacerebbe provare. |
| `956a0f47` | Glielo chiederò la prossima volta che lo vedo. |
| `9247b7a0` | Credo che gli piacerà il nuovo te! |
| `035a0830` | Grazie. Mi farebbe davvero piacere. |
| `0477b0d7` | Lo spero. Vorrei davvero ricominciare con qualcuno. |
| `67592de1` | Però forse è meglio che vada. |
| `f1692a96` | Grazie del suggerimento! |
| `4b38230f` | Non c'è di che. Vado ad aprire il cancello. |
| `dd082478` | Ma certo. |
| `e8ad4791` | Ooooh. |
| `52fc4e08` | Credo che mi piacerebbe! |
| `c4cc497f` | Sei proprio attraente. |
| `55d1f6ef` | ...e anche gentile. |
| `c3e1f198` | Yip! |
| `9c393f61` | Anche tu sei speciale per me. |
| `266836f8` | È... la prima volta che fai yip per me. |
| `b058318f` | In coboldo significa che stai facendo un buon lavoro. |
| `0a093816` | Oh... ah. Mi piace. |
| `3fac5bff` | Mi fa piacere sentirlo. |
| `a99c5c88` | Allora. Che ne dici di un appuntamento? |
| `13cd5511` | È presto... Ma credo di sì! |
| `85fd5266` | Sì. |
| `14e0edf6` | Credo che mi piacerebbe provare! |
| `82d0ea81` | Va bene! Allora tornerò più tardi. |
| `e53b1bd3` | <size=70%><i> cazzo, ho appena rimediato un appuntamento con un drago. |
| `fcff76d4` | Sì! Vado ad aprire il cancello. |
| `730b1ca4` | Mh? |
| `c95a153d` | Oh! Niente. Vado ad aprire il cancello. |
| `5f6a124a` | Oh, va bene. Grazie. |
| `6acf71a3` | Va bene, grazie. |

Positive review: the introduction and direct date choices remain distinct and preserve their later possibilities; the joke about the first yip stays intact. Negative review: do not turn either unlock into a final commitment, exchange choices/destinations, change source flags, close or rebalance source markup, or assign a gender to the player. The other entry scene and actual routing outcomes remain to be reviewed. Fit and branch behavior in final packages remain unverified.

### `ryan-conrad-romance-routing` — Ryan food scene (partial; case remains open)

The three choices below keep introduction, Ryan commitment and Conrad commitment distinct. The player can offer to be Ryan's “someone” without gendered self-description. Gold, bold and size markup follows the source exactly, including its existing nesting. IDs are `yarn:line:` suffixes; paired English differs only by omitted apostrophes in `d38c63ea`, `a0cb3f78`, `36fb380f`, `52f81dde` and `2bfa396c`; the meanings agree.

| ID | Italian target |
|---|---|
| `7c56b2d8` | Allora... stavo pensando alle mie relazioni. |
| `ea66b5af` | In che senso? |
| `7b7b0a3f` | Al futuro delle mie relazioni. |
| `ed4b0d48` | La cosa mi entusiasma. |
| `8aa0fc1a` | Be', sei proprio un bel partito. |
| `a6c1f2f4` | Sono felice per te! |
| `1c90fb6d` | Ma dai. Mi farai arrossire. |
| `30f1f583` | Grazie! |
| `9364911d` | Non vedo l'ora di conoscere gente nuova. |
| `0554966a` | Allora, ancora cibo? |
| `bf059ff3` | Mmh... |
| `29359884` | Che c'è? |
| `b8282714` | Stavo pensando. |
| `2e182063` | È difficile trovare persone fuori dalla mia cerchia attuale. |
| `cb91e703` | Voglio bene a chi mi circonda, ma ci sono tante cose in sospeso. |
| `5da1e074` | Capisci? |
| `e7f0e9ed` | Ha senso. |
| `fe3484ea` | Sì, capisco come mai ti senti così dopo una rottura. |
| `71c0ee9a` | Già, da quando ci siamo lasciati cerco qualcosa di nuovo. |
| `d2558a04` | O qualcuno? |
| `44658d73` | Mmh... |
| `6804839d` | Già. È difficile districare i rapporti nel gruppo dopo una cosa simile. |
| `f9193c0d` | Non ho problemi a farlo. Ma vorrei qualcosa di nuovo. |
| `6f293b7a` | Magari qualcuno di nuovo... |
| `048d7f84` | ...A proposito di quello che dicevo prima. |
| `92bd78f3` | Sì? |
| `28ec716a` | Conosci qualcuno con cui potrei parlare? Sai... di questioni sentimentali? |
| `bedc761d` | <gradient="gold"><b>Conosco un drago rosso. Credo che ti piacerebbe! </b></gradient><size=70%> (Fa incontrare Ryan e Conrad!) |
| `e104b8e4` | <gradient="gold"><b>Oh. Ehm. <size=70%> A me piacerebbe... Se fossi io quella persona. </b></gradient><size=70%> (Conferma la storia con Ryan!) |
| `f5a81524` | <gradient="gold"><b>Non mi viene in mente nessuno.</b></gradient><size=70%> (Conferma la storia con Conrad!) |
| `1d491283` | Oh? |
| `8b7915f4` | Chi sarebbe? |
| `31281c6d` | È un draco rosso DAVVERO carino che viene al lavaggio! |
| `a7181b1a` | È un drago rosso. Credo che vi piacereste! |
| `3605a48a` | Oh! Credo di averlo visto. Quello piccolino, sì? |
| `a035a3fd` | Preferisce «verticalmente svantaggiato»... Ma sì. |
| `69dd6a73` | Mhm! Sta cercando di conoscere gente nuova. |
| `45bc649d` | Oh... |
| `d38c63ea` | Che carino. |
| `ffed6d04` | Oh, fantastico. Sembra che ci assomigliamo. |
| `5c78099a` | Credo che mi piacerebbe conoscerlo! |
| `ca480eed` | Allora vi metterò in contatto. |
| `e6290003` | Non vedo l'ora. Vi metterò in contatto! |
| `70190774` | Grazie! |
| `7734bf93` | Anch'io, grazie! |
| `3b6d644d` | Oh. |
| `ad5d633a` | <i>Oh... |
| `170c6aa3` | Credo che piacerebbe anche a me se quella persona fossi tu. |
| `813c6dd4` | Quindi questo è tipo... il nostro primo appuntamento? |
| `b4990e3d` | A dire il vero, ho una cotta per te da un po'. |
| `22a9094a` | Direi di sì! |
| `0ec807a4` | Davvero? Oh, che dolce. |
| `98f800d3` | Non sapevo che qualcuno potesse affezionarsi tanto a me così facilmente. |
| `09e5bf43` | Comunque sei adorabile. |
| `9fd5b834` | Sì. <size=90%>Oh- <size=80%>sai. Io... <size=70%>Ahah. Sì. Mhm! |
| `563d71ba` | Anche tu! |
| `7a5c7f54` | Non volevo metterti in imbarazzo! |
| `ec6c7823` | Sono solo... felice. |
| `c00d76cd` | Oh, grazie. È solo grazie ai tuoi lavaggi se ho questo aspetto! |
| `63981253` | Sono... felice. |
| `4ff91cbd` | Va bene! |
| `d9c91bca` | E tu invece? Stai vedendo qualcuno? |
| `48d4a45a` | C'è un drago rosso, Conrad. È... irascibile, ma carino. |
| `dee4a32d` | Sì! Conrad, è adorabile. Anche se odierebbe sentirmelo dire. |
| `b90f527f` | Oh, eh, è quel draco piccolino che ho visto arrivare un po' fa, vero? |
| `2f3f5508` | Ehi! È solo... «verticalmente svantaggiato». |
| `a0cb3f78` | Mhm! È lui. |
| `956e5c91` | Oh, scusa. |
| `035e5be6` | Sembra una persona carina! |
| `36fb380f` | Che bello, è carino! |
| `8caa3196` | Ehi, ehm, grazie ancora. |
| `1a9a36e1` | Figurati! Non vedo l'ora che tu conosca Conrad. |
| `cd9b2a8f` | No, grazie a te. Non... vedo l'ora. |
| `0d20d327` | Certo! Grazie per il cibo. |
| `8b878971` | Ah, sì. Sembra divertente. |
| `1db78e06` | Ti racconterò come va, d'accordo? |
| `f83e4966` | Non vedo l'ora di saperlo! |
| `6e0e4e11` | Già. Sarete carini insieme. |
| `d45f4788` | È stato bello... |
| `426f40ff` | Ci rivediamo presto, vero? |
| `e1fa2461` | Lo spero! Vado ad aprire il cancello. |
| `77ca2316` | Sì! Grazie per il cibo. Vado ad aprire il cancello. |
| `5bab2df8` | Già... Non mi era mai capitato un appuntamento con un coboldo. |
| `cab69268` | Ma so già che mi piace molto. |
| `5c86951f` | Mi piaci molto. |
| `a9980f5e` | Sì, è stato davvero bello. |
| `3fa80829` | Eh eh. Sì, anche tu mi piaci. |
| `13c906c7` | Davvero. Sei una persona meravigliosa. |
| `85f901b0` | Grazie per aver condiviso il cibo con me... |
| `266c652e` | Non vedo l'ora di rivederti. |
| `b05c6259` | Non vedo mai l'ora di rivederti. Vado ad aprire il cancello. |
| `0a0d6bc0` | Anch'io! Vado ad aprire il cancello. |
| `9c3d6cb7` | Va bene! A presto. |
| `9b10d450` | Allora, questo Conrad... sembra che ti piaccia? |
| `7e991330` | Eh eh, sì. |
| `e8a91447` | È un bel tipo impegnativo. Ma mi piace. |
| `52f81dde` | Che carino! |
| `c4c81aa9` | Che cosa ti piace di più di lui? |
| `675d7e37` | È tipo. SUPER dotato. |
| `4b3c70d9` | È scontroso, ma anche tenero! |
| `4c11c83e` | È piccolino, mi piace averlo all'altezza degli occhi. |
| `bdca3e1b` | Mi piace... lui. |
| `f16d7940` | Oh... Sì, i draghi più piccoli tendono a... compensare. |
| `dd0c77ae` | Mmm, sì, conosco il tipo. |
| `da21cf49` | Ci sta! Sì, i drachi piccoli sono divertenti. |
| `2bfa396c` | Oh... È davvero dolce. |
| `91ab30f5` | Dovrai raccontarmi come va tra voi! |
| `079b3782` | Grazie per aver condiviso il cibo con me. Sei una persona davvero amica. |
| `a40e531c` | Grazie per il cibo! Vado ad aprire il cancello. |
| `323e546b` | Anche tu sei una persona amica. Vado ad aprire il cancello. |
| `886f5df2` | Va bene, a presto! |

Positive review: introduction produces Conrad/Ryan, and the other two labels explicitly commit to the named romance; all three outcomes remain separate. The vertically challenged euphemism and Ryan's four distinct reasons for liking Conrad remain recognizable. Negative review: do not merge or invert any option, destination or state flag, infer player gender, repair source markup, or promise merely unlocking where the source commits. Remaining route-closure classification and final package execution/fit remain open.

### `ryan-conrad-romance-routing` — first route-specific follow-ups (partial)

These seven groups contain 110 source-bound rows; the paired English differs only by a missing apostrophe in `507bd2b9` (same meaning). They follow the Conrad/Ryan introduction, the player's Ryan route or the player's Conrad route. IDs are `yarn:line:` suffixes. The date with Ryan and Conrad is distinct from the player's own date with Conrad, and later Ryan thanks the player for introducing him to Conrad. Existing branch flags and destinations must remain stock. The following is a partial authored unit, not a claim that every reachable route scene is done.

| ID | Italian target |
|---|---|
| `bb8583c1` | Con Ryan sono abbastanza sicuro che usciremo insieme stasera. |
| `1810e75f` | Hai qualche consiglio? |
| `8e20e028` | Sii te stesso! |
| `5072cc60` | Assicurati di essere pulitissimo. <size=70%><i>eh eh. |
| `3471e9b1` | Faccio del mio meglio. |
| `a241eec6` | Ma finora tutto bene, no? |
| `335c5156` | Credo di sì! |
| `a56c5621` | Se interessi a uno come Ryan, te la stai cavando alla grande. |
| `c642cb17` | Grazie. |
| `ea23c5f9` | Ah. Se solo ci fosse un coboldo capace di lavarmi. |
| `7c13c28e` | Magari. |
| `49b6a167` | Farò in modo che tu sia <i>immacolato. |
| `df86a610` | Scherzi a parte, il tuo lavaggio è decisamente il migliore. |
| `f3e7a8fe` | Grazie. Quando si è belli, ci si sente bene! |
| `28c51dbf` | Allora... un appuntamento. Credo che mi piacerebbe uscire presto! |
| `b9d8a22f` | Ah sì? |
| `2fe8a558` | Mi piacerebbe molto! |
| `ca616238` | Pensavo. Potremmo uscire la settimana prossima? |
| `5c51654f` | Mi sembra bello. |
| `e6006cd6` | Mi farebbe piacere! |
| `70306ba1` | Fantastico! |
| `d3a50f3f` | La prossima volta che vengo a farmi lavare usciamo. |
| `45950848` | Mi piacerebbe! |
| `ffc401d1` | Mi sembra un piano. |
| `69f406a6` | Non vedo l'ora. |
| `ab1bc039` | Sì! Mi sento pulito. |
| `3d2bc74e` | Ehi, ehm, credi che tra me e Ryan funzionerà <i>davvero</i>? |
| `877aced7` | Certo! |
| `b2dfad3e` | Lo spero. |
| `114ac9a0` | Spero che tu abbia ragione. |
| `24efaa49` | Già, anch'io. È davvero gentile. |
| `9ebea3d0` | È difficile non essere nervosi dopo tutto quello che è successo... |
| `088ea4a7` | Ma sono una bomba, quindi andrà bene. |
| `99931b37` | Spero. |
| `0fa31c40` | Però il nostro primo incontro è andato benissimo! |
| `ea2adb20` | Davvero? Raccontami! |
| `f3eeb627` | Fantastico! Quando sarà il vostro primo appuntamento? |
| `7c1adc57` | Mi ha chiamato e ci siamo incontrati. È davvero gentile. |
| `c64bd5ce` | Ha detto che sono alla mano, abbiamo organizzato un appuntamento... |
| `507bd2b9` | Ed è per questo che sono qui! Dopo il lavaggio andrò da lui. |
| `65deb150` | Subito dopo questo lavaggio! |
| `df8fb8c9` | Andremo in un ristorante di pesce... |
| `49bfbfbe` | Ho già prenotato un posto al locale. |
| `d8a2002e` | Allora è meglio che ti faccia uscire! |
| `94fbdbf0` | Sono felice per te. Vado ad aprire il cancello! |
| `4e920759` | Ah... Sì, non vedo l'ora. |
| `02cbdc87` | Grazie, anch'io non vedo l'ora. |
| `fdd800c2` | Sì! Pulito come sempre. |
| `6be807b5` | Hai qualche programma con Ryan? |
| `d1b90e2c` | Non lo so ancora. |
| `722c6ab2` | Pensavo a un appuntamento presto. |
| `4789095b` | Capisco. Insieme siete proprio carini. |
| `e41c6dc5` | Spero davvero che vada tutto bene! |
| `c87d632b` | Sì! Sarebbe fantastico. |
| `5e4d645c` | Insieme siete davvero carini... |
| `cf50dbcc` | Spero che vada tutto bene. |
| `5960dcbb` | Dovrebbe essere tutto, però. Puoi andare ad aprire il cancello? |
| `ed6be68f` | Mi sento immacolato come sempre. |
| `7b5be1f8` | Oh, e ho deciso dove andare. |
| `d8ce8566` | Ah sì? |
| `4efe8211` | Che c'è? |
| `f4af8b88` | C'è questo locale in centro. Si chiama «Wings». È uno dei miei vecchi preferiti. |
| `629f8cff` | Lì dentro sono uno abbastanza importante. |
| `f382336f` | Potrei procurarci i posti <i>migliori</i> per lo spettacolo. |
| `65b23418` | Ah, va bene. Ci sto. |
| `99ff9e7f` | Ooooh, allora devi essere importante. |
| `803bf378` | Cazzo, sono proprio su di giri. |
| `160bf40f` | Comincerò a prepararmi. |
| `ac5afd96` | La prossima volta che vengo avrò prenotato! |
| `3a6afae1` | Puoi andare ad aprire il cancello? |
| `0fcf9908` | Puoi scommetterci. |
| `b59e9091` | ... |
| `23ae97e6` | Tu sei importante. |
| `b2b32876` | Scusa, non sono capace di flirtare. Puoi aprire il cancello? |
| `24832f01` | Non vedo l'ora. |
| `803c8f0c` | Conrad mi ha parlato di te durante il nostro appuntamento. |
| `1121309c` | Ah sì? |
| `871137eb` | Di che cosa? |
| `6298f08b` | Mi ha raccontato di quando è stato picchiato. |
| `f4a8f7fc` | Credo che tu l'abbia aiutato molto più di quanto pensi. |
| `4ef9fe65` | In che senso? |
| `d8c9f912` | Facevo solo il mio lavoro! |
| `7b5c9d8c` | Certo, ma in quel momento aveva bisogno di qualcuno che si preoccupasse per lui. |
| `ed6c9afb` | Da quel che ho capito, era tanto che nessuno... si preoccupava per lui. |
| `573d9362` | Anche se facevi solo il tuo lavoro... credo che l'abbia aiutato molto. |
| `c10d9415` | Quindi grazie da parte sua per la tua premura. |
| `50102b85` | So che a volte può essere irascibile e dimenticarsi di ringraziare. |
| `c6202cf2` | Oh... Grazie. |
| `1c49f05b` | Mi fa piacere sentirlo. |
| `8a79f72c` | Oh. E un'altra cosa. |
| `3028feb5` | Dopo l'appuntamento abbiamo anche fatto sesso. |
| `a618f9c2` | <size=70%><i>Accidenti... |
| `93bd9a2b` | Ryan! |
| `058d9d5c` | Ah, sì. Conrad ha decisamente esperienza... |
| `29ec93b2` | Cooosa? Non c'è niente di male! Pensavo ti avrebbe fatto piacere saperlo. |
| `1760e5d5` | Credo che tu abbia lavato ogni punto. |
| `8150e2a2` | Grazie per avermi aiutato. |
| `3b01eb3b` | Sono sempre felice di lavarti! |
| `3c2c53dc` | Che cosa intendi? |
| `ad31ec4c` | Oh... Non solo per il lavaggio. |
| `aa1c54ab` | Intendo in generale. |
| `c932c99d` | La rottura che ho vissuto prima è stata dura. |
| `5f02ceea` | Questa è stata una splendida via di fuga... |
| `e553c773` | E mi hai presentato Conrad. |
| `7363c004` | È fantastico. |
| `d0f6a49a` | Ci vediamo la prossima volta che vengo, d'accordo? |
| `46c6a3ed` | Mi fa sempre piacere vederti, Ryan. |
| `6aa7ad03` | Vado ad aprirti il cancello. |
| `fc97aa74` | Anche a te. Grazie per il lavaggio. |
| `fbba1293` | Grazie. |

Positive review: each follow-up reflects its actual relationship state; player responses about Ryan and Conrad do not conflate their pair with either player romance. Negative review: do not substitute branch labels or alter state tests, and do not infer a player gender from a romance. Final execution, line fit and the other reachable scenes remain open.

### `ryan-conrad-romance-routing` — Conrad visit-five introductions and exits (partial)

The six state-selected scenes distinguish the player's date with Conrad, Conrad's date with Ryan, and the player's relationship with Ryan. IDs are `yarn:line:` suffixes. The seven Big C targets already reviewed under `big-c-nickname` are reused exactly below; the new unit does not supersede them. Route conditions, transitions and source markup remain unchanged.

| ID | Italian target |
|---|---|
| `1538bc7e` | Ehi, bellezza! |
| `8308bb09` | Come sto? |
| `209ddf97` | Molto bene. |
| `0bd1699e` | Ehm... |
| `b6add8e0` | Già! Sto bene! |
| `0cfcd179` | Però non per un appuntamento. |
| `9accd60e` | Allora laviamolo via per il nostro appuntamento di stasera. |
| `9de16ee9` | Ah! |
| `fa0a9fbb` | Mi stavo solo divertendo. |
| `6c3a98cc` | Va bene, allora laviamolo via per il nostro appuntamento di stasera. |
| `d66b9155` | Non vedo l'ora. |
| `e3cef2bc` | Devo assicurarmi che tu sia immacolato! |
| `405b9622` | Anch'io. |
| `75fef5cb` | Eh... Puoi scommetterci. |
| `cfaffc52` | Sono su di giri. |
| `599ffb25` | Ho già dei posti in quel bar di cui ti parlavo. |
| `c88244b5` | Di sera l'atmosfera è fottutamente fantastica. |
| `5eb243c2` | Ti piacerà. |
| `24ce37ec` | Eeehi. |
| `b2fe309b` | Come mai sei di così buon umore? |
| `3d0a5aeb` | Ehi, Conrad! |
| `08af3902` | Il mio appuntamento con Ryan è stato... |
| `9e9f3e75` | Davvero fantastico! |
| `ab3a5d9c` | Ehi. |
| `116b5405` | Il mio appuntamento con Ryan è stato... |
| `875b5372` | Davvero fantastico! |
| `1646ece2` | Scusa se arrivo tardi. Il mio sonno è tutto sballato. |
| `8076eb95` | Però sono qui solo per un lavaggio. |
| `ebd2af6b` | Presto dovrai raccontarmi ogni dettaglio su Ryan. |
| `c7b3a185` | Va bene! Vado ad aprire il cancello. |
| `7de2a81c` | Non preoccuparti. Lo farò. |
| `5183a6f2` | Grazie. |
| `f474ffa9` | <size=140%>EHI, <size=100%>vorrei un lavaggio. |
| `975a629f` | Ehi, Conrad. |
| `bb3b6c71` | Come mai sei qui così tardi? |
| `016a65e8` | Già, sono io. |
| `2d0b6b06` | Stasera vado in centro. Dovevo essere immacolato. Senti un po'... |
| `8e9e0f98` | Ho saputo di te e del tizio grosso e blu. Ryan, giusto? |
| `18ae08ef` | Scommetto che vi siete divertiti. |
| `a2ff0176` | Spero che sia andata bene. |
| `34cf0601` | Sì! Grazie per averlo chiesto. |
| `a5d2b991` | È andata bene. |
| `33e2bee6` | Mi fa piacere. |
| `d66b7986` | Ora! |
| `405b7ef1` | Conrad ha bisogno di un lavaggio! |
| `eb7cf9e5` | Tutto pulito... |
| `512df07c` | Sai che cosa significa. |
| `c71df70b` | Serata romantica! |
| `48e99d7b` | Prima devo chiudere il negozio... |
| `64889395` | Puoi scommetterci! |
| `f2b894e2` | Dovrò tenerti il posto mentre chiudi. |
| `ded99a0c` | Lo so, ti terrò il posto! |
| `4fc4259c` | Va bene! Posso andare. |
| `d9f422eb` | Ti aspetterò al bar stasera! |
| `eaafe671` | Credo che tu abbia lavato ogni punto! |
| `7c9fe106` | Mi assicurerò che non resti niente tra le tue scaglie. |
| `c6cee89f` | Grazie per avermi fatto entrare così tardi. |
| `50feefe8` | Figurati! |
| `655b8c01` | È sempre un piacere averti qui, Conrad. |
| `f36b8b76` | Mmmhm. Cercherò di sistemare gli orari del sonno... |
| `df0a8598` | Grazie. Per me è sempre un piacere essere qui. |
| `493a82ef` | Comunque. Puoi andare ad aprire il cancello? |
| `d8273d7f` | La notte non comincerà da sola! |
| `f57fc630` | Tutto fatto! |
| `f2527ed7` | Sei <i>immacolato. |
| `646279a0` | Così sembra. |
| `17dbb9b7` | Eccome! |
| `81ebbec0` | Grazie per il lavaggio così tardi nella notte. |
| `3bbab759` | Devi tenermi al corrente di te e Ryan, d'accordo? |
| `ad8ab02e` | Comunque... |
| `0e1fd4b0` | Fate uscire il <i>Grande C</i> da qui! |
| `982fd3c7` | Grande C...? |
| `255362b9` | Va bene, Conrad. |
| `227eda5e` | ... |
| `b44edd29` | Sììì, meglio non usare quel soprannome. |
| `b36365ce` | Ah... Già... |
| `d04df8f8` | Bene, ci si vede! |

Positive review: the correct partner and state remain explicit in each branch; the Big C gag reuses its earlier accepted wording. Negative review: do not exchange route scenes or destination IDs, alter formatting, or turn a future date into a completed one. Final branch execution and visual fit remain pending.

### `ryan-conrad-romance-routing` — remaining named relationship follow-ups (partial)

These eight route-selected groups cover Conrad's fifth-visit conversations, his response to the player's Ryan relationship, and Ryan's corresponding visit-five dialogue and exits. Keep the three relationship states and the stock destinations distinct; IDs are `yarn:line:` suffixes. Player wording does not assume gender.

| ID | Italian target |
|---|---|
| `b983f922` | Allora. Stasera. |
| `2fb3fe55` | Sì? |
| `a0479425` | Non vedo l'ora. |
| `95e2f7cc` | Già. |
| `03d2f0bb` | ... |
| `36779352` | Fai bene. |
| `8c269acb` | Ti piacerà moltissimo. |
| `1a169dbc` | Anche le luci della zona sono fantastiche. |
| `8b0b222c` | Creano proprio l'atmosfera. |
| `1d3b255b` | Riserva l'atmosfera per stasera! |
| `6e82e54c` | Ah sì? |
| `f8b2e23b` | Ah. Va bene. |
| `d4d3ecd5` | Oh sì. |
| `42e3eba2` | Una volta pulito andrò a preparare il nostro posto. |
| `92829935` | Ryan è un drago così gentile. |
| `04b29e42` | Lo è davvero. |
| `28d390ac` | Come mai? |
| `bee397db` | Già, è così premuroso con me. |
| `b9ce2f3c` | È... premuroso. E anche molto comprensivo. |
| `2ffe284b` | Quando l'ho conosciuto stavo ricadendo nelle mie vecchie abitudini. |
| `4815d919` | ...A fare un po' lo stronzo, a dire il vero. |
| `de25de6e` | Lui... Sapeva cosa dire per farmi smettere. |
| `6474d7f7` | È davvero bello! |
| `51d1b41e` | Ryan è un tesoro. |
| `f244d080` | Già... È davvero fantastico. |
| `c7e1b369` | Lo è davvero. |
| `7db0baf0` | Grazie per avermelo presentato. |
| `85ec0862` | Ehi, scusa se arrivo tardi. |
| `13dc0f15` | Va bene. Chiudo tra circa un'ora. |
| `3fbd01fb` | Puoi venire quando vuoi! |
| `a98d068c` | Ah. Va bene, allora non mi dispiace più. |
| `aea0be6b` | Oh, grazie. |
| `3890b91c` | Il tuo appuntamento con Ryan. |
| `dd197e7c` | ... |
| `4b29790b` | Com'è stato il sesso? |
| `f1787092` | Conrad! |
| `52ed140c` | Oh. Ehm. <size=70%>Bello. |
| `674877e5` | Ehi, non c'è niente di male a chiedere! |
| `c4dd137b` | Allora sembra sia stato bello. |
| `e8bc1d95` | Ah, immagino di sì. |
| `7e8c1ae2` | Sai proprio usare bene le mani. |
| `ef91a572` | Sono geloso! |
| `79a1a205` | ...Ma non in modo strano o cattivo. |
| `a6d6bf76` | Allora, tu e Ryan, eh? |
| `30e6b801` | Oh, sì! |
| `c13d4e24` | È sexy. |
| `800c553d` | È il drago dei miei sogni. |
| `570d4953` | Sono felice per te! |
| `7b6c47bd` | Così sembra. |
| `ed5c40ca` | Sono felice per te! |
| `4ec92454` | E tu? C'è qualcuno che ti interessa? |
| `f3b5952a` | Già, anch'io sono felice. |
| `d8f92323` | Più o meno! Sto uscendo di più. |
| `62a82aba` | Ho conosciuto un grifone. Più o meno della mia taglia... |
| `f4982dcd` | Credo abbia una cotta per me. |
| `6585925d` | ...<i><size=70%>Io almeno ne ho una per lui. |
| `163c524a` | Mi fa piacere. |
| `3a5d5ca4` | Sì, sembra uno che saprebbe come provocarti. |
| `ac6d5bd3` | Sono felice per te! |
| `341175f7` | Credo che tu abbia lavato ogni punto. |
| `a2217280` | Grazie per avermi aiutato. |
| `18707b19` | Sono sempre felice di lavarti! |
| `2dd518f0` | Che cosa intendi? |
| `8e407c6e` | Oh... Non solo per il lavaggio. |
| `bbe51f87` | Intendo in generale. |
| `01b4161e` | La rottura che ho vissuto prima è stata dura. |
| `97841169` | È stata una bella via di fuga. |
| `0699aef9` | E sono davvero felice per te e Conrad. |
| `90a9a98e` | Ci vediamo la prossima volta che vengo, d'accordo? |
| `75206eee` | Mi fa sempre piacere vederti, Ryan. |
| `59416000` | Vado ad aprirti il cancello. |
| `e3106999` | Anche a te. Grazie per il lavaggio. |
| `cf716777` | Grazie. |
| `770e7473` | Credo che tu abbia lavato ogni punto. |
| `e613cbe3` | Sai che cosa significa... |
| `7023cc94` | SERATA ROMANTICA! |
| `039a0c83` | Sì? |
| `95aa0bf4` | Puoi scommetterci! |
| `b9cb051a` | Significa che sono pronto a uscire con un certo coboldo. |
| `2ffb026d` | So che devi chiudere il negozio. Mi assicurerò che tu abbia l'indirizzo e potremo incontrarci lì, d'accordo? |
| `8c6e66f3` | Mi sembra un buon piano! |
| `a00f681d` | Non vedo l'ora. |
| `1a5e6184` | Non vedo davvero l'ora. |
| `363f6f6a` | Anch'io. |
| `a722d0fa` | Bene, vai ad aprire il cancello e io andrò sul posto! |
| `3112d78d` | A presto. |
| `3cda84e6` | Allora, raccontami ancora di Conrad! |
| `aaea8391` | Ultimamente è molto più gentile. |
| `7deb9fff` | È come... un gran tenerone circondato da punte aguzze. |
| `4f6344f1` | Ah sì? Sembra un po' una testa calda. |
| `d9534386` | Ma conosco il tipo... Dentro tendono a essere dei gran teneroni. |
| `63024a1f` | Già, è migliorato molto. |
| `7ac62718` | Già. Mi piace. |
| `f5324d68` | Mi fa molto piacere. |
| `56a729f6` | Niente è più attraente di un uomo capace di migliorare! |
| `c0972e81` | Sono felice che tra voi funzioni. |
| `ecf6206f` | Fantastico. Sono felice che tra voi funzioni. |
| `ebdb9888` | Ah, sì, quei tipi sono piuttosto carini. |
| `807fdc76` | Da quello che ho sentito sembra sia migliorato molto ultimamente, sì? |
| `164fdb01` | Mhm, ci sta provando. |
| `99bbb171` | Credo fosse in un ambiente nocivo. Ora sta meglio. |
| `ac1ed298` | Non si può chiedere di più, no? |
| `3a2ed5ef` | Comunque sono felice che tra voi funzioni. |
| `0f8bb606` | Mi fa piacere. |
| `b5dabf9f` | Niente è più attraente di un uomo capace di migliorare! |
| `e2ea4ead` | ...Un lavaggio per il nostro appuntamento di stasera. |
| `73f7f13d` | OH. GIUSTO. |
| `822c0718` | Non vedo davvero l'ora. |
| `e5c7f64a` | Allora mi fa piacere essere qui a ricordartelo. |
| `141c006f` | Anch'io. |
| `ae4d09f6` | Aspetterò al cancello! |

Positive review: the selected scene names and text agree on which pair is together; Ryan's date, Conrad's date and the introduction remain distinct. Negative review: do not swap routes, change choice/flag identities or infer the player's gender. Final runtime and fit are unverified.
