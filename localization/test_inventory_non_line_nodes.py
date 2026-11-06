from pathlib import Path
import unittest

import inventory_non_line_nodes as inventory
from test_map_yarn_context import field_bytes, field_int, instruction, node

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


class NonLineNodeTests(unittest.TestCase):
    def test_transfer_and_line_node_are_distinct(self):
        target = node('Target', instruction(3, field_bytes(1, b'line:12345678')))
        caller = node('Caller', instruction(16, field_bytes(1, b'Target')))
        missing = node('MissingCaller', instruction(16, field_bytes(1, b'Absent')))
        rows = inventory.inspect_nodes({'Target': target, 'Caller': caller, 'MissingCaller': missing})
        self.assertEqual([r['node'] for r in rows], ['Caller', 'MissingCaller'])
        self.assertTrue(rows[0]['namedTransfers'][0]['targetPresent'])
        self.assertFalse(rows[1]['namedTransfers'][0]['targetPresent'])
        bad = node('Caller', instruction(16, field_bytes(1, b'Target') + field_int(2, 1)))
        with self.assertRaisesRegex(ValueError, 'unexpected node-transfer operands'):
            inventory.inspect_nodes({'Caller': bad, 'Target': target})

    @unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned builds required')
    def test_actual_non_line_nodes_are_bound_to_each_build(self):
        platform_rows = []
        for platform, root in (('macos', MAC), ('windows', WIN)):
            with self.subTest(platform=platform):
                report = inventory.inspect(root, platform)
                rows = report['noLineNodes']
                platform_rows.append(rows)
                self.assertEqual((report['totalNodeCount'], len(rows)), (195, 11))
                transfers = [(row['node'], t['target']) for row in rows for t in row['namedTransfers']
                             if not t['targetPresent']]
                self.assertEqual(transfers, [('Alexander_Idle4', 'Alexander_Done')])
                self.assertEqual(sum(len(row['namedTransfers']) for row in rows), 25)
                self.assertTrue(any(row['node'] == 'Ryan_egg' and
                                    any(t['target'] == 'Ryan_egg_dialog' for t in row['namedTransfers'])
                                    for row in rows))
        self.assertEqual(platform_rows[0], platform_rows[1])


if __name__ == '__main__':
    unittest.main()
