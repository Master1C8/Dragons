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

## Managed declaration metadata

The two rewritten managed assemblies in each Russian control package passed
an independent declaration check against their source DLLs. The audit compares
assembly and module identities, existing dependencies, type and interface
declarations, fields and constants, method and parameter metadata, properties,
events, custom attribute blobs, and managed resources. It binds the stock
inputs and the Cecil reader by SHA-256.

| DLL | macOS types / methods / fields | Windows types / methods / fields |
| --- | ---: | ---: |
| Assembly-CSharp | 466 / 2,465 / 1,667 | 459 / 2,408 / 1,637 |
| YarnSpinner.Unity | 172 / 772 / 574 | 172 / 772 / 574 |

The Yarn assembly adds the declared `Yarn.Unity.VnSpeakerDisplay` type and
the `Dragons.SpeakerPresentation` assembly reference. The verifier checks
their identities and helper method declarations before comparing existing
metadata. The package rebuild and adapter checks remain responsible for the
approved instruction edits and the companion's bytes. Raw PE layout and
instruction operands are outside this declaration check.

```sh
dotnet build localization/tools/managed-metadata-audit -o "$managed_metadata_bin"
dotnet "$managed_metadata_bin/managed-metadata-audit.dll" "$stock_dll" "$package_dll"
```

Run for both DLLs per package. Read the macOS DLLs from the signed app and
extract only the corresponding members of the verified Windows ZIP into a
scratch directory. All four receipts in
`localization/work/managed-metadata-20261110.NICDw4/` reproduced byte for byte.
A Cecil reserialization of the packaged Assembly-CSharp DLL passed, and the
same reserialization with only an `OnShow` parameter renamed failed at
`MenuSlotsNew`. An unpinned stock input failed before the metadata comparison.

| Receipt | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Assembly-CSharp | `afe5b165507bdf4c21c42a7439e2657691b276ad590dbd0ee21a72d6165d408d` | `0e939f9129f8eb0b268a778c65ac94afdfc954eaa809c220932409f514f29284` |
| YarnSpinner.Unity | `6e79e4a66cecd5c2e058913c7cdcdbc7d6849e220d2952c9df1a810342a5607c` | `c89b0adaf3f24d5272d371451ff77934af4b0063223e37083ea90865010c4bad` |

## Packaged Unity object payloads

`verify_packaged_objects.py` verifies the complete text-only package directly
against stock and the exact v42 locale inputs. It snapshots and validates the
inputs, then checks the actual app assets or the matching ZIP members. For each
scene it computes the expected TMP string bytes and pinned speaker contrast
change. It reuses the combined Yarn and settings checks for the two shared
assets, including the exact Yarn metadata and repaired project bytes. For all
objects in each checked file, the candidate must equal either the complete
expected edited bytes or the complete original bytes.

```sh
"$PYTHON" -B localization/verify_packaged_objects.py "$platform" "$stock_source" \
  "$locale_inputs" "$built_package" --locale "$locale" \
  --inventory "$shared_inventory" --yarn-scope "$paired_yarn_scope"
```

The complete Russian controls matched all 30,279 macOS and 29,906 Windows
objects across nine files each. Both contained the expected 1,823 Yarn
translations and five restored transitions. The shared settings object
checks accepted the 37 macOS and 31 Windows inputs. The known scene layout,
sprite and texture payloads were compared as object bytes. Positive controls
used the delivered asset bytes. Separate copies failed after changing one
byte immediately before the authorized speaker color field and one byte
outside the repaired Yarn project program.

Receipts are in `localization/work/packaged-object-readback-20261110.975Giq/`.
The macOS receipt SHA-256 is
`c062bd84ca66cdd457ad61f8594187ed26a747e8abce5fd67ba346e6e8083277` and
the Windows receipt SHA-256 is
`f8dfe31a1b93e576631a715d8b35f482c54a70a3f7cb398747c7e41cdf95a31a`.
This check covers the nine serialized files and leaves the separate signed
bundle, ZIP, managed and raw Unity metadata checks in place.

## Serialized animation callbacks

`inventory_animation_events.py` scans the 17 pinned root Unity files, both
built-in resource files and the three local Addressables bundles per platform.
All 250 AnimationClip objects on each platform round-trip byte for byte. Each
build has 50 events. All string arguments are empty, and their function names
have explicit exact dispatch roles.

| Callback | Events per build | Managed consumer |
| --- | ---: | --- |
| `PlayStepSFX` | 37 | Reads an integer step index and applies a material impact response |
| `PlayStepVFX` | 2 | Both same-named handlers return immediately |
| `PlayAudio1` | 9 | One-shot or tool audio playback |
| `PlayAudio2` | 2 | One-shot audio playback |

The seven matching managed method bodies are identical across builds. The
callback inventory adds no authoring IDs. Clip payloads remain exact under
the package object comparison for changed files and the file digest
comparison for untouched assets. A nonempty string argument or unknown
handler fails role classification with a matching positive control.

```sh
"$PYTHON" -B localization/inventory_animation_events.py PLATFORM STOCK_DATA
```

The output reproduced byte for byte on each build. The two reports and the
consumer IL are in `localization/work/packaged-object-readback-20261110.975Giq/`.

