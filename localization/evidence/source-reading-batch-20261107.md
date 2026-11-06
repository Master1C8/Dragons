# Partial source-scene reading

The coordinator read the actual paired English line and option texts for the 44
nodes listed in `source-reading-batch-20261107.json`: 523 distinct line IDs, each
bound to ordered text hashes for both pinned builds. The receipt pins the paired
export and both compiled program hashes. This is a partial source read to find
translation dependencies, not independent editorial acceptance or an assertion
that every branch, command, speaker, asset, or game text has been reviewed.
The paired export is a reading aid and does not itself contain full branch logic.

The reading includes generic dragon responses, Ryan's muddy, date and explosion
scenes, five food-related nodes, the later route-selection scenes for Ryan and
Conrad, and selected Alexander scenes. It overlaps previously recorded romance,
Yip and missing-target cases; it does not replace those control-flow registries.
In particular:

- `RyanDate_Outro` and `RyanExploded_Outro` contain the already protected
  `==`, `title:` and `---` source-marker groups; their role remains unresolved.
- Three later intro nodes contain the developer-oriented flag-recovery wording
  and the three relationship choices already covered by the romance source
  registry. Their apparent purpose does not justify excluding their visible
  text or changing the associated route state.
- `RyanExploded_Intro` mentions an alchemist and uses `they` for an unstated
  referent (`line:e02f464d`, `line:cc4e48a3`). `Alexander_1` repeats the
  alchemist sentence under a distinct ID and separately mentions Igwix
  (`line:fa97376e`, `line:9d7cc63c`); other Alexander material establishes
  that he teaches alchemy. These snippets alone do not establish that Ryan's
  unstated referent is Alexander or Igwix, nor do they prove the speaker or
  reachability of `Alexander_1`. Preserve ambiguity and the distinct IDs while
  checking the complete scene and consumers.
- The food nodes contain separate choices and reactions; `Ryan_ham_dialog`
  includes an alarm about a bone and a distinct flirtatious response. Preserve
  choice identity and scene tone rather than assuming all similar food dialogue
  is interchangeable. The `ryan_food_dialogue` relationship choices and their
  existing source-bound romance groups must be reviewed together.

`verify_source_reading.py` verifies the receipt's exact export hash, builds,
program hashes, node membership, ordered line IDs, per-build text hashes and
counts. Positive controls use both a small fixture and the real paired export;
negative controls change the export, one ID, one source hash, or duplicate a
node and assert the intended failure. This verification checks binding only:
no script can establish that a person or model has actually read or semantically
reviewed the text. Remaining source families and 140 other line-bearing nodes
are not covered by this receipt; no overall completion percentage is implied.

```sh
python localization/verify_source_reading.py \
  localization/work/source-inventory-20261107/yarn-paired-scenes.json \
  localization/evidence/source-reading-batch-20261107.json
python -m unittest discover -s localization -p 'test_verify_source_reading.py'
```
