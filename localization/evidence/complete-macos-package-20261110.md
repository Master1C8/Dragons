# Complete package input validation on macOS

`build_macos_package.py` snapshots the locale directory and runs the
same source-pinned Yarn, speaker, serialized UI, settings and managed
text validation as the Windows replacement builder. A complete
package uses the snapshot that was validated. The macOS builder
includes the five verified Yarn transition repairs, the audited
speaker contrast change, both managed phrase replacements and the
speaker companion. It writes an input receipt into the staged app
before signing and retains the existing launcher marker schema.
The partial-input app builder remains available for isolated probes.

The real macOS control used an English passthrough for most strings
with a few synthetic Cyrillic values. It accepted all 1,823 ordinary
Yarn entries, the separate Alexander display entry, two speaker
labels, 58 UI entries, 37 settings entries and both managed phrases.
Strict signature verification passed on the output path. The
signed receipt matched all 12 input files by SHA-256. The protected
component check verified 10,973 exact source fields in the output.

Three controls each removed one entry from that complete input
set. The command rejected each at its intended coverage check
and produced no app:

| Removed ID | Observed boundary |
| --- | --- |
| `line:fa97376e` | Missing Yarn dialogue ID |
| `sharedassets0.assets#608:label` | Missing settings ID |
| `level0#5208` | Missing serialized UI ID |

The package regression also verifies that the macOS builder is not
called on a validation failure and uses the private validated
snapshot even if the caller's source inputs change. The Windows
control was rebuilt from the original synthetic inputs. The
complete ZIP matched the previous v42 archive byte-for-byte.
All 201 localization tests passed with the optional paired tools
enabled.

Local inputs, reproduction commands, logs and the signed app's
file hashes are under
`localization/work/macos-complete-package-20261110.FWKyAQ/`.
The synthetic app was removed after strict verification and
recording its hashes. The signed receipt was retained separately.
No game was installed or launched. The synthetic text is a
structural control, and final Russian editorial, runtime and
visual acceptance remain open.

| Evidence | SHA-256 |
| --- | --- |
| Signed macOS input receipt | `e11dbeb67b28b0a2a5a8d1af4ff9efaa979322934122e3e8cd30270eb22c9f4e` |
| macOS protected component check | `b3c8e361cc44936209ae533a09187852e2988766304db34543f0028a3a790dc4` |
| Windows v42 ZIP, previous and rebuilt | `bc9c97240c805f589137182733b8418a74c937b87c4805e1ab35e9b5aa52f976` |
