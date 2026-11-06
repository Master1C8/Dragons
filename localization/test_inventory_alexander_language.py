import unittest
from pathlib import Path

import inventory_alexander_language as language

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


class ChoiceTests(unittest.TestCase):
    def test_target_and_identity_are_guarded(self):
        rows = [(5, [(1, 2, b'line:12345678'), (2, 0, 11)])]
        language.choice(rows, 0, 'line:12345678', 11)
        with self.assertRaisesRegex(ValueError, 'unexpected control instruction'):
            language.choice(rows, 0, 'line:12345678', 15)
        with self.assertRaisesRegex(ValueError, 'unexpected control instruction'):
            language.choice(rows, 0, 'line:87654321', 11)


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned game builds required')
class SourceTests(unittest.TestCase):
    def test_real_choice_groups_and_build_differences(self):
        a = language.inspect(MAC, 'macos')['groups']
        b = language.inspect(WIN, 'windows')['groups']
        for name in language.GROUPS:
            self.assertEqual(a[name]['nodeSha256'], b[name]['nodeSha256'])
            self.assertEqual([x['id'] for x in a[name]['lines']], [x['id'] for x in b[name]['lines']])
        self.assertNotEqual(a['proletarian-register']['lines'][0]['sourceSha256'],
                            b['proletarian-register']['lines'][0]['sourceSha256'])
        self.assertEqual(a['teacher-professor-correction']['lines'], b['teacher-professor-correction']['lines'])


if __name__ == '__main__':
    unittest.main()
