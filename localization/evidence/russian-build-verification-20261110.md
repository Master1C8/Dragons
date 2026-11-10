# Russian build verification, 2026-11-10

Source commit `81e761b` on `main` covers all 1,947 v42 package input
positions across the two platforms. The 15 commits after `59287a6`
added the remaining 1,482. The complete package builders accepted
all 12 Russian JSON inputs per platform. Both output receipts match
those files by SHA-256.

| Artifact | Supported build | Artifact identity |
| --- | --- | --- |
| `DragNWash-ru.app` | macOS `9/12/2026_a93aa21a` | Ad hoc signature passed `codesign --verify --deep --strict`. CDHash `b3904b0a73f89f573c02370588d6c1dc272c6f85`. The signed package receipt SHA-256 is `b0d27af866f090916a9d1b75ca1aefff8352daa87a7bd24f90eaa4d1dac5e6a4`. |
| `DragNWash-ru-windows.zip` | Windows `9/9/2026_ee944596` | SHA-256 `89e15f09190188ce479cb2baeea3e5ea5621510a6ba34e29d01479572527cb79`. Archive CRC and all 12 replacement SHA-256 checks passed. |

Read-back of the actual app and ZIP found exactly the 1,823 authored
Yarn values per platform, 16 unchanged source values, and the original
key order and metadata. Each rebuilt Unity scene or shared asset was
also compared with the installed source. The 548 macOS and 534 Windows
serialized texture and sprite objects in those assets were byte-identical.
Twenty focused tests passed for dialogue, special-scene indexing, Yarn
scope and UI preservation.

The runtime controls used a private macOS profile and a cloned
CrossOver bottle with a separate Windows profile. Test copies retained
the delivered scene and shared asset bytes. Each control added two
observer hooks in `MenuMain`; the patcher verified the remaining
instruction sequences of 2,385 macOS and 2,328 Windows methods.
The probe clicked the stock New Game control using Unity's virtual
mouse and observed three active `НОВЫЙ` and three active `Новый` labels,
all with inherited alpha 1 and no renderer culling. Window and focus
samples were `0 0` on all 12 macOS and 24 CrossOver samples. Original
profiles matched their pre-run hashes.

The Windows installation check applied all 12 archive members to a
clone verified against 287 original file hashes. After the runtime
check, restoration returned the clone to those same 287 hashes. The
installed Windows source still matched the baseline.

Local artifacts, build logs, the 284-file app hash inventory, and QA
receipts are under `localization/work/ru-complete-20261110.zjqsdU/`.
This check covers startup and empty New Game slots. Native Windows,
full story progression, occupied slots, save compatibility, pixel
layout and independent editorial review remain open.
