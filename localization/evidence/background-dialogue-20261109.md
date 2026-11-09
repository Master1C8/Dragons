# Conrad intro through the original dialogue controls

The macOS test uses the isolated `Conrad_3_8` fixture, the repair build
and the normal background input route from
[the mount test](background-mount-20261109.md). The game loads the
fixture through its menus, assembles and stores the mount, and starts
`Conrad_Intro_3` after the player interacts at the dragon window.

Profile `B8D1` sent `Enter` after the intro started. Unity emitted
`Player/Attack` and `UI/Submit`, but the run saw no choice or node
completion before its dialogue deadline. The pinned serialized
`LineAdvancer` contains a next-line reference to `Player/Attack`,
but its `separateHurryUpAndAdvanceControls` setting is false.
`LineAdvancer.Start` registers the merged-control path and clears
`nextLineAction` in that mode. The hurry-up reference is
`Player/Plap`, whose keyboard binding is `E`.

The macOS `level1#3938` and Windows `level1#3893` component reads
round-tripped exactly. Both serialize the same input mode and merged
controls setting, and both resolve the references to `Player/Plap` and
`Player/Attack`. The extracted `LineAdvancer` instruction reports
match byte-for-byte across the two builds.

Profile `B8D2` confirmed the active advancer's next-line action was
empty. Pressing and releasing `E` advanced the stock line presenter.
The probe used event-system raycasts and virtual mouse presses to
select the stock option views for `line:83ac5b68`,
`line:0b7589ff` and `line:4d692a01`, in that order. The original
runner reported completion of both `Conrad_Intro_3` and its dialogue.
At that point the dragon remained `WaitingOnIntroDialogue`.
The original `InteractableDismissButton` accepts that state, calls
`GateController.Open`, and changes the dragon state to
`WalkingToWash`.

Profile `B8D3` reproduced the intro completion and tried walking
directly from the window to `DoneButton`. `Player/Move` continued to
emit, but the camera stalled at approximately
`(4.027, 2.230, -10.840)` and the button stayed outside interaction
range. The test stopped on its navigation deadline without pressing it.

Profile `B8D4` left the window along the approach lane, crossed the
wash area and reached selector range of `DoneButton`. The original
selector chose the button at 2.556 units and `E` emitted `Player/Plap`,
but the dragon stayed `WaitingOnIntroDialogue`. The button's
`get_interactsWithHand` returns true. The ordinary cached-target handler
explicitly skips hand-only objects. The original
`HitboxPlapInteractable.Hit` calls the button only for a hand hit.
`PlapperHand.UpdateRaycastTarget` performs a separate three-unit raycast
from the look pose with the hand's aim offset and layer mask 385.
The next gate test needs to observe the actual hand collider target
and confirm contact. Selector range alone does not establish either.

All four observed macOS copies stayed off the foreground with no
on-screen windows. Their original profile comparisons and signature
checks passed. The hidden Windows test remained running.

The local work is in
`localization/work/background-dialogue-20261109.jsmTX8/`.

| Test artifact | SHA-256 |
| --- | --- |
| `B8D1` Unity log | `69b2968fae8e08e83704ff07c7a4d1399c6075f8e2d72c288e89f2e4025ef7f6` |
| `B8D1` observer receipt | `bb732964adb23e32835c4d8c6eeba312f75fd82f174e31bf60e5e9499a9b9983` |
| `B8D2` Unity log | `a6c53da2587d6d6b835facd29e72fe3b422c541d4bff48a6579e89249c041b62` |
| `B8D2` observer receipt | `e5b3c9995f01752affcce0dfe6b1b8d02a9857d8bb69404612d20da5c325d167` |
| `B8D3` Unity log | `e84f732059eb959ff1c708df7ca71cc0ee5a1c1b923229f7de1c8756529505c5` |
| `B8D3` observer receipt | `ab44aec79f7c8265a3db18e9345a64ea28bd3c7a09b8f35671142c622a323e84` |
| `B8D4` Unity log | `8c6d71b3b23eab78393c46f414d953141e1d423263be7c14f4c0de25a86309a9` |
| `B8D4` observer receipt | `5748169859779df960192a3d06639288dc57a1ca2deaa006e8ea996ee6301637` |
| Original `LineAdvancer` IL excerpt | `32a116525fcee9406dae19f28e166dc8c3d0a0cca7404e8a0df0f6c701867820` |
| Original hand and hitbox IL excerpt | `a9fbc9cda4b6aa52961112032bdbead3dae748e57d1badee2869ea5dc5cc7771` |

A separate Windows preflight compiled the companion against the
original Windows Managed assemblies and verified the two menu hook
sites. The patcher compared the original instruction sequences and
branch targets for 2,328 methods. Its scratch output SHA-256 is
`f6ce02097e9d06c3f27120b9ccff1130c5374661abc8fffe544cafea2139ee08`.
That artifact was never launched. The Windows profile and background
runtime boundary still need verification.

The tracked [gameplay companion](../tools/background-input-probe/gameplay-companion)
reproduces the completed intro route. The success markers are
`VN-BG-YARN-COMPLETE Conrad_Intro_3`, `VN-BG-YARN-DIALOGUE-COMPLETE`
and `VN-BG-INTRO-FINAL choices=3`, with no `VN-BG-FAIL`.
The [subsequent gate test](background-gate-20261109.md) verifies the
hand hit and entry into the mount scene. The repaired destinations
remain pending.
