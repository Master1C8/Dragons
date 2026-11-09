# Alexander's colon-ended line in the dialogue body

The optional `line:4b36ea4e` record in the speaker locale preserves the
complete source string in the Yarn table and displays an independently
supplied plain-text body ending with a colon. The display helper requires
the exact ID, raw string, parsed text, character name and character
annotation. It returns a fresh display view with no speaker annotation.
The game's own presenter then hides the name field. Its original line
object and parsed identity remain intact. The normal Yarn locale still
requires the English source value exactly.

Read-back on both builds checked all 717 existing method bodies with
ten specifically authorized display calls and the existing missing-line
replacements. The .NET harness executed the special body through all
three display helpers and verified the hidden-name result. Controls
used the exact sentence with the wrong ID, the correct ID with changed
source, and correct raw text with changed parsed text. The ordinary
body, names, markup and missing-line behavior also passed.
The complete suite passed 189 tests, and the affected source inventory
and source case checks passed again after the v40 update.

## Background gameplay fixture

The isolated `A9B1` macOS and `ProbeA9W1` CrossOver players used the
verified new speaker DLLs, the contrast assets and the same virtual
input route as the [speaker test](speaker-locale-runtime-20261110.md).
In a temporary copy of the repaired YarnProject, the RunLine operands
at instructions 6 and 23 of `Conrad_Intro_3` were redirected to
`line:4b36ea4e` and `line:f167e3d7`, respectively. Complete asset
read-back confirmed that only the two equal-length operands changed.
The protected table value stayed English.

Both players displayed a long synthetic Cyrillic sentence in two
lines with 72 visible non-space glyphs, the name field hidden and
inherited alpha 1. The offscreen crops show both lines and the final
colon on the white panel without visible clipping. Stock choice
`line:83ac5b68` then led to the original `Alexander!` line, with
the name field still hidden. The second frames are retained. The
visual review here covers the first, wrapped frame on each platform.
macOS and Windows recorded 168 and 266 background observations
respectively, all without a visible window or foreground ownership.
The wrappers exited zero after the task-owned players were stopped.
Original profile snapshots matched.

The fixture proves the actual presenter, layout and one advance
through a stock choice. The normal Alexander college branch, its
alternative answer, native Windows execution and the final Russian
editorial decision still need verification. The synthetic sentence
is a rendering input only.

## Local receipts

Inputs and outputs are in `localization/work/alexander-body-20261110.TV8tMJ/`.
The pinned [source case](special-scenes-alexander-colon-20261107.json)
identifies the actual Alexander branch and its two destinations.

| Evidence | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Patched Yarn Unity DLL | `4dd9a7bf00eed9fc939459ba6bf47d3aa348dd39f524c9f36600aa69ae6072c4` | `22488bd3fe456188be74a0a05db135d04253e5de63d7813154ea8e18960d4910` |
| Speaker runtime DLL | `3c83e4ebb75eeff0b5a64be7b13dfa7dfe7cf0d269566444f67ee1da1ae44502` | `514d2d4d9b4c0f28960424c1eebfc67c2fd5b94509bcafda90fe5649eba7ca64` |
| Fixture binding | `3de8cddd4320daa5ae67006273bec081dcb0450978cb496d0c2ad3c02730389b` | `ffd547f1a5eb8ec509c2aa5848ef1d0a827e4bbdbe12db8643954a5f30e11661` |
| Unity log | `60e35b344b865675aacb17b703b125955fa44e9b07313c5c11bccd7b1d516384` | `b5e3f864c7686676d3ee0ab6c99b7f855fbb6fb808d0effd7c6f2f4b3c25e50b` |
| Focus and exit receipt | `6638fe42c106c44aeaa788f688e33f86df3847d0a834985639cfe7a36f9955e2` | `0257adecec91f7a96f5d3a9290423c252044bc7ba1d3d6e1cb900455b84e6239` |
| Wrapped-body original PNG | `a06b41b2d2428479770d37a39a6bf03362ef16626bb8d3b5aa0fc2629fedf96e` | `4e8a4b72cd04ef159e120c2daf181d8819aef261d4c52ff06ae739ff796db98a` |
| Wrapped-body WebP80 crop | `aa98747a88e55512603b783a61651a6fbf1428b6d76d77a98c674b7311a7d006` | `c41c4a12f536971743ce7c80d2c4c24bda904191869e7c19b9b9bb90d6cbe6b6` |
| Following line original PNG | `65abe58f7fb09c3db3b187e2ddbb5f8eb73fc6566d8a4a9d2185075863963e51` | `621f5350a286c9b6bf7f2416dd677c1d85a38d3cfc362be2fe53bda2fd9fefb4` |

The crop bounds were `[0,350,640,130]` from the 640 × 480 macOS frame
and `[0,390,1074,154]` from the 1074 × 544 Windows frame. Neither was
upscaled. The rebuilt patcher reproduced the installed test DLLs
byte-for-byte on both platforms.
