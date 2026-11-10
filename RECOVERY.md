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

The full translation rebuild gate still covers per-locale package inputs,
including the CJK fonts and shaped-text plans. Retain the working inputs until
those rebuilds are verified. `textures-with-text` is the owner's working
directory and stays separate from generated output cleanup.

[The duplicate-package receipt](localization/evidence/archival-duplicate-packages-20261111.json)
maps removed work outputs to their retained, byte-identical copies.

The release card's visual delivery contains 150 published screenshot slots
across 30 locales. The upload readback matched all 150 hosted files.
