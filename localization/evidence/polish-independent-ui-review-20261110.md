# Independent review of the Polish interface and settings

The coordinator read all 123 non-Yarn targets in the expanded delta for `3d2a625`, with 99 macOS and 117 Windows bindings. The review included the save-delete prompt, the separate serialized and managed new-slot labels, six repeated Windows pause menus, macOS-only controls, status text, credit blocks, speaker names and missing-line fallback. The bound translation SHA-256 is `e9bd6034e2d6ad3f72f3d72265b778acd34d47b82674ab81647283a7f89c2665`.

- `settings:TargetFramerate:label` is “Docelowa liczba klatek”, which names a frame count. “Docelowy FPS” states the intended rate compactly. The source labels are `sharedassets0.assets#622:label` on macOS and `sharedassets0.assets#618:label` on Windows.
- `ui:1fb6a23724e3aca3e3503c7a3fac54fc8096c69d78afbb4dff4ffee7136e6ea7` names three credited activities. “Szkielety smoków” denotes skeletons and loses the rigging work. Use “Rigowanie smoków” on the third line, with the two animation lines and the original line order preserved. The bindings are `level2#758` on macOS and `level2#716` on Windows.

The isolated candidate changed exactly those two IDs. Both complete source-bound package input validators accepted it, covering all 12 input files per platform. Author disposition, actual fit and operation of the controls are pending.

The exact reviewed IDs, proposals and validation receipts are under `localization/work/pl-independent-ui-20261110.re2CCT/`. The review receipt SHA-256 is `373976bccc4b54fbd61036a1f9a6e35f2bb67a0df61c858184ccf6fc5c21f053`. Together with the [111-ID independent delta read](polish-independent-delta04-review-20261110.md), 234 distinct IDs of this 460-ID closure have been read. The outstanding 226 IDs and earlier-only closure still need reconciliation.
