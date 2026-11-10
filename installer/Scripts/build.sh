#!/bin/bash
set -euo pipefail
if [ "$#" != 5 ]; then
  echo "Usage: build.sh MAC_PAYLOAD WINDOWS_PAYLOAD GAME_ICON BUILD_SCRATCH DIST" >&2
  exit 2
fi
project=$(cd "$(dirname "$0")/.." && pwd)
mac_payload=$1
win_payload=$2
icon=$3
work=$4
dist=$5
resources="$project/Sources/DragonsInstaller/Resources"
mkdir -p "$work" "$dist" "$resources"
app="$dist/Dragons — VN Revival.app"
win="$dist/Dragons Windows"
archive="$dist/Dragons-Windows.zip"
mac_archive="$dist/Dragons-macOS.zip"
for target in "$app" "$win" "$archive" "$mac_archive"; do
  [ ! -e "$target" ] || { echo "Already exists: $target" >&2; exit 1; }
done
mkdir -p "$work/windows-build"
python3 - "$mac_payload/PackageConfig.json" "$win_payload/PackageConfig.json" \
  "$work/windows-build/InstallerLanguages.h" <<'PYTHON'
import json
from pathlib import Path
import re
import sys

def roster(path):
    config = json.loads(Path(path).read_bytes())
    if not config["payloadReady"] or not all(row["ready"] for row in config["languages"]):
        raise SystemExit("Installer payload is incomplete")
    return [(row["siteLocale"], row["runtimeCode"], row["nativeLanguageName"]) for row in config["languages"]]

mac, win = map(roster, sys.argv[1:3])
if not mac or mac != win:
    raise SystemExit("Installer language lists differ")
for _, runtime, name in win:
    if not re.fullmatch(r"[a-zA-Z0-9-]{1,15}", runtime) or not name.isprintable():
        raise SystemExit(f"Invalid installer language entry: {runtime}")
header = Path(sys.argv[3])
with header.open("w", encoding="utf-8") as output:
    for variable, index in (("languages", 2), ("runtimeCodes", 1)):
        values = ", ".join("L" + json.dumps(row[index], ensure_ascii=False) for row in win)
        output.write(f"static const wchar_t *{variable}[] = {{{values}}};\n")
PYTHON
if [ ! -e "$resources/PackageConfig.json" ] && [ ! -e "$resources/LocalizationPayload" ]; then
  cp "$mac_payload/PackageConfig.json" "$resources/"
  cp -R "$mac_payload/LocalizationPayload" "$resources/"
fi
cmp "$mac_payload/PackageConfig.json" "$resources/PackageConfig.json"
diff -qr "$mac_payload/LocalizationPayload" "$resources/LocalizationPayload"

for arch in arm64 x86_64; do
  swift build --package-path "$project" -c release --scratch-path "$work/swift-$arch" \
    --triple "$arch-apple-macosx14.0"
done
arm=$(swift build --package-path "$project" -c release --scratch-path "$work/swift-arm64" \
  --triple arm64-apple-macosx14.0 --show-bin-path)
x86=$(swift build --package-path "$project" -c release --scratch-path "$work/swift-x86_64" \
  --triple x86_64-apple-macosx14.0 --show-bin-path)
mkdir -p "$app/Contents/MacOS" "$app/Contents/Resources"
lipo -create "$arm/DragonsInstaller" "$x86/DragonsInstaller" -output "$app/Contents/MacOS/DragonsInstaller"
cp -R "$arm/DragonsInstaller_DragonsInstaller.bundle" "$app/Contents/Resources/"
cp "$project/App/Info.plist" "$app/Contents/Info.plist"
cp "$icon" "$app/Contents/Resources/App.icns"
codesign --force --deep --sign - "$app"
codesign --verify --deep --strict "$app"
cmp "$mac_payload/LocalizationPayload/Tools/xdelta3" \
  "$app/Contents/Resources/DragonsInstaller_DragonsInstaller.bundle/Contents/Resources/LocalizationPayload/Tools/xdelta3"

mkdir -p "$win/Resources" "$work/windows-build"
cp "$project/Windows/install.ps1" "$win/"
cp "$win_payload/PackageConfig.json" "$win/Resources/"
cp -R "$win_payload/LocalizationPayload" "$win/Resources/"
cp "$project/Windows/"{Installer.rc,Installer.manifest} "$work/windows-build/"
/usr/bin/sips -s format png "$icon" --out "$work/windows-build/Game.png" >/dev/null
magick "$work/windows-build/Game.png" -define icon:auto-resize=256,128,64,48,32,16 "$work/windows-build/Game.ico"
(
  cd "$work/windows-build"
  x86_64-w64-mingw32-windres Installer.rc -O coff -o InstallerResources.o
)
x86_64-w64-mingw32-gcc -std=c11 -O2 -Wall -Wextra -Werror -municode -mwindows \
  -I "$work/windows-build" "$project/Windows/DragonsInstaller.c" "$work/windows-build/InstallerResources.o" \
  -o "$win/Dragons Installer.exe" -lcomctl32 -lshell32 -lole32
(cd "$dist" && zip -qr "$archive" 'Dragons Windows')
ditto -c -k --sequesterRsrc --keepParent "$app" "$mac_archive"
du -sh "$app" "$archive" "$mac_archive"
python3 - "$app" "$archive" <<'PY'
from pathlib import Path
import sys
app, archive = map(Path, sys.argv[1:])
size = sum(p.stat().st_size for p in app.rglob('*') if p.is_file())
if max(size, archive.stat().st_size) > 100_000_000:
    raise SystemExit('Installer exceeds 100 MB')
print(f'macOS {size} bytes, Windows {archive.stat().st_size} bytes')
PY
