# Polish semantic audit progress

This is the author's source-to-target pass, not the separate independent game-text audit. Worklist and translation hashes and the exact 111 reviewed IDs are recorded in `semantic-audit-ryan-food.json`. The review used both stock English values and current Polish, with the correction at `f16d7940` read from the current payload rather than the older prepared export. The paired scene supplies instruction positions and alternatives, not a proof that every route was played. The existing romance-route decision identifies the three tagged choices and their distinct destinations; authored route transitions and fit remain unrun. Runtime branch evidence for the four Conrad options is recorded separately in `editorial-delta-01.md`.

## Ryan food conversation: 111 IDs read

Reviewed the future relationships discussion and breakup alternatives, Ryan/Conrad matchmaking, Ryan romance and Conrad romance branches, and their separate closing exchanges. The tagged options retain the named routes and distinct unlock/commit semantics; the variants differing only in English apostrophes can share their current Polish target. The adjusted compensation reply is coherent with the selected physical joke. No game runtime or visual acceptance is inferred from this reading.

Findings pending disposition and dependency review:

- `yarn:line:dee4a32d`, instruction 240: English “Though he'd hate I said that” expresses how Conrad would react to the player saying it; `Chociaż nie znosi, kiedy tak mówię` asserts an established repeated reaction. Consider `Chociaż nie znosiłby, gdybym tak powiedział(a)` only after checking a gender-neutral player formulation and neighboring context. No correction has been made.
- `yarn:line:ca480eed`, instruction 162: `W takim razie was skontaktuję` is understandable but unnatural Polish. `W takim razie skontaktuję was ze sobą` is a candidate; compare the parallel instruction 163 before deciding. No correction has been made.

The rest of the 1,947 IDs, protected-value review, dependency closure and required independent audit remain open. The 111-ID count records this bounded human language comparison, not a claim that the full semantic audit or regression has passed. Revisit affected entries if their sources, glossary dependencies or text change.
