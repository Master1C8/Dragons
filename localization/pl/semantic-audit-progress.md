# Polish semantic audit progress

This is the author's source-to-target pass, not the separate independent game-text audit. Worklist and translation hashes and the exact 111 reviewed IDs are recorded in `semantic-audit-ryan-food.json`. The review used both stock English values and current Polish, with the correction at `f16d7940` read from the current payload rather than the older prepared export. The paired scene supplies instruction positions and alternatives, not a proof that every route was played. The existing romance-route decision identifies the three tagged choices and their distinct destinations; authored route transitions and fit remain unrun. Runtime branch evidence for the four Conrad options is recorded separately in `editorial-delta-01.md`.

## Ryan food conversation: 111 IDs read

Reviewed the future relationships discussion and breakup alternatives, Ryan/Conrad matchmaking, Ryan romance and Conrad romance branches, and their separate closing exchanges. The tagged options retain the named routes and distinct unlock/commit semantics; the variants differing only in English apostrophes can share their current Polish target. The adjusted compensation reply is coherent with the selected physical joke. No game runtime or visual acceptance is inferred from this reading.

Findings pending disposition and dependency review:

- `yarn:line:dee4a32d`, instruction 240: English “Though he'd hate I said that” expresses how Conrad would react to the player saying it; `Chociaż nie znosi, kiedy tak mówię` asserts an established repeated reaction. Consider `Chociaż nie znosiłby, gdybym tak powiedział(a)` only after checking a gender-neutral player formulation and neighboring context. No correction has been made.
- `yarn:line:ca480eed`, instruction 162: `W takim razie was skontaktuję` is understandable but unnatural Polish. `W takim razie skontaktuję was ze sobą` is a candidate; compare the parallel instruction 163 before deciding. No correction has been made.

The rest of the 1,947 IDs, protected-value review, dependency closure and required independent audit remain open. The 111-ID count records this bounded human language comparison, not a claim that the full semantic audit or regression has passed. Revisit affected entries if their sources, glossary dependencies or text change.

## Ryan picnic basket and food exchanges: 78 IDs read

Read `Ryan_grab_basket`, `Ryan_egg_dialog`, `Ryan_grapes_dialog`, `Ryan_ham_dialog` and `Ryan_melon_dialog` against the paired English source and Polish target. Ryan brings the basket, the player can respond to individual foods and each option has its own response. The basket introduction is contextualized by `special-scenes/ryan-opening.json`: Ryan first arrives with the picnic basket in his mouth. The egg's color/store answer, stems and dragon digestion, ham bone and suggestive option, and whole-watermelon/swallowing joke remain distinguishable. The English apostrophe-only variants of the basket and ham lines are consistent with their shared target. Source positions and option kinds identify alternatives; actual authored route selection and fit remain unrun.

Findings pending disposition and dependency review:

- `yarn:line:9be63f47`: “Thank you for grabbing that” follows the basket pickup; `Dzięki, że to podnosisz` describes an ongoing action. Check the pickup timing before deciding whether `Dzięki, że to podniosłeś` can be made player-gender neutral.
- `yarn:line:7d9ffc48`: “nothing beats a large gulp” contrasts swallowing with savoring; `nic nie przebije wielkiego kęsa` suggests a bite. Review the swallowing animation and adjacent ham lines before selecting an equivalent.

These 78 IDs plus the 111 Ryan conversation IDs make 189 distinct author-reviewed IDs. The remaining 1,758 IDs and all independent acceptance remain open.

## Ryan first visit and Start node: 79 IDs read

Read first-arrival window, gate, customer interaction, wash conversation, phone guidance and departure nodes, including the option-specific replies and Yip misunderstanding, against both English variants and Polish. The phone points to the window, then entry; the departure asks to open the gate, not enter it. The stock naming and grammatical differences across builds are compatible with the shared targets. `Start` is a source-included Yarn development/test node with eighteen individually numbered test lines; their numbering and the Unity/Yarn references are preserved. The actual availability of this node in normal gameplay and these authored route transitions have not been established by this reading. No new semantic finding was identified in this unit.

