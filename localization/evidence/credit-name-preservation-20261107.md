# Credit-name preservation in the UI adapters

The macOS and Windows UI adapters now validate the `level2` contributor-name
fields against `localization/credit_name_preservation.json` before writing an
asset. The manifest contains 34 paired hierarchy records and their exact source
strings, IDs and SHA-256 hashes. Its SHA-256 is
`08ec3974239d2e32e7289826bc7a5c0764f46ae6d0798a524feeb1607784b675`.
The manifest binds the provisional role report SHA-256
`6219fb3d833a85a61e92392fe7c002738d8b105db61f3f39d82f27153ecfefdc`;
the focused test compares the complete name-candidate set against that report.
Each original asset is independently pinned by the existing adapter. A changed
manifest, source name, missing source ID or attempted replacement of a protected
name fails the guard. Unlisted fields, including credit descriptions, are not
subject to this name guard. It is a conservative rule for the two pinned builds,
not proof of full credit or source-inventory coverage.

The four focused tests passed against both locally available original builds
using `/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python`. They check
the report-to-manifest mapping, changed and stale names, rejection before output,
and actual adapter outputs with a synthetic changed description and all 34 names
read back unchanged. Earlier, before adding the report-to-manifest test, the full
suite passed 145 tests. These tests do not establish runtime display, semantic
translation, a complete preservation manifest or release readiness.

```sh
/Users/antonkrutov/Desktop/Forest/.venv-assets314/bin/python -m unittest discover -s localization -p test_credit_name_preservation.py -v
```
