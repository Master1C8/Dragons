# Paired UI, settings and managed locale scope

The v41 shared inventory changes the roles of seven paired UI templates
and 152 per-build profiler occurrences. The other records and source
fields are identical to v40. Both v41 exports reproduced byte-for-byte.

## Runtime-populated templates

The serialized `slot1Progress` through `slot3Progress` references of
`MenuSlotsLoad` and `MenuSlotsNew` bind to the six audited `level0`
fields on each build. Each load-progress field is a descendant of the
associated button. `MenuSlotsLoad.OnShow` sets `{0} / 14` for positive
progress and hides the button otherwise. The three exact `0/14` strings
are numeric templates.

`MenuSlotsNew.OnShow` writes either the numeric format or the managed
`NEW` literal to every one of its three progress fields on the normal
paths. `Menu.Show` invokes that method synchronously before starting
its one-frame coroutine. The three `GreyedSlotSelect` source values
stay exact. The separate three `NewSlotSelect` labels remain locale
inputs, as does the managed `slot-new` value. The earlier
[background menu observation](slot-code-synthetic-20261107.md#managed-adapter-and-stock-new-game-check-2026-11-10)
confirmed both live sources in the New Game menu. It leaves occupied
states and pixel overlap open.

The pinned `OptionItem.text` field references the one `Option Text`
TMP template in `sharedassets1.assets` on each build. The two
`set_Option` instruction sequences match. Their setter uses the
localized Yarn option body, adding strike-through for an unavailable
option when configured. The stock options presenter invokes the
setter in the population loop. The prefab value stays exact while
the choice uses the Yarn locale. The combined verifier rejects
corruption of that object even when only a Yarn locale is supplied.

The previous managed audit already bound the profiler inputs to
118 ProfilerMarker constructors, 24 UISystemProfilerApi calls and ten
CanvasUpdateRegistry array entries. v41 records all 152 as exact.

## Known locale inputs

| Family | macOS required | Windows required | Exact per platform |
| --- | ---: | ---: | ---: |
| Serialized UI | 58 | 82 | 80 |
| Settings fields | 37 | 31 | 43 |
| Managed display phrases | 2 | 2 | See managed inventory |

The extra 24 Windows UI fields belong to six pause menus. macOS
adds two settings with a label and two options each. The settings
check includes the 42 exact serialized resolution entries and the
empty master-volume label. It preserves choice order and indices
through the existing builders. The two managed locale IDs are
`slot-new` and `yarn-missing-line`, represented by three and two
source literals per platform respectively.

`inventory_non_yarn_scope.py` checks all nine known UI assets,
the pinned settings objects and both full Managed manifests. It
reconciles the registered source IDs and generates a reproducible
scope. The optional complete-input check also requires all candidate
IDs and records each locale file SHA-256. Use platform folders
containing `ui/<asset>.json`, `settings.json`, `slot-new.json` and
`missing-line.json`. The UI folder contains only assets with
translation inputs.

```sh
"$PYTHON" localization/inventory_non_yarn_scope.py \
  --inventory localization/work/source-inventory-20261107/combined-provisional-v41-20261110.json \
  --macos-data "$macos_data" --windows-data "$windows_data" --output "$new_report"
```

Add `--locale ru --macos-inputs "$macos_locale_dir" --windows-inputs "$windows_locale_dir"`
for the completeness check. Both platforms passed with a structural
English passthrough control. Missing settings IDs and changed protected
templates were rejected. Editorial, visual and in-game checks of the
finished translation remain separate, as does the audit for additional
runtime text sources. All 192 project tests passed with the paired build
tools enabled.

## Local evidence

The audit output is in
`localization/work/ui-runtime-source-20261110.ZvHn5U/`.
The non-Yarn scope SHA-256 is
`a7f5900a4c09865abe44ddd96f6ad67d4c47be30c107a57c5d37c1d9637f6e3e`.
The complete-input control report SHA-256 is
`8dc7c55a8c6c5eb1b442eb99c41aac3cd4b040338b3d06f8b8f61624cb20da15`.

| Report | macOS SHA-256 | Windows SHA-256 |
| --- | --- | --- |
| Managed instruction dump | `7a968606960ee9ba04575569f3bed90893f9d20b3544d82757af6880abbd518b` | `d12c495f33298e43b489228ce09488d41ff4c0d9db50db6e83073b8fe8fb7841` |
| Serialized bindings | `dd32ce7974100c4b735bb49193881dd6bc99aff15a82e01231b981a8ca889343` | `d1f23b0f5ad3c106a822b171c9ca3e80309e50aaac2f94384b53cbba0bda7eab` |
