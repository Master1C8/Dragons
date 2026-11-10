# Spanish author dependency closure

This is the author's source-bound dependency handoff for the 61 effective corrections from `df91415` to the Spanish wording at `62a16bd`. It is not independent acceptance. The Spanish translation is unchanged by this handoff. The author review, independent game-text audit, final package validation and final runtime/visual QA are separate states; the latter three remain pending.

## Binding and decisions

- Baseline Spanish JSON SHA-256 `20fc3d75786f81c311f64b5fbd0038c5fda553a77df09864cf799d77051158cf`; reviewed JSON `756de516739d6554b56695eb91624f00d751e2bbc9e8f1f1c190a954c964ef6c`. The authoritative [effective delta](semantic-effective-delta.json) is `95b1ddcbdeb3715360bb075f6541e638186f199dfeabdc8cdbad961c72d1f807` and its ordered 61 IDs match this export exactly.
- [Recipe](editorial-delta-recipe.json) SHA-256 `c613249c8283a1a19a227e75b4b8d23446a3830dcb2baf9d75e5e08d5df051db`. Its per-edit source spans are inclusive **display-instruction** boundaries; a span retains intervening displayed branches when both alternatives belong to the exchange. The recipe explicitly enumerates source IDs for related terms and runtime paths; exact repetitions and the mandatory regression catalog are added by the exporter.
- Immutable v42 source inventory `79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d`; Yarn scope `753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30`; paired scenes `52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995`. The previously accepted Spanish glossary self-review binds locale layer `3ddb6805226140429659f75367979afb69e06c55955dbe09c41a7b04bc3cf5cd`; see [glossary review](glossary-review.md) for evidence and limits.
- Igwix/Igwyx are both stock spellings of the phoenix, supported by the resurrection and self-immolation references; the alchemist is not assumed to be the phoenix. College and crest references include the school's actual name and Alexander's ornamental family crest. The player-directed kobold references include related inflections and distinct character addresses; the mount is a game device; the repeated “out of your scales” expression is compared as an idiom. The two phone branches have different questions and different stock apostrophe spelling for franchise 223.
- In `Conrad_SexScene_Cum`, wait/ready choices go to instructions 14/25, and not-yet/release choices to 41/52; the associated replies are included. In `Ryan_5_intro`, the developer recovery choices target 30, 41 and 52 and set distinct relationship flags. In `Conrad_finished_mount_3`, instruction 89 targets `Conrad_Outro_3` on macOS and `Conrad_Outro` on Windows. These are source bindings, not newly tested runtime behavior. Paired instruction evidence: Conrad receipt `48ad36b3279cb8f065b7e85147468b5fbe2dd8a0435030d70cd46026e1bc450d`, Ryan receipt `75adfc531223f1c5d6cd4986fac0c30ad3f6d9fde443c7288ddf8fe32934bb2b`, under `localization/work/cli-terra-high-20261110.J0KLrx/es/resume-11/semantic/`.
- The Alexander intimacy speaker and lying-down nuance, and the Conrad intimate-scene speaker inference, remain reviewer questions. `Ryan_3_Outro` `5d2d16e0` continues the preceding question fragment; its punctuation should be judged in that context. Do not infer independent approval from this recipe or the structural checks.

## Export and verification

Extended exporter SHA-256 `03f9804df599cc047f82a49e91225354a449f721ec12a12a1b06f4cd749d7b81`, base exporter `3a39e4923570d0b46930cf935a719269e3556e305ee563cff90e1f763a783b7c`; extended exporter last changed at `1606698ac403a30fe553b0b790916cabfe0d456a`. Its imported local modules SHA-256: `assemble_source_inventory.py` `b565808b1e45bb56a14c9cec197e28551f6fe2a0b8a19ca90ae46b6e16a7cc62`; `dialogue_locale.py` `63b451a7f68f1a964035a10dc359952c8116d0c89a9312648d17af9ee760bc0f`; `index_special_scenes.py` `d6dde81b3142f5728d53efa40764e3cf8d2f5b89aca8bbf019d5d796bbae86d4`; `package_inputs.py` `29e92383dfb694ef0a83a0deb4b46361b39bdcf4bdc875eaa41bdc28f56be3d4`; `paired_locale.py` `e2d2ae7e25449318ef07292f2598381fdaed2e46eb161b45d65561b83e8f3694`.

The extended export was run twice with the same pinned inputs and compared byte-for-byte. The identical export at `localization/work/cli-terra-high-20261110.J0KLrx/es/resume-12/closure/export-v2.json` has SHA-256 `fa1d39f9ef99f3b084d55c5b11c737608e5620c5922d64ffcae87b399303fda7`. A negative control removed only `yarn:line:9d7cc63c` from the recipe; the exporter rejected it with `correction decisions must match the effective locale diff`. It contains 61 changed IDs, 679 unique closure IDs and 55 retained protected records: 34 credit names, 15 unreachable Yarn fragment markers and six slot-progress templates. It includes 77 stock-dialogue-token regression IDs. Component counts and canonical compact-JSON list hashes (components overlap):

| Component | IDs | SHA-256 |
| --- | ---: | --- |
| scene | 229 | `4fde51f301941e40003ef471725b11288a0c56be94e32464f8aa8d0478a24ead` |
| repetitions | 6 | `623ca930e43d8fc159ff4ffd120954e019b17fda26c8e24b1306c38920b865c0` |
| glossary/referents | 72 | `7dc0b2d9a4e5cc23b328e2afc128fd55fef15adcd62f4e6a5458a19bb9290b64` |
| runtime | 29 | `5b83f0ef92a5131d84c7a51d25cc7707b9c72172d5c00a6c453692392651a6f2` |
| regression | 414 | `a1d2c0cd02ed46ab949776ab05aa473f5810c04c0baee497dff451b88809fa65` |

Changed-ID list SHA-256 `2bb485fd7fb4d730275fb884dab8b6936524148db02b5fceedc7ab29e517757d`; closure-ID list `3151965eed708c90ae9bb8c9bc81c01c963f450652d7bab3cf87e1ba087c9ec7`; protected-context list `9c65321e6e781e1bd678674ca9bd28cd79017eecaf5361f57a6cc298581bcd19`. The list digest uses the exporter's sorted-key compact UTF-8 JSON plus newline; list ordering is the pinned inventory ordering.

To reproduce from the checkout, use a fresh task-owned directory for `before.json` and a **nonexistent** output path (the exporter refuses to overwrite). Verify the input hashes above first:

```sh
git show df91415:localization/es/translation.json > "$SCRATCH/before.json"
/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python localization/export_editorial_delta_with_regressions.py \
  --inventory localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json \
  --yarn-scope localization/work/yarn-markers-20261110.ridbPA/yarn-scope-v42.json \
  --paired-scenes localization/work/source-inventory-20261107/yarn-paired-scenes.json \
  --before "$SCRATCH/before.json" --after localization/es/translation.json \
  --recipe localization/es/editorial-delta-recipe.json --locale es --output "$SCRATCH/export.json"
shasum -a 256 "$SCRATCH/export.json"
```
