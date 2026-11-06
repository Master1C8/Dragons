import copy
from pathlib import Path
import unittest

import inventory_yarn_protected as protection

ROOT = Path(__file__).parent
PAIRED = ROOT / 'work/source-inventory-20261107/yarn-paired-scenes.json'
AUDIT = ROOT / 'evidence/yarn-targets-20261107.json'


@unittest.skipUnless(PAIRED.is_file() and AUDIT.is_file(), 'pinned source exports required')
class YarnProtectedInventoryTests(unittest.TestCase):
    def setUp(self):
        self.paired = protection.load(PAIRED, protection.PAIRED_SHA)
        self.audit = protection.load(AUDIT, protection.TARGETS_SHA)

    def test_exact_counts_and_expected_source_roles(self):
        result = protection.build(self.paired, self.audit)
        self.assertEqual(len(result['fullValueProtection']), 16)
        self.assertEqual(len(result['prefixProtection']), 18)
        full = {x['id']: x for x in result['fullValueProtection']}
        self.assertEqual(full['line:4b36ea4e']['reason'], 'long-implicit-speaker-needs-adapter')
        self.assertEqual(sum(x['reason'] == 'embedded-title-needs-review' for x in full.values()), 5)
        self.assertEqual(sum(x['reason'] == 'adjacent-marker-needs-review' for x in full.values()), 10)
        self.assertTrue(all(x['expectedPrefix']['macos'] == x['expectedPrefix']['windows']
                            for x in result['prefixProtection']))

    def test_changed_guarded_source_fails_after_matching_positive(self):
        protection.build(self.paired, self.audit)
        changed = copy.deepcopy(self.paired)
        line = next(x for rows in changed['scenes'].values() for x in rows if x['id'] == protection.LONG_COLON_ID)
        line['source']['windows'] = 'Different:'
        with self.assertRaisesRegex(ValueError, 'unexpected long-colon source'):
            protection.build(changed, self.audit)


if __name__ == '__main__':
    unittest.main()
