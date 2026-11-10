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

## Proposed source glossary repair

The standard-localization character roster needs a source entry for
these four unknown roles. The proposal uses one glossary role without
equating the identities across scenes. The player remains covered by
the existing neutral-address entry. Ryan's verified cold-water lines
stay with Ryan, and the general species entry stays a species entry.

Insert the following entry after `dnw-max` in the protected English
glossary. The new ID is absent from both the English and locale layers.

```json
{
  "id": "dnw-anonymous-dragon-speaker",
  "priority": "P2",
  "term": "Unidentified dragon speaker",
  "meaning": "A dragon in one of four generic scenes. Identity, gender and pronouns are unestablished; use neutral wording in each scene.",
  "category": "Character"
}
```

The exact proposed source differs by that insertion only. It leaves
all 27 current entries and their relative order intact. The draft
contains 28 English entries and measures 831 reference tokens and
1,579 file tokens under the CLI's `o200k_base` calculation. Draft file
SHA-256 `24f51ad99f3b78ef06e1ba8ebefb2ab9072c866f4860fe9839055b504ead8baf`.

All 30 current locale maps have the existing 27 IDs. Adding the
source entry and its Russian counterpart would leave one missing
ID in each of the 29 other locale maps. No existing translations
would be removed or edited. The affected Russian review includes
the new role, the player address rule and the four bound choice
groups.

### Approved strategy and canonical validation

On 2026-11-10 the owner approved neutral wording and the local English
and Russian additions with the disclosed impact on the other 29 locale
maps. The Russian draft term is «Безымянный дракон». Its meaning is
«Дракон в одной из четырёх общих сцен. Личность, пол и местоимения не
установлены. В каждой сцене используйте нейтральные формулировки.»

The production CLI's canonical loader was exercised on three disposable
file sets. It accepted the existing 27 entries and 30 complete locale
layers. It also accepted the proposed 28 English and Russian entries
in a control containing only the Russian layer. With all 30 existing
layers present and only Russian updated, the loader rejected the same
proposal at `dragn-wash glossary locale zh is incomplete (1 missing)`.
The validator requires the full ID set in every included locale.
The existing SiteForMods checkout still passes its normal checks.

The approved strategy is recorded in the scene registry. Canonical
integration requires the new ID to be filled in all existing layers
in the same change. The authorized English and Russian drafts are
preserved under `localization/work/anonymous-glossary-proposal-20261110.SY1yqu/`.
The initial authorization did not cover updating the other locale
layers. At this checkpoint the SiteForMods files were unchanged.

### Canonical integration and Russian scene wording

The owner authorized adding only the new entry to all 30 existing
locale layers. SiteForMods commit `29b0bb56b3ce71a1d5a700c840b050af7333084d`
is on local and remote `main`. The committed diff adds one English
entry, one localized entry per layer, and one source-evidence item.
Removing those insertions reproduces the previous English source and
all 810 existing localized entries. The CLI validated 28 source
entries and 30 complete layers. The focused glossary suite passed all
59 tests. The English canonical fingerprint is
`3d261921e114b6feab10f57ad54d43674a75e991d94937686155b92cce399dc3`.
The Russian layer fingerprint is
`dd5e364a4b4bbaef376a5cecc84a1f26162740a73d2f0f33c06f14fb0b45d6b4`.

The affected editorial read compared each new term and meaning
against the source role, the locale's existing dragon term, the four
scene contexts and the approved address rule. The subsequent
coordinator reread checked the uncertainty of identity, gender and
pronouns separately from the neutral wording instruction. The
unaffected preexisting entries were preserved byte for byte. No
independent reviewer participated in this update.

The [Russian wording](../ru/anonymous-dragon-scenes.json) covers all
20 IDs in original group order. The paired Yarn locale reader
accepted every exact English source and Russian text. The manual
read checked both choice paths in each group, including the player's
apology and unfamiliarity with the button, the dragon's remaining
grime, the silent response, the button sound and the emphatic reply.
This is a special-scene preparation artifact. Package integration
and runtime visual review remain pending.
