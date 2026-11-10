# Additive Japanese fallback control

This control uses the same pinned Japanese Noto Sans CJK face,
representative sample, 1,536-character pressure set and Unity players
as the [CJK atlas test](cjk-fallback-runtime-20261110.md).

The test assets append four objects to `sharedassets0.assets`: a
source Font, SDF material, empty 1 × 1 atlas seed, and dynamic TMP
fallback. The original primary's fallback list changes from one
reference to two, with Liberation Sans first. A read-back compared
the bytes of every pre-existing serialized object. All 686 other
macOS objects and 681 Windows objects remained exact, including the
existing source font, fallback, material and all original textures.

The original stock menu loaded in each isolated test copy. The
probe read all Japanese glyph IDs from the live slot label and
matched them against the pinned face. The `ABC` control used the
stock primary and `ЇЄҐ` used the stock dynamic fallback. All 1,536
additional Japanese test characters fit into 16 atlas pages on
both players.

The initial test read the new atlas width as 1024 but the material's
`_TextureWidth` and `_TextureHeight` still carried 512. A second paired
run changed only those two properties in the new material. Both
players then reported 1024 for the atlas and shader width, with
identical glyph and page results. The repeat changed no original
objects. A future adapter must set the atlas dimensions, free
rectangle and both shader size values together.

The macOS and CrossOver runs remained in the background. The
observers verified original profiles and recorded test-player exit.
This verifies the additive object chain, face choice and pressure
set. Pixel appearance, CJK line breaking, other regions in the
additive setup, and complete-package integration remain unverified.

Recipes, assets and logs are under
`localization/work/cjk-append-20261110.9tdhZe/`.

| Artifact | SHA-256 |
| --- | --- |
| Append and original-object receipt | `375c729c61da667165b37e27e93b3aab97c12f8d3bcffec3f325465afc1be669` |
| Glyph checks across both versions | `f6db94bc82db9c1f73ec51bbe4c289c0a0ae5aed6031e33bae36467735c7f263` |
| Aligned macOS Unity log | `2bff5c71b73b2f63689f7254d0512a98d17d07415cc1d67f1bd1b94e970df96d` |
| Aligned Windows Unity log | `04fc79af6624b34cf289eb0e2fcecdef93a6a1de643cb6b83c2c06647b405d87` |