Cumulative distinct IDs read: 268 / 1,947; 1,679 remain. This is author work, with independent acceptance and all unrun checks still open.

## Ryan second visit: 81 IDs read

Read `Ryan_2_intro`, `Ryan_2_required` and `Ryan_2_Outro` against the paired English and current Polish. Ryan returns after an outing, asks when to end a troubled relationship, and later explains his girlfriend sent him to the wash; the player can listen or decline to pry. The paired choice and response positions were compared, including the duplicated overreaction options and replies, and both builds share the English wording in this unit. The colloquial, gender-neutral player formulations and emphasis markup retain the intent. Source instruction positions and choices do not establish actual runtime transitions or fit.

Finding pending disposition: `yarn:line:189d999e`, “Thank you for listening,” appears after Ryan has shared his account. `Dziękuję, że mnie wysłuchujesz` may suggest ongoing listening; consider the gender-neutral `Dziękuję za wysłuchanie` in the closing exchange and compare related thank-you lines. No correction made yet.

Cumulative distinct IDs read: 349 / 1,947; 1,598 remain. Author review only; separate independent acceptance and unrun runtime checks remain open.

## Ryan third visit: 52 IDs read

Read `Ryan_3_intro`, `Ryan_3_required`, `Ryan_3_Outro` and `Ryan_3_wont_use_mount` against both English builds and current Polish. Ryan hesitates on arrival, then explains the breakup and its mixed feelings; the separate responses acknowledge his decision or the difficulty of ending a relationship. The farewell has alternatives affirming friendship and his separate refusal of the mount is conditional context, not a universal statement. The English article and apostrophe variants retain the shared meaning; the size and italic markup are retained as in source. The source positions and choice kinds do not demonstrate live choice routing, conditional behavior or fit. No new semantic finding was identified in this unit.

Cumulative distinct IDs read: 401 / 1,947; 1,546 remain. This is an author pass; independent acceptance and unrun checks remain open.

## Ryan fourth visit and intimate exchanges: 60 IDs read

Compared `Ryan_4_*`, `Ryan_SexScene*` and `Ryan_Conrad_SexScene*` against both source builds and Polish. The previously documented basket-in-mouth staging explains the intentionally impaired speech in `Ryan_4_intro`; the initial yes/no question refers to suggesting Ryan to Conrad, and the question's source markup is retained. In the intimate scenes the paired continuation and climax choices, separate participants and their speaker prefixes remain distinguishable. This reads source positions and existing staging evidence; it does not establish live conditional transitions, animation, or display fit.

Findings pending disposition:

- `yarn:line:9883786d`: “I booked the night” has been rendered as booking a room. The English does not itself identify a room; inspect the actual scene/location evidence before retaining or removing that specificity.
- `yarn:line:fbe86c06`: Conrad's emphatic “Damn right!” after Ryan's joke is understandable as `Cholernie słusznie!` but sounds stilted in Polish. Consider an idiomatic emphatic response preserving the joke and speaker.

Cumulative distinct IDs read: 461 / 1,947; 1,486 remain. This is author review, not independent acceptance or a runtime pass.

## Ryan fifth-visit introductions: 51 IDs read

Compared `Ryan_5_intro` and `Ryan_5_intro_ryan_romanced` against both stock English values and Polish. The recovery choices identify three different pairings; Ryan's alternative greetings distinguish the player/Ryan date, the player/Conrad date and Ryan/Conrad's prior date. The repeat baking explanation and gate request retain their role across branches. The previously recorded romance-route decision supplies the meaning of the pairings, while the node's instruction positions alone do not establish conditional execution or actual state transitions. Developer recovery text and markup remain included. No additional semantic finding was identified in this unit.

