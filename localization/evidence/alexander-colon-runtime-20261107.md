# Isolated synthetic Alexander-line runtime probe

The separate macOS app `work/DragNWash-AlexanderIDProbe.app` was built from
the pinned original with fresh test identity `Q9R6` and synthetic locale input
SHA-256 `0a9b5b080fee27ef65a7e549031b34f09abea32e2919b99b1367fba3ef5830bd`.
Its test-only `Assembly-CSharp.dll` bridge SHA-256
`04db2e70bdf673acf73bed908161748c0998d73e4d704931548785f89938028f` forced
entry to `Ryan_Conrad_SexScene`. In the copied asset only, the first RunLine
instruction of that node was changed from `line:f5f5b815` to the equal-length
`line:4b36ea4e`. A post-test comparison established that this was the only
compiled-program byte change and that the target source table value remained
exact. Test asset SHA-256
`b4b3df1d590d7de606773ef9190d81e863a18e01528a1673a53e9d5ca80c3854`.
The one-off preparation recipe remains in local work at
`alexander-runtime-prepare.py`, SHA-256
`19d22882674199457bf110fea7e1e6123b3c0132330b34ae7f98de4cbacae451`.

The copied Yarn Unity DLL was the synthetic ID/raw/name-bound helper described
in `alexander-colon-synthetic-20261107.md`, additionally instrumented to log
each display helper return. The logging-only patch source remains in local work
`alexander-speaker-log-probe/Program.cs` SHA-256
`87993ec5791e919ab9c1807a72504c70a81b91b203393b2919864de48ed887af`;
the logged DLL SHA-256 was
`b03bb60f0be3ffd6b276a147908e0910a79d8587b21467d64d4f737ffb804fef`.
Log `work/alexander-id-runtime-20261107.log`, SHA-256
`46567992abdddfb542f7db6ca02e5f14805f3f6248b156811178dfeccccd92bf`,
recorded creation of `BuiltinLocalisedLineProvider`, the forced node, and the
helper return marker `ЖЪЬ42` in that order. Given the tested helper checks,
this is evidence that the instrumented name-field path received the matching
ID, raw text and parsed name in this one Unity test. It is not a proof of the
unmodified natural Alexander branch, another presenter path, branch choices,
progression, text readability or final Russian wording.

The exact test process PID 47194 was terminated after capture; the launcher
removed its generated Steam file and verified the test app signature. The
four checked original-profile roots matched their pre-test file-hash inventory
(`work/alexander-runtime-original-profile-baseline-20261107.json`, SHA-256
`09dcdf2a5740fc4d515ef3f8c9445bb3e422d3324ec1939c2cfa01263245fcfd`), and
both original managed assemblies retained their pinned hashes. This does not
establish normal game exit or prove the contents of unexamined save locations.

The verified game window was captured as native 1024 × 824 PNG
`work/alexander-id-runtime-screen-20261107.png`, SHA-256
`aadc55f85413314810b0f1f7985118d3af90cf02550627b3dd5f23802cf260c6`.
The 1024 × 824 WebP80, without upscaling,
`work/alexander-id-review-20261107/screen.webp`, SHA-256
`4cf08975aa2b22e2984547a746845389947093e9ce09cf7495701eecd42db33c`,
was reviewed by authorized independent reviewer `alexander_marker_review`
(`gpt-6.1-terra`, high). A faint small label appeared at the upper-left of the
dialogue box, but its individual glyphs could not be verified; no obvious
clipping was seen, though low contrast limits that judgment. The synthetic
frame is **needs-review**, not a readability or release pass.

The test was forcibly entered and instrumented, used a modified test program,
and ended by SIGTERM. It establishes neither natural gameplay nor installation,
restoration, final layout or Windows behavior. The original special source
line remains protected and ordinary Russian game-text translation is not yet
ready to begin.
