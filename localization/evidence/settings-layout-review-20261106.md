# Synthetic settings caption comparison — 2026-11-06

Independent reviewer: `layout_comparison`, actual model `gpt-6.1-terra`, high reasoning. The owner explicitly approved this two-frame comparison. Both original frames and prepared WebP80 previews were hash-verified and are 1024×824 without upscaling. They show the same synthetic selected option and viewport in separate instrumented isolated test copies; their shared `sharedassets0.assets` differs only in `RectTransform#478` vertical size delta, from −13 to −3. Original and changed assets SHA-256 `96e3f29e601a64f575be6ee60e706eabd8afb47f6b2c6803116a773518ae52fd` and `a06067fa117624a04a5ccb4b2bbfb912d9f0a63ac543f730c2be974acf52ffdf`. They use the same test-only managed assemblies. The original app and saves were not altered.

| Frame | Original SHA-256 | WebP80 preview SHA-256 | Findings |
| --- | --- | --- | --- |
| `work/glyph-option-screen.png` | `75bbad4b90dae1c9842a6f12dfcad89319f82a232f29250321fa6b7e3f6e42ed` | `79381d16b5441e4dec7b169828741dce7b23fa53c44e9c22fb05db35e9c2f208` | Text fit without visible overlap, but the small hard/soft sign shapes could not be reliably distinguished. |
| `work/glyph-option-layout-screen.png` | `0bc2d174a4f4352c06515b53fb928e6955875aee79aebf03fb204e3d8caafd95` | `0fcb980b634d57696913826a3f6be6cffbce8c5a81f6f1b1a0d6a4b2842b3ac6` | The reviewer independently read the synthetic value `Жж Ъъ Ьь 427`; the hard/soft signs were distinguishable. Text fit without evident overlap. Other displayed dropdown values also grew, while row positions and visible control bounds appeared unchanged. |

The following settings control was partially cut by the bottom scroll viewport in both frames. Its appearance when scrolled is not established. This is acceptance only of the compared synthetic sample, not all glyphs, long options, scroll behavior, normal input or a release. The candidate remains test-only until those checks pass.
