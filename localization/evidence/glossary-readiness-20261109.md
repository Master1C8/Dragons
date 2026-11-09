# English and Russian glossary readiness

The repository-owned Drag'N Wash glossary was checked for standard localization
against SiteForMods commit `65b5e0bf4d153e3dfe2ea721e8b59622fc56e562` and the
pinned macOS and Windows source exports. The findings below supersede any
assumption that the older receipts alone close the current glossary gate.

## Input and review bindings

| Item | Verified value |
| --- | --- |
| Raw English file SHA-256 | `245b734e32bc70760e884ae16505e08c6571e5120c7053255fc7435d7905ac4d` |
| Parsed English source SHA-256 from the CLI | `46a5fe93eb5d32fcd1591815f1d5f64ed29f65c5df83f5cbfc75da72a25b97ce` |
| Compact Russian map SHA-256 | `00560fed9bdc23ca10cc7a231c91f65f124ae7781ec6ce0a64f8067c6261234f` |
| Russian per-entry receipt SHA-256 | `70f8db414baa1d2ce341dc890e7afe95b9b1c34b9b88461c618c190573849f68` |
| Source research SHA-256 | `1ab766854e9b70f876374c91c95bce82b194091653c05e22556984f2399d6f07` |
| Review protocol SHA-256 | `5319d645d57ec7abc0c2b136d42ce4d2b14ce1e7f2e64a621bc64d62d63ef03a` |

`./vnrevival glossary work dragn-wash ru` and `./vnrevival glossary check`
confirmed 27 English and 27 Russian entries in identical ID order, with zero
missing, extra, or empty entries. The player remains first. The compact English
reference measures 783 tokens and the raw JSON 1,504, using `js-tiktoken`
1.0.21 and `o200k_base`. Both sizes match the earlier recorded version.

Both historical Russian self-review layers point to the same immutable entry
index. Recomputing each full English entry and Russian term/meaning digest
with recursively sorted keys, compact JSON, UTF-8 literals and no trailing
newline matched all 54 recorded hashes. The complete Russian map digest uses
the stored key order with compact UTF-8 JSON and no trailing newline. A changed
Russian meaning failed at its field digest and omission of the first receipt
failed at the ordered-ID check. Both source and Russian receipts describe two
author readings. Their identity is verified, and any superseding finding
requires new editorial evidence for its affected scope.

## Evidence from both builds

All 58 unique Yarn IDs cited in `glossary-sources.md` are present in both
platform columns of the paired export (SHA-256
`52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995`).
Four cited lines differ, concerning the franchise phone greeting, brand
capitalization and a contraction in a question about equipment. These
differences leave the cited concepts intact. The paired evidence confirms the
existing player, Max and Igwyx distinctions. In particular, Max is the
antecedent of singular `them` in `RyanMuddy_Idle4`, while the girlfriend
mentioned in `Ryan_2_Outro` remains a separate unresolved reference.

The level configuration exports bind both phone scenes to the `phoneDialog`
field on both builds. Their shared closing formula is consistent with a
franchise role. The second call says “we,” which establishes the caller's
wording and leaves the count and identity of individual callers unresolved.
The existing neutral strategy still applies. The five generic `Dragon…`
dialogue nodes have source lines, but their exact node names do not appear in
the 15 scanned level configurations or as literals in either pinned
`Assembly-CSharp.dll` export. None is a target in the 89 named Yarn transfers
per build in the pinned transfer report (SHA-256
`9cd529422340084c5dda98865ad485930d8a92fb6790c77c9a7c2e66a70068e4`).
Their speaker and reachability still need evidence from other entry paths
or runtime. `Start` contains test dialogue, and
`ErrorHasOccurred` contains a diagnostic voice. Keep these distinct from the
named cast while completing the player-facing scope and roster.

The later [game component scan](game-component-strings-20261109.md)
found seven serialized bark references to `DragonColdBalls` in each build.
The [roster follow-up](glossary-roster-followup-20261110.md) traces all
14 exact components to Ryan's GameObjects and confirms that the historical
source-reading receipts cover the complete v41 Yarn set. The other four
generic nodes still lack a verified caller, and runtime presentation
remains open.

## Open editorial findings

- `dnw-franchise-representative` changes the referent in Russian. The English
  meaning denotes the caller or callers. The Russian sentence begins
  “Обращение за кадром” and denotes their communication. The follow-up
  records the proposed neutral role label **Голос франшизы**, the numbered
  location correction **Филиал № 223 сети Drag'N Wash**, and evidence from
  both phone scenes. Canonical integration and the affected editorial
  reviews are still pending.
- The historical glossary proof predates complete shared-source coverage.
  Reconcile the glossary selection and speaking roster against the final
  source inventory before claiming a standard-localization pass. Preserve
  the recorded owner address decisions. The paired evidence reviewed here
  adds no established third-person pronoun for Alexander.
- Conrad's in-scene `big C` nickname depends on his Russian name. The existing
  case binds the self-introduction and the player's two responses
  (`line:0e1fd4b0`, `line:982fd3c7`, `line:255362b9`). The owner chose
  «Большой К» in the [roster follow-up](glossary-roster-followup-20261110.md).
  The complete Russian group still requires special-scene review.

This check is local. Production mirror parity and independent editorial
coverage were not verified. The glossary remains `needs-review`.
