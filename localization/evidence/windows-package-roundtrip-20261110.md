# Windows package application, startup and restoration

The synthetic Windows replacement ZIP, SHA-256
`519eeb352e5fe41f298867e265204d9fd204fa2d24c558e1a54cb61b8edb0dcf`,
was tested against build `9/9/2026_ee944596`. A fresh private clone
matched all 287 file hashes of the installed game before applying it.
The clone was repaired to that baseline before testing because its
earlier source copy lacked the nested Steam App ID file.

The offline harness checked the archive hash, member list, original
replacement hashes and both global Unity hashes. It extracted and
hashed every member before writing to the clone. It backed up each
replaced file locally, then used per-file atomic replacements. The
installed-copy manifest matched the expected 288 files, with exactly
11 replacements and one added companion. A successful removal and
a separate forced I/O failure after the fourth replacement each
restored all 287 original hashes. This tests rollback from the
observed partial copy, without process-crash or power-loss recovery.

The archive was reapplied to the verified clone and launched with
`-batchmode -nographics` in a fresh private CrossOver 26.3.0 Windows 10
bottle. The Unity log bound Mono's loaded `Assembly-CSharp.dll` and
`YarnSpinner.Unity.dll` to the clone. It reported assembly reload
completion and Steam App ID initialization. All 13 samples had no
on-screen window or foreground ownership. The verified test PID was
stopped, its wrapper exited with status zero, and the pre-existing
game process was still present. No additional game files changed
during startup. Removing the overlay again recovered all 287 original
hashes. The installed game and checked Windows player profile matched
their pretest manifests.

The Null graphics device and startup-only route leave the speaker
companion's call path, player interaction, saves and visible Russian
presentation untested for this archive. No synthetic save was written
and no profile directory was created by this run. This was a local
copy operation and CrossOver startup check. Native Windows and final
localized artifacts remain separate acceptance checks.

Local scripts, snapshots and logs are under
`localization/work/windows-package-install-20261110.npP9n6/`.
The 28 staging and backup files verified as duplicates were removed.

| Evidence | SHA-256 |
| --- | --- |
| Source and both offline restored manifests | `404b85b85475ea5ed6c58d43a035cc261bea110fd360170b03a941627c974a32` |
| Applied-copy manifest | `f727f70cdc4a8b81078cdf4fceb71371bc73450a6ad7cf8df1b19e442c0e6f68` |
| Offline verification result | `2b1a52169bd7f86bff86c725774e4ceff1614dd70236e95a55ccd14142b457d7` |
| Original profile baseline | `5a858e8f31feb17760a1236cdfc9eb6c8e31a2c0a9507c3b3b2143bb3a032dee` |
| CrossOver result | `e0246bf5288d8c024f4673d8f8b6fab86db38966eead6513fa2be38b0f0407f8` |
| Unity startup log | `7f876f44e52e5cfdd61b161581cad45d150e800fd98d6b3115cf743813678482` |
