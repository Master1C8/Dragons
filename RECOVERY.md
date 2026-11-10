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
game distribution. The untracked v42 inventory and Yarn scope can be
regenerated as described in [the v42 receipt](localization/evidence/yarn-fragment-markers-20261110.md).
Keep these and the per-locale working package inputs until the full translation
rebuild has been verified from recovered inputs. `textures-with-text` is the
owner's working directory and stays separate from generated output cleanup.

The release card's visual delivery contains 150 published screenshot slots
across 30 locales. The upload readback matched all 150 hosted files.
