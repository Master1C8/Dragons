import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import inventory_romance_routes as inventory


class RomanceRouteInventoryTests(unittest.TestCase):
    def test_conditional_choice_destination_and_flag_value_are_checked(self):
        rows = [(5, [(1, 2, b'line:11111111'), (2, 0, 5), (4, 0, 1)]),
                (9, []), (14, [(1, 2, b'$choice')])]
        inventory.assert_choice(rows, 0, 'line:11111111', 5, True)
        inventory.assert_write(rows, 1, '$choice', False)
        with self.assertRaisesRegex(ValueError, 'unexpected control instruction at 0'):
            inventory.assert_choice(rows, 0, 'line:11111111', 6, True)
        with self.assertRaisesRegex(ValueError, 'unexpected control instruction at 1'):
            inventory.assert_write(rows, 1, '$choice', True)

    @unittest.skipUnless(Path("/Users/antonkrutov/Documents/Drag'N Wash.app/Contents/Resources/Data/sharedassets1.assets").exists(),
                         'pinned original macOS game is unavailable')
    def test_pivotal_choice_markup_order_is_protected(self):
        root = Path("/Users/antonkrutov/Documents/Drag'N Wash.app/Contents/Resources/Data")
        keys, values, *_ = inventory.versions.load(root, inventory.versions.BUILDS['macos'])
        source = dict(zip(keys, values))
        ids = ['line:a0e49f02', 'line:0371fb9c', 'line:36ff6bd9', 'line:7e9d40e6',
               'line:bedc761d', 'line:e104b8e4', 'line:f5a81524']
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'locale.json'
            for line_id in ids:
                with self.subTest(line_id=line_id):
                    value = source[line_id]
                    tags = inventory.dl.TAGS.findall(value)
                    self.assertGreaterEqual(len(tags), 2)
                    self.assertNotEqual(tags[0], tags[1])
                    changed = value.replace(tags[0], '<TEMP_TAG>', 1).replace(tags[1], tags[0], 1).replace('<TEMP_TAG>', tags[1], 1)
                    doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': inventory.dl.OBJECT_HASH,
                           'lines': {line_id: {'source': value, 'text': value}}}
                    path.write_text(json.dumps(doc, ensure_ascii=False))
                    self.assertEqual(inventory.dl.read_locale(path, keys, values)[1][line_id], value)
                    doc['lines'][line_id]['text'] = changed
                    path.write_text(json.dumps(doc, ensure_ascii=False))
                    with self.assertRaisesRegex(ValueError, 'markup order differs'):
                        inventory.dl.read_locale(path, keys, values)

    @unittest.skipUnless(Path("/Users/antonkrutov/Documents/Drag'N Wash.app/Contents/Resources/Data/sharedassets1.assets").exists(),
                         'pinned original macOS game is unavailable')
    def test_original_closure_and_changed_branch_destination_guard(self):
        root = Path("/Users/antonkrutov/Documents/Drag'N Wash.app/Contents/Resources/Data")
        original = inventory.extract(root, 'macos')
        self.assertEqual(len(original['directNodes']), 16)
        self.assertEqual(len(original['staticTransferClosure']), 38)
        self.assertEqual(original['sourceLineCount'], 708)
        self.assertEqual(original['unresolvedNamedTargets'], [])
        keys, values, extras, program, nodes, other = inventory.versions.load(root, inventory.versions.BUILDS['macos'])
        before = b'line:36ff6bd9\x10\x15'
        after = b'line:36ff6bd9\x10\x16'
        self.assertEqual(nodes['Conrad_Outro_3'].count(before), 1)
        changed = dict(nodes)
        changed['Conrad_Outro_3'] = changed['Conrad_Outro_3'].replace(before, after, 1)
        with patch.object(inventory.versions, 'load', return_value=(keys, values, extras, program, changed, other)), \
             self.assertRaisesRegex(ValueError, 'unexpected control instruction at 15'):
            inventory.extract(root, 'macos')


if __name__ == '__main__':
    unittest.main()
