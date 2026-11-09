# Synthetic slot-code localization probe

`tools/slot-code-probe` builds a separate, explicitly test-only assembly from
either pinned original `Assembly-CSharp.dll`. It verifies the source and Cecil
hashes, then checks that the three `MenuSlotsNew.OnShow` instructions at
`0x85`, `0x101` and `0x17c` load `NEW` between the correct slot-progress field
and `TMP_Text.set_text`. Only those three loads are replaced with the fixed
synthetic marker `ЖЪЬ42`; it accepts no Russian translation input and is not
connected to the player builder. Output must be a fresh DLL directly in the
project work directory. It stages and flushes the output before a no-overwrite
rename, and never writes to the source assembly.

After serialization the tool rereads both original and output and compares all
existing method bodies, normalizing only the three specifically validated
source/output literals. It compared 2,385 methods on macOS and 2,328 on
Windows. This comparison includes instruction order, branch targets, locals,
exception handlers and operands; it is not a full metadata equivalence check.
An independent Cecil dump of both output slot methods found three synthetic
markers and all six original `{0} / 14` format strings in `MenuSlotsNew` and
`MenuSlotsLoad`. The original assemblies still matched their pinned hashes.

Local diagnostic outputs, not release artifacts:

- `work/SlotCodeSyntheticMac-20261107.dll`: SHA-256
  `d5d8c8bd09d81b02d757a730cb87f22fa882e71a677e4c1fecc3b429901c3b4f`.
- `work/SlotCodeSyntheticWindows-20261107.dll`: SHA-256
  `ed2f58e930775be2aad6064ebaa76cc1e915235b1b0cc3810ede3696aa7f8e32`.

Two focused tests passed using both original builds. They check the successful
outputs, source hashes, no-overwrite behavior, wrong-build rejection at the
source guard and refusal to write outside the work directory. The separate
synthetic binaries were not run. Actual visibility, the interaction between
the overlaid slot fields, small-window glyphs, save behavior, metadata-wide
equivalence, final translated wording and packaging remain unverified. Earlier
runtime observations and their limitations are in `HANDOFF.md`; this new static
probe does not upgrade them.

Probe source SHA-256 `0d00bacd3456e9daa068dace44cc06e7998cb55dff65723ed7321fe1d8783cd8`.
Build `tools/slot-code-probe/slot-code-probe.csproj` with fresh work-local
intermediate and binary paths; invoke it with `macos|windows ORIGINAL_DLL
FRESH_WORK_OUTPUT_DLL`. The focused test expects the binary in
`work/slot-code-probe-bin` and the two pinned game paths:

```sh
python -m unittest discover -s localization -p test_slot_code_probe.py -v
```

## Managed adapter and stock New Game check, 2026-11-10

The normal macOS app builder now accepts a source-bound `slot-new` record.
The Windows managed artifact command accepts the same ID against its
own source DLL fingerprint. The shared patcher checks the same three
field and setter bindings and compares the original and rebuilt method
bodies. With `ЖЪЬ42` it reproduced both synthetic DLLs above byte-for-byte.
The macOS builder installed both the new-slot and Yarn fallback DLLs
in a signed test app and verified their hashes together with all the
unchanged managed files. The Windows DLL was applied only to a test copy.

The paired runtime controls used fresh isolated profiles and virtual
pointer input on the stock New Game button. No slot was selected.
At the New Game menu, all three code-driven progress fields held
`ЖЪЬ42`. All three separate serialized fields still held `New`.
All six TMP components were active, with inherited alpha 1 and no
CanvasRenderer culling. This establishes two live text sources in
the same menu state. It does not establish how the two layers overlap
on screen or show the complete localized layout.

All 13 macOS and 26 Windows desktop samples showed no window or
foreground ownership. Both verified test processes exited and the
checked original profiles matched their snapshots. Windows ran through
CrossOver. The two added input-observer hooks were validated separately
from the new-slot patch. Native Windows, occupied-slot states,
pixel-level readability and final Russian wording remain open.

Local receipts are under `localization/work/managed-slot-runtime-20261110.eIsBTK/`.

| Artifact | SHA-256 |
| --- | --- |
| macOS player log | `e11ebe782a0f5aef736ff5a69d7722478e8a97c3bdbbbd9ca206ed187d1fb7a6` |
| Windows player log | `0342c0fab6873e4d62d915a2c11df0993532083690b9a26c3b60dade7fc1b47f` |
| macOS observer receipt | `245e8fe775057cfb3775b1cdbcdd226b43c0e82d142907ed6ddedc72ea709356` |
| Windows observer receipt | `ab24f5cd16f196b12bc7d9b360f41cf86e9d71b54e8efb6fc6cbc8dbefcc3b96` |
