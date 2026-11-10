# Options visual diagnostic

Both runs reused the [paired settings inputs](european-text-paths-20261110.md)
under the `uk` test package. The Vietnamese, Polish and Ukrainian strings
are script controls. English labels and original artwork are expected
elsewhere in the frame. These are diagnostic frames for the Options
surface, separate from the final locale galleries.

The probes opened Options through the stock button, verified all three
active TMP strings, and rendered the existing Options root canvas through
the game's Main Camera to an offscreen target. The previous camera and
canvas state were restored after readback. This route keeps the game in
the background and can differ from the normal display surface. The two
players also selected different output resolutions. All 18 macOS and
32 CrossOver window and focus samples returned `0 0`. Both test players
exited, and the observers verified the original profiles.

| Frame | Layout | Glyphs and content | Contamination | RTL |
| --- | --- | --- | --- | --- |
| macOS, 640 × 480 | The three controls each fit on one line. No visible clipping of their text or overlap with adjacent controls. | The samples are present, with no visible replacement squares. At this size the Polish final accent and exact position of the Vietnamese acute are too small to certify. Needs source-pixel review. | No desktop or storefront overlays. | Not applicable |
| Windows through CrossOver, 1024 × 768 | The three labels fit on one line with padding. The partly visible Target Framerate row sits at the bottom scroll boundary, outside the three sample controls. | The Polish and Ukrainian samples are legible. The Vietnamese sample is legible as a phrase, but exact attachment of the acute to its intended letter remains needs-review. | No desktop or storefront overlays. | Not applicable |

Both originals were preserved. The full-frame review used WebP quality
80 at the original dimensions. The frame findings cover only this
offscreen Options control. Source-pixel follow-up and dialogue and
choice frames remain pending.

Local inputs and output are under
`localization/work/european-settings-visual-20261110.Q6lrkb/`.

| Artifact | SHA-256 |
| --- | --- |
| macOS PNG | `5bd4246f52ba2f130fcf898a215fee61cbe7a77047b0fc006e4006832e413bab` |
| macOS review WebP | `4b18be1826c0065393b623d6f8089b4dcec153d1a654a77191df4d045f458148` |
| Windows PNG | `df818128a32f6e40839d6fbdbc1fbf0821627e347d449f89b0f8c914ccd8e40b` |
| Windows review WebP | `17dfc63ad6df5e9ac8f04ebb703e90580bde3867bb5cf92cc3fbc0f56a0c1bd8` |
