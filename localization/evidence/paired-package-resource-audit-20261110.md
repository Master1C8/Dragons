# Paired package resource audit

2026-11-10. Checked the pinned English macOS `9/12/2026_a93aa21a` and
Windows `9/9/2026_ee944596` Data directories against the existing complete
Russian packages. The same v42 inventory and packaging paths serve the six
Terra CLI locales. This audit exercises file preservation on the actual
packages as a control for those shared paths.

| Platform | Stock Data files | Byte-identical files | Changed files | Added files |
| --- | ---: | ---: | ---: | ---: |
| macOS app | 244 | 233 | 11 | 1 |
| Windows ZIP applied to an isolated stock copy | 259 | 248 | 11 | 1 |

The changed files are `level0` through `level6`, `sharedassets0.assets`,
`sharedassets1.assets`, `Managed/Assembly-CSharp.dll` and
`Managed/YarnSpinner.Unity.dll`. The addition is the speaker companion DLL.
The full path and SHA-256 comparison found zero removed files. All 12
Windows archive members matched their payload digests, and their source
digests matched the pinned files or expected absence. The Windows source
tree still matched its pre-check hashes. The earlier QA directory is now
incomplete for this comparison, so this check applied the ZIP to a new
verified stock copy and preserved the earlier directory.

On both platforms the existing verifiers also checked all 31 StreamingAssets
files and all four TextAssets within the 17 pinned serialized assets. Both
TextMeshPro line-breaking references and the line-breaking mode match stock.
Both Unity built-in resource files stayed byte-identical to their own stock
builds. Their one MonoBehaviour resolves to the Unity `GameSkin` GUISkin on
both builds. The local Addressables catalog has a separate
[key and location audit](addressable-catalog-locations-20261107.md#bundle-options-and-key-coverage-2026-11-09).
The original game, saves and textures were left untouched.

Compare full file SHA-256 maps and require only the listed delta after
applying the 12 manifest members to a verified isolated Windows stock copy.
Run the two existing validators against the signed macOS app and the applied
Windows copy with the pinned `localization/font_probe_requirements.txt`.

```sh
python -B localization/verify_streaming_assets.py PLATFORM STOCK_DATA CANDIDATE_DATA
python -B localization/verify_text_assets.py PLATFORM STOCK_DATA CANDIDATE_DATA
```

The comparison command and five receipts are under
`localization/work/shared-source-reconcile-20261110.k7cLAb/`. The paired
file receipt SHA-256 is
`0720c5dba6923ccd6b43b54107fe3c3d08a27a3d6184af422034e4d194ba3d25`.
The Windows ZIP is the same artifact as in the
[Russian build verification](russian-build-verification-20261110.md).

The source gate remains open. Exact file preservation covers untouched
resources even when they contain engine metadata. It does not classify every
player-visible source or prove the complete field-level preservation contract
inside the 11 changed files. The remaining work is to reconcile indirect
runtime text consumers and additional resources against the approved visible
scope, then verify that the parser-derived contract covers every protected
occurrence. The v42 inventory and existing locale worklists retain their
current fingerprints.
