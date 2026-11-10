# New-slot and missing-line display

Source: paired English worklist, `localization/evidence/non-yarn-translation-scope-20261110.md` and the paired resource audit. Three serialized NewSlotSelect labels and the managed `slot-new` input are distinct; the latter maps three original managed occurrences on each build. The missing-line fallback input maps two occurrences per build. Author self-reviewed drafts; actual localized runtime and visual checks remain pending.

| Stable ID | English | Proposed pt-BR |
|---|---|---|
| `ui:3944a555d130038af2323d988762ab1967719d178270e20fc65cd74b7c5efd27` | New | Novo |
| `ui:4cbc97aea69bccfd4defdb896f11600bdcc0964b970916200b59966d037b24e5` | New | Novo |
| `ui:1f92f7d859adfd67efa3a3f37608780f984d3d2e55b5a74774f0dfa70d9d4f86` | New | Novo |
| `display:slot-new` | NEW | NOVO |
| `display:yarn-missing-line` | !! ERROR: Missing line! | !! ERRO: Linha ausente! |

Keep the three GreyedSlotSelect values, numeric progress format and all other protected fields unchanged. Exercise empty and occupied New Game slots on both localized builds, verify both the serialized labels and managed replacement and inspect fit. Trigger the fallback in an isolated controlled test and verify that source IDs and normal line lookup remain intact; do not present fallback behavior as a successful normal dialogue. The shared audit maps managed occurrences to author inputs but does not establish locale runtime correctness or complete source coverage.
