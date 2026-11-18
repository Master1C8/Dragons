#!/bin/bash
set -euo pipefail

if [ "$#" -ne 2 ] && [ "$#" -ne 3 ]; then
  echo "Usage: bash $0 DIRECTORY_WITH_RELEASE_ZIPS NEW_OUTPUT_DIRECTORY [0.2.1|0.2.3]" >&2
  exit 2
fi

archives=$(cd "$1" && pwd)
output=$2
version=${3:-0.2.1}
(
  cd "$archives"
  case "$version" in
    0.2.1) shasum -a 256 -c <<'SHA256'
acda5664d2e283a84a2e51ecad4ceaa5c25bc7866c83c15a075875a9fdb758bb  Dragons-macOS.zip
35070df451dc3f239e1d491bfb94fb2de8fc52e15916a42c70c2e1cf29c29f0a  Dragons-Windows.zip
SHA256
    ;;
    0.2.3) shasum -a 256 -c <<'SHA256'
2ca6af9c0e8555cc332ace39423b4bdbb5e15710ef25efe24a1a8c9a42548814  Dragons-macOS.zip
7e83d5e0e9d35ffd71fabbdafee5613c3f7f201bac8563a3bdf94472d7905ed6  Dragons-Windows.zip
SHA256
    ;;
    *) printf 'Unsupported recovery version: %s\n' "$version" >&2; exit 1 ;;
  esac
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
