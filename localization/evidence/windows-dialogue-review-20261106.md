# Synthetic Windows dialogue and choices visual review

On 2026-11-06 an independently authorized gpt-6.1-terra reviewer (high) examined two WebP80 previews from the Windows build in an isolated CrossOver bottle. The 2048 × 1592 originals were reduced to 1280 × 995 without upscaling. Original and prepared hashes were independently verified.

| Frame | Original SHA-256 | Preview SHA-256 |
| --- | --- | --- |
| Dialogue | `56cfe7d100f6cc33289414a2719e14886348bf8301ad7f38c0c4d9d5c90c4b80` | `1a3297b79d3282af87e747183566a524990d9fe0b7491b853a4c2a3c1c7d21c5` |
| Choices | `da25c56517e3c763ccc123c1dc9af4c73dae4274549984e1d6a346e2b7b4ebc3` | `1909a181fbba986a9e5d6b3b0d18ab9b18127e4cf9fea1d4ab36684564fc3cab` |

The observed dialogue was `Ёё Жж Ъъ Ьь Щщ Ыы Ээ 'Drag'n'wash franchise 223'... 123`; the choices appeared as `Жж Ъъ Ьь 431` and `Юю Яя 632`. These visible letters and digits match the synthetic locale file; exact small punctuation near the closing quote remains uncertain. The reviewer found the visible glyphs readable and contained without obvious missing-glyph boxes, overlap or clipping; the second choice was gray but legible. The title bar is present in both captures. Neither frame tests multiline wrapping or establishes source fidelity for translated content, natural dialogue entry, branch behavior or game-wide coverage. The runtime and input trace is separately recorded in `HANDOFF.md`.
