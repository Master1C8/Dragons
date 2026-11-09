# Conrad gate admission through the original hand hitbox

The macOS repair build reproduced assembly, placement and completion of
`Conrad_Intro_3` through ordinary input in isolated profile `B8G1`.
It left the window through the already tested approach lane and crossed
the wash area. The original macOS `level1` gives `DoneButton` two
different collision objects. Its child `rrr` has a layer-zero box
collider at PathID 3243. The `Plappable` child has a layer-six sphere
collider at PathID 3419 and `HitboxPlapInteractable#4195`, which
references `InteractableDismissButton#3962`. The hitbox and button
components round-tripped to the original serialized bytes.

The probe reads the stock look pose and the hand's aim offset. It uses
the same origin offset and layer mask as the original raycast and
requires the hit to be on the button within the original two-unit
contact cutoff. At 1.256 units from the hitbox center, a mouse
adjustment moved the ray from `beam1_collider` to `rrr` at a
ray distance of 1.068. The probe pressed and released `E`.
The stock handlers changed the dragon from `WaitingOnIntroDialogue`
to `WalkingToWash` and then `WaitingOnBeingWashed`. No dialogue,
flag, movement, or gate handler was called directly by the probe.

The test had 231 samples with no macOS foreground ownership or
on-screen window. It ran through the signed isolated app wrapper,
which removed its generated Steam file and verified the signature
after exit. The four checked original profile roots were identical
before and after.

Profile `B8G2` reproduced the hand interaction and gate admission,
then picked up the assembled mount from storage and carried it to
the performance socket. The pickup left `HasMountFrame=True` and
cleared `PlacedMount`. The ordinary `E` input at the performance
socket left empty hands, set `PlacedMountForUse=True` and started
`Conrad_placed_mount_3` in the original Yarn runner. The observer
stopped the copy after recording this checkpoint. Teardown logged a
`NullReferenceException` from `DialogCommands.OnDialogueComplete`
while the node was active. The receipt establishes entry into the
node. Its completion and the later Yarn transfers remain open.

All 302 desktop samples for `B8G2` showed no foreground ownership
and no on-screen window. Its original profile comparison, Steam file
cleanup and signature verification also passed. The hidden Windows
test stayed running.

Local source and receipts are in
`localization/work/background-gate-20261109.Nx18eu/`.

| Artifact | SHA-256 |
| --- | --- |
| `B8G1` Unity log | `2bb98e8b698938dbdeca91b885050a750b8a59be711139588ce96154b4797b69` |
| `B8G1` observer receipt | `293120cdf0b7b1861558e0661593d80e409c5bd4a7fa0d97325d378d6edc850a` |
| `B8G1` runtime companion | `b82ac5a75a1ce14df594626654b3096d4c50c4bc1a4a80278774bbc74b49764b` |
| `B8G2` Unity log | `e4627ada58d79517bc2c09232c72f9e2ee541c33775814c27ac8eed32c065d24` |
| `B8G2` observer receipt | `8008089decda7a18e7214c7c0083a2e63309b2491195213fce55421bf791366d` |
| `B8G2` runtime companion | `65692213ab78f669a9d162196094f9fa5f11476146d78248d15ad9f6a66dbd06` |

The original macOS and Windows performance-trigger IL excerpts match
byte-for-byte, SHA-256
`a97c0a1700b13ba5efcd6a45b95badb39de5be00e137d02ca9173ceda29ba600`.
The trigger requires an active dragon in `WaitingOnBeingWashed`, no
active dialogue, and an installed model. It reads the start and finish
Yarn node names from the active level configuration. This static
boundary does not establish Windows runtime behavior.

The tracked [gameplay companion](../tools/background-input-probe/gameplay-companion)
includes the route to the performance socket. It builds against
both original Managed sets. The macOS patcher reproduced the
instrumented game DLL from `B8G2`. A Windows fingerprinted scratch
patch also reproduced the previous Windows menu hook artifact. The
Windows companion has no runtime acceptance from these build checks.
The [follow-up performance test](background-performance-20261109.md)
records macOS node completion and Windows slot loading.
