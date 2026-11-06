# Synthetic speaker-display probe

This is a test-only investigation, not a translation or a release mechanism. The
source-pinned patcher changes the two direct calls that assign a parsed Yarn
character name to a TextMeshPro field. It leaves the parsed character identity
and the original line source unchanged. Only `Ryan` and `Conrad` are mapped, to
the artificial values `Жж` and `ЪъЬь`; unknown and absent names pass through.
The separate runtime harness executes the pinned real Yarn parser and modified
helper on desktop .NET, not the Unity presenter. Its per-platform reports and
build reports are in the adjacent `speaker-display-*-20261107.json` files.
Readback compares all 717 pre-existing method bodies after normalizing the two
intended call changes; it does not prove all metadata or dynamic consumers.

The synthetic macOS app `DragNWash-SpeakerMappingProbe.app` used a fresh `Q9R4`
test profile and the dialogue fixture SHA-256
`0a9b5b080fee27ef65a7e549031b34f09abea32e2919b99b1367fba3ef5830bd`.
It contained patched Yarn DLL SHA-256
`8b3906e2bb290fc0761348042abe1c76fea9e565b82eff5d58255877481d5c7f`
and test-only entry bridge SHA-256
`04db2e70bdf673acf73bed908161748c0998d73e4d704931548785f89938028f`.
The bridge derives from the previously exercised auto-navigation test bridge,
changing its single forced entry to `Ryan_Conrad_SexScene`. The Unity log
`speaker-mapping-probe.log`, SHA-256
`bfade054e5cdcbd9a8be5b82ad7e55b5b81a2c1f9a851d546955e533192d96f4`,
records that node; local OCR detected its first dialogue body. The original
window capture SHA-256 is
`ddb23e0916c2f15e93fc731f7d8ddf4fe1807d42797710f86d25528c9935080f`.
The 1024 × 824 WebP80 review copy SHA-256 is
`e7c215ee5070508b43710059ac3d474617f0b95cfd3e676615de2e722d5c43a9`.
Independent review found a very faint label-like cluster at the upper-left of
the dialogue box but could not read it or verify `Жж`, glyphs, or clipping.
This frame therefore does not prove that either modified call executed or that
the mapping rendered. The normal window title and mouse icon were visible.

The verified test PID was terminated; the wrapper removed the matching generated
Steam file and verified the copy's signature. The installed original macOS
`Assembly-CSharp.dll` and `YarnSpinner.Unity.dll` still matched their pinned
hashes. The test used a separate profile; this run did not independently compare
all original save locations or demonstrate normal game exit. Windows Unity
execution, actual name display, identity-dependent game behavior, full-glyph
readability, normal scene entry, and player installation remain unverified.
The unusual source line ending in a colon and the `title:` markers remain
protected pending separate investigation. The synthetic mapping tool is not
integrated into the player builder and must not be used as a release artifact.
