# Spanish contextual author semantic review

Status: in progress. This is an author self-review, not the independent game-text audit. The baseline translation is SHA-256 `20fc3d75786f81c311f64b5fbd0038c5fda553a77df09864cf799d77051158cf`; worklist SHA-256 `8d172ebe8165344df8e705ce041ee57ecba1fb6c9179bbead5fe3ee7975eb7ec`. The complete paired preflight applies to that unmodified baseline only.

## Preliminary reading

Worklist positions 0–199 were read against their Spanish values and macOS English. The two source/target platform variants in 0–99 were compared; Windows spelling differences at `yarn:line:8440a3f4` and `yarn:line:73e4789c` do not change their meanings. Positions 100–199 contain no platform source or target variants. The exact full row objects, stable IDs, both source bindings and target values are preserved in task scratch `resume-10/semantic/initial-0000-0199.json`, SHA-256 `217daa4559461735da7c978ff44dc74b4d7ffec2a30d3cac14440127f3583ffa`. This is a preliminary pass, not complete contextual coverage: inspect actual scene routing and speaker bindings and adjudicate findings before crediting the range as closed. Positions 200–1946 have not been read in this audit.

## Open findings for contextual adjudication

- `yarn:line:a5979ac9`: English Alexander's “my crest”; target `mi escudo`. The later scene `yarn:line:1ff9a04c` / `yarn:line:18d418ab` identifies his head ornament and the approved family-crest term is `cresta familiar`. Verify same referent and correct if confirmed.
- Possible masculine player address: `yarn:line:33440e8c` (`eres perfecto`), `yarn:line:7d13eca0` (`fueras tan... directo`), `yarn:line:ca035ef2` (`como amigo`), `yarn:line:61c8781b` (`el único kóbold`), `yarn:line:c570a462` (`mi kóbold favorito`), `yarn:line:7b59e4d6` (`lo seguro que estás de ti mismo`) and `yarn:line:90dd6d9d` (`entusiasmado`). Confirm speakers, addressees, species-generic usage and neutral glossary requirements in context before proposing changes. `yarn:line:938be2fb` uses `un profano` for a generic layperson; check whether its scene makes it a gendered direct reference to the player.

No translation corrections have been applied. Complete the full source-to-target contextual reading, record exact coverage and findings, then adjudicate and correct with dependency closure and paired stock source/read-back checks. Independent audit, candidate packages and final-corpus runtime/visual QA remain pending.