| Receipt | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| AnimationClip events | `867b162552b76fd42f9aa6ddd9fdb0872729b1c34be14dddf0faf86170943287` | `794ebb6467e1b3422eb5c8e98734b1671322c2017a6106fb0b6dcae2956d573b` |
| Managed callback definitions | `a785bc820522965a774458bca162f0a44e2a2f91f6cd60945b712427eb222ffe` | `a785bc820522965a774458bca162f0a44e2a2f91f6cd60945b712427eb222ffe` |

## Root streamed audio and graphics data

`inventory_streamed_payloads.py` binds all 15 root `.resS` files and five
`.resource` files per build to byte-round-tripped native Unity objects in
the 17 pinned root assets. Each physical stream path is referenced. The
extents do not overlap or leave unexplained bytes. The graphics files
have 1,394 zero alignment bytes in each build, and the audio extents
are contiguous. Every audio extent begins with the FSB5 signature. The
five complete audio files have identical SHA-256 values across platforms.
No VideoClip object occurs in these pinned assets.

| Source object with an external stream | macOS | Windows |
| --- | ---: | ---: |
| AudioClip | 159 | 159 |
| Texture2D | 632 | 625 |
| Cubemap | 32 | 32 |
| Mesh | 221 | 220 |

The stream files contain encoded audio and graphics data. Their inventory
adds no text-authoring IDs. The read uses serialized object metadata and
stream boundaries. Image and sound contents stay encoded.

```sh
"$PYTHON" -B localization/inventory_streamed_payloads.py PLATFORM STOCK_DATA
"$PYTHON" -B localization/inventory_streamed_payloads.py macos STOCK_DATA --candidate-data PACKAGE_DATA
```

The two source reports reproduced byte for byte. The revised Polish app
contains all 20 original files byte for byte. Its Windows ZIP contains
no replacement member for any of those 20 stock paths. Focused checks
accept a zero alignment gap and a contiguous FSB5 extent, then reject a
nonzero gap, an overlapping range and an unexpected audio signature.

| Receipt | SHA-256 |
| --- | --- |
| macOS stock and revised Polish stream comparison | `016e8d425bb16cfe597ce683ca9174b36d0932b14ce63fc8f012586a85663291` |
| Windows stock stream inventory | `8bb761dd0bf658baffca0586695623d04a168d425903afcc63cac46ef0be0d41` |
| Revised Polish package stream receipt | `771fa4f0d47b9469c38593d59e67d672ffcc6b99db308ac0aaba3ba2605ed28f` |

The receipts are in `localization/work/streamed-payloads-20261110.SjeClJ/`.
The same folder records a selected managed-to-native boundary scan across
the pinned Managed inventories. The game assembly has no P/Invoke or
internal-call declaration. Its selected platform-facing calls cover the
Steam overlay callback, Steam initialization and teardown, warning
logging, the Steam ID used in save paths, and quitting the application.
The macOS-only old save manager adds two calls to the same save-path route.
The scan describes the managed boundary for these APIs.

The [source readiness decision](source-readiness-v42-20261110.md)
reconciles these resource and preservation checks against the supported
stock builds. The v42 inventory and all six worklists retain their
fingerprints. Each delivered locale needs its own package verification.

## Polish draft package read-back

The complete authored Polish input from `da65676` has 1,947 IDs and SHA-256
`cbc8b2ea7e50811cac5eab4425618ed97a5f234ee864bdb23e49213b809ab02f`.
The two draft packages in the Polish CLI's `resume-01` directory passed the
independent packaged-object, serialized-metadata and managed-declaration
comparisons against that exact input and the pinned originals. The signed
macOS app passed deep strict verification. The Windows ZIP passed its CRC
check and has SHA-256
`c47184503065d7f537aede628b095dfab69c248e04cb956013ee9f56a7d45034`.
The macOS package receipt SHA-256 is
`f1b13b43e2f5c837be1fc030de4fe49fe574d832e924f127abfc4f7addc5a76a`.

| Read-back receipt | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Unity object payloads, nine files | `ee1afcce69142890c3923acf73e0b6a0a57eedd0aa919cace6f81da604286626` | `539d9419f339d98713b5902b60b6dbbd8f51067d4e6c1117a52507bcf414e1fb` |
| Raw serialized metadata | `8339b7bc47c0b16c79c33a6e716e8f041d534ab8b70f4552e22eb79d0fe6ee0f` | `98db2ec47d01f4d10d4bf470977d280da393ec3b0170bd967b802c6a7023fa84` |
| Assembly-CSharp declarations | `6f24a8725f4e7be5fe70cde5a8e00952fc1a9ff5a3455e089b0dcd0e96d8054b` | `dea6dbf7267dd6754a5fa2fca4a655c83eaa5924b8a4adf74f083ce9fdd2bc9e` |
| YarnSpinner.Unity declarations | `ebab42d6288436574ce8d53d654beb993f8b196d99644c1e1fe38ef9d6759f11` | `7309218f3c196d3904f627d89276042f8071100280aa823609e8c4f750e653f1` |

Receipts and the exact authored input are in
`localization/work/pl-independent-package-20261110.O0cNAR/`. The two packages
contain the expected locale payloads across 30,279 and 29,906 Unity objects.
Polish editorial, delivered-game runtime and visual acceptance are tracked
separately.

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
