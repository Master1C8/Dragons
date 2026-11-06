# Embedded input-action controls

Both pinned `Assembly-CSharp.dll` builds contain `InputSystem_Actions::.ctor`.
The first of its 28 string literals is an embedded input-action JSON document,
passed directly to `InputActionAsset.FromJson`. The remaining 27 literals are
passed directly to `FindActionMap` or `FindAction` with the observed boolean
argument. The source-bound `tools/input-action-source` tool verifies the exact
assembly and Mono.Cecil hashes, the immediate IL instruction sequences, and
that each referenced map or action exists in the corresponding embedded JSON.
Both versions contain three named maps and 24 named actions. Their JSON payloads
have different hashes and lengths, so retain each build's own exact bytes.

These 28 source occurrences per build are input configuration and lookup
identities. They must remain exact, even where a word such as `Pause` resembles
a visible label. They are separate from player-visible button hints, which
still need their own source and runtime classification. The decoded reports
`input-actions-macos-20261107.json` and `input-actions-windows-20261107.json`
are SHA-256 `6272020c5766750fe68af6c6601c8c70c6830bc47b9a558af9b20a124d2f6daf`
and `dd06623f942b4b5619a278f51ba7dc9c6de5845752d7776e4d06c7b86455a998`.
Their JSON payload hashes match the corresponding occurrences in the earlier
managed-string exports; the raw configuration is retained in the local source
inventory, not reproduced in this report.

The shared provisional inventory recipe now binds those 56 occurrences to the
source reports and labels them `preserve-exactly-input-control`; its current
v3 output SHA-256 is
`02fb2a7f8a309023a37d80f9e41d50e289feceef899fa6dd826d90ab523c6e41`.
This classification is an input to the future complete exact-preservation
contract, not a claim that a final installer validates these code paths. The
remaining managed literals and all other unclassified families stay open.

Focused positive tests verify both pinned assemblies, the 28 occurrences per
build and embedded JSON/action relationships; the wrong-build assembly is
rejected at the intended source guard. Assembler tests verify all 56 exact-role
bindings and preserve unrelated source counts. Static source inspection does
not establish actual input behavior, all dynamically loaded controls, other
assemblies, or runtime presentation.

Build `tools/input-action-source/input-action-source.csproj` with .NET 8 and
Mono.Cecil 0.11.6 into fresh work-local directories; run the resulting DLL as
`input-action-source macos|windows ORIGINAL_Assembly-CSharp.dll`. Recreate the
provisional inventory using the command in `provisional-source-union-20261107.md`
with a fresh output path, then run the corresponding focused tests.
