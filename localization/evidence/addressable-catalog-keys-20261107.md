# Binary Addressables catalog keys

The previous local Addressables inventory fingerprinted `catalog.bin` but did
not parse it. `tools/addressable-catalog-keys` now lists the keys by invoking
the pinned game's `Unity.Addressables.dll` `ContentCatalogData.LoadFromFile`
with internal-ID resolving disabled, followed by the resulting locator's
`Keys` property. Unity documents `ContentCatalogData` in the
[Addressables 2.9 API](https://docs.unity.cn/Packages/com.unity.addressables%402.9/api/UnityEngine.AddressableAssets.ResourceLocators.html).
The local `aa/settings.json` records Addressables version 2.9.1. This is a
read-only diagnostic, not a Unity game launch.

Unity's native `UnsafeUtility.MemCpy` cannot execute in the desktop .NET
harness. The tool loads a transient in-memory copy of the pinned
`Unity.ResourceManager.dll` in which its 13 direct calls to that method use a
small managed `Buffer.MemoryCopy` adapter. It does not write the diagnostic DLL
or change the original. It validates the complete root managed-DLL name/hash
manifest, Mono.Cecil binary and the original catalog hash before the call, and
rechecks the catalog afterwards. The substitution is an experiment and is not
proof of equivalence to Unity's native runtime. Dependent assemblies are read
from the already validated original bytes.

Both catalogs returned 24 unique string keys: three bundle-named keys, nine
`.compute` paths, `English (en)`, `Locale`, and ten 32-character hexadecimal
keys. The two outputs agree except for one platform-specific shader-bundle
key. Local reports:

- `work/catalog-keys-macos-20261107.json`: SHA-256
  `4c45edb46cd93768980e8ce076ee553b3142b88df3007ca34216fb106ca9c29a`.
- `work/catalog-keys-windows-20261107.json`: SHA-256
  `8f45106fc4ed8c05a643d972a715d2ddefc9dcff8fc233213da46f94905358e8`.

An exploratory attempt to enumerate `AllLocations` failed in the desktop
harness when Unity's native exception logger was invoked. The underlying
location-decoding exception was therefore not recovered. This result does not
establish complete locations, resource types, internal paths, dependencies,
dynamic or remote catalog contents, runtime behavior, or absence of other
text. The existing separately inspected bundle object inventory remains the
evidence for their contents; key names alone do not establish the mappings.

Two focused tests reproduced both reports byte-for-byte, checked known keys
and counts, and rejected a wrong-build managed inventory and an altered catalog
at their respective fingerprint guards. Tool source SHA-256
`d84c2e964db1e0b8a8a11fa1850fed40d62a3aa4ffc7e9dd948d02a10caac576`;
test SHA-256 `c1ad05ad96f4a78bfe53e14a1d75750087373da2fc32d9c76f5bc4a5ad2665a0`.

```sh
dotnet build localization/tools/addressable-catalog-keys/addressable-catalog-keys.csproj -p:BaseIntermediateOutputPath=ABSOLUTE_NEW_OBJ/ -o ABSOLUTE_NEW_BIN/
dotnet ABSOLUTE_NEW_BIN/addressable-catalog-keys.dll macos ORIGINAL_MAC_DATA
dotnet ABSOLUTE_NEW_BIN/addressable-catalog-keys.dll windows ORIGINAL_WINDOWS_DATA
python -m unittest discover -s localization -p test_addressable_catalog_keys.py -v
```

The focused test expects its built tool at `work/addressable-catalog-keys-bin`
and the original game paths. The full source handoff remains incomplete.
