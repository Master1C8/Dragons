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
maps duplicate Unity assets to one remaining local copy per hash. Copy the
recorded source to the former path, restore its mode and verify its SHA-256.

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

The [historical German batch receipt](localization/evidence/archival-de-partial-20261111.json)
covers 18 intermediate assets whose rebuilds matched byte for byte. Download
the receipt's input archive from the `recovery-inputs-v0.2.1` maintainer draft,
check its archive hash and extract the dialogue JSON files. Match each JSON
and rebuilt asset to the SHA-256 in the receipt. Set `DRAGONS_SITE_LOCALES`
to the canonical locale catalog and use the stock Data paths described above:

```sh
python3.12 -B localization/dialogue_locale.py "$macos_stock_data/sharedassets1.assets" \
  --locale "$macos_batch_json" --output "$macos_batch_output"
python3.12 -B localization/windows_ui_locale.py "$windows_stock_data" sharedassets1.assets \
  --requested-locale de --dialogue-locale-file "$windows_batch_json" --output "$windows_batch_output"
```

The [historical installer receipt](localization/evidence/archival-obsolete-installers-20261111.json)
records the superseded build outputs. Its intermediate Windows installer
script can be recreated by extracting the compressed patch and applying it to
the Git blob named in the receipt. Compare the result to the recorded SHA-256.

The [Windows stock ZIP receipt](localization/evidence/archival-windows-stock-zip-20261111.json)
lists all 287 files in the old Parallels test fixture. To recreate the
fixture, ZIP those relative paths from the owned Windows stock game directory
and verify each member against the listed SHA-256. The recovery check rebuilt
the fixture and verified all members without running it.

The release card's visual delivery contains 150 published screenshot slots
across 30 locales. The upload readback matched all 150 hosted files.
