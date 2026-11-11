# Dragons recovery

The accepted VN Revival release is 0.2.1 with 30 languages on each platform.
The GitHub draft `archive-v0.2.1` stores the two accepted archives for the
maintainer. Its target is the source revision present at archival review,
`9d49f9ecfd39c22c6963a4235927f60a11600b9d`. The release was built before that
revision was verified on GitHub, so the target is not build provenance.

| Accepted file | Size in bytes | SHA-256 |
| --- | ---: | --- |
| `Dragons-macOS.zip` | 65,328,455 | `acda5664d2e283a84a2e51ecad4ceaa5c25bc7866c83c15a075875a9fdb758bb` |
| `Dragons-Windows.zip` | 63,984,695 | `35070df451dc3f239e1d491bfb94fb2de8fc52e15916a42c70c2e1cf29c29f0a` |

## Rebuild the installers with the accepted payloads

From the canonical checkout, use an authenticated account with repository
write access. The normal build requires SwiftPM, macOS signing tools,
MinGW-w64 and ImageMagick. It stages generated Swift resources in the checkout.
Start with no generated resources there, or use the exact resources from the
same accepted release. The build rejects differing resources.

```sh
mkdir -p localization/work
recovery=$(mktemp -d "$PWD/localization/work/recover.XXXXXX")
mkdir "$recovery/downloads"
gh release download archive-v0.2.1 --repo Master1C8/Dragons \
  --pattern 'Dragons-*.zip' --dir "$recovery/downloads"
bash installer/Scripts/restore-release-inputs.sh "$recovery/downloads" "$recovery/restored"
mac="$recovery/restored/macos/Dragons — VN Revival.app/Contents/Resources"
windows="$recovery/restored/windows/Dragons Windows/Resources"
bash installer/Scripts/build.sh \
  "$mac/DragonsInstaller_DragonsInstaller.bundle/Contents/Resources" \
  "$windows" "$mac/App.icns" "$recovery/build" "$recovery/dist"
```

The accepted ZIP hashes verify the archives as delivered. Rebuilding the
installer executables can change the signatures and ZIP metadata. Use the
table above when restoring the accepted distribution bytes.

The archive check downloaded both ZIPs from GitHub, built both installers
with fresh Swift resources and build directories, and compared the packaged
resources byte for byte. The rebuilt macOS app passed strict code signature
verification and contains arm64 and x86-64 executables. The rebuilt Windows
GUI is x86-64. Both rebuilt ZIPs passed integrity checks.

## Edit translations and rebuild game patches

The editable locale JSON files and their hashes are tracked. The recorded
`installer/App/LocalePackages.json` refers to working package locations from
the original delivery. For a translation change, follow the game patch
builders in [localization/README.md](localization/README.md), then generate a
fresh package inventory and prepare the installer payloads. The released
installer payloads above are sufficient for installer code changes, but
contain no stock game files and cannot compile a new translation by themselves.

Use the owned stock macOS build `9/12/2026_a93aa21a` and the stock Windows
build `9/9/2026_ee944596`. If the macOS game has the Dragons installer
backup, reconstruct a fresh stock app and verify all 281 files against the
tracked manifest. The destination's parent must already exist.

```sh
python3 -B localization/restore_macos_stock.py \
  "$HOME/Documents/Drag'N Wash.app" "$recovery/Stock.app"
```

The Windows stock Data directory was verified on the external CrossOver
volume. Both game sources are owner's copies. The archive contains no
game distribution.

## Restore the v42 translation build inputs

Both released platform inventories use the same v42 source inventory and
Yarn scope. The separate maintainer draft `recovery-inputs-v0.2.1` holds
these two extracted inputs. Keep this draft private. Restore into a fresh
directory inside the same recovery workspace:

```sh
mkdir "$recovery/v42-download" "$recovery/v42-inputs"
gh release download recovery-inputs-v0.2.1 --repo Master1C8/Dragons \
  --pattern Dragons-v42-build-inputs.zip --dir "$recovery/v42-download"
(
  cd "$recovery/v42-download"
  printf '%s  %s\n' \
    77995ec1fcb3e753986a52612ab782540db8affaf03439cb15aa89a2ffca9939 \
    Dragons-v42-build-inputs.zip | shasum -a 256 -c
)
unzip -q "$recovery/v42-download/Dragons-v42-build-inputs.zip" -d "$recovery/v42-inputs"
```

The expected SHA-256 of each extracted file is in
[the v42 receipt](localization/evidence/yarn-fragment-markers-20261110.md).
The ZIP and both extracted files were verified after downloading the draft.

For changes to the shared source inventory itself, the
[inventory reconstruction receipt](localization/evidence/archival-source-inventories-20261111.json.gz)
pins the discovery exports and the corresponding Git revisions. Download the
receipt's export archive from the same maintainer draft, verify its SHA-256
and extract the JSON files. Rebuild v42 or select an earlier name from the
receipt:

```sh
python3.12 -B localization/restore_source_inventory.py \
  localization/evidence/archival-source-inventories-20261111.json.gz \
  combined-provisional-v42-20261110.json \
  --exports "$extracted_exports" --output "$recovery/rebuilt-inventory.json"
```

The tool verifies the exports and uses the recorded assembler and role
manifests from Git. The archival check reproduced v42 and 30 earlier
inventories byte for byte using the downloaded exports.

The [historical inventory delta receipt](localization/evidence/archival-historical-inventory-deltas-20261111.json)
pins 16 earlier inventory snapshots and comparison inputs. Download its
archive from the same draft and verify the archive and patch hashes. Rebuild
each row's `baseInventory` with the command above, verify its SHA-256 and
decode the matching patch with Zstandard 1.5.7.

```sh
zstd -q -d --patch-from="$verified_base_inventory" "$verified_patch" -o "$fresh_output"
```

Verify the decoded file's SHA-256 and restore its recorded mode. The
[inventory copy receipt](localization/evidence/archival-inventory-copies-20261111.json.gz)
maps old paths to an extracted `export`, a rebuilt `inventory` or the
original path recorded in the `delta` receipt. Copy the corresponding
verified bytes and apply the recorded mode. The check restored all 16
snapshots and matched all 67 copies to their recovered sources.

The [early inventory report receipt](localization/evidence/archival-initial-inventory-reports-20261111.json.gz)
pins 21 reports built from the original game data. Export the listed
revision and run its tool against the verified stock paths. For
`map_yarn_context.py`, pass both Data paths as `--macos-data` and
`--windows-data`. The hierarchy and level tools take platform and Data
path. The UI exporter takes the macOS Data path, the recorded asset
and `--export "$base_report"`.

Build the two managed scanners in Release with the pinned SDK and
Mono.Cecil. Pass platform and the verified stock Managed directory to
`text-setter-consumers`, with the optional recorded `argument`.
Pass platform and the stock
`Assembly-CSharp.dll` to `managed-strings`. Capture stdout as the base
report for both scanners and the Python inventory commands. Then run:

```sh
python3.12 -B localization/restore_initial_inventory_report.py \
  "$early_inventory_receipt" "$recorded_path" --base "$base_report" \
  --output "$fresh_report"
```

The helper verifies both fingerprints and reapplies the early JSON
layout and fields recorded in the receipt. For the earlier resource-route
reports it omits the two categories added by the later scanner.

For the nine locales with additional font inputs, download
`Dragons-font-build-inputs.zip` from the same maintainer draft. Verify its
SHA-256 before extracting it into `$recovery/fonts`:

```text
801372ac08bfd35e8c67599ff88ad5c8b455dd4d4972c6cff1e72cc488721e7d
```

For `ja`, `ko`, `zh` and `zh-TW`, use `cjk/<locale>.otf` as `--cjk-font`.
Use the license from `LocalizationPayload/Licenses/<locale>/NotoSansCJK-OFL.txt`
in the recovered platform installer as `--cjk-license`.

For `ar`, `fa`, `he`, `hi` and `th`, use the extracted `shaped` directory as
`--complex-plans` and the platform installer's
`LocalizationPayload/Licenses/<locale>/NotoShaped-OFL.txt` as `--complex-license`.
Build `localization/tools/prepared-text-probe/prepared-text-probe.csproj` with
.NET 8 in Release configuration. Use its DLL for `--complex-tool`. Resolve
`Managed/Dragons.PreparedTextLayout.dll` in the platform installer's locale
record in `PackageConfig.json`, then use its `payloadPath` and `payloadSHA256`
as `--complex-layout` and `--complex-layout-sha`. Pass
`73d128727531f04feb2990e9b369d7da196ca7746254109f695eaa3a428a5ae4`
as `--complex-report-sha`. The builder checks that the archived shaping plan
matches the exact release translation. Regenerate shaping plans for text edits.

