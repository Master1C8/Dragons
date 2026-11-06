import unittest
from pathlib import Path

import inventory_yarn_controls as controls

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned game builds required')
class ControlInventoryTests(unittest.TestCase):
    def test_real_substitutions_and_numeric_source_ids(self):
        for platform, root in (('macos', MAC), ('windows', WIN)):
            with self.subTest(platform=platform):
                result = controls.inspect(root, platform)
                self.assertEqual(result['lineCount'], 1839)
                self.assertEqual(result['substitutionCounts'], {0: 1839})
                values = {r['lineId']: r['digitRuns'] for r in result['numericLiteralLines']}
                self.assertEqual(values['line:c2bdc402'], {'7': 1})
                self.assertEqual(values['line:a99c515c'], {'223': 1})
                self.assertEqual(values['line:4183ca7e'], {'223': 1})


if __name__ == '__main__':
    unittest.main()
