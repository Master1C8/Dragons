# Background virtual keyboard through the stock main menu

The normal macOS builder made four separate test-profile copies with
the opt-in Yarn repair and a no-op locale fixture. The fixture preserves
the selected source value and uses the pinned Yarn string object
fingerprint. An initial fixture using the enclosing asset fingerprint
was rejected before app output. The successful menu-input probe used
profile `B8I4`, `LSBackgroundOnly`, `-batchmode -nographics` and the
existing signed app wrapper.

The test patch adds one call at the start of `MenuMain.OnShow` to attach
the probe and two instructions at the start of `MenuMain.OnEvent` to
observe its argument. Read-back compared the original instruction
sequences and branch targets of all 2,385 managed methods after
removing those prefixes. The companion enables background execution
for the test copy, adds a virtual keyboard, applies a neutral state,
presses Escape and releases it. It does not invoke menu actions or
change game state beyond sending device state. The extra
`ProbeEscape` action observes the same keyboard as a control.

Both source builds have a serialized `MenuMain.intents` entry for
`Cancel`. Its action references `UI/Cancel` in `sharedassets0.assets`
(PathID 645 on macOS and 640 on Windows), with ID
`15cef263-9014-4fd5-94d9-4e4a6234a6ef`. The referenced action assets
are `globalgamemanagers.assets#2283` on macOS and
`globalgamemanagers.assets#2282` on Windows. Both bind
`*/{Cancel}`. The components, references and action assets
round-tripped exactly.

| Profile | Input boundary | Observed result |
| --- | --- | --- |
| `B8I1` | `InputSystem.QueueStateEvent` in the after-update callback | The sequence ran. No action or menu intent appeared. |
| `B8I2` | Same input with attempted runtime binding inspection | The test reflection helper threw before it queued a key. `MenuIntents` is nested serialized data inside the menu component. This run gives no input result. |
| `B8I3` | Queue with raw-event and independent action observers, without the faulty reflection code | No raw event was observed on the virtual device. The key state was false and the independent action value was zero. |
| `B8I4` | `InputState.Change` with the same virtual keyboard and observers | Neutral emitted no actions. Escape emitted the original `UI/Cancel` and `Player/Pause` actions, reached the stock `MenuMain.OnEvent` with intent `Cancel`, and gave a pressed key and independent action value of one. |

The successful run had zero on-screen windows and no macOS foreground
ownership in all 20 samples. Unity internally reported `isFocused=True`
in batch mode, so these observations establish background operation at
the macOS desktop boundary. The observer stopped the verified isolated
process after the key release. The wrapper removed its generated Steam
file and verified the signature. The four original profile roots
matched their baseline; the hidden Windows CrossOver test remained
running. The test did not load a slot, walk, place equipment, or reach
a Yarn transition. It gives a way to exercise the stock input pipeline
for those next checks. Windows execution and visible Cyrillic remain open.

The receipts and alternate probe sources are in
`localization/work/background-input-20261109.UU2LOG/`.

| Successful run artifact | SHA-256 |
| --- | --- |
| Patched game DLL | `7d97754b9cff4f74090db3acce1c918a254472115786c181892f90ea0201a098` |
| Test companion used in Unity | `359eb5f80e91ece6e4dd787e6433676eae471fa2fcb52ce60dfddba63186cb45` |
| `run4/unity.log` | `068be48f72afbdea1a811b5cacb096ace690e18e58e2b0e36b552f3eb09db9d6` |
| `run4/result.json` | `c45f9f1debdf208c89512b22b7fe25a2e9a696e3c5c865452270379375937d1f` |

The [test-only source](../tools/background-input-probe) builds a
.NET Standard companion against the original macOS Managed DLLs and a
.NET 8 patcher with Mono.Cecil. Build into a fresh work directory and
invoke the patcher from the Dragons checkout:

```sh
dotnet build localization/tools/background-input-probe/companion/companion.csproj \
  "-p:GameManaged=$original_mac_managed" \
  "-p:BaseIntermediateOutputPath=$out/companion-obj/" -o "$out/companion-bin"
dotnet build localization/tools/background-input-probe/patcher/patcher.csproj \
  "-p:BaseIntermediateOutputPath=$out/patcher-obj/" -o "$out/patcher-bin"
dotnet "$out/patcher-bin/patcher.dll" "$original_mac_managed/Assembly-CSharp.dll" \
  "$companion_dll" "$companion_sha256" "$out/InstrumentedAssembly-CSharp.dll"
```

Building from the tracked source reproduced the patched game DLL
byte-for-byte. Supplying the Windows game DLL failed at the expected
fingerprint guard and produced no output.
