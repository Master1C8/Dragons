import unittest
from pathlib import Path

import inventory_alexander_questions as checks
import inventory_conrad_language as conrad

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


class BranchTests(unittest.TestCase):
    def test_changed_destination_is_rejected(self):
        rows = [(5, [(1, 2, b'line:31fa3bdf'), (2, 0, 18)])]
        checks.expect(rows, 0, 5, [(1, 2, b'line:31fa3bdf'), (2, 0, 18)])
        with self.assertRaisesRegex(ValueError, 'unexpected control instruction'):
            checks.expect(rows, 0, 5, [(1, 2, b'line:31fa3bdf'), (2, 0, 49)])


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned builds required')
class SourceTests(unittest.TestCase):
    def test_all_three_source_groups_match_across_builds(self):
        mac, win = conrad.inspect(MAC, 'macos')['groups'], conrad.inspect(WIN, 'windows')['groups']
        self.assertEqual(mac, win)
        self.assertEqual({name: len(group['lines']) for name, group in mac.items()},
                         {'dirty-double-meaning': 12, 'professional-double-meaning': 15, 'big-c-nickname': 14})
        dirty = next(x for x in mac['dirty-double-meaning']['lines'] if x['id'] == 'line:5a5e7f21')
        self.assertEqual(dirty['instructionIndex'], 9)


if __name__ == '__main__':
    unittest.main()
