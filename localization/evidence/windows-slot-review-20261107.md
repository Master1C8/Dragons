# Synthetic Windows slot labels visual review

On 2026-11-07 local time, an independently authorized gpt-6.1-terra reviewer (high) inspected one no-upscale WebP80 source-pixel crop of the Windows build running in an isolated CrossOver bottle. Original `localization/work/windows-slot-synthetic.png` SHA-256 `3c88ac6b7f6b2ba70b808220c327baeaa57ed0ed7df84c6db064691806fba572` was 2048 × 1592. Prepared crop `localization/work/windows-slot-review-20261106/slots.webp` SHA-256 `335a29c1d588f00bc89c6b72a62f097290bf423bc249436c22f52d4c4cbe9b6c` used bounds `(900, 770, 350, 400)` and retained native dimensions. Both hashes matched.

The three labels showed synthetic `ЪъЬь`; hard/soft signs and case were distinguishable, with no apparent clipping or overlap and visible padding. Part of the larger third slot panel lies outside the crop. The observation covers this test sample and viewport in CrossOver, not the whole frame, other strings, a smaller window, or native Windows.
