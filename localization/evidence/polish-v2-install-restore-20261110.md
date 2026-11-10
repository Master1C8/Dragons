# Polish v2 package installation and restoration controls

These checks used the historical v2 pair identified in the [Polish checkpoint](../pl/CHECKPOINT.md#corrected-package-read-back), built from translation SHA-256 `cb471d50b18d79b659744dcf6360b25ba63d9ba42c2428e95196e040341dda2e`. The current Polish draft is newer. Repeat the controls on the final unchanged package hashes.

- **macOS.** Copied the actual signed v2 app with `ditto` into a new isolated destination. All 284 bundle files and their modes matched, including the package manifest, and the installed copy passed deep, strict signature verification. Removing that copy restored the previous destination tree. The original game and package matched their initial inventories and hashes. Manifest SHA-256 `0dfd708280c1541e9002cbefd253208a2d19b1f1512bd8df1455e48e11a76329`.
- **Windows.** Applied the v2 ZIP to an isolated copy of the complete stock Windows Data tree, replacing 11 files and adding one companion. Every replacement matched its manifest hash. Unrelated files retained their bytes and modes. Reversing the overlay restored the 259 stock files and 16 directories. A wrong-stock-file control failed before the first replacement. A controlled interruption after the first replacement and the companion addition restored the full baseline. The original Data tree and ZIP were unchanged. ZIP SHA-256 `b0f45d5452c5efc15f8de558dde129cf2f8f94bfe56ed84ff29bda9f96315d3d`.

No game was started. These filesystem controls do not establish native Windows installer behavior, game execution, or recovery from an abrupt process or machine loss.

| Local proof under `localization/work/` | Result SHA-256 |
| --- | --- |
| `pl-macos-v2-restore-20261110.PsUhGB/result.json` | `e4459a65003a8d472b626ff379106c90659faf8518846316f112e4883bb311a7` |
| `pl-windows-v2-restore-20261110.li8pXl/result.json` | `9ef2ce6d309df2765f6ea42d6737d4d5146430febc523ad3df3b65d97317e5b2` |

Each proof directory includes the exact `check.py` used. Temporary game copies were removed after verification.

## Canonical package rebuild

The repository's unmodified `localization/verify_locale_package.py` verified both retained v2 artifacts against fresh rebuilds from the immutable `0d34c62` translation snapshot. Python 3.14.6 ran the canonical verifier with the pinned UnityPy, TypeTreeGeneratorAPI and fontTools versions. It checked 284 macOS files and 13 Windows archive members, and reran component and serialized metadata preservation. Its receipts matched the earlier lane-owned verifier byte for byte.

The commands and logs are under `localization/work/polish-v2-canonical-rebuild-20261110.wft3Nk/`. Receipt SHA-256 values are `da662c0330c61561984cba3969075176bf69f572554afaa0f61a1d8144a8c341` for macOS and `1f54a68d0d088781959d61bafb8c83623c021194bea7f338c45fc8e9c652a4d8` for Windows. These results exercise the normal verifier on real paired artifacts. The newer Polish text still needs its own rebuilt packages and acceptance checks.
