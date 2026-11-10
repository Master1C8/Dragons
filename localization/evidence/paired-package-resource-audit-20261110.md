# Paired package resource audit

2026-11-10. Checked the pinned English macOS `9/12/2026_a93aa21a` and
Windows `9/9/2026_ee944596` Data directories against the existing complete
Russian packages. The same v42 inventory and packaging paths serve the six
Terra CLI locales. This audit exercises file preservation on the actual
packages as a control for those shared paths.

| Platform | Stock Data files | Byte-identical files | Changed files | Added files |
| --- | ---: | ---: | ---: | ---: |
| macOS app | 244 | 233 | 11 | 1 |
| Windows ZIP applied to an isolated stock copy | 259 | 248 | 11 | 1 |

The changed files are `level0` through `level6`, `sharedassets0.assets`,
`sharedassets1.assets`, `Managed/Assembly-CSharp.dll` and
`Managed/YarnSpinner.Unity.dll`. The addition is the speaker companion DLL.
The full path and SHA-256 comparison found zero removed files. All 12
Windows archive members matched their payload digests, and their source
digests matched the pinned files or expected absence. The Windows source
tree still matched its pre-check hashes. The earlier QA directory is now
incomplete for this comparison, so this check applied the ZIP to a new
verified stock copy and preserved the earlier directory.

An independent raw-object diff of those nine Unity assets confirmed identical
object identity and type sets. It compared 30,197 unchanged objects on macOS
and 29,802 on Windows. The 82 macOS and 104 Windows changed objects were
all independently bound to v42 UI or settings display candidates, the two
pinned Yarn objects, or the four source-bound speaker contrast targets.
The Windows object diff reads the original ZIP members and validates their
manifest digests. This establishes exact preservation of non-target objects
inside the changed files. Target-object field checks and managed method
checks still follow their dedicated adapters. The object delta receipt
`serialized-object-delta.json` has SHA-256
`dc81148bd6568fb5eff0b77fdee205c8b684ab89daadb69dc3d74f302a78cb56`.

On both platforms the existing verifiers also checked all 31 StreamingAssets
files and all four TextAssets within the 17 pinned serialized assets. Both
TextMeshPro line-breaking references and the line-breaking mode match stock.
Both Unity built-in resource files stayed byte-identical to their own stock
builds. Their one MonoBehaviour resolves to the Unity `GameSkin` GUISkin on
both builds. The local Addressables catalog has a separate
[key and location audit](addressable-catalog-locations-20261107.md#bundle-options-and-key-coverage-2026-11-09).
The original game, saves and textures were left untouched.

Compare full file SHA-256 maps and require only the listed delta after
applying the 12 manifest members to a verified isolated Windows stock copy.
Run the two existing validators against the signed macOS app and the applied
Windows copy with the pinned `localization/font_probe_requirements.txt`.

```sh
python -B localization/verify_streaming_assets.py PLATFORM STOCK_DATA CANDIDATE_DATA
python -B localization/verify_text_assets.py PLATFORM STOCK_DATA CANDIDATE_DATA
```

The comparison command and five receipts are under
`localization/work/shared-source-reconcile-20261110.k7cLAb/`. The paired
file receipt SHA-256 is
`0720c5dba6923ccd6b43b54107fe3c3d08a27a3d6184af422034e4d194ba3d25`.
The Windows ZIP is the same artifact as in the
[Russian build verification](russian-build-verification-20261110.md).

## Serialized source follow-up

All 17 root Unity serialized files in each actual Data directory match the
existing pinned asset inventory. A source-only scan resolved all 3,498 macOS
and 3,435 Windows MonoBehaviour script references, independently reproducing
the counts in the [extended text-route audit](extended-text-routes-20261110.md).
Among the selected built-in text and media object types, the only hits were
the four known TextAssets. Unity built-in resources were checked separately.

Outside the game, TMP, legacy UI, Yarn, settings and input assemblies already
covered by dedicated recipes, 577 macOS and 576 Windows components round-tripped
byte for byte. Their 221 nonempty payload string occurrences per build are the
previously audited localization listener's method and argument type, probe
volume scene GUIDs, render debugger prefab types and animation triggers, rig
serialization versions and a decal texture property name. This bounded scan
found no additional player-facing phrase among those fields. The general
schema could not round-trip 79 objects per build. The Unity Localization
settings object among them has a separate verified segment decoder. The other
78 are light/decal, probe volume, render-pipeline settings or orbit-camera
components. All 79 objects in each build matched the packaged controls byte
for byte, across 13 assets per build. This closes their byte preservation in
the audited packages. Their unresolved schemas still limit source discovery.

The source-only component type and field reports are in the same work folder.
Their file names end in `-serialized-component-types.json` and
`-additional-components.json` respectively. The unresolved-object comparison
receipt SHA-256 is `13aaa471787cfb0679a695601b401fcfa3eadd2f21a3d212754a50109686d98f`.
No images or textures were decoded or altered for this pass.

## Six-locale worklist reconciliation

The existing `de`, `es`, `fr`, `it`, `pl` and `pt-BR` exports have the same
ordered 1,947 authoring rows, build mappings, source values, v42 inventory
and Yarn scope hashes, and 27-case registry. Each file has its own locale
identifier. Of the 1,126 distinct special-scene source references, 46 are
source identities outside the authoring rows. All 46 exist in the pinned
inventory. Thirty-six remain exact, including 15 fragment delimiters and
21 managed or UI templates and fallbacks. Ten managed occurrences feed the
two existing paired locale inputs `display:slot-new` and
`display:yarn-missing-line`. The [Polish source-binding receipt](../pl/CHECKPOINT.md#special-scene-structural-preparation)
records the individual source roles and the equality check confirmed this
same scope across all six lanes. There are zero unexplained missing authoring
rows among these registered case references.

The source gate remains open. Exact file preservation covers untouched
resources even when they contain engine metadata. It does not classify every
player-visible source or prove the complete field-level preservation contract
inside the 11 changed files. The remaining work is to reconcile indirect
runtime text consumers and additional resources against the approved visible
scope, then verify that the parser-derived contract covers every protected
occurrence. The v42 inventory and existing locale worklists retain their
current fingerprints.
