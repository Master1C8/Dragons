# Source component baseline — 2026-11-10

With the pinned v42 inventory SHA-256 `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`, ran the existing `localization/verify_preserved_components.py` read-only against both stock Data directories using Python 3 with the task-owned `venv` and `-B`. Both exited 0. macOS verified 10,973 exact-value game-component fields in 668 serialized objects; Windows verified 10,936 in 661. This checks known source object bytes against the shared inventory. It does not exercise locale application, other protected families, a package or runtime.

The existing `test_paired_locale.py` suite passed 2 tests, and `test_verify_yarn_preservation.py` passed 4 tests. These are adapter unit tests; they do not prove localization or in-game rendering. `test_verify_preserved_components.py` matched no files and ran 0 tests; it is not counted as validation.
