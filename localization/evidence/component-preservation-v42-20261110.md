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

## Complete-package guard

The complete macOS builder now checks the signed staging app
before exclusive publication. The Windows builder checks the
staged replacement assets before compression and exclusive
publication. Both report the same preservation receipt as the
standalone verifier. The partial macOS test builder retains its
existing behavior. The receipt stored in the macOS app and the
Windows archive manifest use their existing formats.

Both structural controls passed with the existing synthetic
inputs. macOS verified 668 objects and 10,973 fields and retained
the prior signed input receipt. Windows verified 661 objects and
10,936 fields. The complete Windows ZIP still has the original
v42 SHA-256 above.

The negative controls changed exactly one serialized intent
from `Cancel` to `Cancem`. On macOS the injection ran after
the original staging builder signed the app. On Windows it
ran after the level adapter's read-back, and the control also
updated the staged file digest so the archive hash check would
not be the rejecting boundary. Each builder rejected the
expected object, `level0#5237` on macOS and `level0#5215`
on Windows. Neither published an output. The Windows compressor
was never called, and both staging directories were cleaned.

The local controls and reports are under
`localization/work/package-component-guard-20261110.hIfXa6/`.
The stopped macOS synthetic app was removed after strict
signature verification and retaining its file hashes. All 202
localization tests passed with the optional paired tools enabled.

| Receipt | SHA-256 |
| --- | --- |
| Paired publication controls | `ad2b6dfbbe53d7d5a4b300b1cc3d46207dfb7df964ead6fadc7712b7169ef254` |
| Windows package report | `d2f23c8ccfa18201f33f9961d0a007d402939cb78b3b5541af7e2898ebe40f1f` |
| Test suite log | `728cad9d796661d65ccf99aa259bb2f4c2a3115b280ad9185812ffcf51a0312b` |
