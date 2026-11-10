# Dragons language installer

## Use

On macOS, extract `Dragons-macOS.zip` and open **Dragons — VN Revival**.
On Windows, extract the entire `Dragons-Windows.zip` and open
**Dragons Installer.exe** inside the extracted folder.

Choose one of the 30 bundled languages and select **Install**.
The installer finds the Steam installation when possible. If discovery
fails, use **Choose Game…** to select the existing game folder. Close the
game before installing or changing a language.

After a successful install, the installer requests launch through Steam
for a registered installation. A manually selected standalone copy
launches directly. The game reads the installed locale files on future
launches. Run the installer again to switch languages. A Steam update or
file verification can restore stock files. Reapply the language only
when the installer accepts the source build.

## Supported inputs and verification

The pinned source builds are macOS `9/12/2026_a93aa21a` and Windows
`9/9/2026_ee944596`. The game is identified through Steam App ID
`4739660` where applicable and through exact content fingerprints on
both platforms. macOS requires 14 or later and the installer executable
is universal arm64/x86_64. The Windows installer is x86-64.

The SwiftUI and Win32 shells and the receipt, ownership and recovery
code were adapted from **The Murder of Sonic the Hedgehog Localization**
at commit `d9213cfbc4b650f73be80e46c54a340f26fd941a`. The game adapter
adds pinned Dragons paths and locale overlays. macOS prepares and
ad-hoc signs a copy, verifies it, then exchanges the app bundles on the
same volume. The Windows adapter uses the base's per-file replacement
and rollback journal, with an installation lock and same-volume staging.
Both paths reject unknown changes to files the patch owns. Original
asset backups stay local and outside the player's save profile.

The installer carries binary deltas and new companion DLLs. It does not
carry a full copy of the game or need a player-side Python or .NET SDK.
The included decoder is [xdelta3 3.2.2](https://github.com/jmacd/xdelta/releases/tag/v3.2.2).
The release archive digests used for arm64 macOS, x86-64 macOS and
x86-64 Windows are respectively
`27dcf763beb075ed28061ef136613f4bc6ea3999cb424f23a7d59f18ca2d7c8b`,
`e217f4d0f92357ee890f9d8b5571f7eb836a86ff87e8834bed0b9d9b38630f86` and
`d48f7651d86b78fdca397057b46601f89131f37219675df736db70af44ec3379`.
Combine the two macOS executables with `lipo` and ad-hoc sign the result
before preparing the payload. The decoder and font license texts are
included with the payload.

## Build and test

Use `Scripts/prepare-payload.py --help` to generate macOS and Windows
resource directories with `--inventory App/LocalePackages.json`. The
inventory pins both local packages and the translation for each locale.
Both installers use the same locale list, and the Windows picker is
generated from its packaged configuration.
Pass the original Data directory for each platform, the host encoder,
the target decoder and its license. The generator reconstructs each
delta and checks its exact output hash before adding it to the package.
For macOS, build the Steam App ID path patcher with the .NET 8 SDK:

```sh
dotnet build Scripts/SteamPathFix/SteamPathFix.csproj -c Release -o "$BUILD_SCRATCH/steam-path-fix"
```

Pass `--steam-path-fix "$BUILD_SCRATCH/steam-path-fix/SteamPathFix.dll"`
when preparing the macOS payload. The patch keeps the App ID file
inside the signed app when the game starts.

Run `Scripts/build.sh MAC_PAYLOAD WINDOWS_PAYLOAD GAME_ICON BUILD_SCRATCH DIST`
with absolute paths. Supply the original game's `PlayerIcon.icns`.
The build uses SwiftPM, macOS signing tools, MinGW-w64 and ImageMagick.
Generated SwiftPM resources are ignored by Git. When switching payload
inputs, clear only those generated resource files before building.

The test drivers under `Tests/` apply the installers to disposable
game directories and verify repeated installation, locale switching and
the actual installed asset hashes. The macOS driver compiles alongside
`InstallerCore.swift` and `PackageConfig.swift`, and accepts a disposable
game bundle and the macOS payload directory. The Windows driver accepts
a directory containing a ZIP of the pinned test game files and an
unpacked Windows installer directory. The fixture executable must be
the text file `test only`, so this check cannot start the game.
