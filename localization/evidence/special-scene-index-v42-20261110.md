# Known special-scene source index

This records the initial v42 index. The
[staged-typography follow-up](staged-typography-20261110.md) records the
current index and the additional cases.

`index_special_scenes.py` resolves 21 existing Yarn cases from 11
registries against the pinned v42 source inventory. It checks each
registry's source fingerprint, links the cases to their original
evidence, and verifies their direct and contextual IDs. Each named
scene includes the surrounding node context. The romance cases retain
their wider route scope as context. The fragment case keeps its 15
exact marker IDs and eight restored suffix IDs distinct.

The index also binds two runtime display cases. New-slot wording has
nine source occurrences across the paired serialized labels and the
managed writes. Its context includes 18 exact progress formats and
templates. The missing-line fallback has four managed occurrences.
Its context preserves the unused provider's fallback and the option
prefab template. The [non-Yarn source evidence](non-yarn-translation-scope-20261110.md)
binds the consumer, and the [extended route audit](extended-text-routes-20261110.md)
documents the separate Unity table settings.

| Scope | Unique count |
| --- | ---: |
| Cases | 23 |
| Direct source IDs | 247 |
| Union of direct and contextual IDs | 1,101 |

These counts include exact technical values and IDs used by multiple
cases. They describe indexed dependencies. The contextual route sets
do not establish additional mandatory Russian wording. Final locale
decisions, editorial acceptance and any remaining special-case
discovery stay separate.

Build the index with the v42 inventory and a fresh output path:

```sh
"$PYTHON" localization/index_special_scenes.py \
  --inventory "$shared_inventory" --output "$fresh_index"
```

Two builds reproduced byte-for-byte. Local output
`localization/work/special-scene-index-20261110.w7Zw7p/index-v42.json`
has SHA-256
`1c4e05bfc6878fd968e87f083b8f39516709c94a5a34696ce6475e75e50c5203`.
The focused tests passed and distinguish a valid same-node dependency
from an existing ID in the wrong node.