Cumulative distinct IDs read: 512 / 1,947; 1,435 remain. This is author review, with independent acceptance and live route checks still open.

## Ryan fifth-visit required conversations: 84 IDs read

Compared the three `Ryan_5_Required_*` nodes against both English builds and current Polish: the player discusses Conrad's improvement, Ryan describes his date with Conrad and the player's kindness, or Ryan and the player arrange their own date. Distinct food, bar, movie and walking alternatives and Ryan's responses retain their meaning. The source-bound `special-scenes/ryan-date.json` records the approved movie titles, sequel and salmon/dragon joke; the Polish setup and correction keep the odd self-identification needed for that joke. Ryan suggests a hotel room after the bar choice (`yarn:line:88c36bc7`), which supplies some related context for the unresolved `9883786d` finding, but this does not establish whether all later intimate paths are in that room. No additional finding in this unit. Live option transitions and fit remain unrun.

Cumulative distinct IDs read: 596 / 1,947; 1,351 remain. Author comparison only; independent game-text audit remains pending.

## Ryan fifth-visit farewells and action responses: 46 IDs read

Compared the three `Ryan_5_Outro_*` nodes and four `Ryan_5` action responses against both English builds and current Polish. Ryan's gratitude has different referents in the player/Conrad and Ryan/Conrad routes, while his own romance sets up the date and departure; the alternatives and gate requests retain those distinctions. `yarn:line:95aa0bf4` uses the natural `A jakże!` for “Damn right!” and is relevant to the pending Conrad line `fbe86c06`; the speakers and contexts differ, so this is comparative evidence rather than an automatic replacement. No new finding. Actual route execution, action triggers and fit remain unrun.

Cumulative distinct IDs read: 642 / 1,947; 1,305 remain. Author review is not independent acceptance.

## Conrad first visit and action responses: 50 IDs read

Compared the two introductions, first required conversation, alternate interaction, departure and two action nodes against both English builds and current Polish. The special-endings decision in `special-scenes/conrad-endings.json` records the euphemism and distinct answers; the departure uses the approved `stojak` term and preserves the differing apology and promise replies. The separately identified introductory nodes should not be assumed to occur on the same path. The prior isolated Conrad fixture demonstrated synthetic choice progression and the v2 sample demonstrated three authored choices, but neither proves these full authored routes, action triggers, nor visual fit for the present payload.

Findings pending disposition:

- `yarn:line:6fa847ba`: “Mate you gotta get in on this” urges participation; `musisz tego spróbować` may imply the player should experience the service as a customer. Check the preceding question and response branch to select the intended agency.
- `yarn:line:72b244b7`: `Ależ to było zajebiście dobre!` conveys the response but is an awkward Polish collocation for “That felt damn good!” Consider a more natural emphatic sensation while retaining the tag.

Cumulative distinct IDs read: 692 / 1,947; 1,255 remain. This is author work, not independent acceptance.

## Conrad second visit: 60 IDs read

Compared the injury arrival, conversation, departure and alternate interaction against both English builds and Polish. The player can inquire or express sympathy, and Conrad's subsequent admission and apology remain distinct from the alternatives; his medkit request and changed attitude connect the arrival and departure. `Conrad_2` is a separate interaction and its relationship to a particular playthrough has not been established here. Both stock builds have identical English in this unit. Actual route conditions and display fit have not been tested.

Findings pending disposition:

- `yarn:line:1a5e1ba4`: `Jak zachowywać?` is an incomplete Polish question for “Act what way?” in response to Conrad asking why he acts this way. A neutral construction is needed.
- `yarn:line:b4a29141`: `żeby tu trochę upiększyć` lacks a natural object for sprucing the place up; compare the connected gift context before revision.
- `yarn:line:0de4fe62`: `Dobrze się przygotowujesz` suggests a repeated action rather than the player's preparedness on this occasion. Consider a gender-neutral state description.

