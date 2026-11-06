import tempfile
import unittest
from pathlib import Path

import inventory_addressables as addressables
import inventory_text_assets as inventory

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
WORK = Path(__file__).parent / 'work'


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned game builds are required')
class AddressablesTests(unittest.TestCase):
    def test_both_builds_locale_and_bundle_objects(self):
        mac = addressables.inspect(MAC, 'macos')
        win = addressables.inspect(WIN, 'windows')
        self.assertEqual(mac['locale'], win['locale'])
        self.assertEqual(mac['locale']['fields']['m_Identifier']['m_Code'], 'en')
        for report in (mac, win):
            types = [entry['objectTypes'] for entry in report['bundles']]
            self.assertEqual(types, [{'AssetBundle': 1, 'MonoScript': 1},
                                     {'AssetBundle': 1, 'MonoBehaviour': 1},
                                     {'AssetBundle': 1, 'ComputeShader': 9}])
            self.assertEqual(report['bundles'][1]['containers'][0]['path'],
                             'Assets/Localization/English (en).asset')

    def test_changed_catalog_rejected_after_matching_positive(self):
        assets = inventory.inspect(MAC, 'macos')['assets']
        with tempfile.TemporaryDirectory(prefix='addressables-', dir=WORK) as tmp:
            root = Path(tmp)
            for name in assets:
                (root / name).symlink_to(MAC / name)
            (root / 'Managed').symlink_to(MAC / 'Managed', target_is_directory=True)
            src = MAC / 'StreamingAssets' / 'aa'
            dest = root / 'StreamingAssets' / 'aa'
            for name in {**addressables.COMMON, **addressables.FILES['macos']}:
                path = dest / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.symlink_to(src / name)
            self.assertEqual(addressables.inspect(root, 'macos')['locale']['fields']['m_Identifier']['m_Code'], 'en')
            catalog = dest / 'catalog.bin'
            catalog.unlink()
            data = bytearray((src / 'catalog.bin').read_bytes())
            data[-1] ^= 1
            catalog.write_bytes(data)
            with self.assertRaisesRegex(ValueError, 'Addressables input changed: catalog.bin'):
                addressables.inspect(root, 'macos')


if __name__ == '__main__':
    unittest.main()
