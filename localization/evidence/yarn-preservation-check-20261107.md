# Independent Yarn-only asset preservation check

`localization/verify_yarn_preservation.py` verifies a separately supplied Yarn-only
`sharedassets1.assets` against the pinned original for either supported build and
the exact supplied locale JSON. It first applies the existing source/version and
locale guards. It reconstructs the exact expected localization object from the
source keys, authorized values and original per-entry metadata, then compares it
byte-for-byte with the candidate. Every other Unity object is compared byte-for-byte
with the original, including the entire compiled Yarn project object and program.
Duplicate/missing/extra object identities or any byte discrepancy are rejected.
This is a read-only check; it neither writes game assets nor replaces the builders'
own validation.

Positive controls used separate synthetic locale data for each original build.
The macOS candidate asset SHA-256 was
`99f4c8d831010c12948e1fb5ba9c4abcb5868b60332263de733f587ff1f11ea3`,
the locale JSON SHA-256
`0a9b5b080fee27ef65a7e549031b34f09abea32e2919b99b1367fba3ef5830bd`;
11,393 objects matched their respective expected bytes. The Windows candidate
asset SHA-256 was
`17830a73257c1931737ee9d66df158723cb3cf55ece5d28f6631d05e9de03af0`,
the locale JSON SHA-256
`d01f3bbd41e3a9c21492005efa3b9b6861cdf1c2f66d0f80b1e30f9cded58b92`;
11,381 objects matched. Each input replaces one source entry with artificial
glyphs and is not a translation. Both candidates are local work artifacts.

The focused tests include a real macOS candidate copied in memory and saved to a
disposable file with one changed byte in the compiled project object. The check
rejected that specific object while the matching unmodified candidate passed.
Unit-level controls also reject a changed expected localization object, changed
other object, absent object, and changed localization metadata, with matching
positives. These object comparisons do not execute Yarn semantics. An older
Windows wrapping fixture was rejected by the current Russian digit guard before
object comparison; it was created before that guard and was not modified or
counted as a passing preservation test.

The check deliberately rejects an asset containing independently translated UI
objects, even if those changes are legitimate. Combined Yarn/UI assets need a
separate expected-object composition contract before this can become a complete
package gate. This verifies raw compiled controls and metadata for the selected
asset; it does not classify all source text, independently validate every locale
guard, cover other assets or dynamic code, prove natural translation/rendering,
or establish safe installation/restoration. Ordinary translation remains gated
on the complete shared inventory and preserve-exact contract.

Run with the pinned Python dependencies:

```sh
python localization/verify_yarn_preservation.py macos ORIGINAL_DATA CANDIDATE_ASSET LOCALE_JSON
python localization/verify_yarn_preservation.py windows ORIGINAL_DATA CANDIDATE_ASSET LOCALE_JSON
python -m unittest discover -s localization -p 'test_verify_yarn_preservation.py'
```
