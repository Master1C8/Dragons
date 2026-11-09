# Inline speaker display with unchanged Yarn identity

The pinned `LinePresenter` has an inline name path when its separate name
field is absent and `showCharacterNameInLine` is enabled. That path reads
`LocalizedLine.Text` at `IL_009c`; the earlier separate-label probe does not
change it. The new desktop probe demonstrates a display-only replacement for
that path with the original Yarn parser and `LocalizedLine` from each build.

The probe recognizes the plain `Ryan: ` and `Conrad: ` prefixes in the raw and
parsed text. It requires exactly one `character` annotation over the exact
prefix and leaves a line unchanged if another markup range starts inside that
prefix. It creates a distinct display result with a matching display-name
annotation and shifts the body attributes by the UTF-16 length difference.
It parses only the new plain prefix. The existing body string, attribute
order, values and covered substrings survive without reparsing. The original
line's ID, raw source, parsed name, markup and name-stripped body remain
unchanged.

Both builds passed for all 18 IDs in the existing exact-prefix manifest.
Three synthetic markup controls exercised shorter, longer and same-length
labels. The synthetic bodies included ranged Yarn markup, a zero-length
pause and literal TMP markup. Six fallback controls covered text without a
name, an unknown name, a title-like marker, Alexander's colon-ended sentence,
markup overlapping the name, and a mismatched raw prefix. The macOS build
also rejected the Windows selector and a modified paired export at their
respective fingerprint checks before emitting a report.

Local receipts reproduced byte-for-byte. They are in
`localization/work/speaker-inline-20261109.SJXiG2/`:

| Build | Report SHA-256 |
| --- | --- |
| macOS | `6f9293508733729cbbb4a8c624bdb8c7c9a520e737f5736a93364e8322d7f08e` |
| Windows | `9bf5c2da128d90731640146704504022483f20903000ba16b09cbe941d5000e3` |

This first stage tested the actual parser and display-data transformation
under .NET. The next stage below binds that transformation to the presenter.

Run from the Dragons checkout with a different output directory for each
platform. The helper pins the paired export and both loaded Yarn assemblies.

```sh
dotnet build localization/tools/speaker-inline-probe/speaker-inline-probe.csproj \
  "-p:GameManaged=$original_managed" \
  "-p:BaseIntermediateOutputPath=$test_output/obj/" -o "$test_output/bin"
dotnet "$test_output/bin/speaker-inline-probe.dll" "$platform" \
  localization/work/source-inventory-20261107/yarn-paired-scenes.json
```

## Test-only presenter integration

The optional inline mode of `speaker-display-probe` replaces the pinned
`IL_009c` getter in `LinePresenter.RunLineAsync.MoveNext`. The other two
replacements are the existing separate-name label assignments. Read-back
verified all 717 original method bodies after normalizing these three exact
calls. The only new assembly reference points to
`Dragons.SyntheticSpeakerInline.dll`, a .NET Standard 2.1 companion built
from the same view code as the standalone probe. Default patcher mode
reproduced both its previous DLLs and its report bytes.

The inline bridge selects 18 stable IDs from the fingerprinted protected
prefix manifest and passes the exact expected source speaker to the
companion. Unknown IDs return the original parsed text. The companion
requires that the source speaker and both raw and parsed prefixes agree.
The original presenter retains its separate-label and name-suppression
branches, including the options fallback. The patcher checks the companion
SHA-256 before any output and verifies the two external calls and inline
ID literals after read-back.

The .NET harness executed the actual injected bridge in both rebuilt DLLs
with the fingerprinted companion. All 18 IDs mapped, the two marked-body
controls retained their ranges and values, and eight fallback cases
returned the original view. The new fallback checks use an unknown ID
with a valid prefix and a protected ID with the other speaker's prefix.
A wrong companion hash was rejected before output on both builds. The
two patched DLLs and the execution receipts reproduced byte-for-byte.

Local receipts are in `localization/work/speaker-presenter-20261109.TqasB1/`.

