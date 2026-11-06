# Synthetic ID-bound display for the Alexander colon line

The source line `line:4b36ea4e` in `Alexander_2` is identical in both pinned
builds and ends in a colon. The existing Yarn parser treats its sentence as
an implicit `CharacterName` and its name-stripped body is empty; the source
line remains protected by the normal translation guard. Its scene, nearby
branch choices and unresolved presentation concerns are documented in
`alexander-colon-introduction-20261107.md`.

`tools/speaker-line-probe` extends the earlier **test-only** speaker display
experiment. At the two separately identified name-field setter sites, its
helper returns the fixed synthetic marker `ЖЪЬ42` only when all three match:
`LocalizedLine.TextID`, the entire `RawText` including the colon, and the
parsed character-name value. A mismatch falls through to the pre-existing
synthetic name mapping or unchanged parsed name; it does not silently match
the special case. The helper leaves the line ID and parsed identity unchanged.
It does not modify the Yarn source table or compiled program. The patcher
validates the original Yarn Unity DLL fingerprints, verifies that the two
inspected providers assign `Yarn.Line.ID` to `LocalizedLine.TextID`, and
compares 717 original method bodies after normalizing only the two expected
display calls. It does not establish all metadata equivalence or every consumer.

The separate `speaker-line-runtime-test` harness runs each pinned Yarn parser
and the corresponding modified helper on desktop .NET. It supplies `TextID`
and `RawText` itself; it is not an execution of the game provider or presenter.
The focused tests verify the source match and negative controls for a different
ID, a different parsed name and extra text after the original colon. They also
check ordinary synthetic Ryan/Conrad mapping, unknown/no-name behavior, unchanged
identities, original DLL hashes and wrong-build rejection. Two tests passed on
both original builds. The following diagnostic DLLs were reproduced byte-for-byte:

- `work/YarnSpeakerLineSyntheticMac-v2-20261107.dll`: SHA-256
  `2a1499e2df774bc34f1465f811f94d1949db8c5be0a480b698161de6b6971dbb`.
- `work/YarnSpeakerLineSyntheticWindows-v2-20261107.dll`: SHA-256
  `e5e6b0755be13f8d4d8524b82838d645c04345c7e78b5249692ce0032f4a7c77`.

This experiment supports a possible source-bound name-field adaptation only.
It is not a Russian rendering, and no target wording has been chosen. The
display helper does not cover inline name fallback or every options layout;
actual provider `RawText`, original and translated screen presentation,
branch progression, readability and final payloads remain unverified. It is
not integrated into the builder and must not be shipped. No game was launched.

Patcher SHA-256 `d3fbda894f53fd250bfcfd9f98d1e0519ea75513e8fa0038e9dbaf6bc5d8490f`;
harness SHA-256 `a85b8c3d4ecac505235555c75bb4e2bf61c93aae45910d57011a7e7928fcc786`;
test SHA-256 `9348fbe4471f87de4ebf8b8e040a9e5e29958994d5260c898188a1a39df53516`.

Build both `tools/speaker-line-probe` and `tools/speaker-line-runtime-test`
projects with separate work-local intermediate and output paths, then run:

```sh
python -m unittest discover -s localization -p test_speaker_line_probe.py -v
```

The test expects the two built tools, the existing synthetic map, the two
diagnostic DLLs, and both pinned game-managed directories under the paths in
the test. These are local work inputs, not a finished package.
