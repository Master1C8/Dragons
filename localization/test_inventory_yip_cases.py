import unittest
from unittest.mock import patch

import dialogue_locale as dl
import inventory_yip_cases as inventory
from test_map_yarn_context import field_bytes, instruction, node


class YipSourceInventoryTests(unittest.TestCase):
    def fixture(self):
        ids = ['line:11111111', 'line:22222222']
        mac = ['Yip-Man!', 'Other line']
        win = ['Yip-Man!', 'Changed line']
        lines = {}
        for index, key in enumerate(ids):
            location = {'node': 'Scene', 'instructionIndex': index, 'kind': 'line'}
            lines[key] = {'macos': location, 'windows': location,
                          'sourceSha256': {'macos': dl.sha(mac[index].encode()),
                                           'windows': dl.sha(win[index].encode())}}
        context = {'lineIds': lines, 'programSha256': {},
                   'nodeSha256': {'macos': {'Scene': 'a'}, 'windows': {'Scene': 'b'}}}
        program = {'Scene': node('Scene', instruction(4, field_bytes(1, b'PlaySFX \"yip\"')))}
        return context, (ids, mac, None, None, program, None), (ids, win, None, None, program, None)

    def test_case_insensitive_broad_search_captures_names_and_inflections(self):
        self.assertEqual([x['source'] for x in inventory.matching_spans('Yip-Man and YIPPED, yipping')],
                         ['Yip', 'YIP', 'yip'])
        self.assertEqual(inventory.matching_spans('not present'), [])

    def test_complete_node_context_retains_changed_other_build_line(self):
        context, mac, win = self.fixture()
        with patch.object(inventory.mapping, 'build', return_value=context), \
             patch.object(inventory.versions, 'load', side_effect=[mac, win]):
            result = inventory.build('mac', 'win')
        self.assertEqual(list(result['matches']), ['line:11111111'])
        self.assertEqual(len(result['nodes']['Scene']['macos']['lines']), 2)
        self.assertEqual(result['commands']['macos'][0]['command'], 'PlaySFX \"yip\"')
        self.assertNotEqual(result['nodes']['Scene']['macos']['lines'][1]['sourceSha256'],
                            result['nodes']['Scene']['windows']['lines'][1]['sourceSha256'])

    def test_source_hash_mismatch_fails_at_fingerprint_guard(self):
        context, mac, win = self.fixture()
        win = (win[0], ['changed', win[1][1]], None, None, win[4], None)
        with patch.object(inventory.mapping, 'build', return_value=context), \
             patch.object(inventory.versions, 'load', side_effect=[mac, win]), \
             self.assertRaisesRegex(ValueError, 'source fingerprint mismatch: windows line:11111111'):
            inventory.build('mac', 'win')


if __name__ == '__main__':
    unittest.main()
