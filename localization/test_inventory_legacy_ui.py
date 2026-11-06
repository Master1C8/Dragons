import tempfile
import unittest
from pathlib import Path

import inventory_legacy_ui as legacy
import inventory_text_assets as inventory

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WINDOWS = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
WORK = Path(__file__).parent / 'work'


class HierarchyTests(unittest.TestCase):
    def test_order_and_invalid_hierarchies(self):
        self.assertEqual(legacy.hierarchy(2, {1: 0, 2: 1}, {1: 'root', 2: 'child'}), ['root', 'child'])
        with self.assertRaisesRegex(ValueError, 'broken or cyclic'):
            legacy.hierarchy(2, {1: 2, 2: 1}, {1: 'root', 2: 'child'})
        with self.assertRaisesRegex(ValueError, 'broken or cyclic'):
            legacy.hierarchy(2, {2: 1}, {2: 'child'})


@unittest.skipUnless(MAC.is_dir() and WINDOWS.is_dir(), 'both pinned builds are required')
class PinnedInventoryTests(unittest.TestCase):
    def test_both_builds_roundtrip_and_match_legacy_fields(self):
        a, b = legacy.inspect(MAC, 'macos'), legacy.inspect(WINDOWS, 'windows')
        self.assertEqual(len(a['entries']), 149)
        self.assertEqual(a['entries'], b['entries'])
        self.assertFalse(a['unresolvedScripts'])
        self.assertFalse(b['unresolvedScripts'])
        self.assertTrue(all(r['asset'] == 'resources.assets' and r['hierarchy'][0].startswith('DebugUI')
                            for r in a['entries']))

    def test_changed_source_is_rejected_at_asset_guard(self):
        report = inventory.inspect(MAC, 'macos')
        with tempfile.TemporaryDirectory(prefix='legacy-inventory-', dir=WORK) as directory:
            root = Path(directory)
            for name in report['assets']:
                (root / name).symlink_to(MAC / name)
            (root / 'resources.assets').unlink()
            data = bytearray((MAC / 'resources.assets').read_bytes())
            data[-1] ^= 1
            (root / 'resources.assets').write_bytes(data)
            with self.assertRaisesRegex(ValueError, 'unsupported source: resources.assets'):
                legacy.inspect(root, 'macos')


if __name__ == '__main__':
    unittest.main()
