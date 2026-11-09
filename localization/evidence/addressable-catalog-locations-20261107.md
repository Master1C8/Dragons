# Partial binary Addressables locations

The prior key-only diagnostic failed to enumerate locations because Unity's
native exception logger masked the original error. The separate read-only
`tools/addressable-catalog-locations` experiment retains the same pinned source,
catalog and in-memory managed `MemCpy` substitution, and redirects ten direct
`Debug.LogException(Exception)` call sites in that transient module to a
captured diagnostic stream. It requires exactly three captured
`SecurityException` instances mentioning native `Hash128ToStringImpl`; any
other count or exception rejects the report. The original DLLs and catalogs
are not modified. Neither substitution proves equivalence to the Unity runtime.

Both builds produced 13 partial location records: three bundle locations, one
`UnityEngine.Localization.Locale` and nine `UnityEngine.ComputeShader`
locations. The English locale's internal asset path and its two bundle
dependencies match the independently extracted locale bundle and monoscripts
bundle. Each compute shader's internal path matches a container entry in its
single shader-bundle dependency. The tests reconcile the complete returned sets
with both previously fingerprinted bundle reports. The three bundle-option
`Data` values could not be decoded because native `Hash128` string conversion
failed; this is not a complete location, type, metadata or dependency audit.
Do not infer that other dynamic or remote catalogs cannot exist or that runtime
loading succeeds from this diagnostic.

Local, reproducible reports:

- `work/catalog-locations-macos-20261107.json`: SHA-256
  `3eacf6693c145f181eb04472f0ebc4d0f725c455d82524efef8d221ba517c0c0`.
- `work/catalog-locations-windows-20261107.json`: SHA-256
  `e927980a9fdb76723787f39d41db0d25f73ad4fb91e78424265cf446312c0c67`.

Two focused tests passed: both reports were reproduced byte-for-byte and
reconciled to the earlier bundle inventories, and a wrong-build managed tree
and altered catalog were rejected at the respective fingerprint guards. This
is static diagnostic evidence; no game was launched or localized text created.

Tool SHA-256 `661e6f5f5024cc00b95e1f3086994bed1e571e1bfee381479fd4ed361bb36a45`;
test SHA-256 `59245289f8c56ddcfc75e02a3b00d068c14296f2ba1533ec269f9332c7c70e5c`.

```sh
dotnet build localization/tools/addressable-catalog-locations/addressable-catalog-locations.csproj -p:BaseIntermediateOutputPath=ABSOLUTE_NEW_OBJ/ -o ABSOLUTE_NEW_BIN/
dotnet ABSOLUTE_NEW_BIN/addressable-catalog-locations.dll macos ORIGINAL_MAC_DATA
dotnet ABSOLUTE_NEW_BIN/addressable-catalog-locations.dll windows ORIGINAL_WINDOWS_DATA
python -m unittest discover -s localization -p test_addressable_catalog_locations.py -v
```

The tests expect the tool in `work/addressable-catalog-locations-bin` and both
locally pinned game paths. The full localization source handoff remains open.

## Bundle options and key coverage, 2026-11-09

The optional `--bundle-options` mode works around the remaining native
conversion at one verified call in the in-memory Addressables decoder.
It checks that the pinned `Hash128` layout consists of two sequential
`UInt64` fields, then records the two raw words. No native hash string is
used to load or identify a bundle. The old mode still reproduces the
historical partial reports byte-for-byte.

On each build all 24 keys resolved. Their union exactly matches the 13
enumerated locations, and the three bundle option objects decoded with
zero diagnostic exceptions. The report preserves the key-to-location
relationships and the original IDs, providers, and dependencies. Tests
independently compare the key list to the earlier key report, compare
locations with the earlier location report, compare each bundle size to
its local file, and verify that the raw hash bytes match the corresponding
bundle key suffix. All three options disable Unity Web Request for local
bundles. The only catalog listed at startup in both pinned settings files
is the local `catalog.bin`, with no dependencies or extra initialization
entries.

The local catalog and its three previously decoded containers therefore
account for the locale configuration and nine compute shaders, without a
string-table location. A scoped direct-reference scan of all 170 macOS
and 172 Windows managed assemblies found one game-code Addressables call,
`SceneLoader`'s `LoadSceneAsync`, and three Yarn Unity calls in its
localized-object and Unity string database code. No direct call to the
public `LoadContentCatalogAsync` appeared in the scan. This is a static scan and
leaves runtime scene lookup, provider activation, indirect external catalogs,
and sources outside this inventory unverified.

Local outputs are in `localization/work/addressables-bundle-options-20261109.MY028D/`.

| Evidence | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Catalog options and key coverage | `9163d2e8c3c46ec05cae999ecf4c1b80ddb73962c02d0ea036fac0ab93246db1` | `6ec0991b541d39a43879887ca31cab3492ecc4823585d7325d8ca02a4efb1aee` |
| Managed API reference scan | `861099ae6adb9bd979c8614eee4c595ee3e211a885273c686b125a1e6fc92961` | `2bdf3e95442a5d3ac0689c33c145c848a46e30571709bc32ca7e2aff0231f46c` |

```sh
dotnet ABSOLUTE_NEW_BIN/addressable-catalog-locations.dll macos ORIGINAL_MAC_DATA --bundle-options
dotnet ABSOLUTE_NEW_BIN/addressable-catalog-locations.dll windows ORIGINAL_WINDOWS_DATA --bundle-options
DRAGONS_CATALOG_OPTIONS_TOOL=ABSOLUTE_NEW_BIN/addressable-catalog-locations.dll \
  python -m unittest discover -s localization -p 'test_addressable_catalog_locations.py' -v
```
