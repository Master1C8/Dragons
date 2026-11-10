# Stock source readiness for the six CLI locales

**Passed for authoring.** This decision applies to the English stock
macOS `9/12/2026_a93aa21a` and Windows `9/9/2026_ee944596` builds,
with text baked into textures excluded by the owner. It covers the
game's shipped text and the existing source-bound locale adapters.
Injected mods, custom external content and the Steam client interface
are outside that scope.

The shared inventory SHA-256 remains
`79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`.
The paired Yarn scope remains
`753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30`.
The v42 file and worklists retain their original bytes so active CLI
sessions can continue from their exact checkpoints. Their historical
provisional labels are superseded by this decision for these hashes.

## Coverage and protection

- The fresh worklist exporter reopened both stock builds. The same
  1,947 authoring IDs, build-specific sources, routing bindings and
  27 special-case groups match all six saved worklists. The 27,113
  inventory IDs are unique and the exact-role validator accepted the
  role coverage and source bytes. The two build readers accepted
  1,923 macOS and 1,941 Windows authoring bindings.
- All 41 root files on each build are accounted for by 17 serialized
  files, 20 native streams and four engine/product sidecars. The
  reconciliation also checks both built-in resources, every Managed
  assembly and all 31 StreamingAssets files. Windows plugin support
  files remain outside the locale overlay. The initialization manifests
  bind assembly names, type names and method identities to the stock
  Managed directory. The startup config contains engine settings and
  the app identity file contains company and product names.
- The serialized and managed route audits account for stock Yarn,
  legacy and TMP display paths, persistent UnityEvents, resources,
  the local Addressables catalog, managed declaration strings and
  animation callbacks. The single TMP input field on each build has
  empty text. The stock TMP style sheet at `resources.assets#1387`
  contains 11 style keys, markup and fixed asterisks. Both objects
  round-trip exactly. The audited unbound objective and debug templates
  and inactive Unity Localization fallbacks retain their source values.
  The managed-to-native trace places the selected game-specific native
  calls on the Steam, save identity and application lifecycle paths.
- The exact contract uses the inventory roles, source-bound adapters
  and whole-object or whole-file equality where fields are protected
  together. The fresh source read verifies 10,973 macOS and 10,936
  Windows exact game component fields. Yarn table metadata, retained
  speaker prefixes and approved transition repairs have separate exact
  checks. The packaged-object and serialized-metadata verifiers cover
  the nine changed Unity files. The two changed DLLs use pinned
  instruction edits and declaration checks. The two Russian controls
  and the complete Polish draft exercise the same preservation
  contract on actual packages.

The [paired package audit](paired-package-resource-audit-20261110.md),
[extended text route audit](extended-text-routes-20261110.md) and
[non-Yarn scope](non-yarn-translation-scope-20261110.md) record the
source bindings and reproductions. The reconciliation script is under
`localization/work/source-readiness-20261110.MqDA8v/`. The
[reconciliation receipt](source-readiness-v42-20261110.json) has SHA-256
`c4a2587e6fa57ca27fef6e9244665340a848fb7ec5b4efd87a5dede88f85d7a7`.
The shared canonical worklist content hash is
`f3444fce4dff7c79684651c2bc6434dcf2617decff2962aedcaac7581bdaba34`.

## Locale entry conditions

Each CLI can use its existing v42 worklist once its own glossary and
renderer prerequisites pass. Review all 27 locale-specific wording
decisions and technical contracts before ordinary batches. Recheck
exact preservation, editorial evidence, font coverage, both artifacts
and background runtime behavior on each delivered locale. A newly
discovered stock text path or changed source fingerprint reopens the
affected source coverage and downstream work.
