import unittest

import map_yarn_context as mapping


def varint(n):
    out = bytearray()
    while n >= 128:
        out.append((n & 127) | 128)
        n >>= 7
    return bytes(out) + bytes([n])


def field_bytes(number, value):
    return varint(number * 8 + 2) + varint(len(value)) + value


def field_int(number, value):
    return varint(number * 8) + varint(value)


def instruction(op, operands):
    return field_bytes(7, field_bytes(op, operands))


def node(name, *instructions):
    return field_bytes(1, name.encode()) + b''.join(instructions)


class YarnContextMappingTests(unittest.TestCase):
    def test_line_and_conditional_option_are_bound_to_their_node(self):
        line = field_bytes(1, b'line:12345678') + field_int(2, 2)
        option = field_bytes(1, b'line:abcdef01') + field_int(2, 5) + field_int(4, 1)
        nodes = {'Scene': node('Scene', instruction(3, line), instruction(5, option))}
        result, hashes = mapping.map_nodes(nodes, ['line:12345678', 'line:abcdef01'])
        self.assertEqual(result['line:12345678'], {'node': 'Scene', 'instructionIndex': 0,
                         'kind': 'line', 'substitutionCount': 2})
        self.assertEqual(result['line:abcdef01'], {'node': 'Scene', 'instructionIndex': 1,
                         'kind': 'option', 'substitutionCount': 0, 'destination': 5,
                         'hasCondition': True})
        self.assertEqual(len(hashes['Scene']), 64)

    def test_duplicate_id_is_rejected(self):
        line = instruction(3, field_bytes(1, b'line:12345678'))
        with self.assertRaisesRegex(ValueError, 'invalid or duplicated line ID'):
            mapping.map_nodes({'Scene': node('Scene', line, line)}, ['line:12345678'])

    def test_unknown_operand_is_rejected(self):
        line = instruction(3, field_bytes(1, b'line:12345678') + field_int(9, 1))
        with self.assertRaisesRegex(ValueError, 'unexpected line operands'):
            mapping.map_nodes({'Scene': node('Scene', line)}, ['line:12345678'])

    def test_missing_table_id_is_rejected(self):
        line = instruction(3, field_bytes(1, b'line:12345678'))
        with self.assertRaisesRegex(ValueError, 'line inventory mismatch: 1 missing, 0 unknown'):
            mapping.map_nodes({'Scene': node('Scene', line)}, ['line:12345678', 'line:abcdef01'])

    def test_unknown_instruction_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unexpected instruction'):
            mapping.map_nodes({'Scene': node('Scene', instruction(24, b''))}, [])


if __name__ == '__main__':
    unittest.main()
