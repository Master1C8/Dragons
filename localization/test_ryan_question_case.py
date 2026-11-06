import hashlib
import json
from pathlib import Path
import unittest

EVIDENCE = Path(__file__).parent / 'evidence'


class RyanQuestionCaseTests(unittest.TestCase):
    def test_whole_node_and_choice_bindings_in_both_builds(self):
        registry = json.loads((EVIDENCE / 'special-scenes-ryan-question-20261107.json').read_text())
        raw = (EVIDENCE / 'yarn-context-map-20261107.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), registry['sourceInventorySha256'])
        context = json.loads(raw)
        case = registry['cases'][0]
        for platform in ('macos', 'windows'):
            self.assertEqual(context['nodeSha256'][platform][case['node']], case['nodeSha256'])
            actual_ids = {key for key, row in context['lineIds'].items()
                          if row[platform]['node'] == case['node']}
            self.assertEqual(set(case['sourceLineIds']), actual_ids)
            self.assertEqual(len(case['sourceLineIds']), len(actual_ids))
            for key, destination in case['choiceDestinations'].items():
                row = context['lineIds'][key][platform]
                self.assertEqual((row['kind'], row['destination']), ('option', destination))


if __name__ == '__main__':
    unittest.main()
