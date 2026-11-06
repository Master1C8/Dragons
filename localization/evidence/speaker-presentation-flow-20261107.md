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
