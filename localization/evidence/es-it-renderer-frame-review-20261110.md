# Spanish and Italian renderer frame review

2026-11-10. The separate, fresh review contexts inspected all 15 unresolved
full-frame images from the existing synthetic renderer runs. Each review
attempt used one or two WebP80 previews of one locale. Source PNGs remain
unchanged. An initial Spanish answer included rows outside its delivered
packet and the importer rejected it. The replacement queues explicitly
restricted results to delivered indices and imported every actual frame.
The translation CLI sessions retained GPT-6.1 Terra High. The isolated visual
queue pinned GPT-6.1 Sol High, as required by the workstation review runner.

## Spanish

All four dialogue and choice frames passed their visual checks on macOS and
Windows via CrossOver. The Windows Options frame shows all three expected
Spanish labels and their marks. It has a failed layout finding at the lower
viewport boundary where part of the stock-English `Target Framerate` label
is visible. The Spanish CLI is checking the stock scroll behavior and whether
the complete row can be reached. The current frame establishes neither the
cause nor a translation-specific layout defect.

The macOS Options layout passed, but two labels had unresolved fine marks.
Source-pixel crops from the unchanged 640×480 original also left the marks
in `Pingüino ¿qué?` and `Año, sí` unresolved. A new offscreen render at a
higher native render-target resolution is needed for those marks. Preserve
the original layout evidence and the separate logged 40-point body control.

## Italian

The four previously unread Windows CrossOver dialogue and choice frames
passed. The other four macOS dialogue and choice frames passed layout and
contamination checks, and their source-pixel crops resolved all four text
and mark uncertainties. Together with the two previously reviewed 64-point
body frames, this covers the 10 captured dialogue and choice surfaces.

The macOS Options layout passed. All three native pixel crops still leave
small accents unresolved. The Italian CLI is preparing a higher-resolution
offscreen capture of the same settings labels and renderer, with the same
layout and an isolated profile. The Polish probe used an actual 1920×1440
Unity render target successfully without a visible or focused window. It is
a proven route to adapt with the Spanish and Italian samples. See
[Polish renderer feasibility](../pl/CHECKPOINT.md#polish-renderer-feasibility-same-session-continuation) for its local evidence.

## Receipts

The queue directory is `localization/work/es-it-renderer-review-20261110.vDBLoY/`.
The source manifests bind the original files, scope and prior run receipts.
The crop manifests bind exact source hashes and native pixel bounds. These
checks concern the isolated early feasibility fixtures. Final translated
packages, native Windows and full-corpus visual acceptance are separate.

| Ledger relative to queue directory | SHA-256 |
| --- | --- |
| `es/packet-only-ledger.json` | `530904ac739c12cee97e4f7c4cfe082553b041e2c689075993186e1284be7bbb` |
| `es/accent-ledger.json` | `ab40c6dc9ecae06655e8c61a8f9a942de1156f5ee32eccc51b3fb31e17e5ac8d` |
| `it/packet-only-ledger.json` | `9228e0a7631033ad0d1cf8db441d7edffdddadde0fbb4d9f38330ec239b968c4` |
| `it/accent-ledger.json` | `2eb36aa59201ea4d8edc9c161630bea8d9a8b503be7946f246a9c0028a447e94` |
| `it/settings-accent-ledger.json` | `2b37a3889a4cdde1a93e8cbb39b32fe59eb86120d0f442e235a86447b427c06c` |
