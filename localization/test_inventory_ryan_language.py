import unittest
from pathlib import Path

import inventory_alexander_questions as checks
import inventory_ryan_language as ryan

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


class BranchTests(unittest.TestCase):
    def test_choice_target_positive_and_negative(self):
        rows = [(5, [(1, 2, b'line:f1c14f75'), (2, 0, 107)])]
        checks.expect(rows, 0, 5, [(1, 2, b'line:f1c14f75'), (2, 0, 107)])
        with self.assertRaisesRegex(ValueError, 'unexpected control instruction'):
            checks.expect(rows, 0, 5, [(1, 2, b'line:f1c14f75'), (2, 0, 115)])


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned builds required')
class SourceTests(unittest.TestCase):
    def test_source_spans_and_version_differences(self):
        a = ryan.inspect(MAC, 'macos')['groups']
        b = ryan.inspect(WIN, 'windows')['groups']
        self.assertEqual({k: len(v['lines']) for k, v in a.items()},
                         {'editor-route-prompt': 3, 'mouth-full-speech': 8, 'salmon-guy-dragon': 17,
                          'movie-title-choices': 19, 'conrad-height-euphemism': 18})
        for name in a:
            self.assertEqual(a[name]['choiceDestinations'], b[name]['choiceDestinations'])
            self.assertEqual([r['id'] for r in a[name]['lines']], [r['id'] for r in b[name]['lines']])
        diffs = {x['id'] for name in a for x, y in zip(a[name]['lines'], b[name]['lines'])
                 if x['sourceSha256'] != y['sourceSha256']}
        self.assertEqual(diffs, {'line:d38c63ea', 'line:a0cb3f78', 'line:36fb380f'})


if __name__ == '__main__':
    unittest.main()
