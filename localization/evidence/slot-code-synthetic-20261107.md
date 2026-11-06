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
