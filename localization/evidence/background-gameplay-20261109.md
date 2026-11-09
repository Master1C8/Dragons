# Background macOS save loading and gameplay input

The source-pinned macOS app builder produced fresh test-profile copies
with the opt-in five-node Yarn repair and an unchanged source value in
the locale fixture. The input companion used the two already verified
menu hooks from [the initial input test](background-input-20261109.md).
It enabled background execution and applied keyboard and mouse device
states. Game state observations were read-only.

The isolated profiles loaded a synthetic legacy slot from
`defaultUser/slot1/savegame.dgn`. The fixture reused the six prior-level
flags from the paired Windows gameplay check and added the macOS
`version: 1` header. Its SHA-256 is
`d84b9801813a463d1e6c4c8f66322f7dad9f2083419590f0c2070ca406b7a981`.
It starts at save index 7 with no `PlacedMount` flag. In the pinned
macOS assets, `LevelFlow` at `sharedassets1.assets#10660` maps index 7
to `Conrad_3_8` at PathID 10657. The decoded flow object round-tripped
byte-for-byte.

The test ran with `LSBackgroundOnly`, Metal and `-batchmode`. Unity
reported a 640 × 480 viewport. The probe resolved the center of each
original menu button and checked that its event-system raycast hit the
button before applying mouse state. The stock `UI/Point` and
`UI/Click` actions clicked `LoadGame` and then `LoadSlot1`.
The `PlayGame` scene loaded, read the fixture flags, reported
`DeliveredMountFrame=True` and started the dragon walk routine.

Profile `B8I5` measured 0.0067 units of camera movement during neutral
input, followed by 3.2031 units after `W` activated `Player/Move`.
Profile `B8I6` reproduced the 3.2031-unit movement and applied a
horizontal mouse delta. The stock `Player/Look` action rotated the
camera by 1.9040 degrees. This establishes walking and turning in the
loaded scene with ordinary input consumers.

In profiles `B8I7` and `B8I8`, walking and turning made the stock
selector choose `crowbar_socket`. `Enter` emitted `Player/Attack`.
The first run's observer used a component cast for the tool asset and
could not read the result. The corrected observer in `B8I8` found
`EmptyHands`. The original `Interacter.Awake` IL registers its
interaction handler on `Player/Plap`.

Profile `B8I9` sent `E` after the stock selector chose the crowbar
socket, verified the exact `Crowbar` asset in the player's hands,
then turned to `ShipmentCrateMountFrame` and sent `E` again.
`Player/Plap` handled both presses and the crate's original
`opened` field became true. The run ended with the crowbar still
equipped. The mount frame had appeared near the opened crate at
`(1.0598, 0.0584, -9.3493)`. Another active socket had the same
name, `MountFrame_Socket (1)`, at `(3.5900, 0.1600, 10.6020)`.
Use the object context when continuing the equipment route.
Mount placement and the repaired Yarn transfer remain unverified.

The copies used the existing signed app wrapper. Each observed run had
zero on-screen windows and no foreground ownership in every sample.
The test-only processes were stopped by verified identity after their
receipts. The wrapper removed their generated Steam files and verified
the signatures. The four checked original save and preferences roots
were byte-identical before and after. The existing Windows process was
left running.

Local probes and receipts are in
`localization/work/background-gameplay-20261109.CDqP5o/`.

| Test profile | Player log SHA-256 | Observer receipt SHA-256 |
| --- | --- | --- |
| `B8I5` | `941414384a488acf2c8229bdb6bffadb17caf38b67c99142b3a9d85bc61c3e1b` | `66a86a19d150fc38b1fb4a8d9767b3faa00374434c389575e25b25048f0860b8` |
| `B8I6` | `5aa47bb976158314dc676c54166cdfcd9a9b907641638e22d09037f61850c789` | `a63420965ef34a35b5dab25aa29cb15077294ed1594cab40e143e5b984e4cad3` |
| `B8I8` | `dcaafd141c17b02c9b620258b78ddbec78f4a823de678bcf60dde1f9c15313b2` | `30f381a27b917998f0094e314acd475f10142a035a5fefad2ddcd68b6f35c909` |
| `B8I9` | `6b05994495c99527385314adf38af21e8a18bef5d5a507a82fb8419af93d00da` | `87a638c2bf905ceb364bf2fd81be3fd940d04ae2fcd2c10ee11bcfa359ed838e` |

The [gameplay companion and synthetic slot](../tools/background-input-probe/gameplay-companion)
reuse the [menu patcher](../tools/background-input-probe/patcher).
For reproduction, build the gameplay companion in place of the
keyboard-only companion in the earlier recipe. Seed the tracked slot
fixture only in the fresh isolated bundle's `defaultUser/slot1` path
before launching its signed batch-mode copy. A successful observer
receipt requires both equipment results and absence of `VN-BG-FAIL`.
Building the tracked companion and running it through the menu patcher
reproduced the instrumented game DLL byte-for-byte.
