# Polish v2 dialogue frame review handoff

The [Polish runtime checkpoint](../pl/CHECKPOINT.md#authored-package-representative-runtime-2026-11-10) records the macOS and CrossOver runs. The queue under `localization/work/pl-v2-visual-review-20261110.YD0x4q/bound-v2/` contains all ten saved frames from those two runs. It covers three active dialogue choices and both body sizes on each platform. The originals are preserved. Prepared input uses WebP quality 80 at the native 640 × 480 or 1024 × 768 dimensions.

The first queue linked the authored translation through the working tree. The replacement queue binds the same captures to an immutable local copy of `localization/pl/translation.json` from `0d34c62`, whose SHA-256 is `cb471d50b18d79b659744dcf6360b25ba63d9ba42c2428e95196e040341dda2e`. The initial queue remains available as a record of preparation. Use the replacement queue for any authorized review of this snapshot.

| Binding | SHA-256 |
| --- | --- |
| Native manifest | `970af5da0eebe1310ecff4b1eeaa4c7c302296d3d7ac0dba4568ebe47bb342df` |
| Original provenance | `c3e66708cdc5912afcf1a5b8c75a1c3d7f1a98291df5172eeba7c15c36a257ed` |
| Prepared source bindings | `3cd599bd956fdf65b92011689f8da769dcdd91f230f1215c1647028755e95647` |
| Initial review ledger | `0a6ee274fb741f183841bcc2488da0d9cebb3e5f24bd41516d4634baa35f96da` |

The prepared queue reports 10 pending judgments and has issued no review requests. The checkpoint separately records the author's inspection of four frames. Independent pixel review remains pending. For any later translation or renderer change, recheck which frame inputs remain applicable against the new artifact before reusing the v2 evidence.
