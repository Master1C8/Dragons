import unittest
from pathlib import Path

import classify_ui_sources as classification

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


class ClassificationTests(unittest.TestCase):
    def test_known_paths_and_unknown_path(self):
        self.assertEqual(classification.classify('level0', ['Menu', 'Menu_DeleteSave', 'Text']),
                         'menu-text-translate-candidate')
        self.assertEqual(classification.classify('level2', ['Canvas', 'CreditScroll', 'Name']),
                         'credit-name-preserve-candidate')
        with self.assertRaisesRegex(ValueError, 'unclassified UI hierarchy'):
            classification.classify('level0', ['UnexpectedRoot', 'SomeText'])


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned game builds required')
class PinnedSourcesTests(unittest.TestCase):
    def test_all_known_ui_fields_are_accounted_for(self):
        result = classification.build(MAC, WIN)
        self.assertEqual(result['pairedHierarchyCount'], 162)
        self.assertEqual(sum(bool(x['macos']) for x in result['entries']), 138)
        self.assertEqual(sum(bool(x['windows']) for x in result['entries']), 162)
        self.assertEqual(result['roleCounts']['pause-menu-translate-candidate'], 24)
        self.assertEqual(result['roleCounts']['credit-name-preserve-candidate'], 34)
        self.assertEqual(result['roleCounts']['settings-prefab-template-needs-consumer-review'], 11)
        items = {x['macos']['id']: x for x in result['entries'] if x['macos']}
        self.assertEqual(items['level0#5208']['provisionalRole'], 'menu-text-translate-candidate')
        self.assertEqual(items['level0#5201']['provisionalRole'], 'slot-progress-runtime-replaced')
        self.assertEqual(items['level0#5205']['provisionalRole'], 'slot-new-label-serialized-candidate')
        self.assertTrue(all(x['sameText'] is True for x in result['entries'] if x['macos']))


if __name__ == '__main__':
    unittest.main()
