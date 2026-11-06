import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
spec = importlib.util.spec_from_file_location('build_game', Path(__file__).with_name('build_game.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BuildSafetyTests(unittest.TestCase):
    def test_experimental_layout_requires_a_test_profile_before_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'Original.app'
            source.mkdir()
            destination = root / 'Output.app'
            with self.assertRaisesRegex(ValueError, 'requires an isolated test profile'):
                module.build(source, root / 'locale.json', 'ru', destination, test_caption_layout=True)
            self.assertFalse(destination.exists())

    def test_experimental_slot_font_requires_a_test_profile_before_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'Original.app'
            source.mkdir()
            destination = root / 'Output.app'
            with self.assertRaisesRegex(ValueError, 'requires an isolated test profile'):
                module.build(source, root / 'locale.json', 'ru', destination, test_slot_font=True)
            self.assertFalse(destination.exists())

    def test_rejects_existing_destination_and_overlapping_source(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'Original.app'
            source.mkdir()
            destination = root / 'Existing.app'
            destination.mkdir()
            marker = destination / 'owner-data'
            marker.write_text('keep')
            with self.assertRaises(FileExistsError):
                module.build(source, root / 'missing.json', 'ru', destination)
            self.assertEqual(marker.read_text(), 'keep')
            with self.assertRaisesRegex(ValueError, 'overlap'):
                module.build(source, root / 'missing.json', 'ru', source / 'Copy.app')

    def test_locale_mismatch_stops_before_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'Original.app'
            asset = source / module.ASSET_RELATIVE
            asset.parent.mkdir(parents=True)
            asset.write_bytes(b'fixture')
            (source / 'steam_appid.txt').write_bytes(b'fixture')
            dest = root / 'ru.app'
            with patch.object(module.dl, 'load_asset', return_value=(None, None, b'', [], [], [])), \
                 patch.object(module.dl, 'read_locale', return_value=('fr', {})):
                with self.assertRaisesRegex(ValueError, 'not requested'):
                    module.build(source, root / 'locale.json', 'ru', dest)
            self.assertFalse(dest.exists())
            self.assertEqual(asset.read_bytes(), b'fixture')

    def test_source_symlink_is_rejected_before_copy(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / 'Original.app'
            source.mkdir()
            outside = root / 'external'
            outside.write_text('preserve')
            (source / 'link').symlink_to(outside)
            dest = root / 'Localized.app'
            with self.assertRaisesRegex(ValueError, 'symlink'):
                module.build(source, root / 'locale.json', 'ru', dest)
            self.assertFalse(dest.exists())
            self.assertEqual(outside.read_text(), 'preserve')

    def test_failure_between_staged_writes_leaves_no_final_app(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, destination = root / 'Original.app', root / 'Localized.app'
            source.mkdir()
            (source / 'owner-data').write_text('original')
            def incomplete(_source, _locale, _requested, staged, *args):
                staged.mkdir()
                (staged / 'first-file').write_text('written')
                raise ValueError('failure after first write')
            with patch.object(module, '_build_unpublished', side_effect=incomplete):
                with self.assertRaisesRegex(ValueError, 'failure after first write'):
                    module.build(source, root / 'locale.json', 'ru', destination)
            self.assertFalse(destination.exists())
            self.assertEqual((source / 'owner-data').read_text(), 'original')
            self.assertEqual(sorted(p.name for p in root.iterdir()), ['Original.app'])

    @unittest.skipUnless(sys.platform == 'darwin', 'macOS exclusive rename required')
    def test_published_result_and_competing_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, destination = root / 'Original.app', root / 'Localized.app'
            source.mkdir()
            def prepare(_source, _locale, _requested, staged, *args):
                staged.mkdir()
                (staged / 'result').write_text('verified fixture')
                return {'locale': 'ru'}
            with patch.object(module, '_build_unpublished', side_effect=prepare), \
                 patch.object(module.subprocess, 'run') as verify:
                module.build(source, root / 'locale.json', 'ru', destination)
                self.assertEqual((destination / 'result').read_text(), 'verified fixture')
                verify.assert_called_once_with(['codesign', '--verify', '--deep', '--strict', str(destination)], check=True)
            self.assertEqual(sorted(p.name for p in root.iterdir()), ['Localized.app', 'Original.app'])
            destination2 = root / 'Other.app'
            def compete(_source, _locale, _requested, staged, *args):
                staged.mkdir()
                (staged / 'result').write_text('candidate')
                destination2.mkdir()
                (destination2 / 'owner-data').write_text('preserve')
                return {'locale': 'ru'}
            with patch.object(module, '_build_unpublished', side_effect=compete), \
                 patch.object(module.subprocess, 'run') as verify:
                with self.assertRaises(FileExistsError):
                    module.build(source, root / 'locale.json', 'ru', destination2)
                verify.assert_not_called()
            self.assertEqual((destination2 / 'owner-data').read_text(), 'preserve')
            self.assertEqual(sorted(p.name for p in root.iterdir()), ['Localized.app', 'Original.app', 'Other.app'])

    @unittest.skipUnless(sys.platform == 'darwin', 'macOS exclusive rename required')
    def test_post_publication_verify_failure_retains_result(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source, destination = root / 'Original.app', root / 'Localized.app'
            source.mkdir()
            def prepare(_source, _locale, _requested, staged, *args):
                staged.mkdir()
                (staged / 'result').write_text('candidate')
                return {'locale': 'ru'}
            with patch.object(module, '_build_unpublished', side_effect=prepare), \
                 patch.object(module.subprocess, 'run', side_effect=RuntimeError('verification failed')):
                with self.assertRaisesRegex(RuntimeError, 'verification failed'):
                    module.build(source, root / 'locale.json', 'ru', destination)
            self.assertEqual((destination / 'result').read_text(), 'candidate')
            self.assertFalse(any(p.name.startswith('.localization-build-') for p in root.iterdir()))


if __name__ == '__main__':
    unittest.main()
