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


if __name__ == '__main__':
    unittest.main()
