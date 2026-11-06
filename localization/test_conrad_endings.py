import hashlib
import json
from pathlib import Path
import unittest

EVIDENCE = Path(__file__).parent / 'evidence'


class ConradEndingsCaseTests(unittest.TestCase):
    def test_complete_groups_and_both_build_branch_bindings(self):
        registry = json.loads((EVIDENCE / 'special-scenes-conrad-endings-20261107.json').read_text())
        raw = (EVIDENCE / 'yarn-context-map-20261107.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), registry['sourceInventorySha256'])
        context = json.loads(raw)
        case = registry['cases'][0]
        for platform in ('macos', 'windows'):
            for group in case['groups']:
                node = group['node']
                self.assertEqual(context['nodeSha256'][platform][node], group['nodeSha256'])
                actual = {key for key, row in context['lineIds'].items() if row[platform]['node'] == node}
                self.assertEqual(set(group['sourceLineIds']), actual)
                self.assertEqual(len(group['sourceLineIds']), len(actual))
            for key, destination in case['choiceDestinations'].items():
                actual = context['lineIds'][key][platform]
                self.assertEqual((actual['kind'], actual['destination']), ('option', destination))


if __name__ == '__main__':
    unittest.main()
