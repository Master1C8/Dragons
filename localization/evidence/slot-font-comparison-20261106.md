# Synthetic slot font-size comparison

Two authorized independent gpt-6.1-terra reviewers (high) assessed a five-character synthetic label `ЖжЪъЬ` on 2026-11-06. One compared full 1024 × 824 WebP80 previews; a separate reviewer compared only source-pixel crops. No representation was upscaled, and all originals and previews were hash verified.

| State | Original SHA-256 | Full preview SHA-256 | Slot 1 crop SHA-256 |
| --- | --- | --- | --- |
| Original font size 20 | `e578cba01b421215e06a659073c5456e4fca6d8e408c7e8e1c750419a432a7db` | `17e253d8b26ea850063ea41c28081ce241266491adc5b7f1787e3981b62577af` | `48747dd72216fc4342f401f3d2c94abc875ab234f2efd0b35ec1f27a19771052` |
| Test-only font size 18 | `1527423fbc1534f204f755ad507e4c0c302c71c5130d1bab5a47ac5717a4a2d2` | `639997ecdb6f3292ac16d2d5b7aa8e3fbcd34f030a256f855dcd3cd2e99b82bc` | `f6c6eab80ad4edae340dc8889fd20baff2ee753894321b0cc541e49448e28a2b` |

Both crops use source bounds `(520, 410, 110, 55)`. Full-frame review found the reduced version had more right-side room without apparent wrapping or collision, while remaining a small readable label. The crop reviewer found both five-character runs apparently contained and the reduced version better separated from the right border. Both reviewers could not confidently distinguish all hard/soft-sign details and case at this size. Consequently exact glyph identity and pixel-level clipping remain needs-review, and the test-only candidate is not accepted as a final font or release change. These observations cover this single synthetic sample only.
