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

This tests the actual parser and display-data transformation under .NET.
The helper is separate from the player builder. Integration still needs a
call-site patch bound to the supported presenter and the approved locale,
with the protected IDs bound at that call site. The integration must honor
the presenter's separate-label and name-suppression branches. The options
presenter, the Alexander special case, renderer timing, readability and
actual in-game execution remain separate checks.

Run from the Dragons checkout with a different output directory for each
platform. The helper pins the paired export and both loaded Yarn assemblies.

```sh
dotnet build localization/tools/speaker-inline-probe/speaker-inline-probe.csproj \
  "-p:GameManaged=$original_managed" \
  "-p:BaseIntermediateOutputPath=$test_output/obj/" -o "$test_output/bin"
dotnet "$test_output/bin/speaker-inline-probe.dll" "$platform" \
  localization/work/source-inventory-20261107/yarn-paired-scenes.json
```
