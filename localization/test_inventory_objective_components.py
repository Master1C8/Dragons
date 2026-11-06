import unittest
from pathlib import Path

import inventory_objective_components as inventory

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


class IdentityTests(unittest.TestCase):
    def test_exact_script_identity(self):
        self.assertTrue(inventory.selected('', 'ObjectiveDisplay'))
        self.assertTrue(inventory.selected('TMPro', 'TextMeshPro'))
        self.assertFalse(inventory.selected('TMPro', 'TextMeshProUGUI'))
        self.assertFalse(inventory.selected('Other', 'ObjectiveDisplay'))


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned game builds required')
class SourceTests(unittest.TestCase):
    def test_scoped_inventory_of_both_builds(self):
        for platform, root in (('macos', MAC), ('windows', WIN)):
            with self.subTest(platform=platform):
                report = inventory.inspect(root, platform)
                self.assertEqual(len(report['assets']), 17)
                self.assertEqual(report['matches'], [])
                self.assertEqual(report['unresolvedScriptReferences'], [])


if __name__ == '__main__':
    unittest.main()
