# Managed assemblies preserved by localization builds

The macOS app builder now pins the original `Managed` inventory before
copying and compares the signed staging app with that snapshot before the
exclusive rename. The verifier rejects extra or missing files, symlinks
and changed library bytes. It uses the same sorted `filename|SHA-256`
manifest representation as the pinned managed-code discovery tools.

| Build | DLLs | Original managed manifest SHA-256 |
| --- | ---: | --- |
| macOS | 170 | `b3186bc39207255e937f5856be09906dc1a428d83a964d5f368f30861e32603c` |
| Windows | 172 | `9a14fcb1198ca8308ad90a38a1988367074c1f2ec8b6f0a8d97ef3d3c074fc56` |

A fresh signed macOS app with synthetic dialogue and all five Yarn repairs
passed the integrated check and a separate comparison at its final path.
The repair-only Windows copy also passed a separate comparison with its
pinned original. The CLI rejected the older instrumented macOS test copy
at the exact changed `Assembly-CSharp.dll` and rejected the Windows source
under the macOS selector. The real-builder regression substitutes a DLL in
the staging app at the mocked signing boundary and proves rejection,
staging cleanup, and preservation of the source. All 176 tests passed.

Local receipts are in
`localization/work/managed-integrity-20261109.eAbhRe/`. The standalone
verifier takes the two distinct `Managed` paths:

```sh
python3 localization/verify_managed_assemblies.py macos ORIGINAL_MANAGED BUILT_MANAGED
python3 localization/verify_managed_assemblies.py windows ORIGINAL_MANAGED BUILT_MANAGED
```

This establishes preservation of all managed strings in these asset-only
builds, including literals whose roles are still unresolved. Any future
authorized managed patch will need a verified replacement contract for the
specific assemblies. The remaining asset families and runtime acceptance
retain their own checks.
