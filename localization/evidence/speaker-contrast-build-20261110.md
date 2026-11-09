# Speaker name contrast on macOS and Windows

The player builders can use the stock black speaker style in the four
scenes whose original names are white. The adapter matches the pinned
presenter index and exact source object SHA-256 before replacing the
packed and floating-point colors. It composes with UI string edits in
the same scene. The already-black `level4` stays byte-identical.
No font, sprite or texture is replaced.

The paired tests independently decoded each of the eight modified
name components. The original and rebuilt object trees differed only
in `m_fontColor` and `m_fontColor32`. Every other Unity object was
byte-identical except the independently requested UI string in each
paired `level1` composition test. A full macOS app with all four scenes
passed strict signature verification. The Windows builder emitted four
separate scene files. All 189 tests passed with the paired build tools
enabled.

The source scan traced the name through the `Line Presenter` hierarchy
in all five scenes on each platform. The sibling Image uses the same
sprite reference in every scene of each build, `sharedassets1.assets#951`
on macOS and `sharedassets1.assets#943` on Windows. This binds the
serialized panel structure. The actual color under the name is observed
in the runtime captures below.

## Background comparison

The [white-name runs](speaker-locale-runtime-20261110.md) served as
controls. The black-name runs used fresh `S9B1` and `ProbeS9W2` profiles,
the same exact fixture Yarn asset and the same two speaker DLLs. The
scene files differed only in the four audited scenes. The background
companion used the same route, test values, full-reveal check, and stock
choice `line:83ac5b68`. Both runs reproduced all 18 TMP glyph checks
and captured both lines. The 173 macOS and 261 CrossOver samples had
no visible windows or foreground ownership. Both wrappers finished
with status zero after the task-owned test players were stopped.
Original profile snapshots matched.

Both prepared second-line crops show a dark italic name on the white
panel, without visible clipping or overlap. The body remains legible.
On the original PNGs, the name-region count of grayscale pixels
below 96 changed from zero to 18 and 78 on the first and second
macOS frames, and from zero to 86 and 251 on the Windows frames.
The median of every region stayed 254. The sampled source rectangles
are `(76,409)–(145,423)` and `(130,424)–(245,449)`, with exclusive
right and bottom edges. This count establishes the appearance of
dark strokes for the first line as well as the visually reviewed
second line. It does not independently identify the exact characters.

## Local receipts

The scratch directory is `localization/work/speaker-contrast-20261110.8i848J/`.
The exact scene and fixture comparisons are in `ab-assets.json`
SHA-256 `075d8803ac24c07a0d9dfcd7aec734b722e122d0a72627b2376e723833e72355`.
The source-pixel comparison is in `pixel-counts.json`
SHA-256 `562d3270ee17607a30c61ec2ead8ff64d1fd25a18e509146280bc66f3a6bec7c`.

| Evidence | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Panel hierarchy scan | `50f0008d6ff3e684178c5527a57de9dea258a3766d9f6173783fecd111387888` | `afd37af4589f73127d2ee15b59412c3625092d4b8f500f23f86bafa302bec26f` |
| Unity log | `e078589ccff7aff853731e2816b4438065cbeaced3340b864474d43b17ae7548` | `be37291a18204b6060f21ec890fb7547ba0e44bb5e8ef2977c66a0bde31f9ea4` |
| Exit and focus receipt | `ec97085f37d05451e510dd5297a601194e21fde1afda479a7d0546d7775acf16` | `cd69070e8580470cee0efba76cba4096d356a446cd7b7c8b387723ec3909d6b0` |
| First frame PNG | `e14ed7af33a8b13a74db57877c293b7f496fc140372c4aa85a345dd3730c1334` | `bd6eafd4cb644004e86325f6d1ffafb46f184c3dcae5cb55a68108d0339c3d79` |
| Second frame PNG | `150255d36b212724ebedf28ed19ef9055f2a2513b6e2783b8f1632e3559d1fee` | `96aa2ffa39a2eb41acdbffde727815bb4d23fb51213328a368c544e73d4d13fd` |
| Second frame WebP80 crop | `1cb3adb5c21db831abd2b1a5e984dd37b82f3918cd18101ba111a0bee0893728` | `216e3d3968fded636f6fae18cc7b70eed1c39b5c24a074d6faf4631e819d1cfa` |

The crops are `[0,360,640,120]` from the 640 × 480 original and
`[0,408,1074,136]` from the 1074 × 544 original, with no upscaling.
The rendered comparison covers the isolated `level1` fixture.
The other three corrected scenes still require final-artifact pixel
review. This run leaves inline rendering, natural speaker-scene
entry, the Alexander exception and the final Russian names open.
