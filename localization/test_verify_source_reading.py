import copy
import hashlib
import json
from pathlib import Path
import unittest

import verify_source_reading as reading

ROOT = Path(__file__).parent


class SourceReadingTests(unittest.TestCase):
    def setUp(self):
        self.corpus = {'builds': {'macos': 1, 'windows': 2}, 'programSha256': {'macos': 'a', 'windows': 'b'},
                       'scenes': {'Node': [{'id': 'line:12345678', 'source': {'macos': 'old', 'windows': 'old'}}]}}
        self.raw = json.dumps(self.corpus).encode()
        self.receipt = {'schema': 1, 'status': 'partial-source-read',
                        'pairedScenesSha256': hashlib.sha256(self.raw).hexdigest(),
                        'programSha256': self.corpus['programSha256'], 'builds': self.corpus['builds'],
                        'nodesRead': 1, 'lineOccurrences': 1, 'uniqueLineIds': 1,
                        'nodes': [{'node': 'Node', 'lineIds': ['line:12345678'],
                                   'sourceHashes': {p: reading.digest_rows(self.corpus['scenes']['Node'], p)
                                                    for p in ('macos', 'windows')}}]}

    def test_changed_receipt_and_corpus_rejected_at_expected_boundaries(self):
        self.assertEqual(reading.verify(self.raw, self.receipt)['uniqueIds'], 1)
        with self.assertRaisesRegex(ValueError, 'paired scene fingerprint changed'):
            reading.verify(self.raw + b' ', self.receipt)
        changed = copy.deepcopy(self.receipt)
        changed['nodes'][0]['lineIds'][0] = 'line:87654321'
        with self.assertRaisesRegex(ValueError, 'reviewed node IDs changed'):
            reading.verify(self.raw, changed)
        changed = copy.deepcopy(self.receipt)
        changed['nodes'][0]['sourceHashes']['windows'] = 'wrong'
        with self.assertRaisesRegex(ValueError, 'reviewed source text changed'):
            reading.verify(self.raw, changed)
        changed = copy.deepcopy(self.receipt)
        changed['nodes'].append(copy.deepcopy(changed['nodes'][0]))
        with self.assertRaisesRegex(ValueError, 'duplicate or unknown reviewed node'):
            reading.verify(self.raw, changed)

    def test_real_partial_read_binding_when_export_available(self):
        corpus = ROOT / 'work/source-inventory-20261107/yarn-paired-scenes.json'
        if not corpus.is_file():
            self.skipTest('pinned paired export required')
        receipt = json.loads((ROOT / 'evidence/source-reading-batch-20261107.json').read_text())
        result = reading.verify(corpus.read_bytes(), receipt)
        self.assertEqual((result['nodes'], result['uniqueIds']), (44, 523))
        alexander = json.loads((ROOT / 'evidence/source-reading-alexander-20261107.json').read_text())
        result2 = reading.verify(corpus.read_bytes(), alexander)
        self.assertEqual((result2['nodes'], result2['uniqueIds']), (35, 351))
        first_ids = {key for node in receipt['nodes'] for key in node['lineIds']}
        second_ids = {key for node in alexander['nodes'] for key in node['lineIds']}
        self.assertTrue(first_ids.isdisjoint(second_ids))
        conrad = json.loads((ROOT / 'evidence/source-reading-conrad-20261107.json').read_text())
        result3 = reading.verify(corpus.read_bytes(), conrad)
        self.assertEqual((result3['nodes'], result3['uniqueIds']), (63, 521))
        third_ids = {key for node in conrad['nodes'] for key in node['lineIds']}
        self.assertTrue((first_ids | second_ids).isdisjoint(third_ids))
        remaining = json.loads((ROOT / 'evidence/source-reading-remaining-20261107.json').read_text())
        result4 = reading.verify(corpus.read_bytes(), remaining)
        self.assertEqual((result4['nodes'], result4['uniqueIds']), (42, 444))
        last_ids = {key for node in remaining['nodes'] for key in node['lineIds']}
        self.assertTrue((first_ids | second_ids | third_ids).isdisjoint(last_ids))
        paired = json.loads(corpus.read_bytes())
        all_ids = {line['id'] for node in paired['scenes'].values() for line in node}
        self.assertEqual(first_ids | second_ids | third_ids | last_ids, all_ids)
        self.assertEqual(len(all_ids), 1839)


if __name__ == '__main__':
    unittest.main()
