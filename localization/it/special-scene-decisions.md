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

Seven of 27 cases have author-reviewed wording recorded above; the remaining 20 require complete contextual decisions. Several cases overlap: when their complete groups are reviewed, reconcile any shared IDs with the accepted wording here and reopen affected decisions if wording must change. No ordinary translation has begun. Final implementation, package, runtime and visual checks remain separate.
