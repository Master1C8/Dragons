#!/bin/bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: bash $0 DIRECTORY_WITH_RELEASE_ZIPS NEW_OUTPUT_DIRECTORY" >&2
  exit 2
fi

archives=$(cd "$1" && pwd)
output=$2
(
  cd "$archives"
  shasum -a 256 -c <<'SHA256'
acda5664d2e283a84a2e51ecad4ceaa5c25bc7866c83c15a075875a9fdb758bb  Dragons-macOS.zip
35070df451dc3f239e1d491bfb94fb2de8fc52e15916a42c70c2e1cf29c29f0a  Dragons-Windows.zip
SHA256
)

mkdir "$output"
ditto -x -k "$archives/Dragons-macOS.zip" "$output/macos"
ditto -x -k "$archives/Dragons-Windows.zip" "$output/windows"
mac_app="$output/macos/Dragons — VN Revival.app"
mac_resources="$mac_app/Contents/Resources"
codesign --verify --deep --strict "$mac_app"
test -x "$mac_resources/DragonsInstaller_DragonsInstaller.bundle/Contents/Resources/LocalizationPayload/Tools/xdelta3"
test -f "$output/windows/Dragons Windows/Resources/LocalizationPayload/Tools/xdelta3.exe"
test -f "$mac_resources/App.icns"
