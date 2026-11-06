# Alexander language-dependent source groups

A coordinator reading of the macOS text in Alexander-named Yarn nodes identified two additional candidates for groupwise Russian adaptation: the use and attempted repetition of “proletarian” with a plainer clarification, and Alexander correcting “teacher” to “professor”. Their full relevant choices, branch continuations, source IDs, acceptance scenarios and unresolved decisions are in `special-scenes-alexander-language-20261107.json` (SHA-256 `72f5dfa5d8ba396d92c7bf67c6912d05022940f2197e073b0a651b5e7f5b0809`). This reading does not prove exhaustive discovery, reachability, visual presentation or independent editorial review. Actual Russian wording remains unprepared and unreviewed; glossary and source gates remain open.

`inventory_alexander_language.py` binds the two groups to the pinned source programs and both English tables, checks four exact choice IDs and destinations and their convergence jumps, and records the source hash and instruction index of each group member. `alexander-language-groups-20261107.json` SHA-256 `4ea4eea0d6fdba66138a4a4d9019920baecd836a801b033fbdc1447e57f21183` reproduced byte-for-byte. The corresponding node bytecode matches across builds. The first sentence in the proletarian group has a spelling difference in an unrelated word between builds, so its source hashes differ; the operative term remains the same. The six selected teacher/professor group values match.

The registry's two ID lists were checked against both source-bound group records and their inventory fingerprint. A matching choice passes the focused test, while changing its ID or destination fails the intended guard. The complete suite passed 99 tests with `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. Those checks do not exercise gameplay or establish that either route is reachable. Tool SHA-256 `18bac461346a0379161130c44e4a1ca9e6e4df2df70c064ba06579dd5259088e`; test SHA-256 `e78cdffc85c2e3942750075d7fe46cce45812a9348111c73f0560862054e9caf`.

Reproduce with the pinned dependencies:

```sh
python localization/inventory_alexander_language.py --macos-data ORIGINAL_MAC_DATA --windows-data ORIGINAL_WINDOWS_DATA
python -m unittest discover -s localization -p 'test_*.py'
```
