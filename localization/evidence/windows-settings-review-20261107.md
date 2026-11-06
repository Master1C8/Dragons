# Synthetic Windows settings visual review

On 2026-11-07 local time, an independently authorized gpt-6.1-terra reviewer (high) inspected two prepared views from an isolated CrossOver run:

- Full settings frame original `windows-settings-afterwait.png` SHA-256 `bb8c196a0abe67a5aa4cce06919f35cddb742b97e61005f60710afb7ab5b71e4`; WebP80 preview `options.webp` SHA-256 `9b7b4deddbca47756ead94d3eba4bdc6f3703b68143a58033c27754e67a5f098`, reduced from 2048 × 1592 to 1280 × 995.
- Expanded-dropdown original `windows-settings-dropdown.png` SHA-256 `840d20af0fe75e502f868746c71b9fd5171329c50f323334d11a372d10c0c09d`; WebP80 source-pixel crop `dropdown-crop.webp` SHA-256 `d33338c710db3f8de4f075f712ae06935898dd4f5b280556b168652e3cd17275`, bounds `(1380, 1100, 340, 220)`, no upscaling. Both prepared files are under `localization/work/windows-settings-review-20261107/`.

All hashes matched. The synthetic label `ЖЮЯ 427` appeared legible and aligned with its dropdown without obvious collision or clipping. The crop showed `Off` and Cyrillic-like value text ending in `431`, but the reviewer could not verify every sign and its case against intended `ЪъЬь 431`. Visible text did not overlap or clip vertically; horizontal control edges were outside the crop. The bottom settings row was partly outside the viewport with a scrollbar indicating more content, so that single frame does not establish a defect. Persistence evidence is separate in `HANDOFF.md`. These observations do not establish all settings or native Windows behavior.
