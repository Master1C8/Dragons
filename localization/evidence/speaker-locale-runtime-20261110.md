# Speaker display in both background players

The [paired speaker build](speaker-locale-build-20261110.md) supplied both
speaker DLLs byte for byte. The macOS test used an APFS clone of the signed
builder output, with the isolated `S9A1` profile, a background-only plist
and a new signature. Windows used a cloned test game in the private CrossOver
bottle and a fresh `ProbeS9W1` profile. The complete Managed inventories
were compared with the installed games. The only differences were the two
speaker DLLs, the managed new-slot DLL with two test input hooks, and the
test input companion. Both original Managed manifests and Yarn asset pins
still matched after the runs.

Stock virtual mouse and keyboard input loaded the isolated Conrad slot and
entered `Conrad_Intro_3`. A temporary fixture redirected its RunLine at
instruction 6 to `line:f5f5b815` and its RunLine at instruction 23 to
`line:5660dc8b`. Complete Unity object read-back found only those two
equal-length operand substitutions in the already repaired YarnProject.
Stock dialogue input selected `line:83ac5b68` between the two checks. This
exercises both name assignments and the real branch input between them
without claiming entry to the original scene that uses those two IDs.

Both players produced the same four TMP readings. In order, the first
body and name were `ЖЪЬ Жюя` and `Жж`; after the choice, the second body
and name were `ЖЮЯ` and `ЪъЬьЯяЖ`. All 18 non-space glyphs per platform
resolved to the matching code point in LiberationSans SDF - Fallback.
The fields were active, had inherited alpha 1 and were neither culled nor
reported as overflowing by TMP. The input companion waited for full reveal
before requesting each offscreen frame through the stock `PlayerFace`
camera with the same temporary Canvas routing as the earlier Cyrillic probe.

macOS supplied 165 off-foreground samples and Windows supplied 265. All
reported no on-screen windows. The task-owned games were stopped after the
second capture and both wrappers exited with status zero. Original profile
snapshots matched. The macOS wrapper verified the app signature and removed
its generated Steam file. The pre-existing Windows game process remained
running. An initial Windows observer stopped at a profile path assertion
before starting a player. Correcting that path was sufficient to start the
verified Windows run.

## Pixel review and source style

The second-line crops show a readable dark body in both players. The separate
name above it appears as a faint outline on the white panel. Its exact glyphs
could not be verified from the crops, and the name remains **needs-review**
for contrast. The OCR attempt failed in the local Vision execution backend
before returning results. First-line frames are retained with the component
evidence; pixel review here covers the second line on each platform.

The pinned original presenter fields were audited across all five dialogue
scenes in both games. Each scanned asset, presenter and text target matched
its recorded SHA-256. The two TMP objects in each scene passed byte-exact
schema round-trip. Both builds use black body text and the same material
reference for the two fields in each scene. The name field is already black
in `level4`; it is white in `level1`, `level3`, `level5` and `level6`.
The rendered failure is proven in `level1`. Matching the stock black name
style is a testable correction for the white fields, subject to checking the
panel and rendered name wherever a correction applies.

## Local evidence

Files are in `localization/work/speaker-runtime-20261110.O82oIa/`.
The companion source SHA-256 is
`9fa656628e6a1977fea2b4ed70b1d5cf9c8f6c88540c86f9cded608b9f7b0967`.
The style inventory script SHA-256 is
`f3582546c692af7782cd80909fc5f1892b3e618094358743ddd80ca2134f7d0d`.

| Evidence | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Fixture binding | `575d8092d3315d4b34a2a9c1066223c8a8d5c4a331447d328ec8ef379a666581` | `182681110e3c8b7915b1174499ffc0c9c292486e55581b0c2c481e81a94f3a2d` |
| Unity log | `2e4d76239c4d02bf129cca18dc85b512248def82b82ab2c6a5cff0f426a99966` | `26dbc3a835f60952e1e67cbaa060fac917a217a1b99ab799304542f7d32974ef` |
| Exit and focus receipt | `7e91c883c929768571d08bca20f8e8b2891c3eca1f168ef65b33ab59e3552722` | `fbc576641a169c90f128ac3115596454f1d0d47140c5313ac9b926f782608ebe` |
| First frame PNG | `28467b4cc47cc6791e3f2f515ddc374a20290b235da01ec7d0aa98df1f22f362` | `927cb4ad50c8e3b1af05074aa2d001d1d13e1fd70db35539c885d4bb8dcc138f` |
| Second frame PNG | `30d36014ad6936b0c43cd0184ca7ffe24892743e148e33e5ae9550242dbbe19b` | `babccf31a2623502faf83b90f878a5fa91463e45703f52a34de42ed72a3b64af` |
| Second frame WebP80 crop | `a8cd7988c727557591a879c710553c0ba16e02ad9322416ace881fc45fe3d211` | `baafe12006cfc77e46cea0dd99434006081ebc6bee454503bc4345c32634a7a1` |
| Serialized style inventory | `958a089a60fae7bebbde89717663fc4026b30e4e9f8a11cc797b4434c647219f` | `494ef821b077c6605129bdfffcc6e772439e45b195dba9d941b0322a2afb9af7` |

Crop bounds in original pixels were `[0, 360, 640, 120]` from the 640 ×
480 macOS frame and `[0, 408, 1074, 136]` from the 1074 × 544 Windows frame.
Neither was upscaled. Originals remain on disk. This was a synthetic
separate-name check. Natural entry, inline rendering of the player adapter,
the Alexander exception, end-of-scene completion, final wording and
release artifact verification remain open.
