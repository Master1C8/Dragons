# v42 locale workload and current draft coverage

The audit loads the pinned shared inventory and paired Yarn scope
and verifies both installed source builds. It uses the package's
known non-Yarn scope checker and the exact source-role contract.
Both tracked Russian files pass the ordinary Yarn locale reader
against their own pinned source table.

| Package input | macOS IDs | Windows IDs | macOS English words | Windows English words |
| --- | ---: | ---: | ---: | ---: |
| Ordinary Yarn | 1,823 | 1,823 | 10,111 | 10,107 |
| Alexander display body | 1 | 1 | 9 | 9 |
| Speaker labels | 2 | 2 | 2 | 2 |
| Serialized UI | 58 | 82 | 156 | 186 |
| Settings | 37 | 31 | 54 | 44 |
| Managed display phrases | 2 | 2 | 4 | 4 |
| Total | 1,923 | 1,941 | 10,336 | 10,352 |

These are package input IDs and source words per build. The word
count ignores markup, placeholders and standalone numerals.
Exact-text repetitions are retained by ID. The ordinary Yarn
sets contain 1,594 distinct exact strings on macOS and 1,593 on
Windows, with context-distinct uses kept separate.

The union contains 1,947 input IDs. The 1,917 shared IDs include
1,892 with identical English source and 25 differing Yarn values.
Those 25 require each platform's exact `source` in the locale file.
The six macOS-only inputs are settings fields. The 24 Windows-only
inputs are serialized pause-menu fields. The two managed input
IDs represent five literal occurrences per build.

The source role check identifies 12,757 exact-value occurrences
on macOS and 12,692 on Windows, including the Alexander table value
whose display body is translated separately. Another 18 ordinary
Yarn entries per build have an exact speaker prefix and a display
body. These are inventory counts. Candidate preservation is
verified by the existing artifact checks.

The tracked locale inputs supply the same 15 Yarn IDs and the
same Russian texts on both platforms. Fourteen are changed text,
and `line:7426a997` is unchanged punctuation. There are 1,808
missing ordinary Yarn inputs on each platform. Across the
complete package input scope, 1,908 macOS and 1,926 Windows
inputs are absent from the tracked drafts. None of the 15
is counted as accepted in the current editorial process.

Both `line:a99c515c` and `line:4183ca7e` use the superseded
«Франшиза Drag'n Wash № 223» wording. The current SiteForMods
Russian glossary uses «Филиал № 223 сети Drag'N Wash». These
two draft lines need the same terminology correction and
review with their phone-scene dependencies. The audit leaves
both historical drafts intact. The anonymous roster decision
and the special-scene editorial gates remain open.

The two audit runs reproduced byte-for-byte. Scratch artifacts
are under `localization/work/locale-workload-v42-20261110.yWvbM2/`.

| Input or report | SHA-256 |
| --- | --- |
| Shared inventory | `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d` |
| Paired Yarn scope | `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30` |
| Current compact Russian glossary | `20af03f9c319deaad522827173654c9b5dc1564d2272f8937a16185796c1749b` |
| Tracked macOS draft | `04c367fac3a38afb50c4ab373ccde797fb0113e9f7a090e49d65182f831370d2` |
| Tracked Windows draft | `4b0f4adcef2e50522112e5c9d32aeacde611643b365097d3005009b115ca5318` |
| Audit script | `d530cc5f07b614cd4b7fffbfe86bfd447a8e13341a47bd5915f2e1fb3d832fed` |
| Workload report | `bb103681be80b5d598a820d7fa0d08da1da675cc61993283e4ce450e5ee15a9e` |

## Paired authoring worklist

The [export command](../README.md#paired-text-authoring-worklist)
binds the workload to the actual package file and input key for each
build. It rechecks both source builds with the existing Yarn and
non-Yarn readers, uses the pinned v42 inventory and Yarn scope, and
rebuilds the 27-case special-scene index. Each of the 25 changed
English values retains both platform sources. The six macOS-only and
24 Windows-only rows have one destination each. The 15 existing
drafts per build remain separate from acceptance. The Alexander
display body points to `speakers.json` and the exact-only Yarn markers
stay outside the authoring rows.

Two exports were byte-identical. A structural control reconstituted
12 locale files per platform using only the worklist, with existing
draft values where present and English passthrough elsewhere. The
normal complete-package input validator accepted all 1,923 macOS and
1,941 Windows inputs. Substituting the macOS source for Windows
`line:a99c515c` failed at that line's source check. Removing the
Windows-only `level1#3862` failed at the required UI-field check.
These controls exercise routing, coverage and exact source binding.
All 19 targeted scope, index and dialogue-reader tests passed.
The controls did not produce game builds or new Russian wording.

The worklist and controls are under
`localization/work/authoring-worklist-20261110.NQgxrM/`.
The verified worklist SHA-256 is
`9e44119b0edc8fc272b08d89de6c30c7f51db571b9645c94979e5a0f67756038`.
