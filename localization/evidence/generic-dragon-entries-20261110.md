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

## Anonymous address dependencies and branch control

The [anonymous-address case](special-scenes-anonymous-dragons-20261110.json)
binds all 12 unlabeled lines and eight player options in the four
project-only nodes. All 20 source values are the same across the
two builds. The case keeps the player and anonymous dragon as
separate roles and avoids merging the four unknown callers.
Neutral agreement is still an open owner decision. The pending
adaptation must also preserve silence, the button sound and the
contrast between ordinary and emphatic agreement.

A desktop control pins the two original compiled programs and
the shared Yarn VM. It enters each node directly in a new memory
store and selects each of its two available options. All eight
runs per build completed in their entry node with the expected
menu order. Their union covers exactly the 20 registered IDs.
The dismissal options have distinct replies. The apology leads
to `line:d726f776`, while unfamiliarity with the button leads to
`line:fb47f998`. Both continue to `line:6d77feef`. The other
three pairs converge to the same line and command sequences.

The buzzing trace delivers the literal `FinishDialogue $dragonName`
command. The thanks trace delivers `Open gate_armature 12` and
`SetDragonState "WalkingToExit"` on either choice. The probe records
these original commands. It does not invoke their Unity handlers
or establish player reachability, gender or rendered behavior.
The wrong-build control was rejected at the program hash guard.

The v42 index now has 27 cases, 271 direct IDs and 1,126 distinct
direct and contextual IDs. Both index runs were byte-identical,
and both focused index tests passed. Local artifacts are under
`localization/work/anonymous-dragon-choices-20261110.nMBD1r/`.

| Artifact | SHA-256 |
| --- | --- |
| Desktop control source | `f11865618b3b4e363ab2e8316b6d8c5376be0a227dfc5f65e1b026d1217489f3` |
| Both branch traces | `82833a3c50b0af164b80ec00ca151989ea8dd76b8bd9d44050e3b17f344c1bce` |
| Current v42 special-scene index | `3769a0882796dfe90277639ed8366219e4a9feec486fc81e271547b50d80abb8` |
