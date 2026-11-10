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