| Build | Patched Yarn Unity SHA-256 | Execution receipt SHA-256 |
| --- | --- | --- |
| macOS | `73192452a93f2ea49ba866a9933b4ca8e8edf68cf946bd5f522472e3513e8e67` | `c0fb8702b1bf43d17a098f4516f03f1ed9d076caf55f0c93ca1f5807868f77fb` |
| Windows | `3ba4b03c5ca3d46145b8d4f143f5d9ca3f160fbd02302e58fe081554f8117266` | `c0b664cd7e9ce7bc63652adaccc007a4076fff884fe928aabcfa34ce41b6281a` |

For each build, compile `tools/speaker-inline-runtime` with the same
`GameManaged` path as the desktop harness. Invoke the patcher from the
checkout using a new DLL path directly under `localization/work`:

```sh
dotnet "$patcher_dll" "$platform" "$original_managed/YarnSpinner.Unity.dll" \
  "$synthetic_map" "$patched_dll" "$inline_runtime" "$runtime_sha256"
```

In a disposable copy of the desktop harness output, replace its Yarn Unity
DLL with the emitted DLL, then execute:

```sh
dotnet "$copied_harness/speaker-inline-probe.dll" "$platform" \
  localization/work/source-inventory-20261107/yarn-paired-scenes.json \
  "$patched_sha256" "$inline_runtime" "$runtime_sha256"
```

The current mapping values are synthetic. Desktop execution invokes the
injected bridge directly. Unity presenter execution, typewriter timing,
visual acceptance, Alexander's special case and the player builder remain
open.

## macOS Unity execution in the background

The isolated profile `B8F1` loaded a two-line synthetic Cyrillic fixture
through the signed app builder. The fixture keeps the exact English speaker
prefixes, and its asset SHA-256 is
`f2833c739fe394a515eb6f0db51e294950704139b4944fe5d96e781bdfc7189e`.
Two earlier fixture variants were rejected before app output at the markup
and visible-digit guards. The accepted fixture contains plain synthetic text.

The fresh app used the previously pinned test entry bridge, which selects
the isolated slot and starts `Ryan_Conrad_SexScene`. The test-only
`tools/speaker-inline-unity-probe` modifies the pinned macOS presenter DLL
to clear the separate name reference and enable inline mode in `Awake`.
It adds a Unity log for the value returned by the existing inline bridge.
The instrumented DLL SHA-256 is
`0da48d759503988e86f0992d66daf02f1f445ceeab262e779fe56d540ddee87e`.
The tracked instrumenter reproduced those exact bytes and rejected the
Windows DLL at the input fingerprint guard before writing output.

The copy used `LSBackgroundOnly` and the normal isolated app wrapper with
`-batchmode -nographics`. Unity 6000.3.14f1 initialized a null graphics device.
The game ran the forced node and logged `VN-INLINE-UNITY-VIEW` followed by
`Жж: ЖЪЬ Жюя`. This proves the real line presenter reached the injected
branch and the companion produced the expected synthetic value in Unity.
All 32 samples found the test PID off the foreground with no on-screen
window. The pre-existing Windows process remained running.

After this marker, the observer sent SIGTERM to the verified macOS test
PID. `DialogCommands.OnDialogueComplete` threw a `NullReferenceException`
while `DialogueRunner.OnDestroy` canceled the forced node. The wrapper
returned status zero, removed the matching temporary Steam file and
verified the signature. The four checked original profile roots matched
their prelaunch state. The shutdown exception leaves normal completion
unverified even though the earlier return value was observed.

Local evidence is in
`localization/work/speaker-unity-background-20261109.X5dcpl/`.
`unity.log` SHA-256 is
`8320676a200920cc0d70fd4508adfc22860c3ed4d0047320266da2e409f99fd8`;
`result.json` SHA-256 is
`68afc08e235c7555a4d807c396d8bd49623cf42c9bea6f7a6b5ba63f1af9c66e`.
This run did not produce a frame. Visible glyphs, typewriter timing,
advancing past the first line, Windows Unity execution and normal gameplay
remain open.
