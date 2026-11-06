"""Tests for test-only profile isolation and its per-file failure boundary."""
import importlib.util
from pathlib import Path
import plistlib
import shutil
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import isolated_profile as profile


SOURCE = Path.home() / "Documents/Drag'N Wash.app"
READY = SOURCE.is_dir() and importlib.util.find_spec('UnityPy') is not None


class ProfileIdentityTests(unittest.TestCase):
    def test_invalid_code_and_existing_preferences_are_rejected(self):
        with tempfile.TemporaryDirectory(prefix='dragnwash-profile-home-') as directory:
            home = Path(directory)
            with self.assertRaisesRegex(ValueError, 'four uppercase'):
                profile.identity('../x', home)
            expected = profile.identity('Q7F2', home)
            pref = home / 'Library/Preferences' / (expected['bundle'] + '.plist')
            pref.parent.mkdir(parents=True)
            pref.write_bytes(b'keep')
            with self.assertRaisesRegex(FileExistsError, 'already exist'):
                profile.identity('Q7F2', home)
            self.assertEqual(pref.read_bytes(), b'keep')

    def test_collision_is_checked_in_both_environment_and_account_homes(self):
        with tempfile.TemporaryDirectory(prefix='dragnwash-profile-homes-') as directory:
            root = Path(directory)
            environment_home, account_home = root / 'environment', root / 'account'
            expected = profile.identity('Q7F2', environment_home)
            pref = account_home / 'Library/Preferences' / (expected['bundle'] + '.plist')
            pref.parent.mkdir(parents=True)
            pref.write_bytes(b'keep')
            with patch.object(profile.Path, 'home', return_value=environment_home), \
                 patch.object(profile.pwd, 'getpwuid', return_value=SimpleNamespace(pw_dir=str(account_home))):
                with self.assertRaisesRegex(FileExistsError, 'already exist'):
                    profile.identity('Q7F2')
            self.assertEqual(pref.read_bytes(), b'keep')


@unittest.skipUnless(READY, 'pinned macOS game and UnityPy required')
class ProfileAssetIntegrationTests(unittest.TestCase):
    def make_copy(self, root):
        app = root / 'Test.app'
        for name in (profile.GLOBAL_REL, profile.PLIST_REL):
            target = app / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(SOURCE / name, target)
        (app / 'Contents/Resources').mkdir(exist_ok=True)
        return app

    def test_copied_profile_has_unique_identity_and_original_is_unchanged(self):
        import UnityPy
        with tempfile.TemporaryDirectory(prefix='dragnwash-profile-test-') as directory:
            root = Path(directory)
            source_global = (SOURCE / profile.GLOBAL_REL).read_bytes()
            source_plist = (SOURCE / profile.PLIST_REL).read_bytes()
            prepared = profile.prepare(SOURCE, 'Q7F2', home=root)
            app = self.make_copy(root)
            original_identity = profile.identity
            with patch.object(profile, 'identity', side_effect=lambda code: original_identity(code, root)):
                result = profile.apply(app, prepared)
            self.assertEqual(result['product'], 'ProbeQ7F2')
            self.assertEqual(plistlib.loads((app / profile.PLIST_REL).read_bytes())['CFBundleIdentifier'],
                             result['bundle'])
            env = UnityPy.load(str(app / profile.GLOBAL_REL))
            player = next(o for o in env.objects if o.type.name == 'PlayerSettings').read(check_read=False)
            self.assertEqual((player.companyName, player.productName), ('Codex Test Sandbox', 'ProbeQ7F2'))
            self.assertTrue((app / 'Contents/Resources/vn-test-profile.json').is_file())
            self.assertEqual((SOURCE / profile.GLOBAL_REL).read_bytes(), source_global)
            self.assertEqual((SOURCE / profile.PLIST_REL).read_bytes(), source_plist)

    def test_failure_after_first_file_retains_partial_copy_and_existing_temp(self):
        with tempfile.TemporaryDirectory(prefix='dragnwash-profile-failure-') as directory:
            root = Path(directory)
            prepared = profile.prepare(SOURCE, 'Q7F2', home=root)
            app = self.make_copy(root)
            plist = app / profile.PLIST_REL
            old_plist = plist.read_bytes()
            blocker = plist.with_name('Info.test-profile.tmp')
            blocker.write_bytes(b'preserve')
            original_identity = profile.identity
            with patch.object(profile, 'identity', side_effect=lambda code: original_identity(code, root)):
                with self.assertRaises(FileExistsError):
                    profile.apply(app, prepared)
            self.assertNotEqual((app / profile.GLOBAL_REL).read_bytes(), (SOURCE / profile.GLOBAL_REL).read_bytes())
            self.assertEqual(plist.read_bytes(), old_plist)
            self.assertEqual(blocker.read_bytes(), b'preserve')
            self.assertFalse((app / 'Contents/Resources/vn-test-profile.json').exists())


if __name__ == '__main__':
    unittest.main()
