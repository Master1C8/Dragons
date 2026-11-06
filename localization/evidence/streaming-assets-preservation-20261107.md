# Local StreamingAssets preservation

Each pinned build has 31 regular files in local `StreamingAssets`: seven
previously inventoried Addressables files and 24 additional `.bytes` files in
`APVStreamingAssets`. The 24 APV relative paths, file sizes and SHA-256 hashes
are identical between these two builds; their combined payload is 54,931,216
bytes, and the sorted path/size/hash manifest SHA-256 is
`7e82d379c31e6bdfa8d1b276eb2d46be64eb551be7ca4c2a481443c70cdaf56a`.
Individual records for each platform are in `streaming-assets-files-20261107.json`
SHA-256 `3e47e1ce339802dc091708de2c492b1fe298b5ca9bee0298c1904e327328df6f`.
This is a file inventory, not a semantic decode of APV data or the Addressables
binary catalog. Do not infer that these files contain no text or are never read.

`verify_streaming_assets.py` first checks the supported original game build,
source Addressables identities and hashes, and the pinned complete APV
path/size/hash manifest. It compares every candidate local StreamingAssets path,
size and digest to the source, rejects symlink or non-regular entries, and
requires separate candidate and original data paths. The check passed on one
existing isolated macOS copy (31 files, 54,984,939 bytes) and one separate
Windows test copy (31 files, 54,967,722 bytes). These are test copies, not
player packages or proof of installation, and no game was launched for this
check. The verifier is not yet wired into the player build.

Focused tests include a real-source positive check for each build and mutated
in-memory source-manifest records rejected separately at APV and Addressables
guards. Temporary file fixtures verify a matching positive, changed file,
added path and symlink rejection. The latter comparison tests do not simulate
concurrent mutation or a complete installed game. Source and candidate files
are not modified. This check does not cover non-streamed files, semantic roles,
remote resources, runtime loading, translation, or restoration.

```sh
python localization/verify_streaming_assets.py macos ORIGINAL_DATA SEPARATE_COPY_DATA
python localization/verify_streaming_assets.py windows ORIGINAL_DATA SEPARATE_COPY_DATA
python -m unittest discover -s localization -p 'test_verify_streaming_assets.py'
```
