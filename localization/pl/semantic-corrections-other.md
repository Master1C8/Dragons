# Alexander and other encounter findings: author dispositions

The eight paired-source changes, before and after text and both stock build entries are bound in `semantic-corrections-other.json`. This is author self-review, not the independent game-text audit. Scene positions and limitations are in `semantic-audit-progress.md`.

- `61c8781b` keeps Alexander's exclusive preference for the player, the kobold, as the person washing him; the responses at `db997182` and `ee3c126b` distinguish thanks and the private washers question.
- `3f153aaf` and `da9cfdcf` retain the Ryan and Conrad alternatives and a recent date without asserting the player is travelling back from it. The subsequent question at `a9253ddf` concerns Ryan; actual flag routing remains untested.
- `116f0e16` makes wash completion idiomatic; compare Conrad's distinct `eaafe671` correction in `semantic-corrections-conrad.md`.
- `8ee41fdc` changes only the awkward application of the verb to cultural and family ties. The preceding explanation `18d418ab`, the family crest referent and all ordered size tags remain intact. The earlier special-scene snapshot is historical; the affected text requires dependency closure and actual fit review.
- `21235886` and `7ead92b1` make Ryan's repeated request to approach where he can see and talk to the player idiomatic; `82b63c18` and `c4fc9b28` retain the distinct follow-up reasons.
- `f716a163` keeps the playful premise that Ryan arranges the date where the busy player is, rather than literally carrying an event. The dating context is `eed2cc64` through `5483c5fd` and the invitation to enter is `6126a614`.

The complete structural guard accepted 1,947 IDs (macOS 1,923, Windows 1,941) for payload SHA-256 `5fa6af152deb0b47aabb82ee607b8dd33e326905b2029335c6dbdaa83055b83e`. These changes do not pass the dependency closure, mandatory regression, current-payload runtime, visual fit or independent audit. Earlier v2 artifacts remain bound to their prior payload; no new package or game copy was made.
