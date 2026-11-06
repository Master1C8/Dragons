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
