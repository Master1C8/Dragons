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
is visible. Source-matched stock and Spanish CrossOver tests both reproduced
that initial masked viewport state, then scrolled the real control to move
the row fully inside the viewport. The two new after-scroll frames visibly
show the entire label and its control. Both passed. The initial partial row
is stock scrolling behavior and the Spanish layout finding is resolved.

The macOS Options layout passed, but the 640×480 frame and its source-pixel
crops left marks in `Pingüino ¿qué?` and `Año, sí` unresolved. A new genuine
1280×960 Unity offscreen render preserved the same three Spanish labels and
passed layout. Its source-pixel crop verified `Año, sí`. A second, wider
crop verified the complete `Pingüino ¿qué?`, including the beginning omitted
by the first crop and all required marks. The initial layout and these
targeted checks close the bounded Spanish renderer findings. Both new
40-point dialogue frames also pass punctuation, accents and fit on macOS and
CrossOver, independently of the already reviewed 64-point control.

## Italian

The four previously unread Windows CrossOver dialogue and choice frames
passed. The other four macOS dialogue and choice frames passed layout and
contamination checks, and their source-pixel crops resolved all four text
and mark uncertainties. Together with the two previously reviewed 64-point
body frames, this covers the 10 captured dialogue and choice surfaces.

The macOS Options layout passed. The three native pixel crops left small
accents unresolved. The Italian CLI captured the same settings labels in a
new 1280×960 Unity offscreen render from the existing 640×480 batch-mode
screen. The independent review verified all three labels, required marks,
punctuation and fit. This closes the bounded Italian renderer finding and
retains the earlier layout observation. The Polish probe used the same
approach with a 1920×1440 render target and a hidden window. See
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
| `es/scroll-ledger.json` | `a119b2ba91d630df459f5e38c726fc02a87eb0bcb4027110f2d61c093d9c13da` |
| `es/body40-ledger.json` | `c7cec02c5827e31bf303826536348c0dcf7de8424d07ee769cf4bede7610d071` |
| `it/high-options-ledger.json` | `de5c37ff2b191b3d0b88b92de5813dc8dced28ccd917415b979dfb3496e14bd4` |
| `es/high-options-ledger.json` | `bc872cc9c2bc0f5c398dd09fa1fc62a95cccb8b41fcbee9af2b0980beca598ef` |
| `es/high-accent-ledger.json` | `290072c026c1a9e1bca7d9c39db85af1a875a66d5413e0911785af0461d1cb24` |
| `es/pinguino-wide-ledger.json` | `d4256de0b8ec2aa189ccd1f088c33f505e770d02febf86cd60d0c9ef737d1ee6` |
