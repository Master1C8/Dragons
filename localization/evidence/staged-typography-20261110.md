# Staged Yarn typography and special-scene index

The paired source scan checked all 1,839 Yarn entries per build. Sixteen
IDs per build use a gradient or at least two size tags. All 16 match
between builds in ID, tag sequence and occupied text regions. Twelve
were already indexed. The [typography registry](special-scenes-typography-20261110.json)
adds four IDs in three cases.

| Case | Direct IDs | Source effect |
| --- | --- | --- |
| Conrad's emphatic greetings | `line:36073321`, `line:f474ffa9` | Greeting at 140% followed by ordinary text. The earlier greeting uses the yellow-orange gradient. |
| Conrad's scales aside | `line:6c193ba9` | The aside drops to 70% and italic before ordinary size returns. |
| Ryan branch hesitation | `line:9fd5b834` | The player's choice shrinks through 90%, 80% and 70% in successive beats. |

The Yarn locale reader keeps the exact tag order and checks whether
each tag-delimited region contains printable, non-whitespace text.
All 32 unchanged source controls passed. The prior reader accepted all
32 mutations that moved text into a later region and left a zero-width
space behind. The new reader rejected all 32 at the region check, with
tag tokens, tag order and visible digit runs unchanged. A focused
Russian control also checks the styled option and its outcome caption.
All 200 project tests passed, including the original-asset transition
builder test.

In both pinned source builds, the TMP settings select
`Color Gradient Presets/`. The ResourceManager resolves `gold` and
`yellow - orange` to `resources.assets#1383` and `#1384`. Both presets
decode as `TMP_ColorGradient` and have identical object hashes across
builds. Five existing `LinePresenter.lineText` targets and the
`OptionItem.text` target per build have rich text enabled. The
read-only check validated the source asset hashes and exact
serialization of the inspected components. See the
[TMP bindings](staged-typography-bindings-20261110.json).
The check establishes serialized support. Final Russian wording,
Unity rendering and fit remain pending.
The [runtime follow-up](styled-cyrillic-runtime-20261110.md) separately
checks stock dialogue sizing and gradient mesh data on synthetic
Cyrillic samples.

The v42 index rebuilt twice byte-for-byte using the command in
the [initial index receipt](special-scene-index-v42-20261110.md).
That revision contains 26 cases, 251 direct IDs and 1,106 distinct
direct and contextual IDs. The [anonymous-scene follow-up](generic-dragon-entries-20261110.md#anonymous-address-dependencies-and-branch-control)
records the current revision. Local outputs are under
`localization/work/staged-typography-20261110.el5ul4/`.

| Evidence | SHA-256 |
| --- | --- |
| Current v42 index | `fa499f0f93bbc5471baf951222185460f719e5c7bb8d5bbabd0483dfb8cd2104` |
| Paired controls | `896a82c914108da4fa0c790c932522426f4c81ab1ba640e226044c32965b6dcd` |
| Serialized TMP bindings | `b20ccccb2e17b32f9bf6a69d41ad18d64e13c4bf90de60874e22ca67ee3760e1` |
