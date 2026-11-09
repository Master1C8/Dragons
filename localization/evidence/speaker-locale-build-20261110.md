# Paired Yarn speaker locale build

The player adapter translates display names for the 18 protected Yarn line
IDs with a `Ryan: ` or `Conrad: ` prefix. The original line, ID, raw
text, character annotation and body remain unchanged. The presenter gets a
separate display view. Both the separate-name and inline branches require
the expected ID, source name and prefix, with the existing name-suppression
branches intact. The speaker locale can share a build with the two missing-line
literal changes in the same Yarn DLL.

The .NET test loaded the actual original core and patched Unity assemblies
from both platforms. It executed both display helpers for all 18 source IDs,
two marked-body cases and eight fallback cases. It checked the name in the
separate field, inline annotation and attribute ranges, the original line
after both operations, and the raw and parsed missing-line values.
The fallback cases cover an unknown ID, a mismatched name or raw prefix,
overlapping markup, an ordinary line, an unknown speaker, a title and the
colon-ended Alexander sentence. The ordinary Yarn locale reader also rejects
added whitespace in the audited source prefixes before writing assets.

The macOS builder signed an isolated `S9A1` app with two synthetic dialogue
values, all five transition repairs, the speaker adapter, a missing-line
replacement and the managed new-slot label. Strict signature and full Managed
inventory verification succeeded. The Windows check prepared both DLLs from
its pinned Yarn source. A fresh build of the patcher reproduced the exact DLL
bytes on both platforms, including the bytes inside the signed macOS app.
The legacy probe modes also reproduced their previous DLL digests and receipt
fields.

| Platform | Rebuilt Yarn Unity SHA-256 | Runtime companion SHA-256 |
| --- | --- | --- |
| macOS | `097e29ae3be42fd0a00aa6daaf67b671e6e3d8215c33af48810bac2e5442a6b5` | `bea6639af43f94085f20d6f5a9f22fdd148741de5215a3e1892b759a6e4f907d` |
| Windows | `9a45e2f382d0108dc8988557c68d4c884d50792d0efada6becb3aa81eb506ac5` | `97296354519d1270e4ef3de26c2f322374d5e906dd280d980104f792312cac44` |

Inputs and receipts are in `localization/work/speaker-locale-20261110.jgtHXC/`.
The macOS build log SHA-256 is
`3ad4bf875c011da9d32c4b5a3602ea0174784757805116b7ec1b61e14e698be8`.
The Windows preparation receipt SHA-256 is
`016b57c3c978d5979e7e7ce0841fff6a05ebddd6679aaeeacab0061f9c81f2cb`.
The rebuilt-tool test environment and suite log are in
`localization/work/speaker-locale-final-20261110.osxldd/`.
All 187 tests passed with both paired build tools enabled.

The display values in these builds are artificial. The newly built macOS
app and Windows DLL pair still need Unity runtime verification, readable
in-game frames and progression checks. The Alexander exception remains
preserved and unresolved. Windows package integration and approved Russian
name wording remain open.
