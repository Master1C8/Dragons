# Synthetic choice and continuation visual review

On 2026-11-06 an independent reviewer using gpt-6.1-terra (high) inspected exactly two prepared 1024 × 824 WebP80 previews, with no upscaling. All original and preview hashes below were independently verified. The reviewer saw synthetic probe text and did not receive expected strings in advance.

| Frame | Original SHA-256 | Prepared WebP SHA-256 | Observed |
| --- | --- | --- | --- |
| `localization/work/choice-probe-screen.png` | `559b90aa6a02c05dce32a8fa35d2af6ee23df79be1c1f30554c3c77381c82682` | `37851dec8027ecfa439faf577c6ebbf1140dd861810d963f65d0c0c0f786be6f` | `Жж Ъъ Ьь 431`, `Юю Яя 632` |
| `localization/work/choice-trace-probe-screen.png` | `dcf9e9d96b3785c94396b332daf3ef3315e2305f723c9045a9cab1e5c9cddb00` | `e2f42fa1081ec0f3bde951bad08fdd335fe77959f44ec78898fb48d91ab88dc9` | `ЖЮЯ 741` |

The reviewer found the visible strings readable and contained within their panels, without apparent clipping, overlap, missing glyphs or broken spacing. The second option appeared gray but legible. The coordinator compared the observed strings with the synthetic locale values; they match. These observations apply only to these two images and strings. The separate instrumented branch trace establishes the selected programmatic branch, not normal player input; longer strings, other screens, final font coverage and game-wide visual quality remain unverified.
