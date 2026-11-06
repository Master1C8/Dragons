# Synthetic hard/soft-sign crop review — 2026-11-06

Independent reviewer: `glyph_crop_review`, actual model `gpt-6.1-terra`, high reasoning; owner separately authorized these exact two source-bound crops. The reviewer checked source/preview hashes, read the crops independently before comparing the expected synthetic sequences, and did not launch the game or inspect any additional images. Crops were produced by `python3 -B ~/.codex/tools/screenshot_preview.py` from the originals at source pixel scale, WebP80, without upscaling. Full-frame observations are recorded separately in `glyph-probe-review-20261106.md`.

| Source and SHA-256 | Crop bounds and preview SHA-256 | Observation | Status |
| --- | --- | --- | --- |
| `work/glyph-dialogue-screen.png` `32eaf5df36e793d98e408e007e0e8c80c32785bf044ec316ced73ff40fec79b4` | `(175, 735, 680, 44)`; `glyph-review-20261106/dialogue-crop.webp` `83e6bbb9dee35a4c65d461f8e2726aaecab261d6edc041e9a81f0183bab3d7c8` | Reviewer read the expected synthetic sequence `Ёё Жж Ъъ Ьь Щщ Ыы Ээ`; uppercase and lowercase hard/soft signs appeared distinguishable, with no apparent clipped strokes. | pass for these glyphs in this exact dialogue crop, not the completed corpus or all layouts. |
| `work/glyph-option-screen.png` `75bbad4b90dae1c9842a6f12dfcad89319f82a232f29250321fa6b7e3f6e42ed` | `(690, 465, 130, 40)`; `glyph-review-20261106/option-crop.webp` `9df57366bc8fe2298db7334c95ffb6ab6cca6e3ed9a45f770d0f8be7c48090f7` | Reviewer read the expected sample `Жж Ъъ Ьь 427`; uppercase signs appeared distinguishable and the text appeared contained, but the lowercase pair was too small to distinguish confidently at native pixels. | needs-review for lowercase hard/soft sign readability in this narrow role. |

The observations apply only to these synthetic, instrumented builds and frames. They do not prove full alphabet/corpus coverage, settings scroll behavior, normal input, saved settings, translation correctness or release readiness.