For regenerating plans, the maintainer draft also contains
`Dragons-shaping-source-inputs.zip` (SHA-256
`d2bde546b9d160ef605731636c7051ac5b1a1b4212881bce7d15a8de8b60690b`). It holds
the pinned Arabic, Hebrew, Hindi and Thai source fonts and licenses, plus the
paired source worklist. Use Python 3.12 with `font_probe_requirements.txt` and
`uharfbuzz==0.51.7`, ICU 78 and the pinned [reference shaper](https://github.com/Master1C8/the-murder-of-sonic-the-hedgehog-localization/blob/d9213cfbc4b650f73be80e46c54a340f26fd941a/Scripts/prepare-complex-script-fonts.py).
The reference shaper's SHA-256 is
`30c13e3ba4a7650528840bbbe09ad3c73ccd4029a0f778b9387ca7cb3485cbb8`.

```sh
python3.12 -B localization/probe_complex_fonts.py --rtl-corpus --ltr-corpus \
  --icu "$icu_library" --macos-data "$macos_stock_data" \
  --windows-data "$windows_stock_data" --site-catalog "$site_catalog" \
  --worklist "$shaping_inputs/shared-worklist.json" --fonts "$shaping_inputs/fonts" \
  --hebrew-font "$shaping_inputs/fonts/NotoSansHebrewLatin-Regular.ttf" \
  --shaper "$reference_shaper" --output "$recovery/shaping-probe"
```

The downloaded sources were used to regenerate all five locales' plans.
The offline check found zero plan boundary failures and zero uncovered glyphs
on both platforms. The regenerated report has SHA-256
`37b34d1751b3e3b45766c9e6b4aab7eca8a0aabc7c57136b5f97a2a20ce2fb70`.
Use the frozen plans above for exact 0.2.1 reproduction.

The [historical font output receipt](localization/evidence/archival-historical-font-outputs-20261111.json.gz)
records exact matches for earlier font probes and their reports.
Export `localization` from the recorded Git revision and run the same
probe command from that export. Use the revision entry's `corpusFlags`
and pass ICU when that entry calls for it. Verify the catalog, source
archive and reference shaper fingerprints. The recovery check matched
all 42 files from that recipe.

The [font and signature delta receipt](localization/evidence/archival-font-signature-deltas-20261111.json.gz)
covers the earlier Persian font and two signed
libraries from the renamed discovery fixture. Download the receipt's
archive from the maintainer draft and verify its SHA-256. The Persian
`basePath` names the rebuilt font under the `fe6b56b` output directory.
Resolve the other base paths in the verified stock macOS app. Check each
base and patch hash, then decode with `zstd -d --patch-from="$base"`.
The decoded outputs matched all three hashes and both libraries passed
strict code signature verification.

`localization/rebuild_release_packages.py` selects the correct recovered
runtime, fonts and license for each locale. Build the three .NET tools in
Release configuration into `managed-fallback`, `speaker-display-probe` and
`prepared-text-probe` subdirectories of the directory passed as `--tools`.
Set `DRAGONS_SITE_LOCALES` to the actual canonical locale catalog.

```sh
python3.12 localization/rebuild_release_packages.py windows ja \
  --stock "$windows_stock_data" --accepted "$recovery/restored" \
  --v42 "$recovery/v42-inputs" --fonts "$recovery/fonts" \
  --tools "$tools_dir" --output "$recovery/DragNWash-ja.zip"
```

For macOS, use `macos`, the restored stock `.app` as `--stock` and a new `.app`
path as `--output`. `--inputs` selects the preserved historical locale files
when they are needed to reproduce older package metadata.

For the exact Russian 0.2.1 package inputs, download
`Dragons-ru-package-inputs.zip` from the same draft. Its SHA-256 is
`0059dffe0b9b48f3010bf57aad56903b25ba8746637d5fe4f86f92b77dd1b413`.
It contains a separate 12-file input directory for each platform, checked
against the original package receipts. Use the extracted `macos` or `windows`
directory as the locale input argument to the complete package builder.
Use the tracked `localization/ru/translation.json` for new edits.

For an exact rebuild of the Russian release, use Python 3.12 with
`localization/font_probe_requirements.txt` and build the managed fallback and
speaker patch tools with .NET 8 as described in the localization README. In the
accepted installer resources, select the Russian `PackageConfig.json` entry
for `Managed/Dragons.SpeakerPresentation.dll`. Pass the file at its `payloadPath`
under `LocalizationPayload` as `--speaker-runtime`. Its SHA-256 is
`3c83e4ebb75eeff0b5a64be7b13dfa7dfe7cf0d269566444f67ee1da1ae44502`
on macOS and `514d2d4d9b4c0f28960424c1eebfc67c2fd5b94509bcafda90fe5649eba7ca64`
on Windows. The recovered stock macOS app has an empty `Contents/Resources/VNRevival`
directory from the stock snapshot. Remove that empty directory from the
disposable recovered copy when matching the original Russian package tree.

The recovery check rebuilt and compared all 284 macOS bundle files and all 13
Windows ZIP members. The macOS bundle passed strict signature verification and
the rebuilt Windows ZIP also matched the original archive SHA-256 in full.
The historical Russian output paths in `installer/App/LocalePackages.json`
are generated paths. If regenerating the entire installer payload through
`prepare-payload.py`, recreate the Russian packages at those paths or update
a fresh inventory to point to the verified rebuilt outputs. The installer
rebuild using accepted payloads does not require these intermediate packages.

The remaining 29 locales rebuilt on both platforms from the recovered
inputs, including all nine locales that use additional fonts. All 29 Windows
ZIPs matched the original SHA-256. All macOS bundle files and their modes
matched. Only an empty `Contents/Resources/VNRevival` directory differed for
`ar`, `fa`, `fr`, `he`, `ko`. To reproduce the exact directory tree,
keep that empty directory in the disposable stock source for these locales
and remove it for the other locales. [Package rebuild evidence](localization/evidence/archival-package-rebuilds-20261111.json).

The per-locale intermediate package paths in `installer/App/LocalePackages.json`
are historical. Rebuild the packages there when reusing that inventory, or
make a fresh inventory with the new output paths. For unchanged installer
payloads, use the archived installer build route above.

`textures-with-text` is the owner's working directory.

[The duplicate-package receipt](localization/evidence/archival-duplicate-packages-20261111.json)
maps removed work outputs to their retained, byte-identical copies.
The [historical CLI asset receipt](localization/evidence/archival-duplicate-cli-assets-20261111.json)
maps duplicate Unity assets to a source path per hash. Recover the recorded
source if it has been archived, then copy it to the former path, restore
its mode and verify its SHA-256.
Use the same procedure for the [remaining generated asset duplicates](localization/evidence/archival-duplicate-generated-assets-20261111.json).

For the Windows slot-case source in that receipt, use the tracked
[synthetic input](localization/evidence/windows-slot-case-control-20261106.json)
with `windows_slot_ui_probe.py` and the verified Windows stock Data
directory. Pass it as `--locale-file` and select a fresh `.assets` output
directly in `localization/work`. The output must match SHA-256
`050d4c3450ab7aed852678d3a607375e1f91f18824cd0102ff68aa8843f8dc0e`
before using it to restore the recorded copies.

The [historical probe delta receipt](localization/evidence/archival-probe-deltas-20261111.json.gz)
preserves 26 source files referenced by earlier duplicate and fixture
recovery records. Download the receipt's archive from the maintainer draft
and verify its SHA-256. For each requested source path, select the stock
`sharedassets1.assets` for its recorded platform and verify `baseSha256`.
Verify the extracted patch member against `patchSha256`, then decode it
with Zstandard 1.5.7.

```sh
zstd -q -d --patch-from="$stock_sharedassets1" "$verified_patch" -o "$fresh_output"
```

Verify the output against the row's `sha256` and apply its recorded mode
before restoring the dependent duplicate or fixture. The recovery check
decoded every patch from the downloaded archive and matched all 26 files
byte for byte.

The [staged asset delta receipt](localization/evidence/archival-staged-asset-deltas-20261111.json)
uses the same procedure for the Alexander body controls on both platforms
and the Windows speaker control. Here each row names the stock file as
`basePath`, relative to the verified stock macOS app or Windows game
directory. Check the archive, patch and base fingerprints before decoding.
The three rebuilt files matched the original assets byte for byte.

The [Unity control delta receipt](localization/evidence/archival-unity-control-deltas-20261111.json.gz)
uses the same procedure for 53 earlier Unity controls and the signed Mono
library from the installer discovery fixture. For `stock-macos` or
`stock-windows`, resolve `basePath` inside the verified stock app or game
directory. For `release-ru-macos`, restore the accepted Russian
`sharedassets0.assets` with the release asset recipe below. Verify the
archive, patch and base hashes. All 54 files were restored from the
downloaded archive and matched the original SHA-256 values. The signed
library also passed strict signature verification.

The [runtime control delta receipt](localization/evidence/archival-runtime-control-deltas-20261111.json.gz)
pins 517 distinct generated outputs, including .NET launchers, game
test executables, assembly controls and test bundle signature resources.
For `macos` and `windows` bases, resolve `basePath` inside the verified
stock app or game directory. For `dotnet-host`, download the pinned
Microsoft host package from the receipt's URL and verify its archive and
member hashes. Extract `basePath` and use it as the Zstandard base.
Check each patch and restored SHA-256 and apply each destination's mode.
The downloaded delta archive reproduced all 953 files.

The [renderer assembly receipt](localization/evidence/archival-renderer-assemblies-20261111.json.gz)
maps 93 distinct TextMeshPro and Yarn assemblies to compact deltas from
verified stock assemblies or an earlier output in the same family.
Download its archive from the maintainer draft and restore a recorded
path into a fresh output:

```sh
python3.12 -B localization/restore_renderer_assembly.py \
  "$renderer_receipt" "$recorded_path" --archive "$verified_archive" \
  --macos-stock "$recovery/Stock.app" --windows-stock "$windows_game_root" \
  --output "$fresh_output"
```

The restore verifies the archive and each base, patch and output hash.
The downloaded archive reproduced all 93 distinct assemblies, including
the renderer sources referenced by historical binary copy receipts.

The [embedded display plan receipt](localization/evidence/archival-embedded-display-plans-20261111.json.gz)
records 16 historical plan and map files from those TMP assemblies.
Restore the file named in `assemblyPath` with the renderer assembly
command. Install the receipt's two Python package pins in a disposable
Python 3.12 environment, then run:

```sh
python3.12 -B localization/restore_embedded_display_plan.py \
  "$embedded_plan_receipt" "$recorded_path" --assembly "$restored_tmp_dll" \
  --output "$fresh_plan"
```

The helper decodes the embedded resource without loading the assembly
into Unity. For the early RTL plans, it applies the recorded single-line
selection and Persian glyph index mapping. The recovery check matched
all 16 output hashes and modes.

The [isolated profile receipt](localization/evidence/archival-isolated-profiles-20261111.json.gz)
records the stock PlayerSettings fingerprint and test identity for 208
historical assets. Restore into a fresh output with the pinned UnityPy
version and the stock `globalgamemanagers` file for the recorded platform:

```sh
python3.12 -B localization/restore_profile_control.py \
  "$profile_receipt" "$recorded_path" --stock-global "$stock_globalgamemanagers" \
  --output "$fresh_output"
```

The helper verifies the exact object changes and file hash. It restores
asset bytes without creating or loading a game profile.

The stock asset receipts identify replaceable files in old runtime probes
on [macOS](localization/evidence/archival-macos-stock-copies-20261111.json)
and [Windows](localization/evidence/archival-windows-stock-copies-20261111.json).
For an existing probe directory, run `python3.12 localization/restore_probe_assets.py`
with its platform receipt, the stock Data directory and the probe path.
The helper checks every restored file against the receipt and preserves
the recorded permissions. These historical probes are separate from the release
packages and the normal build inputs.

The nested stock receipts use the same helper with a different source root.
Use the entire restored stock `.app` for the
[macOS receipt](localization/evidence/archival-macos-nested-stock-20261111.json),
the owned Windows game directory containing `DragNWash.exe` for the
[Windows receipt](localization/evidence/archival-windows-nested-stock-20261111.json),
and the owned bottle's `drive_c/windows` directory for the
[CrossOver receipt](localization/evidence/archival-crossover-nested-stock-20261111.json).
The CrossOver receipt covers only stock `system32` and `syswow64` files. The
helper verifies the original bytes before putting each file back.

The [CrossOver application receipt](localization/evidence/archival-crossover-app-stock-20261111.json.gz)
covers additional historical bottle files identical to the installed CrossOver
26.3 distribution. For a retained bottle, pass
`/Applications/CrossOver.app/Contents/SharedSupport/CrossOver` as the stock root
and the retained bottle directory as the probe path. The receipt maps each
installed Wine source file to its bottle path. The recovery check restored
1,709 files into a fresh test directory and verified their bytes and modes.

For smaller stock assets and standalone copies, the same helper accepts
compressed receipts. Use the stock macOS Data directory for the
[macOS receipt](localization/evidence/archival-macos-remaining-stock-20261111.json.gz),
the stock Windows `DragNWash_Data` directory for the
[Windows receipt](localization/evidence/archival-windows-remaining-stock-20261111.json.gz),
and the owned bottle's `drive_c/windows` directory for the
[CrossOver receipt](localization/evidence/archival-crossover-remaining-stock-20261111.json.gz).

The [CrossOver runtime metadata receipt](localization/evidence/archival-crossover-runtime-metadata-20261111.json.gz)
covers 1,836 copied WinMD files, Mono machine configurations and services
tables. Use `restore_archived_members.py` with `--crossover-windows` set
to the owned bottle's `drive_c/windows` directory. The check reproduced
every recorded file and verified its size, hash and mode.

The [release asset receipt](localization/evidence/archival-release-probe-assets-20261111.json.gz)
records which 0.2.1 installer entry restores each matching historical probe
file. Use the verified, extracted installer archives and both stock Data
directories:

```sh
python3.12 -B localization/restore_release_probe_assets.py \
  localization/evidence/archival-release-probe-assets-20261111.json.gz \
  "$recovery/restored" "$macos_stock_data" "$windows_stock_data" "$probe_path"
```

The helper checks the decoder, stock inputs, delta files and restored asset
hashes. The archival check restored all 187 distinct release assets before
removing local copies.

The [stock and ZIP member receipt](localization/evidence/archival-stock-and-zip-members-20261111.json.gz)
maps remaining byte-identical historical copies to the restored stock macOS
app, owned Windows game directory, accepted installer resources, or retained
local test ZIPs. Restore files within an existing historical test directory:

```sh
python3.12 -B localization/restore_archived_members.py \
  localization/evidence/archival-stock-and-zip-members-20261111.json.gz \
  "$probe_path" --macos-stock "$recovery/Stock.app" \
  --windows-stock "$windows_game_root" --accepted "$recovery/restored"
```

The recovery check restored 1,148 files and verified their SHA-256 and modes.
If a ZIP source is listed in the historical locale, Ukrainian or shaped
package receipts below, rebuild the ZIP before restoring any member from it.

The [remaining input copy receipt](localization/evidence/archival-input-copies-20261111.json.gz)
covers additional copies from Git, the owned CrossOver Windows system
directories and previously verified recovery archives. Download the listed
archives from the maintainer draft and check their SHA-256 values. Pass
their directory as `--recovery-archives` to `restore_archived_members.py`.
Pass the owned bottle's `drive_c/windows` directory as
`--crossover-windows` for the system copies. The helper verifies the
size and hash of each restored member and applies its recorded mode.
The [additional system copy receipt](localization/evidence/archival-runtime-system-copies-20261111.json.gz)
uses the same option. All 272 copies matched files restored independently
from the owned Steam and GOG Galaxy bottles.

The [installer and Windows runtime copy receipt](localization/evidence/archival-installer-and-windows-runtime-copies-20261111.json.gz)
records 204 test bottle copies of the Windows installer cache and
system INI files. Restore those rows with the owned Steam bottle's
`drive_c/windows` directory as `--crossover-windows`. The GOG Galaxy
bottle matched the same bytes at each `alternateSource`. Restore the
remaining two rows with `--accepted` after restoring the accepted
installers. The check matched all 206 files and modes.

The [remaining stock runtime copy receipt](localization/evidence/archival-stock-runtime-copies-20261111.json.gz)
uses the same helper with the macOS and Windows stock roots. It covers
11,191 exact copies, including Unity streaming data and Mono configuration
files. The recovery check copied every recorded file and verified its
size, SHA-256 and mode.

The [installer copy receipt](localization/evidence/archival-installer-resource-copies-20261111.json.gz)
maps generated payload copies in old installer work directories to identical
files in the accepted 0.2.1 installer archives. Use the same helper and
`--accepted "$recovery/restored"`. The recovery check restored 3,086 files
and verified their hashes and modes.

The [image copy receipt](localization/evidence/archival-image-copies-20261111.json.gz)
maps duplicate historical screenshots and previews to retained files.
Restore them with the same helper and the relevant probe path. The check
restored and verified every duplicate by SHA-256 and mode.
If the source is an accepted upload PNG, restore it first from the gallery
source PNG archive described below.
The [QA copy source receipt](localization/evidence/archival-qa-copy-sources-20261111.json.gz)
maps 213 source files used by 371 rows in the image copy receipt.
Download `Dragons-qa-copy-sources.zip` from the maintainer draft and check
the archive SHA-256. Create the recorded parent directories for the needed
source paths. Restore those sources first with `restore_archived_members.py`
and `--recovery-archives`, then run the image copy receipt for the
dependent paths. The recovery check verified all 213 source hashes and modes.
For an image whose hash is cited by the historical QA documents, use the
[referenced QA image receipt](localization/evidence/archival-referenced-qa-images-20261111.json.gz).
Download its archive from the maintainer draft, verify its SHA-256 and
pass the archive directory as `--recovery-archives`. The check restored
all 212 cited image files byte for byte.
The [paired transition control receipt](localization/evidence/archival-transition-paired-control-20261111.json.gz)
uses the same recovery command for the original control frame and both
logs named in the transition report. The downloaded archive reproduced
all three files byte for byte.

The [rebuilt QA preview receipt](localization/evidence/archival-rebuilt-qa-previews-20261111.json.gz)
records 31 previews reproduced from the original PNGs. Check the input
PNG and installed preview helper hashes, then run the helper with the
recorded Pillow and libwebp versions:

```sh
python3.12 -B ~/.codex/tools/screenshot_preview.py "$original_png" --output "$fresh_webp"
```

Verify the WebP hash and apply the recorded mode. The
[preview source PNG receipt](localization/evidence/archival-preview-source-pngs-20261111.json.gz)
pins the 31 originals in the maintainer draft. Download its archive,
verify its SHA-256 and restore the needed original with
`restore_archived_members.py --recovery-archives` before generating
the preview. The check restored every original from the downloaded
archive and reproduced all 31 WebP hashes.

The [binary copy receipt](localization/evidence/archival-binary-copies-20261111.json.gz)
maps historical executable and library copies to exact files in the stock
game, accepted installers, installed CrossOver, owned Windows runtime, or
Mono.Cecil 0.11.6. Rows with a checkout source identify a retained test file.
For CrossOver application files, pass
`--crossover-app /Applications/CrossOver.app/Contents/SharedSupport/CrossOver/lib/wine`.
For the owned Windows runtime, pass `--crossover-windows` with the bottle's
`drive_c/windows` directory. For Mono.Cecil, pass `--mono-cecil` with the
NuGet package's `lib/netstandard2.0` directory. Only the source roots needed
by the selected rows are required. The check restored 42,207 binaries and
verified their hashes and modes.

The [historical probe binary receipt](localization/evidence/archival-historical-probe-binaries-20261111.json.gz)
records 17 patched Assembly-CSharp and YarnSpinner.Unity assemblies and
their byte-identical aliases. Download its delta archive from the
maintainer draft and use the same `restore_renderer_assembly.py` command
with this receipt, the verified stock roots and the recorded path.
Restore a checkout source before running the binary copy receipt for
its dependent paths. The recovery check verified all 31 files and the
52 references in the binary copy receipt.

The [managed probe rebuild receipt](localization/evidence/archival-historical-managed-probe-rebuilds-20261111.json.gz)
records twelve early DLLs and IL reports. Restore the named sources,
using `git cat-file blob` for the listed project descriptors. Build in
Release with the recorded .NET SDK and Mono.Cecil. Run each tool against
the verified stock platform files:

- `stock-scan` takes platform and `Assembly-CSharp.dll`. For the earlier
  Windows report, verify `unfilteredSha256`, then omit the recorded
  `METHOD` header and its instructions up to the next `METHOD` header
  or end of file.
- `disk-patcher` takes platform, `Assembly-CSharp.dll` and a fresh DLL
  path. The `speaker-line-probe` takes platform, `YarnSpinner.Unity.dll`,
  the recorded synthetic map and a fresh DLL directly in the recovery
  project's `localization/work`.
- `fallback` and `fallback-full` take the stock Managed directory.
  `wrap-inspect` takes the stock macOS `Unity.TextMeshPro.dll`. Capture
  stdout as the report.
- For `metadata`, restore the named control DLL with
  `restore_renderer_assembly.py`. Place the pinned Mono.Cecil DLL at
  `bin-final/Mono.Cecil.dll` next to the `mutate` directory. Run the
  built mutator with the control DLL, a fresh output path and
  `parameter`.

The recovery check verified the original fingerprints of all twelve
outputs and nine source files.

The [historical .NET probe build receipt](localization/evidence/archival-historical-dotnet-probe-builds-20261111.json)
pins 28 managed outputs whose source snapshots are in Git. Build with
.NET SDK 8.0.131 and access to the recorded NuGet dependencies:

```sh
python3.12 -B localization/restore_historical_dotnet_probe.py \
  localization/evidence/archival-historical-dotnet-probe-builds-20261111.json \
  "$recorded_path" --output "$fresh_dll"
```

The helper verifies each Git source and rebuilt output. The check matched
all 28 original DLLs and verified the 28 dependent entries in the binary
copy receipt. Restore a needed source DLL before replaying its copies.

The [historical symbol and assembly receipt](localization/evidence/archival-historical-dotnet-symbols-20261111.json)
uses the same command for 38 portable PDBs and 50 DLLs. The builds pin
the Git inputs, compiler paths and embedded-source selection observed
in the original portable PDBs. The helper reproduces the original
Source Link setting and verifies the restored bytes. All 88 outputs and
92 dependent entries in the binary copy receipt matched.

The [historical managed source receipt](localization/evidence/archival-historical-managed-source-deltas-20261111.json)
pins 125 project descriptors required by the generated metadata receipt
and 22 C# sources used by technical evidence or the text copy receipt.
Download its delta archive from the maintainer draft and use
Zstandard 1.5.7 with the canonical Git checkout:

```sh
python3.12 -B localization/restore_managed_probe_source.py \
  localization/evidence/archival-historical-managed-source-deltas-20261111.json \
  "$recorded_path" --archive "$source_delta_zip" --output "$fresh_source"
```

The helper verifies the archive, the base Git blob and the restored
file. All 147 files and 211 dependent text copies matched. The recovered
macOS settings probe also compiled with .NET SDK 8.0.131 against the
verified stock Managed directory.

The [Windows Yarn preservation input](localization/evidence/windows-yarn-preservation-control-20261107.json)
recreates the synthetic control in the
[preservation check](localization/evidence/yarn-preservation-check-20261107.md).
Use the Windows dialogue command below with locale `ru`. The rebuilt
asset matched the historical digest and passed the independent verifier.

The [source copy receipt](localization/evidence/archival-git-source-copies-20261111.json.gz)
maps retired local snapshots to byte-identical blobs reachable from its
recorded Git revision. Use `restore_archived_members.py` with the receipt
and a retained test directory. The Polish staged asset in that receipt
comes from the rebuilt `draft-v2` Windows package described below.

The [Yarn test asset receipt](localization/evidence/archival-yarn-probes-20261111.json)
records six synthetic missing-line assets. Restore a recorded path from the
matching stock Data directory with Python 3.12 and the pinned UnityPy version:

```sh
python3.12 -B localization/restore_yarn_probe_asset.py \
  localization/evidence/archival-yarn-probes-20261111.json "$recorded_path" \
  --stock "$stock_data" --output "$fresh_output"
```

The check reproduced all six files byte for byte and verified that only the
intended serialized object changed. Restore these sources first if the
generated asset duplicate receipt points to one of them.

The [historical locale package receipt](localization/evidence/archival-historical-locale-packages-20261111.json.gz)
pins seven German, French and Polish test builds. Recover the translation
from `localeSourceRevision` and check it against `localeInputSha256`. Use
the builder at `builderRevision` with the recovered v42 inputs and the tools
and speaker runtime named in the row. Verify their hashes before rebuilding.
Use the restored stock app for macOS and the verified stock Data directory
for Windows. Remove the empty `Contents/Resources/VNRevival` directory from
the disposable macOS stock copy before building.

```sh
git show "$locale_source_revision:localization/$locale/translation.json" > "$historical_input"
python3.12 -B "localization/build_${platform}_package.py" "$stock" "$historical_input" \
  --locale "$locale" \
  --inventory "$v42/combined-provisional-v42-20261110.json" \
  --yarn-scope "$v42/yarn-scope-v42.json" \
  --managed-tool "$managed_tool" --speaker-tool "$speaker_tool" \
  --speaker-runtime "$speaker_runtime" --speaker-runtime-sha "$speaker_runtime_sha" \
  --output "$fresh_output"
```

The five rebuilt Windows ZIPs matched the recorded SHA-256. The two rebuilt
macOS bundles matched the recorded manifest and every surviving file and
directory. Both passed strict code signature checks.

The [historical control receipt](localization/evidence/archival-historical-controls-20261111.json.gz)
records Russian and Ukrainian controls, the Arabic and Persian caption
packages, and two earlier standalone Unity test assets. Download the two
small archives named in the receipt from the maintainer draft and verify
their hashes and the hashes of the members you use. Extract each
`inputPrefix` as its own directory. Pass that directory as the Windows
synthetic, structure or guard input. For the Ukrainian staged assets, pass
its `structure-control.json` to the normal builders.

Use the normal build command above with the receipt's builder revision,
archived v42 inputs, Ukrainian tools and accepted speaker runtime. The
Russian pair uses the tracked Russian translation at that revision.
Compare its Windows ZIP directly. On macOS compare the manifest, the
recorded surviving files and directories, and the strict code signature.
For the Ukrainian staged assets, recover `sharedassets1.assets` from the
rebuilt macOS app or Windows ZIP and check its recorded fingerprint.

For the Arabic and Persian captions, use the tracked locale at
`builderRevision` with the archived `wrap` shaped tools, layout, plans and
license. Use the builder modules from this receipt's revision. For the
synthetic, structure and caption ZIPs, verify `basePackageSha256` before
restoring the historical ZIP from the rebuilt one. Only caption restoration
requires the object archive. The structure ZIP also has a historical
manifest timestamp and mode recorded in the receipt.

```sh
python3.12 -B localization/restore_historical_control.py \
  localization/evidence/archival-historical-controls-20261111.json.gz "$control_name" \
  --base "$verified_base" --archive "$verified_archive" --output "$fresh_output"
```

For `transition`, the base is `windows-choice-probe-v2.assets` restored from
the historical probe delta receipt. Use the object archive. For
`speaker-legacy`, the base is stock macOS `sharedassets1.assets` and the
archive is the control inputs ZIP. This restores a historical synthetic
test asset containing an intentional speaker delimiter. Verify the final
hashes before using any of these outputs to restore older duplicates,
including the Russian Windows duplicates recorded in
`archival-duplicate-packages-20261111.json`.

The [CLI and CJK package receipt](localization/evidence/archival-cli-cjk-packages-20261111.json.gz)
records the same rebuild procedure for the two Polish CLI drafts on both
platforms and the German Windows candidate. Use the exact translation from
each row's `localeSourceRevision`. Use the tool archive and Mono.Cecil
dependencies described in the Ukrainian receipt below. The three Windows
ZIPs and all surviving files of the two macOS bundles matched.

For the Japanese diagnostic builds in the same receipt, create a locale
template with `paired_locale.catalog` and `paired_locale.template` from v42.
For each ID, use its bound source text, with a `platforms` mapping when the
sources differ. Apply the two `syntheticInput.replacements` and serialize as
UTF-8 JSON with two-space indentation, unescaped Unicode and a final newline.
Verify the resulting input hash. Use the usual CJK flags with the recovered
Japanese font and license, then take `sharedassets1.assets` from the rebuilt
package. Both diagnostic staging files matched their recorded SHA-256.

The [CJK font control receipt](localization/evidence/archival-cjk-font-probes-20261111.json)
pins the ten earlier replacement-font controls. Invoke
`restore_cjk_font_probe.py` with the receipt, recorded path, `--stock` Data
directory, archived regional `--font` and fresh `--output`. For macOS,
first restore the accepted Russian `sharedassets0.assets` with the release
asset recipe and pass it as `--base-asset`. The Windows controls use the
stock asset directly. All ten controls matched byte for byte.

The [remaining CJK control and font receipt](localization/evidence/archival-cjk-remainder-20261111.json.gz)
records four additive Japanese fallback controls. Use the pinned Japanese
font and accepted OFL license with the stock Data directory for the
recorded platform. The command restores the Russian base from the accepted
installer for macOS and uses the stock base for Windows.

```sh
python3.12 -B localization/restore_cjk_append_probe.py "$receipt" "$control_name" \
  --stock "$stock_data" --accepted "$recovery/restored" \
  --font "$recovery/fonts/cjk/ja.otf" --license "$japanese_ofl" --output "$fresh_output"
```

For `japanesePackageAssets`, rebuild the Japanese synthetic packages with
the input recipe above and take the recorded `packageMember`. For
`koreanPackages`, recover `localization/ko/translation.json` from
`localeSourceRevision` and verify the input hash. Use
`rebuild_release_packages.py` at `builderRevision` with `--inputs` set to
that file, the archived Ukrainian tools with Mono.Cecil, and the same
stock and release inputs described above. The Windows ZIP matched its
recorded SHA-256. The macOS package matched the recorded manifest and
every surviving bundle file and directory, and passed strict signature
verification.

The receipt also maps `fontCopies` to exact members of the frozen font
build archive and `upstreamFonts` to the pinned upstream release URLs.
Verify each restored file's SHA-256 and apply its recorded mode.

To recreate the signed library from the historical installer discovery
fixture, download the receipt's `discoverySignature.delta` from the
maintainer draft. Verify its hash and the hash of `stockPath` in the
restored macOS app. Decode with Zstandard 1.5.7 as above, using the stock
library as `--patch-from`. The decoded library matched the historical
SHA-256 and passed strict signature verification.

The [Ukrainian verification receipt](localization/evidence/archival-uk-verification-20261111.json.gz)
pins three historical structure-control inputs and the two exact .NET tools
used by those builds and the older German, French and Polish builds above.
Download the receipt's archive from the maintainer draft and verify its
archive and member hashes. Copy the fingerprinted `netstandard2.0` DLLs
from Mono.Cecil 0.11.6 into both tool directories. For Ukrainian, use the
corresponding `uk/<variant>/structure-control.json` as the historical input
and the accepted installer speaker runtime with the recorded platform hash.
The normal builders reproduced all three Windows ZIP hashes and the
surviving files of the two retained macOS bundles. The rebuilt closure
package also supplied the exact Yarn asset for both fixture variants.

To rebuild an [Alexander or choice fixture](localization/evidence/archival-uk-yarn-fixtures-20261111.json),
use the Ukrainian closure package's `sharedassets1.assets` from the stock
platform's Data layout within the rebuilt package. Pass it as
`--base-asset` to `restore_yarn_probe_asset.py` with the fixture receipt.
The four rebuilt fixture files matched their recorded SHA-256 values.

The [shaped verification receipt](localization/evidence/archival-shaped-verification-20261111.json.gz)
pins the earlier renderer builds used by the Parallels fixtures. Download its
tool archive from the maintainer draft and verify its archive and member
hashes. Copy the Mono.Cecil DLLs from the Ukrainian receipt into each tool
directory. Use the archived v42 inputs, shaped plans and licenses described
above. The `current` variant uses the prepared-text project from its recorded
Git revision, built with .NET 8 in Release configuration. The `wrap` variant
uses the archived prepared-text tool.

Use the stock and locale inputs and normal package command above. Supply
`--complex-plans`, `--complex-report-sha`, `--complex-tool`,
`--complex-license`, `--complex-layout` and `--complex-layout-sha` from the
receipt and recovered inputs. Before invoking the builder, extract the five
recorded historical Python modules from `builderRevision` into a temporary
directory and place that directory ahead of `localization` in Python's module
search path. The verification invoked the package entry point through
`runpy.run_path` with this search order and preserved the normal arguments.
Remove the empty `Contents/Resources/VNRevival` directory from the disposable
stock macOS copy.

The rebuilt Windows ZIPs match their recorded SHA-256 values. The rebuilt
macOS packages pass strict code signature verification and match the surviving
bundle files and directories. The [staged renderer asset receipt](localization/evidence/archival-shaped-staged-assets-20261111.json)
maps five test files to exact members of those rebuilt packages. Restore
them using `restore_archived_members.py` after rebuilding the referenced
package. Restore the package and staged sources before restoring any older
fixture ZIP that references them.

The [Python environment receipt](localization/evidence/archival-python-environments-20261111.json)
pins the Python versions and dependency lists for four retired CLI environments.
Create a fresh venv with the listed Python and install those exact requirements
with `pip install --no-deps`. The recovery check installed the dependencies
and imported UnityPy, TypeTreeGeneratorAPI and fontTools. Its pinned
`tpk_ar` wheel was built from the source distribution.

The [Python target receipt](localization/evidence/archival-python-targets-20261111.json)
records the separate wheel installs used by three CLI locales and the
static shaping check. Use each recorded Python and pip version to install
its requirements into a fresh directory with
`python -m pip install --no-deps --target "$target" ...`.
The check imported the recorded modules and matched all surviving
package files. It also compared the generated script bodies, installation
records and compiled Python code.

The [German batch receipt](localization/evidence/archival-de-partial-20261111.json)
and the [early German and French batch receipt](localization/evidence/archival-de-fr-early-20261111.json)
cover 41 intermediate assets whose rebuilds matched byte for byte. The
[dialogue probe receipt](localization/evidence/archival-dialogue-probes-20261111.json.gz)
adds 19 exact matches with the same rebuild commands. Download
the corresponding input archive from the `recovery-inputs-v0.2.1` maintainer
draft, check its archive hash and extract the dialogue JSON files. Use the
recorded `archiveMember` when present. Match each
JSON and rebuilt asset to the SHA-256 in the receipt. Set `DRAGONS_SITE_LOCALES`
to the canonical locale catalog and use the stock Data paths described above.
Set `batch_locale` to the locale in the receipt, or `de` for the German-only
receipt.

```sh
python3.12 -B localization/dialogue_locale.py "$macos_stock_data/sharedassets1.assets" \
  --locale "$macos_batch_json" --output "$macos_batch_output"
python3.12 -B localization/windows_ui_locale.py "$windows_stock_data" sharedassets1.assets \
  --requested-locale "$batch_locale" --dialogue-locale-file "$windows_batch_json" \
  --output "$windows_batch_output"
```

The [historical installer receipt](localization/evidence/archival-obsolete-installers-20261111.json)
records the superseded build outputs. Its intermediate Windows installer
script can be recreated by extracting the compressed patch and applying it to
the Git blob named in the receipt. Compare the result to the recorded SHA-256.

The [legacy fixture receipt](localization/evidence/archival-legacy-fixtures-20261111.json)
records the retired five-language installer outputs and the exact Windows
executable used by the stock and ZIP member receipt. Download the fixture
input archive from the maintainer draft and check its SHA-256. Extract
`installer/Dragons Installer.exe` and verify the recorded dependency hash.
Restore it first if rebuilding the previous installer test directory. The
old complete installers were superseded by the verified 0.2.1 archives.
The previous Windows script is recoverable from the recorded Git revision.

The [installer delta receipt](localization/evidence/archival-installer-deltas-20261111.json.gz)
records eight historical installer deltas that can be reproduced from
existing asset archives. Recover the exact target using `targetReceipt`
and match `targetSha256`. Select `stockPath` from the verified stock app
or Windows game directory for the recorded platform. Use the encoder
from the accepted macOS installer and verify its SHA-256 first.

```sh
"$verified_encoder" -e "-A$application_header" -s "$stock_file" "$target_file" "$fresh_delta"
```

Use the receipt's `applicationHeader`, check the generated delta hash
and apply each destination's recorded mode.

The [installer delta copy receipt](localization/evidence/archival-installer-delta-copies-20261111.json.gz)
maps 49 duplicate VCDIFF files to their historical originals.
Restore those sources first from the
[legacy installer input receipt](localization/evidence/archival-legacy-installer-inputs-20261111.json.gz).
It pins 15 original deltas and four configuration files used by the
installer delta and historical text copy receipts. Download and verify
the archive from the maintainer draft, then restore the needed originals
with `restore_archived_members.py --recovery-archives`. The check matched
all 19 restored files. Each delta decoded to its recorded target hash
using the verified stock file and the accepted Xdelta executable. All
15 also re-encoded byte for byte using their original headers.

The [window and Yarn rebuild receipt](localization/evidence/archival-window-and-yarn-rebuilds-20261111.json.gz)
records 142 copies of two Swift test utilities. Compile the recorded
`window.swift` with the pinned Swift compiler and name the output
`window`. For `discovery`, export the two installer sources from the
recorded revision and pass them and `Discovery.swift` to `swiftc` in
the listed order, with `-o discovery`. Check the executable hash before
restoring the recorded copies.

For the 52 Yarn binaries, use `compare_yarn_versions.load` at
`stockImportRevision` with the verified stock Data directory and
platform spec. Its fourth return value is the stock program. For a
repaired variant, read the spec's `project` object from
`sharedassets1.assets` with UnityPy. Pass its raw bytes and platform
to `repair_project` from `repairRevision`. Read the little-endian
program length at `PROGRAM_SIZE_OFFSET` in the returned bytes and
extract that many bytes from `PROGRAM_OFFSET`. Verify the output hash.

The same receipt pins the signed Burst plug-in from the renamed
discovery fixture. Download its patch from the maintainer draft.
Verify the patch and stock plug-in hashes, then decode with the
recorded stock base and Zstandard. The decoded file matched the
original fingerprint and passed strict signature verification.

The [French test asset receipt](localization/evidence/archival-french-stock-20261111.json)
records the stock references used by the original French compaction. The
[French compaction receipt](localization/evidence/archival-french-compaction-20261111.json.gz)
pins both sets of patches and their original manifests in the maintainer
draft. Verify the archive and extract each row's `patchMember`. Use
`sharedassets1.assets` from the restored macOS or verified Windows stock Data
directory for the platform recorded in the row.
Verify the reference and patch hashes before restoring to a fresh file:

```sh
zstd -d --patch-from="$stock_sharedassets" "$patch" -o "$fresh_output"
```

Match the output to `sha256` in the compaction receipt and apply the
recorded mode. All 74 assets decoded from the downloaded archive matched
their recorded size and hash.

The [Windows stock ZIP receipt](localization/evidence/archival-windows-stock-zip-20261111.json)
lists all 287 files in the old Parallels test fixture. To recreate the
fixture, ZIP those relative paths from the owned Windows stock game directory
and verify each member against the listed SHA-256. The recovery check rebuilt
the fixture and verified all members without running it.

The [test fixture ZIP receipt](localization/evidence/archival-test-fixture-zips-20261111.json)
pins eight exact historical ZIPs used for Parallels and installer testing.
Download the receipt's components archive from the `recovery-inputs-v0.2.1`
maintainer draft, verify its hash and extract it. Set `windows_game_root`
to the owned directory that contains `DragNWash.exe`, and select a recorded
path from the receipt:

```sh
python3.12 -B localization/restore_fixture_zip.py \
  localization/evidence/archival-test-fixture-zips-20261111.json "$recorded_path" \
  --windows-stock "$windows_game_root" --components "$extracted_components"
```

The restore checks every member and the exact ZIP SHA-256. The receipt
identifies retained local test components alongside the stock game and the
small components archive.
When a checkout path has already been cleaned up, rebuild it from its
recorded source before running the fixture command. The shaped package and
staged asset receipts cover the earlier renderer ZIPs and their staged data.
The runtime control and isolated profile receipts cover instrumented
assembly and PlayerSettings files. The Unity control and binary copy
receipts cover the remaining archived asset and companion library paths.

The legacy fixture input archive also stores the exact live-renderer
companion DLL used by the older fixture ZIPs. Restore it to the path in
`companion` and verify its hash before replaying those fixtures. For the
six windowed Parallels ZIPs, extract the archive and verify its members.
Decode each `patches` entry from stock Windows
`DragNWash_Data/globalgamemanagers` into the specified component path,
checking the base, patch and output hashes. Pass the resulting component
directory and the legacy fixture receipt to `restore_fixture_zip.py`.
All six rebuilt ZIPs matched their recorded SHA-256 values.

The release card's visual delivery contains 150 published screenshot slots
across 30 locales. The upload readback matched all 150 hosted files.

The [published gallery receipt](localization/evidence/archival-gallery-copies-20261111.json.gz)
pins the locale, position and SHA-256 of every accepted screenshot. Run the
read-only export with the canonical SiteForMods CLI and use a fresh private
output directory:

```sh
"$site_cli" game screenshots export "$fresh_export" --game dragn-wash --all-locales
```

Match each slot and the hash of each downloaded file. The export reproduced
all 150 slots and the exact bytes of 121 historical local WebP copies.
The original delivery PNGs are separate inputs. To restore the historical
capture log, download the receipt's metadata archive from the maintainer
draft and run:

```sh
python3.12 -B localization/restore_gallery_capture.py \
  "$gallery_receipt" "$metadata_archive" "$fresh_export" "$fresh_log"
```

The helper verifies the private metadata and reconstructs the embedded
image bytes from the matching published export. Its output matched the
original capture log byte for byte.

The [gallery source PNG receipt](localization/evidence/archival-gallery-source-pngs-20261111.json.gz)
maps each accepted published slot to its original upload PNG. Download
`Dragons-published-gallery-source-pngs.zip` from the maintainer draft and
verify the archive SHA-256. Extract one member per source hash and verify
its size and hash. Each `files` entry records the original upload path
and mode. The archive contains 121 unique sources for the 150 accepted
slots. Its members retain the original PNG bytes for future gallery edits.

The [worklist and editorial report receipt](localization/evidence/archival-report-rebuilds-20261111.json.gz)
records 75 exact authoring worklist copies and ten editorial report
rebuilds. Use the commands in the [localization guide](localization/README.md)
at the recorded `builderRevision` with the verified stock Data and v42
inputs. For a worklist with `draftRevision`, use the tracked translation
from that revision and verify `draftSha256`. Omit the locale file argument
when that revision is absent. For an editorial report, use the recorded
exporter and retrieve the before and after translations from their Git
revisions. Check both hashes. Extract `recipeArchiveMember` from the
report input archive and `sceneMember` from the source inventory export
archive. Verify the archive and member hashes. The rebuilt outputs preserve
the original audit scope and report bytes.

The [additional authoring and scope receipt](localization/evidence/archival-authoring-scope-and-editorial-20261111.json.gz)
pins four templates and worklists, four Yarn scope reports and eight
editorial exports. Check the downloaded archive and catalog hashes.
Use the receipt's Git revisions with the normal commands in the
[localization guide](localization/README.md).

The early worklist and template commands load the locale catalog from
its former Desktop path. Export their `localization` directory into the
recovery workspace and run the recorded module with the verified catalog
assigned at import time. Pass the normal module arguments after its name.

```sh
python3.12 -B -c '
import runpy
import sys
from pathlib import Path
sys.path.insert(0, sys.argv.pop(1))
import dialogue_locale
dialogue_locale.SITE_LOCALES = Path(sys.argv.pop(1))
runpy.run_module(sys.argv.pop(1), run_name="__main__", alter_sys=True)
' "$revision_export/localization" "$verified_site_catalog" "$module" "$@"
```

For the early Russian worklist, export its tracked platform drafts and
pass them as `--draft-root`. Verify the base worklist hash. For each
platform entry without a `draft`, read its recorded file and line key
from that platform's draft directory. When the line exists, check its
source against the worklist and append its text as `draft`. Set each
build's `draftSha256` to null and recalculate its `draftCount` from the
entries with a draft. Write UTF-8 JSON with two-space indentation,
literal Unicode and a trailing newline. The Ukrainian worklist uses the
verified generated Ukrainian template as `--locale-file`.

For a Yarn scope report, restore the named inventory and run
`inventory_yarn_scope.py` from the recorded revision with both verified
stock Data directories. The two earlier v40 variants use the verified
scope as a base. Remove `scopePolicy` for the first variant. For the
structure control, append the receipt's `localeCoverage` block to the
unmodified v40 scope and serialize it in the same JSON format.

For the eight editorial exports, recover each input from its recorded
Git blob or archive member. Use the pinned scene export, v42 inventory
and v42 scope with the named exporter. All 16 restored files matched
their original fingerprints.

The [direct editorial export receipt](localization/evidence/archival-direct-editorial-exports-20261111.json)
pins seven working reports for Italian and Brazilian Portuguese. Recreate
the two worklists from the report rebuild receipt with no draft argument.
In a disposable directory, place the worklists at their recorded paths.
Restore the two translations and two Portuguese receipts with
`git show "$revision:$path"`. Restore the independent Portuguese review
from the cited technical evidence archive using its receipt. Verify all
seven input hashes before running the export.

```sh
export_dir="$report_root/localization/work/direct-editorial-20261110"
mkdir -p "$export_dir"
cp localization/tools/historical-direct-editorial/export.py "$export_dir/"
(cd "$report_root" && python3.12 -B localization/work/direct-editorial-20261110/export.py)
```

Verify each needed output's SHA-256 and apply its recorded mode. The check
matched the seven reports and the original exporter byte for byte. For the
two separate scanner project copies in `gitCopies`, run
`git cat-file blob "$source"` and verify the resulting bytes.

The [platform input receipt](localization/evidence/archival-platform-inputs-20261111.json.gz)
pins 1,952 materialized dialogue, settings, UI and related JSON inputs.
Restore v42 first and set `DRAGONS_SITE_LOCALES` to the canonical locale
catalog. The helper reads the recorded Git translation revision and runs
the normal paired input materializer for the selected platform and member:

```sh
python3.12 -B localization/restore_platform_locale_input.py \
  "$platform_input_receipt" "$recorded_path" --inventory "$shared_inventory" \
  --yarn-scope "$paired_yarn_scope" --output "$fresh_input"
```

The check reproduced all 433 distinct inputs byte for byte.

The [platform projection receipt](localization/evidence/archival-platform-input-projections-20261111.json.gz)
records 190 earlier per-platform input selections. Use the same v42 inputs
and locale catalog. The helper verifies each pinned Git translation, binds
the selected entries to the catalog and restores their historical order
and JSON formatting.

```sh
python3.12 -B localization/restore_platform_locale_projection.py \
  localization/evidence/archival-platform-input-projections-20261111.json.gz \
  "$recorded_path" --inventory "$shared_inventory" \
  --yarn-scope "$paired_yarn_scope" --output "$fresh_input"
```

The recovery check matched the original bytes and file modes for all
190 selections.

The [historical Yarn table receipt](localization/evidence/archival-historical-yarn-tables-20261111.json)
pins 35 dialogue readback tables for Ukrainian, German and Polish and
19 Ukrainian structure controls. Restore v42 and, for a dialogue table,
supply the stock Data directory for the platform named in the receipt.
Omit `--stock-data` for a structure control.

```sh
python3.12 -B localization/restore_historical_yarn_table.py \
  localization/evidence/archival-historical-yarn-tables-20261111.json \
  "$recorded_path" --inventory "$shared_inventory" \
  --yarn-scope "$paired_yarn_scope" --stock-data "$stock_data" \
  --output "$fresh_input"
```

The helper verifies stock assets, the Git translation snapshot and the
projected output. All 54 restored files matched the original bytes and
file modes. The check also confirmed that stock data from the wrong
platform is rejected before creating an output.

The [Git review diff receipt](localization/evidence/archival-review-diffs-20261111.json.gz)
records the before and after blobs for 105 historical staged review diffs.
Restore a recorded path with the same Git checkout:

```sh
python3.12 -B localization/restore_review_diff.py \
  "$diff_receipt" "$recorded_path" --output "$fresh_diff"
```

The helper uses temporary comparison trees and verifies the original
SHA-256. All input blobs are reachable from `main`.

The [static discovery report receipt](localization/evidence/archival-discovery-reports-20261111.json.gz)
pins 12 outputs from the owned stock builds. Restore the stock Data
directories and use the recorded tool and revision. For `managed`,
export the recorded tool directory from Git, build its project in
Release with the pinned .NET SDK and Mono.Cecil, then run the DLL with
the platform, stock Managed directory and recorded mode. For
`export_yarn_instructions.py`, supply the platform, stock Data directory
and `--output`. The other Python reports write JSON to stdout. For
`candidateStock`, copy the stock `.resS` and `.resource` files into a
separate directory and pass it as `--candidate-data`. Compare the
result to the recorded hash and restore each path's mode.

The [historical static probe receipt](localization/evidence/archival-static-probe-reports-20261111.json.gz)
records four original sources and 15 reports. For `initial` and `native`,
copy the recorded `Program.cs` and project file into a fresh directory and
build in Release with the pinned SDK. Run the DLL with the verified stock
Managed directory as its sole argument. For the two Python probes, set
`PYTHONPATH` to `localization` exported from `pythonImportRevision` and
use the pinned Python requirements. The `stream` script takes platform
and stock Data directory. The `settings` script takes the stock Data
directory and platform in that order. Capture stdout in each case.

The [historical static scanner receipt](localization/evidence/archival-historical-static-scanners-20261111.json.gz)
pins the archive of four earlier scanner binaries. Verify the downloaded
archive and restore the named scanner with `restore_archived_members.py`.
Supply the runtime configuration, dependency manifest and pinned
Mono.Cecil DLL from the Release build above. Run the scanner with
platform, stock Managed directory and the report's optional `argument`.
All eight reports from the downloaded scanners and seven reports built
from source matched their original fingerprints.

The [final usage evidence receipt](localization/evidence/archival-final-usage-20261111.json)
pins the private archive with the final Model usage manifest, supporting
evidence and readback. Verify its SHA-256 and the individual member hashes.

The [cited technical evidence receipt](localization/evidence/archival-cited-technical-evidence-20261111.json.gz)
links historical read-backs, editorial reports and runtime logs to the
tracked documents that record their SHA-256 values. Download
`Dragons-cited-technical-evidence.zip` from the maintainer draft and verify
its SHA-256. Create the needed destination parents and restore a selected
test directory with `restore_archived_members.py` and `--recovery-archives`.
The archive holds 786 distinct members for 1,015 files. The recovery check
matched every file to its recorded hash.

The [background input reflection receipt](localization/evidence/archival-background-input-reflection-20261111.json.gz)
pins the B8I2 Unity log, launcher log and observation result for the
reflection-failure control. Download its archive from the maintainer
draft, verify the archive hash and restore the three files using
`restore_archived_members.py` with `--recovery-archives`. The check
matched all three original hashes and modes.

The [component scout receipt](localization/evidence/archival-component-scouts-20261111.json.gz)
records five original scout scripts and 14 outputs. Export `localization`
from the receipt's `importRevision` into a temporary directory, then use
that directory for imports. Run the recorded scout from the canonical
checkout with Python 3.12, the pinned Unity dependencies and the
corresponding verified stock Data path.

```sh
PYTHONPATH="$revision_export/localization" python3.12 -B "$recorded_scout" \
  "$platform" "$stock_data" "$fresh_json" > "$fresh_stdout"
```

Verify the selected JSON or stdout hash and apply the recorded file mode.
All 14 outputs were rebuilt byte for byte.

The [component and transition report receipt](localization/evidence/archival-component-and-transition-reports-20261111.json)
pins the first two component exports, the transition IL reports and their
source files, and the initial v18 inventory.

For a component export, run `inventory_game_components.py` at the
recorded revision with the verified stock Data directory. Keep the role
field only on Yarn references and serialize the projected export:

```sh
python3.12 -B "$component_tool" "$platform" "$stock_data" > "$full_report"
python3.12 -B - "$full_report" > "$fresh_report" <<'PY'
import json
import sys

with open(sys.argv[1], encoding='utf-8') as source:
    report = json.load(source)
for component in report['objects']:
    for field in component['fields']:
        if field['role'] != 'preserve-exactly-yarn-node-reference':
            del field['role']
print(json.dumps(report, ensure_ascii=False, indent=2))
PY
```

For the IL reports, copy the recorded `Program.cs` to a fresh directory,
extract `projectBlob` there as `scan.csproj` with `git cat-file blob`, and
build it in Debug with the pinned SDK and Mono.Cecil. Pass the platform's
verified stock Managed directory to `dotnet scan.dll` and capture stdout.
Both reports matched their original hashes. The original Swift window
inspection source is also tracked with its byte-for-byte fingerprint.

For the initial v18 inventory, rebuild the verified v17 base with the
source inventory recipe above. Download the receipt's patch from the
maintainer draft, verify both hashes and decode with the same Zstandard
command used for the historical inventory deltas.

The [historical text copy receipt](localization/evidence/archival-text-copies-20261111.json.gz)
records 3,055 byte-identical copies of test reports, local tools and logs.
Restore a selected directory with `restore_archived_members.py`. For
`qaTools` rows, pass the installed screenshot review scripts directory
as `--qa-tools`. For `checkout` rows, the recorded local original is
the recovery source and must remain available until its replacement is
verified. The check restored every copy and matched its hash and mode.

The [screenshot review stream receipt](localization/evidence/archival-screenshot-review-streams-20261111.json)
pins 73 stdout logs from completed visual review attempts. Download the
compact review fields and the existing QA copy source ZIP from the
maintainer draft, then restore a selected log:

```sh
python3.12 -B localization/restore_screenshot_review_stdout.py \
  localization/evidence/archival-screenshot-review-streams-20261111.json \
  "$recorded_path" --metadata "$review_fields" --images "$qa_source_zip" \
  --output "$fresh_log"
```

The helper verifies both archive hashes and each embedded image hash.
It restores the original JSON event stream from the stored review
fields, usage and referenced WebP sources. The downloaded inputs
reproduced all 73 logs byte for byte. The original review state and
image archives remain the acceptance sources.

The [empty generated directory receipt](localization/evidence/archival-empty-generated-dirs-20261111.json.gz)
lists blank bundle signature and .NET reference directories left after
their files were archived or rebuilt. Recreate the recorded path with
`mkdir -p` and apply its listed mode if a historical fixture needs it.
All 537 paths were recreated and verified empty before cleanup.

The [empty bundle and build tree receipt](localization/evidence/archival-empty-bundle-and-build-trees-20261111.json.gz)
lists 5,914 directories left by retired macOS bundles and .NET builds.
Recreate needed paths from the top down with `mkdir -p` and apply their
recorded modes. The recovery check recreated the full recorded structure.

The [empty CrossOver system tree receipt](localization/evidence/archival-empty-crossover-system-trees-20261111.json.gz)
lists 7,956 empty directories from the system and Program Files trees
of 68 historical test bottles. Each relative directory existed in both
recorded source bottles. To restore a historical test tree, recreate the
recorded directories from the top down and apply their modes. The check
recreated the selected trees and verified their structure and modes.

The [retired test directory receipt](localization/evidence/archival-empty-retired-test-dirs-20261111.json.gz)
lists 1,625 empty directories and directory-only subtrees from earlier
builds and test runs. Recreate the needed paths from the top down with
`mkdir -p` and apply their recorded modes. The verification recreated
the recorded structure, checked each mode and matched the inherited
macOS provenance attribute on the build host. The selection excluded
runtime profiles, saves, owner paths and directories carrying ACLs or
other extended attributes.

The [test bundle plist receipt](localization/evidence/archival-test-bundle-plists-20261111.json.gz)
records 351 static bundle files and 159 generated test `Info.plist`
variants. Use `restore_archived_members.py --macos-stock` for the static
rows. For a projected row, verify the stock `Contents/Info.plist` hash,
load it with Python's `plistlib.loads`, and apply the recorded `updates`
and `remove` entries. Serialize with the recorded `format` and
`sortKeys` arguments to `plistlib.dumps`. Verify the output hash and
restore its mode. The check matched all 510 files.

The [.NET generated metadata receipt](localization/evidence/archival-dotnet-generated-metadata-20261111.json.gz)
lists NuGet restore graphs, generated imports and MSBuild intermediate
metadata for 419 historical projects. Recover the project descriptor from
its recorded Git blob or checkout path and use the corresponding project
sources and dependency pins. Build with .NET SDK 8.0.131 in the needed
configuration. Supply the pinned stock Managed directory as `GameManaged`
for projects that require it. Builds of the two named projects from an
export without intermediates regenerated the listed file types in Debug
and Release. Paths embedded in the new files reflect the current build
location. One historical project was excluded because its resolved and
declared dependencies differed.
The historical static probe receipt also lists 216 empty
`CopyComplete` markers. Fresh Debug and Release builds emitted that
marker. The check copied the generated empty file and verified each
recorded mode.

The [assembly metadata receipt](localization/evidence/archival-dotnet-assembly-metadata-20261111.json.gz)
pins four outputs from .NET SDK 8.0.131. Use a disposable build directory
and set `historical_path` to a checkout-relative key from the receipt.
The restored file is written to a new path.

```sh
mkdir -p "$build_dir"
git cat-file blob b99f7aa8cd35ecdeabd42b9a7116c0c62626ffaf > "$build_dir/scan.csproj"
printf '%s\n' 'System.Console.WriteLine("Assembly metadata");' > "$build_dir/Program.cs"
DOTNET_CLI_UI_LANGUAGE=ru dotnet build "$build_dir/scan.csproj" -c Debug \
  --nologo --disable-build-servers -p:NuGetAudit=false --ignore-failed-sources \
  -p:SourceRevisionId=b9768e3654135662bafbaf14ee283be0036e5a58
python3 -B localization/restore_dotnet_assembly_metadata.py \
  localization/evidence/archival-dotnet-assembly-metadata-20261111.json.gz \
  "$build_dir" "$historical_path" "$restored_file"
```

The restore tool verifies the SDK output, reapplies the historical
assembly attributes where needed, and checks the restored bytes before
writing. The check matched all 259 files and their recorded modes.

The [dependency metadata receipt](localization/evidence/archival-dotnet-dependency-metadata-20261111.json)
pins 45 earlier `.deps.json` files. Build the four template variants with
.NET SDK 8.0.131. Set `cecil` to the Mono.Cecil 0.11.6 DLL at
`lib/netstandard2.0/Mono.Cecil.dll` and verify its SHA-256
`831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf`.

```sh
for variant in package reference plain standard; do
  mkdir -p "$build_dir/$variant"
  cp localization/tools/historical-dotnet-dependencies/{scan.csproj,Program.cs} "$build_dir/$variant/"
  dotnet build "$build_dir/$variant/scan.csproj" -c Debug \
    --nologo --disable-build-servers --ignore-failed-sources \
    -p:NuGetAudit=false -p:Variant="$variant" -p:CecilPath="$cecil"
done
python3 -B localization/restore_dotnet_assembly_metadata.py \
  localization/evidence/archival-dotnet-dependency-metadata-20261111.json \
  "$build_dir" "$historical_path" "$restored_file"
```

The helper verifies the selected SDK template and substitutes the
recorded assembly name. All 45 outputs matched the original bytes and
modes. Restore the 17 source paths needed by the historical text copy
receipt before replaying its 281 dependent copies.

To recreate the historical counter snapshot, point the restore tool at the
original read-only Codex journal directory or an exact copy:

```sh
python3.12 -B localization/restore_usage_snapshot.py \
  "$usage_receipt" "$usage_archive" "$codex_journal_root" "$fresh_snapshot"
```

The downloaded manifest identifies the 56 exact journal prefixes used
for the snapshot. The check verified each prefix and reproduced the
original counter file. The private archive stores the prefix manifest
and the final evidence files.

The [CLI event stream receipt](localization/evidence/archival-cli-event-streams-20261111.json)
records 108 completed CLI streams. Download the index named in the
receipt from the maintainer draft and pass the owner's original Codex
journal directory or an exact copy. The GitHub asset contains references
and event structure. The command text, command outputs and model replies
come from the read-only local journals.

```sh
python3.12 -B localization/restore_cli_events.py \
  localization/evidence/archival-cli-event-streams-20261111.json \
  "$recorded_path" --archive "$cli_event_index" \
  --journal-root "$codex_journal_root" --output "$fresh_log"
```

The check used the downloaded index and verified all 28 journal prefixes.
It reproduced all 108 streams byte for byte and checked their file modes.
The [follow-up receipt](localization/evidence/archival-cli-event-stream-followup-20261111.json)
uses the same command for the Italian continuation that also recorded
file-change events. Its archive carries the file names and operation
types, and the journal supplies the text. The restored stream matched
the original bytes.

The [renderer acceptance index](localization/evidence/archival-renderer-acceptance-20261111.json)
pins the static shaping, staged line break, paired runtime and Parallels
reports. Download its archive from the `recovery-inputs-v0.2.1` maintainer
draft, verify the archive SHA-256, then verify each report against its entry
in the index. All four report hashes matched on download. The reports retain
the scope of the earlier tests.
