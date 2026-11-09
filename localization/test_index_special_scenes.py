from pathlib import Path
import unittest

import index_special_scenes as index
from assemble_source_inventory import INVENTORY_NAME

INVENTORY = Path(__file__).parent / 'work/source-inventory-20261107' / INVENTORY_NAME


class SpecialSceneIndexTests(unittest.TestCase):
    def test_wrong_node_dependency_fails_after_matching_control(self):
        nodes = {'Scene': [{'id': 'line:abc'}], 'Other': [{'id': 'line:xyz'}]}
        case = {'id': 'test', 'node': 'Scene', 'sourceLineIds': ['line:abc']}
        self.assertEqual(index.case_inputs(case, nodes), ({'yarn:line:abc'}, set()))
        case['sourceLineIds'] = ['line:xyz']
        with self.assertRaisesRegex(ValueError, 'direct dependencies do not match the node'):
            index.case_inputs(case, nodes)

    @unittest.skipUnless(INVENTORY.is_file(), 'paired v42 inventory required')
    def test_all_known_cases_bind_and_keep_direct_and_context_distinct(self):
        report = index.build(INVENTORY)
        self.assertEqual(report['caseCount'], 23)
        self.assertEqual(report['uniqueDirectIds'], 247)
        cases = report['cases']
        self.assertEqual(len(cases['alexander-college-self-introduction']['directIds']), 9)
        self.assertEqual(len(cases['alexander-college-self-introduction']['contextIds']), 2)
        self.assertEqual(len(cases['new-slot-display']['contextIds']), 18)
        self.assertEqual(len(cases['missing-yarn-line-display']['contextIds']), 3)
        self.assertTrue(all(not set(c['directIds']).intersection(c['contextIds']) for c in cases.values()))
