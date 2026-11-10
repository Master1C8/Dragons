# Italian renderer: pending visual review handoff

2026-11-10. Text-only handoff; no visual judgment was made in this resume. Windows captures are CrossOver. All paths below are absolute. Reviewed `body-uk` frames remain accepted only for the bounded observation documented in `renderer-probe-resume.md`.

Originals and previews below were rehashed against their manifests, and their decoded dimensions were checked without rendering them into model context. WebPs are recorded as quality 80 by the producing helper manifest; no visual pass follows from metadata. For each frame, inspect the entire preview in an authorized fresh bounded context; record glyphs, accent marks, clipping, overlap, fit and uncertainty. Use no more than two prepared images per context. If a mark is ambiguous, crop only the relevant original using the canonical helper and record source hash and exact bounds. Do not overwrite originals or previews.

| Platform / pending frame | Original SHA-256 | Preview SHA-256 | Dimensions |
| --- | --- | --- | --- |
| macOS `body-vi.png` | `59d3604e0ec5687577508a3eb1588a7ace55ed8350ee593e92d057dd88765d95` | `8583f749cc35e259ace939464ffcd7982ddc2a708deb20555f195ed424a83cad` | 640 × 480 |
| macOS `line_0b7589ff.png` | `1f5c7ecdb06c47dd0a6396437fb6bfc58e5d155be8f67a6da144f08a47c26829` | `aa053893002d89b51c13dfb83de5a75f52cd866e96269b09a6cd745b2646cbc7` | 640 × 480 |
| macOS `line_4d692a01.png` | `0dd544a7a6149af221958218cb54fac9e7146a4ca3ad1dc0ad44a2f19b3173ae` | `e3a5a9c817982b8dbf4c507e63eb62bd8f8eed1857d308f210b352e67aaffdd8` | 640 × 480 |
| macOS `line_83ac5b68.png` | `96ff472fb3d87aa039f17d19504073ec2ea0d13f71634c92866919d9d99c8f26` | `50ddebd4a743bea814144401510b311e4312a1621ee6ba50d6cc1409f806add9` | 640 × 480 |
| Windows CrossOver `body-vi.png` | `129195a7603e5b5d3c0a83dd37eb187189a1686bcbd603443db7ef386b2827eb` | `102c2fa810de4c9286895190860190c78e8e808937ab665245e180601006e5a0` | 1074 × 543 |
| Windows CrossOver `line_0b7589ff.png` | `bcaef7ef6d52e55026f1842bd7d86ce75034fbdfb13513f9068c1b081f763eee` | `3bbd579b11de42ce71ee0c32251f164e8115ad0e758e59844a5bbb89118cfa62` | 1074 × 543 |
| Windows CrossOver `line_4d692a01.png` | `6189bccc92d54e33375a7e6da7d05ae99c706260b15beda1fcc9774707f8e4ed` | `e4e0eda3dc52c72b350b98d87a9cf02733fbe4af993b79832ef6e92fe1f82348` | 1074 × 543 |
| Windows CrossOver `line_83ac5b68.png` | `8608707e434e8289a26e4c7b1a8ca6d3a239bdb8187059fdfbbe82550509f144` | `94f6474dd2f09f23ac70d4b9446e7160a05c77861f7d29b582a7512d9ed8b219` | 1074 × 543 |

The original and same-basename WebP files for each row are in:

- macOS: `/Users/antonkrutov/Desktop/Dragons/localization/work/cli-terra-high-20261110.J0KLrx/it/resume-01/probe/visual-mac/run/frames`
- Windows CrossOver: `/Users/antonkrutov/Desktop/Dragons/localization/work/cli-terra-high-20261110.J0KLrx/it/resume-01/probe/visual-win/frames`

The hash-bound source-to-preview manifest files are `previews.jsonl` in each directory. Their SHA-256 values are macOS `20d003271a3e8c54e68cd06c5024070c48bcc7d8eaf26879126a1e1c4c6fe515` and Windows CrossOver `0276b3f7c24263266211090ed6e8f89639a6bb0bc8870427ddb7e692f5407e2c`. These hashes are provenance checks, not a claim of a cryptographic signature.

## macOS settings accent

- Original: `/Users/antonkrutov/Desktop/Dragons/localization/work/cli-terra-high-20261110.J0KLrx/it/resume-01/probe/settings-mac/run/options.png` SHA-256 `0be46f74cc1ba9fb6d524b5d2b07cfd454de4db9e7b0ec9d289712819f945156`, dimensions (640, 480).
- Existing preview: `/Users/antonkrutov/Desktop/Dragons/localization/work/cli-terra-high-20261110.J0KLrx/it/resume-01/probe/settings-mac/run/options.webp` SHA-256 `f6d2b3a1f39ba54e7a409b1acb220e338897e33f92651401d9d240b50af69fcf`, dimensions (640, 480).
- The prior full-frame observation found the synthetic labels on one line but could not resolve small accent placement. In a fresh authorized visual context, identify the precise source-pixel rectangle first, then run the helper below with actual integer bounds and a new task-owned output. Do not guess coordinates or infer a pass from glyph metrics.

```sh
python3 -B ~/.codex/tools/screenshot_preview.py '/Users/antonkrutov/Desktop/Dragons/localization/work/cli-terra-high-20261110.J0KLrx/it/resume-01/probe/settings-mac/run/options.png' --crop X Y WIDTH HEIGHT --output 'localization/work/cli-terra-high-20261110.J0KLrx/it/resume-03/settings-accent-crop.webp'
```

Capture provenance, prior tests and all other limitations are in `localization/it/renderer-probe-resume.md`. A crop is a supplemental mark check, not a substitute for frame review.
