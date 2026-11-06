# Unity UI managed string extraction

The pinned `managed-strings` extractor now also scans all `ldstr` instructions,
including nested methods, in `Unity.TextMeshPro.dll` and `UnityEngine.UI.dll`
for both supported builds. Each occurrence retains its full method, ordinal,
IL offset, literal and neighboring calls. These are not paired across builds;
matching names or offsets alone do not establish equivalent use. The source and
Mono.Cecil hashes are checked before extraction. The current extractor source
SHA-256 is `b70c593f925b00edd474f01f5685a0e5955253f315aa162f9be9411730034f4f`;
the earlier three-assembly extraction and its historical tool fingerprint are
documented in `managed-code-discovery-20261107.md`.

| Build | Assembly | Occurrences | Distinct values | Local export SHA-256 |
| --- | --- | ---: | ---: | --- |
| macOS | Unity.TextMeshPro | 368 | 254 | `3f85b9d2458ba010fed921bcfdd46073e65ba1917c7c1b6455b63d4146802388` |
| Windows | Unity.TextMeshPro | 368 | 254 | `1c258b4d54b65a9268560fc77e89a8a8221132be94e7611dad5a7c6ef8da2e19` |
| macOS | UnityEngine.UI | 210 | 163 | `43506a8ce205f5c19048dcd96fed9d962fbac1b54f455cd33ae5ad2f66d77462` |
| Windows | UnityEngine.UI | 210 | 163 | `5a690f36f96654e4cced458207c636ed965b1d26443b06a83e20b634e930ae74` |

The exports reproduce byte-for-byte using the original local DLLs. Two focused
tests re-extract each source and check every count and identity; the negative
controls pass a Windows DLL to each macOS selector and verify the specific
source-hash rejection before output. The assembler tests separately verify
all 1,156 occurrences enter the provisional union as `needs-classification`,
including representative dropdown and input-field values on both platforms.

These are engine literals and can include diagnostics, object names, keys and
potential default UI text. No runtime reachability, displayed-text denominator
or completeness across other assemblies is inferred. The two libraries do not
cover generated, reflected or remote text. The previously observed setter and
dropdown limitations remain in `managed-text-sinks-20261107.md`.

Rebuild `tools/managed-strings/managed-strings.csproj` using fresh work-local
intermediate and output paths. Run its DLL with selectors `macos-tmp`,
`windows-tmp`, `macos-unity-ui` and `windows-unity-ui` against the matching
original DLLs, writing new exclusive output files in the inventory work folder.
Then run `python -m unittest discover -s localization -p test_managed_engine_strings.py -v`
and `python -m unittest discover -s localization -p test_assemble_source_inventory.py -v`.
The first test expects the pinned scanner build and original game paths.