Cumulative distinct IDs read: 752 / 1,947; 1,195 remain. Author review only; independent acceptance remains pending.

## Conrad third visit: arrival, tutorial and route choice: 62 IDs read

Compared the phone's mount delivery, Conrad's greeting and the separate Ryan introduction and player date branches against both stock English builds and Polish. The crate and gate instructions are distinct. The source-bound `special-scenes/romance-routes.json` and `special-scenes/yip.json` document the route labels and yip responses, and the player/Ryan versus Conrad choices remain distinct. The earlier v2 fixture exercised three sample authored choices in this introduction on macOS and CrossOver; it does not prove the present revision or subsequent romance paths. The separate `db592d76` Conrad response also renders “Damn right!” as `A jakże!`, useful context for the pending `fbe86c06` finding. Actual delivery, conditional branching, later routes and display fit remain unverified.

Finding pending disposition: `yarn:line:a0cf6cae` attaches `z którymi mógłbym spędzać czas` to both people and places, an awkward construction because spending time with places is not intended. Preserve both hangout locations and people with separate grammatical relations.

Cumulative distinct IDs read: 814 / 1,947; 1,133 remain. Author review is not independent acceptance.

## Conrad third visit: action conversations: 50 IDs read

Compared the mount placement, both action completions, action start and idle responses against both English builds and Polish. The same completion line appears under distinct IDs in two contexts and the two are consistent. `special-scenes/conrad-wordplay.json` documents the dirty double meaning and the delayed professional punchline: the player refers to professional work, Conrad says he too is a professional and then clarifies what he receives. The placement and completion nodes are action-dependent; their names and source positions do not prove live triggers or order. One English typo differs across builds but shares the intended target. Actual action transitions and display fit are unrun.

Finding pending disposition: `yarn:line:12e8ae42` is literally understandable but `użyj rąk na moim kutasie` is unnatural Polish for the sexual instruction. Consider idiomatic wording that preserves directness and the reason Conrad gives.

Cumulative distinct IDs read: 864 / 1,947; 1,083 remain. Author review only; independent acceptance remains pending.

## Conrad fourth visit: introductions and question opening: 61 IDs read

Compared the three relationship introductions, their conditional recovery choices, and the alternatives introducing Conrad's question against both stock English builds and current Polish. The berries answer recurs in distinct paths, while the date with the player, meeting Ryan and ordinary visit stay distinct. The source-bound `special-scenes/romance-routes.json` describes relationship choices, but this reading does not demonstrate flag selection or transitions; the repeated `Conrad_required_4` options are conditional alternatives. Actual route execution and fit remain unrun.

Finding pending disposition: `yarn:line:07bd7f57` uses masculine `Zrobiłeś` for the player, whose gender is not specified in English. It also forms a two-line interrupted question with `yarn:line:6c193ba9`; revise that dependency together without losing the awkward flirtation or the subsequent aside.

Cumulative distinct IDs read: 925 / 1,947; 1,022 remain. Author review only; independent acceptance remains pending.

## Conrad fourth visit: relationship conversations and actions: 45 IDs read

Compared the player/Conrad date plan, Conrad/Ryan date advice, player/Ryan discussion and four action responses against both English builds and Polish. The date partners remain distinct, as do the advice choices and their replies. Conrad's gryphon interest is in the player/Ryan conversation, not the Conrad/Ryan date. The node positions indicate alternatives but do not establish their live routing or whether action responses fire. Actual display fit and gameplay remain unrun.

Finding pending disposition: `yarn:line:3a5d5ca4` uses `potrafi podrażnić` for “he'd push some buttons”. In the conversation about the gryphon Conrad likes, the English idiom may suggest arousal or provoke irritation; inspect scene and idiomatic context before settling this ambiguity.

Cumulative distinct IDs read: 970 / 1,947; 977 remain. Author review only; independent acceptance remains pending.
