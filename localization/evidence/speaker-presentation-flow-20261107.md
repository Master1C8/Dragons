# Speaker presentation control flow

The source-pinned scanner `tools/speaker-presentation-flow` extracts the
relevant line and option presenter instruction slices directly from both
original Yarn Unity assemblies. The resulting 51 and 57 instructions are
identical between the pinned builds. The local reports are
`work/speaker-presentation-flow-macos.json` SHA-256
`a99c9a7bf8e08e37d4400792368ff01fb7ba3d94d2e48812174c393762085d77`, and
`work/speaker-presentation-flow-windows.json` SHA-256
`b1ff5ad85b269b5402514701a2016e0d2948e321262a69ec7fc8512b3dbdc8fd`.

In the line presenter, if `characterNameText` is null and
`showCharacterNameInLine` is true, the selected body is `LocalizedLine.Text`
(`IL_009c`), not `TextWithoutCharacterName`; the synthetic display helper is
not called on this branch. If the text component is null and the flag is false,
the body omits the parsed name (`IL_00af`). With a non-null name component,
the body also omits the parsed name (`IL_00c2`) and, when its container and
name permit, a separate name field is filled (`IL_0112`–`IL_0117`). The known
five serialized line presenters have non-null name components, but runtime
mutation and other possible presenters are not excluded.

For the options presenter, the inspected last-line block runs only when its
last-line container, last line, and `showsLastLine` permit it. When its
character-name container is null, the chosen body is
`TextWithoutCharacterName` (`IL_027c`–`IL_0287`); with a non-null container
and nonempty name, a separate name field is set if present. The known five
serialized option presenters disable `showsLastLine`, but a changed runtime
configuration remains possible. The raw `Text` value is retained in the
non-null-container branch when the parsed name is empty.

Consequently the test-only helper that changes the two name-field setters is
not a complete general display mapping: it cannot translate an inline parsed
prefix and cannot make a name appear on a name-stripping fallback. A production
approach must define and test the intended behavior for all applicable paths,
including markup and parser identity, without assuming these fallback paths
are reached in normal gameplay. The colon-ended Alexander line and readable
glyphs remain separate unresolved cases. These are static observations, not a
runtime or visual acceptance.

Two focused tests passed on both source DLLs: one asserts branch targets and
getter/setter sites in the identical slices; the other supplies the Windows DLL
to the macOS scanner and checks the specific unsupported-source rejection.
Scanner source SHA-256
`dc2bfe7e16628f2529353f05c24e89d330c4d23f1899ab5368dd73a575bb02ea`.

```sh
dotnet build localization/tools/speaker-presentation-flow/speaker-presentation-flow.csproj -p:BaseIntermediateOutputPath=ABSOLUTE_NEW_OBJ/ -o ABSOLUTE_NEW_BIN/
dotnet ABSOLUTE_NEW_BIN/speaker-presentation-flow.dll macos ORIGINAL_MAC_YARN_UNITY_DLL
dotnet ABSOLUTE_NEW_BIN/speaker-presentation-flow.dll windows ORIGINAL_WINDOWS_YARN_UNITY_DLL
python -m unittest discover -s localization -p test_speaker_presentation_flow.py -v
```

The test expects the scanner at `localization/work/speaker-presentation-flow-bin`
and the currently pinned local game paths; absent inputs cause a skip.

## v34 serialized presenter templates

The paired UI-role and presenter exports bind 15 fields in each build
to exact presenter references. There are three per scene in `level1`
and `level3` through `level6`: `lineText`, `characterNameText` and
`lastLineText`. Each target is below the corresponding presenter's
serialized CanvasGroup. Its starting alpha is zero, and the target
has no intermediate CanvasGroup that ignores that parent. The
presenter and CanvasGroup objects passed byte-exact read-back.

All five stock line presenters use `LetterTypewriter`. The original
`RunLineAsync` assigns the speaker label or hides its container
before opening the CanvasGroup. Its `PrepareForContent` call assigns
the parsed line and sets the visible character count to zero before
the fade. All five stock option presenters have `showsLastLine=false`.
Their startup code binds the missing last-line container to the
label's GameObject, and the option path hides that container before
fading in. The managed scan found only the two expected reads of
`showsLastLine` and no write to it in either stock managed inventory.
The existing paired `Conrad_Intro_3` probe exercises the original
presenter with real line data on each build. It covers one dialogue
path and does not replace the source bindings for the other scenes.

The recipe preserves these 15 paired template values. Both v34
outputs matched byte-for-byte and changed only the 15 roles from
v33. The source proof covers the pinned stock components and ordinary
presenter code. External mods, arbitrary reflection and a pixel-level
check of all scenes are outside this pass.

The local scans and source are under
`localization/work/presenter-template-flow-20261109.FIRHil/`.

| Artifact | SHA-256 |
| --- | --- |
| Canvas binding script | `b6daaa667ef58287d24ee1a7e4fe5baf0b34f3e8d71f60c7a43a684f7f6fe868` |
| Managed scanner source | `b16a080ae1c018f9ea9b79aadf4a88a937660ba397c817633c34c5fa288f14d4` |
| macOS Canvas bindings | `6c7f24fb594f04e665bdaace892de95dd670b1c86ae0d9b5de02c9acc3b03fbd` |
| Windows Canvas bindings | `b779fd2da156563d787209dbb3920db61dfecea123c264747834bc91e6674046` |
| macOS managed scan | `c6970d9018daa70cc3363ca67e4444588d5b017bee52f87491bfee79ba032ec9` |
| Windows managed scan | `c9488b0206e0796376c082fb0bdd3609f2f47842b4787f4e0415ad25a295949b` |
