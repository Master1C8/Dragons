# Italian special-scene source index check

2026-11-10. This is a structural preparation check, not locale wording or a special-scene editorial pass. The paired English worklist SHA-256 is `692c32667546db79d51cab95d4894bb97f7f78b4fda0756465f90c0a5e6319d2`, inventory `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`. It contains 1,947 unique package authoring IDs and indexes 27 known groups with 271 distinct direct source IDs. A direct set difference against package IDs yields 25 source IDs; these are source occurrences, not missing authoring rows:

- `yarn-missing-named-destinations`: 15 marker IDs are `preserve-exactly-unreachable-yarn-fragment-marker` in v42. They must remain exact; see `localization/evidence/yarn-fragment-markers-20261110.md`.
- `new-slot-display`: six managed occurrences are represented by the single `display:slot-new` authoring row, with three source occurrences per platform under `sourceIds`.
- `missing-yarn-line-display`: four managed occurrences are represented by `display:yarn-missing-line`, with two source occurrences per platform under `sourceIds`.

This reconciles the 25-ID difference against the worklist's source bindings. It does not prove complete discovery, validate all consumer behavior, or replace positive/negative technical tests. Eleven of the 13 indexed source registry files report `incomplete`; two report `source-bound`. Those are recorded statuses, not a new independent discovery audit. The broader v42 source and preservation gate remains open as described in `CHECKPOINT.md`. No target wording has been authored.
