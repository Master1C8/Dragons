# Synthetic slot width comparison

An independently authorized gpt-6.1-terra reviewer (high) compared two 1024 × 824 WebP80 previews of the same synthetic label `Жж Ъъ Ьь 427` on 2026-11-06. All original and preview hashes were verified.

| State | Original SHA-256 | Preview SHA-256 |
| --- | --- | --- |
| Original text margins | `109be11f1694fa4d942f4f48c6646b009f882a3078f5ad6cc5794b3c5be0e422` | `29c52938b0f589483513c3b1c6ea36dfc3b6db60e7d409b888b13a8358538893` |
| Test-only margins 130/130 | `4d4d08c59d9817db0b66e72556fdb13a9db5ecfabdb54517d380f61064e2f9da` | `2013bb84aaed4737a30e37175fcba7c5eeb620d7779d4ad91b8cccf4f83179c1` |

Both samples wrapped onto two lines. In the wider candidate the Cyrillic groups appeared on the first line and `427` on the second, with the first line visibly extending beyond the colored label background on both sides, especially to the right. There was no obvious collision with the large slot labels. The exact signs and whether the field edge clips glyphs remain uncertain at this representation. The candidate is not accepted or enabled for normal builds; no game-wide conclusions follow.
