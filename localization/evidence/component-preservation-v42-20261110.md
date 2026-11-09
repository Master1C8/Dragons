# Exact game component preservation

`verify_preserved_components.py` loads the pinned v42 inventory,
classifies each source occurrence as exact, display, or a combination
of the two, and groups the exact serialized game fields by their
owning object. It verifies each complete MonoBehaviour's original
digest in the candidate Data directory. Whole-object comparison
preserves every nested string at its original field and array index.
It also detects missing objects, duplicate identities and conflicting
inventory digests.

| Build | Exact game component fields | Verified serialized objects |
| --- | ---: | ---: |
| macOS | 10,973 | 668 |
| Windows | 10,936 | 661 |

The macOS test used a signed output of the normal builder with all
1,823 Yarn, 58 UI, 37 settings and two managed inputs plus the
speaker locale. The input was a structural control with English
passthrough and synthetic speaker values. The Windows test used the
eight relevant files extracted and SHA-verified from the synthetic v42
ZIP, SHA-256
`bc9c97240c805f589137182733b8418a74c937b87c4805e1ab35e9b5aa52f976`.
Both candidate outputs passed. The exact Windows `level0#5215`
object passed before the negative test. Changing its serialized
`Cancel` intent to `Cancem` failed on that PathID. The eight related
regression tests passed in a separate run. A concurrent first run
ran out of disk space while creating a second full macOS test bundle.
Removing the completed synthetic app after signature and manifest
verification allowed the serial rerun to pass.

Local receipts remain in
`localization/work/preserved-components-20261110.ipqH8U/`.

| Receipt | SHA-256 |
| --- | --- |
| macOS component verification | `b3c8e361cc44936209ae533a09187852e2988766304db34543f0028a3a790dc4` |
| Windows component verification | `18703fda9ec66138e41017b05682a87a9295f2d7d6fe5edffcd3e44d3c68b924` |
| Signed macOS file manifest | `8d567a003d574b7834a99bae4452ba352c47d68a5667188654725f03b1b6ffd3` |

The counts for Yarn, UI, settings, managed and legacy UI in these
receipts describe the v42 inventory roles. Artifact verification for
those families remains with their respective adapters. This check
proves the known exact game component bytes and does not expand
source discovery, editorial or runtime coverage.
