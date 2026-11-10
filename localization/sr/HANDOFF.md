# Serbian localization checkpoint

2026-11-10. Drag'N Wash `sr`, Serbian Cyrillic and Ekavian. Supported stock builds: macOS 9/12/2026_a93aa21a and Windows 9/9/2026_ee944596. Textures and saves are out of scope. Authored by `gpt-6.1-terra` high; no delegated or independent review.

- Translation: `localization/sr/translation.json`, 1,947/1,947 authored IDs; SHA-256 `3ea2186600f5fcceb15196b955d7e4c63b5cc1b73465bf911671fecc42cdfc28`.
- Shared worklist SHA-256 `496d41967a72994bf63de2acf810bdd1e6995806b4f2219fc9f9e61c4f572a45`; inventory `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`; Yarn scope `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30`.
- Serbian glossary snapshot SHA-256 `a521605ecaa362b043e582ec523f5c2526cd4efd60828c0bfcbd2cff2ebadff1`, SiteForMods revision `29b0bb56`.
- One self-edit read covered all worklist rows against the English source and the 25 paired differing English values, followed by wording corrections and an affected-neighbor recheck. The film-title separator was subsequently corrected to preserve the Yarn implicit-speaker delimiter rule. This is self-review, not independent editorial acceptance. Runtime, visual and independent review remain not run.
- `verify_authored_yarn.py --complete` passed on the stated final hash: 1,823 dialogue bindings per platform. It used the existing relocation wrapper and a local Python environment because the canonical SiteForMods checkout and originally specified Forest interpreter were absent.
- The shared static package builder and fresh-rebuild verifier completed through the existing relocation wrapper under Python 3.12 with the same dependency versions as the prior local environment. Receipt `localization/work/cli-terra-high-wave3-20261110.71d8AW/sr/packages-3ea2186600f5/result.json`, SHA-256 `d5d5e2065ce8bf4656887b2376c09c599fec6d61d1c049f73ccd5d626baf2605`. It records 284 matched macOS bundle files and 13 matched Windows archive members.
- macOS: `localization/work/cli-terra-high-wave3-20261110.71d8AW/sr/packages-3ea2186600f5/DragNWash-sr.app`.
- Windows: `localization/work/cli-terra-high-wave3-20261110.71d8AW/sr/packages-3ea2186600f5/DragNWash-sr-windows.zip`.
- A prior Python 3.9 attempt stopped during macOS comparison because `hashlib.file_digest` was unavailable; its partial output is retained separately as `packages-3ea2186600f5-python39-incomplete`. No game or installer was launched. Project-wide archival remains pending; this locale task does not close the multilingual project.
