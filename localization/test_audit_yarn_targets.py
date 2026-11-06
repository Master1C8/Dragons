import unittest

import audit_yarn_targets as audit
from test_map_yarn_context import field_bytes, field_int, instruction, node


class YarnTargetAuditTests(unittest.TestCase):
    def test_missing_target_and_matching_embedded_marker_remain_distinct(self):
        texts = {'line:11111111': '==', 'line:22222222': 'title: Missing', 'line:33333333': '---'}
        instructions = [instruction(16, field_bytes(1, b'Missing'))]
        instructions += [instruction(3, field_bytes(1, key.encode())) for key in texts]
        targets, markers = audit.inspect_program({'Scene': node('Scene', *instructions)}, texts)
        self.assertFalse(targets[0]['targetPresent'])
        self.assertEqual(targets[0]['matchingEmbeddedTitle']['lineId'], 'line:22222222')
        self.assertEqual(len(markers['Missing']['adjacentRunLines']), 2)
        self.assertNotIn('Missing', {'Scene'})

    def test_actual_node_and_embedded_marker_are_separate_facts(self):
        branch = instruction(16, field_bytes(1, b'Existing'))
        title = instruction(3, field_bytes(1, b'line:11111111'))
        nodes = {'Scene': node('Scene', branch, title), 'Existing': node('Existing')}
        targets, _ = audit.inspect_program(nodes, {'line:11111111': 'title: Existing'})
        self.assertTrue(targets[0]['targetPresent'])
        self.assertIsNotNone(targets[0]['matchingEmbeddedTitle'])

    def test_unexpected_transfer_operand_is_rejected(self):
        bad = instruction(16, field_bytes(1, b'Missing') + field_int(2, 1))
        with self.assertRaisesRegex(ValueError, 'unexpected node-transfer operands'):
            audit.inspect_program({'Scene': node('Scene', bad)}, {})

    def test_unknown_line_id_is_rejected(self):
        line = instruction(3, field_bytes(1, b'line:11111111'))
        with self.assertRaisesRegex(ValueError, 'unknown RunLine ID'):
            audit.inspect_program({'Scene': node('Scene', line)}, {})


if __name__ == '__main__':
    unittest.main()
