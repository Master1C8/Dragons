# Paired locale reader preflight

The coordinator checked the committed authoring snapshot at `75c839e` against all six worklists in the [approved source receipt](source-readiness-v42-20261110.json). Each present target was resolved by the shared locale reader and passed to the canonical source/target reader in its actual platform and asset envelope. The check covers authored IDs, placeholders, markup, staged text regions, and protected Yarn speaker prefixes. It does not load built assets or certify wording, runtime or layout.

| Locale | IDs authored on all bound platforms | macOS / Windows bindings checked | Rejected bindings |
| --- | ---: | ---: | ---: |
| de | 502 | 502 / 502 | 0 |
| es | 116 | 116 / 116 | 0 |
| fr | 644 | 644 / 644 | 0 |
| it | 0 | No authored file | |
| pl | 1,947 | 1,923 / 1,941 | 0 |
| pt-BR | 248 | 248 / 248 | 2 |

The pt-BR failures are the same Yarn choice on both builds, `yarn:line:f1c14f75`. Stock text is “Yip-Man - The Final Yip”. The draft “Yip-Man: O Último Yip” adds a colon, and the package dialogue reader rejects it because Yarn uses colons for implicit speaker labels. The worklist export and a markup-only comparison do not exercise this guard.

On a separate snapshot, “Yip-Man - O Último Yip” passed all 248 authored bindings on each build. Reinstating only the colon failed at the intended guard on both builds. The related “Os filmes do Yip-Man são bem cafonas...” at `yarn:line:4b9046ec` passed without changes. The lane should apply the source-safe separator in the Yarn choice and its scene decision, leave the glossary entry as reviewed, and rerun the paired reader on the current draft before ordinary batches. This handoff leaves the live writer's files alone.

The read-only audit, snapshots and results are under `localization/work/paired-reader-regressions-20261110.OGNwFq/`. The initial report SHA-256 is `7f6cf26032810ce5d3f2d5b09c2e960513b965195354b4afe860c321a2d5bb51` and the paired control receipt SHA-256 is `6af544ccc4ff6862ac3e38a3d8224a885e4a7f8249321709913329797f58b388`.
