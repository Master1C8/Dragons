# Conrad mount assembly in the background

The macOS probe uses the signed repair copy, the same isolated
`Conrad_3_8` slot and the ordinary input path established in
[the preceding gameplay test](background-gameplay-20261109.md).
It checks that the game's interactable selector points at the expected
object before pressing `E`. It reads tool identities and flags after the
original handler runs.

Profile `B8M1` reproduced crowbar pickup and opening the first crate,
then returned the crowbar to its socket. The stock selector did not
accept the first crate's `MountFrame_Socket (1)` with empty hands. The
original macOS `level1` explains that result. The first crate socket at
PathID 4087 holds the `MountFrame` asset and has pickup disabled. The
other socket with the same name, PathID 4091, accepts the assembled
`Mount` and sets `HasMountFrame` and `PlacedMount`.

The source component chain for the missing assembly step is:

| macOS `level1` component | Binding |
| --- | --- |
| `4042` | The second crate's `Onahole_Socket` permits picking up the insert. |
| `3944` | The first crate's `Onahole_Socket` accepts that tool and sets `BuiltMount`. |
| `4069` | The `BuiltMount` delivery enables the complete socket. |
| `4376` | `MountFrame_Socket_Complete` permits picking up the assembled `Mount`. |
| `4091` | The storage socket accepts the assembled `Mount`. |
| `4275` | The separate performance socket requires `HasMountFrame` and sets `PlacedMountForUse`. |

The serialized component reads round-tripped to the original bytes.

Profile `B8M2` opened both crates through the original input handlers,
returned the crowbar, picked up the insert and used it on the assembly
socket. The game set `BuiltMount=True` and enabled the complete socket.
The probe picked up the exact `Mount` asset, walked to the storage socket
and pressed `E` after the stock selector chose it. The same slot had
`BuiltMount=False`, `HasMountFrame=False` and `PlacedMount=False` on
scene entry. The original storage interaction left `EmptyHands`,
`HasMountFrame=True` and `PlacedMount=True`. Both flags were still
true at the final observation, and the dragon moved from
`WaitingToAppear` to `WalkingToWindow`.

Profile `B8M3` subscribed to the original Yarn runner's node-start and
node-completion events. After placement it held neutral input for
35 seconds. The dragon reached `WaitingToBeLetIn` and no intro node
started. The pinned `InteractableDragonWindow` accepts input in this
state. Its original handler changes dragon state and passes the level
configuration's intro to `DialogCommands.StartDialogue`.

Profile `B8M4` repeated the assembly and placement, waited for
`WaitingToBeLetIn`, then walked back to the window. After the stock
selector chose `DragonWindow`, `E` invoked the original player action.
The dragon moved to `WaitingOnIntroDialogue`, and the original Yarn
runner emitted `Conrad_Intro_3` on its node-start event. The copy was
stopped at this checkpoint, with no node-completion event observed.

The serialized `LineAdvancer` at macOS `level1#3938` references
`Player/Attack` for next line and `Player/Plap` for hurry-up.
The [dialogue test](background-dialogue-20261109.md) traces how the
runner changes those bindings at startup. The mount test covers
neither line advancement nor any repaired destination.

Each run recorded no foreground ownership or on-screen window across
all samples. The wrapper removed its generated Steam files and verified
its signatures after the test processes exited. The four checked
original profile roots were identical before and after. The hidden
Windows test remained running.

Local source and receipts are in
`localization/work/background-mount-20261109.yDBnlW/`.

| Test profile | Unity log SHA-256 | Observer receipt SHA-256 |
| --- | --- | --- |
| `B8M1` | `f12cbea6e593347b91ea88312fcb8116a895f2ec5826b852a2f869fc5252d174` | `0f37d7fcaff14ac5af9b7a6152527a74f3942032f515b1528a4b548da436109e` |
| `B8M2` | `4edd8ad35e740d2140ca98e4d5e3923085c237484446884772a94fe0115d8b68` | `ff8f28469d89114229b81edb7a9cf8f6b16addb842a888af32bf4bcc3972b855` |
| `B8M3` | `93efbff48b381f6c3510f2427a324ff83205a3ef483f6895a09c6ae4b01cef78` | `eaf790ce2758719bff8df21150b59906b058da3f0f1e7f59a31666c4255797e5` |
| `B8M4` | `92d21e826c7458dea0194f2d4cafd19ab41aee23f6865c0296e8fba07ec22ae7` | `8edc40933faf5e3e6ab9d7a1fd3f25aa984bf2cd585388af951d25b847ccc72d` |

The tracked [gameplay companion](../tools/background-input-probe/gameplay-companion)
now covers this route. Its rebuild produced the same instrumented
game DLL as the successful Unity run. A positive receipt requires
`VN-BG-MOUNT-FINAL HasMountFrame=True PlacedMount=True`,
`VN-BG-YARN-START Conrad_Intro_3`, and absence of `VN-BG-FAIL`.
The intro completion, performance socket and repaired Yarn destinations
still need ordinary runtime coverage.
