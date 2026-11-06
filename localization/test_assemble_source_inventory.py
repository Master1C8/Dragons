import json
from pathlib import Path
import tempfile
import unittest

import assemble_source_inventory as inventory

ROOT = Path(__file__).parent
WORK = ROOT / 'work/source-inventory-20261107'
ROLES = ROOT / 'evidence/ui-source-roles-20261107.json'


class SourceInventoryUnitTests(unittest.TestCase):
    def test_pinned_input_and_duplicate_ids_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / 'sample.json'
            p.write_text('{"ok": true}', encoding='utf-8')
            digest = inventory.dl.sha(p.read_bytes())
            self.assertEqual(inventory.load_pinned(p, digest), {'ok': True})
            p.write_text('{"ok": false}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'unsupported source export'):
                inventory.load_pinned(p, digest)
        rows = {}
        inventory.put(rows, {'id': 'same', 'source': 'first'})
        with self.assertRaisesRegex(ValueError, 'duplicate inventory identity'):
            inventory.put(rows, {'id': 'same', 'source': 'second'})
        self.assertEqual(rows['same']['source'], 'first')

    @unittest.skipUnless(WORK.is_dir() and all((WORK / f).is_file() for f in inventory.FILES),
                         'all pinned source exports required')
    def test_all_selected_source_families_and_platform_bindings(self):
        result = inventory.build(WORK, ROLES)
        self.assertEqual(result['status'], 'provisional-not-translation-ready')
        self.assertEqual(result['familyCounts'], {'legacy-ui': 149, 'managed': 1818,
                                                  'settings': 80, 'ui': 162, 'yarn': 1839})
        entries = {r['id']: r for r in result['entries']}
        sample = entries['yarn:line:4b36ea4e']
        self.assertEqual((sample['node'], sample['instructionIndex']), ('Alexander_2', 14))
        self.assertEqual(sample['source']['macos'], sample['source']['windows'])
        self.assertEqual(sample['role'], 'preserve-exactly-pending-source-role')
        self.assertEqual(sum(r['role'] == 'preserve-exactly-pending-source-role' for r in result['entries']), 16)
        self.assertEqual(sum(r.get('preserveExactPrefix') is not None for r in result['entries']), 18)
        mac_only = entries['settings:LookInvertY:label']
        self.assertEqual(mac_only['source']['macos'], 'Invert Look Y')
        self.assertIsNone(mac_only['source']['windows'])
        self.assertTrue(all(len(r['source']) == 1 for r in result['entries'] if r['family'] == 'managed'))
        controls = [r for r in result['entries'] if r['role'] == 'preserve-exactly-input-control']
        self.assertEqual(len(controls), 56)
        self.assertEqual(sum('macos' in r['source'] for r in controls), 28)
        self.assertEqual(sum('windows' in r['source'] for r in controls), 28)
        self.assertTrue(all('InputSystem_Actions::.ctor()' in r['method'] for r in controls))
        self.assertEqual(len(entries), sum(result['familyCounts'].values()))


if __name__ == '__main__':
    unittest.main()
