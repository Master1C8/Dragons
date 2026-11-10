# German revised Alexander line and package verification

The German correction in `32091d1` changes one authored ID, `yarn:line:4b36ea4e`. The coordinator accepted the restored superlative and reread all 11 source-bound positions in the affected Alexander scene. The college name and register agree with the nearby dialogue, the speaker-adapted line ends in a colon, the next line is still `Alexander!`, and both stock options keep their destinations. The tracked German independent scope has 200 unread positions after this reread.

The revised payload SHA-256 `b5aae5f915ea1e1be07b081ae1faaf599a7d91d22bfaf671cb2f5ced61f64009` built and verified as 284 macOS bundle files and 13 Windows ZIP members. Compared with the previous candidate, only `YarnSpinner.Unity.dll` changed in the game data. The Windows manifest and macOS manifest and signing material changed with it. The macOS executable matched byte-for-byte after stripping signatures from disposable copies. This confirms the package-level effect of the speaker-specific correction.

The macOS copy passed strict signature and isolated install/removal checks. The Windows overlay passed isolated installation, interrupted-apply rollback, wrong-source rejection and full restoration. Both stock trees were unchanged. The revised app manifest SHA-256 is `c9b5a374301a8b1ae350aefa4e89967d030f3c453b0fda75770f01057fa96ea1` and the ZIP SHA-256 is `e3d54fcbd43c303d7ccc3ce2ca265ea493f0262add01cf2b500ae55c7ae1f224`.

Packages and receipts are under `localization/work/de-32091d1-packages-20261110.ubuZNO/`. The independent reread and package-difference receipt SHA-256 is `d6b4080d5abef67530393c6e08b55fdb22679076c67dab6982bdc9fd01808f4a`. Game execution and visual fit remain pending.

Two superseded, reproducible French and Polish macOS candidates were removed after checking the older source snapshots, fresh-rebuild reports and verified replacements. Both historical Windows ZIPs, package manifests, scripts and receipts are preserved. The cleanup receipt SHA-256 is `3f950f9a367174ff1c541158a6e4734970d13bdc176bfed90b4f355bacf7bc94`; measured available space increased by 2,293,399,552 bytes.
