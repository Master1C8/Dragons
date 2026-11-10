# Polish packages after the first editorial correction batch

Both packages were built with the canonical builders from the immutable Polish translation at `ed84902`, SHA-256 `5fa6af152deb0b47aabb82ee607b8dd33e326905b2029335c6dbdaa83055b83e`. This is the complete 1,947-ID draft after the first author correction pass.

| Platform | Verified rebuild | Artifact identity |
| --- | --- | --- |
| macOS | All 284 bundle files and the deep, strict signature | Signed manifest `263aa8fc9bedf1673a7a5230e26f1ade8968674c4d8c981367f8018521c5284f` |
| Windows | All 13 ZIP members | ZIP `e6b5b7d5c5e555641ba9cc7157bafdc9daca6669e365d7d732685a5a54af8838` |

The unmodified verifier rebuilt each package independently and checked protected component fields and serialized metadata. The authored Yarn reader accepted both platform inputs. The corrected draft introduced no new characters outside the [verified stock font set](font-role-coverage-20261110.md#authored-corpus-preflight).

Installation and restoration were exercised on isolated copies. The copied macOS app matched all 284 files and passed deep, strict signature verification before removal. The Windows overlay replaced 11 files and added one companion. Unaffected entries stayed exact, and restoration matched all 259 source files and 16 directories. A wrong-source control failed before writes, and a controlled interruption after the first replacement and companion addition rolled back. Originals stayed unchanged. No games were started for these checks.

The retained packages, input snapshot, pinned commands and results are under `localization/work/pl-ed84902-packages-20261110.AYFETd/`. The combined build receipt SHA-256 is `96d10f2b70a7a26b931009b34b251ad83afaeaf43161aef9ae5f412315984924`. Independent editorial acceptance, current-payload gameplay and visual fit remain pending. An additional wording correction would require another artifact build and appropriate verification.
