# CJK package integration

Both complete package builders now accept the pinned Noto Sans CJK
2.004 regional OTF and upstream OFL notice for `zh`, `zh-TW`, `ja`
and `ko`. The asset adapter appends the additional face, material,
empty atlas seed and TMP fallback after the stock Liberation Sans
chain. Atlas dimensions and material dimensions are both 1024.
The adapter serializes and checks every old and new object before
replacing the privately staged asset.

Eight diagnostic packages used the normal complete build commands.
They used the shared 1,947-ID format with English passthrough and
two target-script sample values in each locale. The packages are
technical controls. Their text has no editorial or release status.

| Locale | macOS | Windows |
| --- | --- | --- |
| `zh` | Signed app and resource read-back passed | Archive CRC and member read-back passed |
| `zh-TW` | Signed app and resource read-back passed | Archive CRC and member read-back passed |
| `ja` | Signed app, resource read-back and isolated slot control passed | Archive, member read-back and isolated CrossOver slot control passed |
| `ko` | Signed app and resource read-back passed | Archive CRC and member read-back passed |

Read-back verified the region-specific font bytes and license in
every package, the package manifest digest of the patched asset, a
localized Yarn sample, and the exact bytes of existing font,
material and texture objects in the changed shared asset.
The normal component-preservation gate also passed during all builds.
The Russian regression reproduced the previous Windows ZIP and
macOS resource bytes. The suite ran 206 tests with 201 passes and
five skips.

The Japanese runtime test cloned the signed output and applied the
Windows archive to a clone checked against the 287-file stock
inventory. The test copies used isolated profiles and two verified
observer hooks. The game loaded the additional Japanese face, retained
Liberation Sans for Latin and Cyrillic, and admitted all 1,536
stress characters in 16 pages with matching shader and atlas width.
All 15 macOS and 38 Windows focus/window samples were `0 0`. Both
test players exited and original profiles matched their initial hashes.

Remaining checks include target-language corpus coverage, rendered
text and layout in gameplay, native Windows, editorial review and the
release-specific installation workflow. The Japanese slot probe
measures glyph identities and atlas insertion, separate from pixel
inspection and gameplay progression.

Local build commands, assets and receipts are under
`localization/work/cjk-package-20261110.dgT1p7/`.

| Artifact | SHA-256 |
| --- | --- |
| Eight package read-back results | `1d95c6e06ddf57d8ecc26d06b917715c9049532a7d2fc1974cfd3dc4fdd82d77` |
| Japanese macOS Unity log | `2b279620ad9f1b9736e9f92512c4d6e79c9b269a2df459cbb95e6ff9c4cb7d92` |
| Japanese Windows Unity log | `e25164a0ff1d1982697329e8114cbc1a0c53277b03e347e012f9f949e6d75aac` |
