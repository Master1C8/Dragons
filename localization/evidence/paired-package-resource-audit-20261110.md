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
the audited packages.

A second pass recovered an exact schema prefix for all 34 decal and 33 light
components per build. The schema's only string is the Unity object name.
The remaining four or eight bytes per object consist exclusively of 32-bit
words equal to zero or one. The data therefore adds no display strings to the
known stock scope. `serialized-light-decal-tails.json` has SHA-256
`c393b5f9da0a2eea6a2870a43a1428888fbb3fc543bb8b569087f04ebb8a3b7e`.

The remaining eleven components on each build now round-trip in full with
`inventory_render_components.py`. The tool supplies the 31 source-bound
managed-reference schemas and corrects string-array containers that the
generator labels as scalars. The stock graph and lighting scans produce
identical field paths, roles and values across builds despite the platform
object-ID differences. All 22 raw object hashes match the existing package
preservation receipt. A new nonempty field without a declared role is rejected.

| Component | Objects per build | Nonempty strings per build | Bound roles |
| --- | ---: | ---: | --- |
| Orbit camera | 4 | 244 | Graph IDs, ports, camera parameters and type or object names |
| Probe volume baking | 6 | 108 | Scene and resource IDs, streamed paths, scenario keys and object names |
| URP global settings | 1 | 68 | Rendering layer names, managed type identities and the object name |

On both pinned Managed inventories, `CameraDirectionSet.PositionCamera` passes
`Distance` to `BaseGraph.SetParameterValue`, whose body compares it to the
stored parameter name. Graph port fields feed edge deserialization, connection
and delegate construction. Lighting scenario names participate in cell-data
resolution, selection and blending, and the probe volume debug registration
also reads them. The inspected URP layer API calls the native rendering-layer
name getter. The direct scan found no separate managed caller of that API in
the pinned game libraries. These are rendering and graph fields. The audit
does not infer the absence of arbitrary indirect or native debug consumers.

Reproduce on each original Data directory with:

```sh
python -B localization/inventory_render_components.py PLATFORM STOCK_DATA
```

Each report reproduced byte for byte in a second run. Receipts and the local
IL scanner sources are in `localization/work/camera-schema-20261110.9Z7wXW/`.
The macOS and Windows field reports have SHA-256
`75cdc4b49476f3e0caafeb261e15d9d43ea87bac2fbb6541458b2cb761265947` and
`3fd56a8ffc02c5183625c85aa63d2ed9b639642e21bff58dc2e5a4bbea8442a9`.
Camera IL reports match each other at
`208a6843e807a0258cab976e95a4b3f323857abc30cf012d87b7430b4b29227c`.
Render IL reports match each other at
`84d4c37facb9acb1dd4840da7ac51ad9487cb0cac377d219b280efe163bfe50c`.

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

## Rebuild from the shared translation file

The current macOS and Windows package commands rebuilt the complete Russian
control from `localization/ru/translation.json` using the pinned stock sources,
v42 inventory, Yarn scope and managed/speaker tools. The rebuilt signed macOS
app has the same 245 Data-file hashes as the earlier complete package. All
12 Windows replacement payloads and their member names match byte for byte;
the archive passes the CRC check. Both package receipts differ only in the
`dialogue.json` input digest. On each platform the new materializer's 1,823
key/source/target records are exactly equal to the earlier platform JSON map
in Git. The object key order differs, which accounts for the receipt and
Windows archive SHA-256 changes without any game payload difference.

The two build logs and the exact comparison receipt are in
`localization/work/paired-package-replay-20261110.bH9dWR/`.
`comparison.json` has SHA-256
`40f50a49d83b01159c5cf458d29ad09037f4acc5023d984dcdd0d85c5f442f7f`.
The targeted assembler, paired input, Yarn scope and preservation, combined
asset, component, non-Yarn, TextAsset and StreamingAssets tests passed, 33 in
total. This reproduction exercises
the complete v42 packaging path on the existing Russian control; it does
not expand the extracted source families or settle runtime reachability.

`verify_locale_package.py` makes the package replay check repeatable for
each locale. The existing Russian control artifacts passed with their exact
historical platform inputs restored from Git `702cb7e^`. The complete macOS
bundle matched all 284 files, paths and modes and passed signature verification.
All 13 Windows ZIP members matched the reference, including the receipt and
12 payloads. Two focused regressions checked a matching control and rejected
a modified macOS file outside the localized assets and a changed ZIP member
with matching inventory and receipt. The rebuild preserves the builder's
source-pinned object and managed checks. This closes package comparison for
these two artifacts. Source discovery and runtime reachability remain open.

The same verifier now independently compares the original Unity v22 metadata
against the actual app files and ZIP members. It permits the total file size,
each object's stored size and relative offset to change. Type records, object
IDs and type indices, script and external references, reserved fields and the
rest of the metadata must match byte for byte. Object extents must stay within
the file, with at most 15 zero padding bytes between objects and at the end.
The unchanged portions of the metadata matched across all nine replaced Unity
assets per platform, covering 30,279 macOS and 29,906 Windows object descriptors.
A focused regression permits a longer payload that relocates the next object
and rejects a same-length external path mutation and nonzero payload padding.

The integrated verification used the actual complete Russian control packages
and historical inputs restored from `702cb7e^`. The receipts in
`localization/work/serialized-metadata-20261110.rrvXVj/` have SHA-256
`f814bda5cab3deb57757d03efacc9bbda7e49e177c070f4ef67c88230cdb7b59` for macOS and
`4c01d6ab325ca222fa1689e243363cf8e60b21afda08d3bfea89b1c6e287c122` for Windows.
This closes the raw metadata comparison for the nine assets in the controls.
Object payloads and managed assemblies retain their separate checks.

The source gate remains open. Exact file preservation covers untouched
resources even when they contain engine metadata. It does not classify every
player-visible source or prove the complete field-level preservation contract
inside the 11 changed files. The remaining work is to reconcile indirect
runtime text consumers and additional resources against the approved visible
scope, then verify that the parser-derived contract covers every protected
occurrence. The v42 inventory and existing locale worklists retain their
current fingerprints.

## Concurrent commit ownership

Write the owner marker only after a successful exclusive `mkdir` of the Git
commit lock. A failed acquisition must leave the directory, marker and index
untouched. Hold the same ownership through stage, complete index inspection,
commit and committed-tree verification. The Polish command that produced
`533c375` completed its intended tree verification before its cleanup failed
because another worker wrote an owner marker after that worker's `mkdir`
failed. The subsequent label identified the Portuguese session even though
the acquisition had failed. Reconcile the exact original commit command,
verified tree and live process identities before recovering that lock. A
busy-lock regression must show the original owner bytes and index intact.
