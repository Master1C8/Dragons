# Ryan scene findings: author dispositions

The author rechecked the linked English and Polish scene positions in `semantic-audit-progress.md` and applied the eight paired-source corrections recorded with exact before and after strings and both build inputs in `semantic-corrections-ryan.json`. This is author self-review; the separate independent game-text audit has not accepted these revisions.

- `dee4a32d`: Ryan anticipates Conrad's reaction to his description; the conditional avoids presenting it as an established repeated reaction. The related description is `48d4a45a`.
- `ca480eed` and adjacent alternative `e6290003`: both matchmaking promises now use the same idiomatic expression for putting the two dragons in touch; the preceding request is `5c78099a`.
- `9be63f47`: the basket introduction follows Ryan bringing the basket in his mouth; the thanks refers to its pickup, in a player-gender-neutral form. The scene staging is recorded in `special-scenes/ryan-opening.json`.
- `7d9ffc48`: swallowing a large piece now contrasts with savoring food at `ec8243d8`, rather than merely taking a large bite. The source positions identify the dialogue context, not a reviewed swallowing animation; runtime/fit remain open.
- `189d999e`: thanks for listening refers naturally to the preceding account, without assigning player gender; the replies `8ead9ee9` and `fd145efe` remain unchanged.
- `9883786d`: the preceding invitation `0eb37f1a` and response `099ec7fd` establish a night reservation but do not by themselves establish a room; the separately optional hotel suggestion `88c36bc7` does not justify adding a room on all paths.
- `fbe86c06`: Conrad answers Ryan's physical joke at `41b9659f`; the idiomatic emphatic response keeps Conrad's exact speaker prefix. The analogous source phrase at `95aa0bf4` and `db592d76` was compared, not assumed to dictate this speaker's wording.

The initial pass and its earlier hash remain historical records. The current payload SHA-256 is `9df974fb2b9d952768cd342c32d6252131b891b78aac342b5c43d90734641aa8`. Complete structural guard accepted 1,947 IDs, including 1,923 macOS and 1,941 Windows inputs; this is not a semantic, branch, visual or independent pass. The mandatory delta closure and regression, the other pending findings, current-payload packaging and runtime, native Windows and visual acceptance remain open. No existing v2 artifact has been regenerated or accepted.
