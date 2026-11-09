# Generic dragon node entry audit

The source scan verified the stock macOS and Windows build hashes
before decoding both Yarn programs and inspecting 17 serialized files
and 31 StreamingAssets files per platform. It searched exact ASCII
node names in the pinned files and decoded the three local Unity
bundles per platform. It then attributed each hit in the serialized
files to an object. The managed scan checked all 170 macOS and 172
Windows root DLLs against the existing filename-and-hash manifests.
It inspected direct and delegate method references, IL string literals
and selected field reads and writes with Mono.Cecil 0.11.6. A control
that changed only the expected `Assembly-CSharp.dll` digest was
rejected at the assembly fingerprint check.

The 80 inspected managed method bodies have the same entry routes on
both builds. The single instruction difference is the oviposition
bark priority, 4 on macOS and 3 on Windows. Both versions store the
same constructor argument as the dialogue title. The scan found no
IL string literal containing any of the five generic name suffixes.

| Observed route | Origin of the node name |
| --- | --- |
| Window and phone interactions | Active level intro or phone configuration |
| Player talks to a dragon | `WalkNWashDialogueShooter` selects a current entry from the level's progress dialogue array |
| Idle, mount and other progress barks | Level dialogue selection or an explicit managed node literal |
| Serialized bark and performance components | The stored dialogue title or name |
| `YarnRunDialogOnEnable` | The stored `targetDialog` |
| Yarn runner autostart | The stored `startNode`, set to `Start` on the five identified runners per build with serialized autostart disabled |

The paired original programs each contain 195 nodes, 89 named
transfers and 1,472 command instructions. The original Yarn DLL's
protobuf enum identifies `PeekAndRunNode` and `PeekAndDetourToNode`
as fields 17 and 19. Neither occurs in either program. No named
transfer or command text names any of the five generic nodes. None
of the command opcodes directly requests a new dialogue or project.

| Node | Dialogue lines | Player choices | Stock serialized name occurrences |
| --- | ---: | ---: | --- |
| `DragonAlmostClean` | 3 | 2 | Yarn project only |
| `DragonAnnoyedByBuzzing` | 1 | 2 | Yarn project only |
| `DragonConfusedAboutDismissal` | 5 | 2 | Yarn project only |
| `DragonSatisfiedAndLeaves` | 3 | 2 | Yarn project only |
| `DragonColdBalls` | 4 | 0 | Yarn project and seven Ryan bark components per build |

The four project-only names appear in
`sharedassets1.assets#10719` on macOS and `#10707` on Windows.
The `DragonColdBalls` positive control recovers the same seven
objects per build as the [earlier Ryan audit](glossary-roster-followup-20261110.md#ryans-cold-water-bark).
These checks bound the observed stock entry paths. Live Unity
coverage and external or reflective invocation were outside the
probe. Preserve all 20 IDs in scope and retain the open owner
decision on neutral treatment of the anonymous speaker.

Local scripts and evidence are under
`localization/work/generic-dragon-entries-20261110.Phf2KD/`.

| Artifact | SHA-256 |
| --- | --- |
| `Program.cs` | `444aef98579cb47156e00917485ddf0fc640ab0eb303777d91a7ed082399e7ba` |
| `check-source.py` | `6b9b4e9ffd4e93dd5e5c65a3df31f8c5aacb6f2da45ecdb5a553cf75b81fa481` |
| `macos-entries.il` | `18688bac460a5fbea680bfa00187dfc3e084b93b41657e3f6e56fd9596d878e6` |
| `windows-entries.il` | `f7d35b299464822f3a896aa3af34b2f9f9f7a7af4073e03c724c2ef0f9435f4f` |
| `paired-objects.json` | `b26520115a581599870b6f350106625d093773b5ed28d59697461272a38c1df3` |
