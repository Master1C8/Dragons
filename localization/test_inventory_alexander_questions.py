import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import inventory_alexander_questions as inventory
from test_map_yarn_context import field_bytes, field_int


class AlexanderQuestionInventoryTests(unittest.TestCase):
    def test_initial_boolean_values_preserve_false_and_true(self):
        false_value = field_bytes(1, b'$flag') + field_bytes(2, field_int(2, 0))
        true_value = field_bytes(1, b'$other') + field_bytes(2, field_int(2, 1))
        actual = inventory.initial_values([(3, 2, false_value), (3, 2, true_value)])
        self.assertEqual(actual['$flag'], [(2, 0, 0)])
        self.assertEqual(actual['$other'], [(2, 0, 1)])

    def test_duplicate_initial_key_is_rejected(self):
        value = field_bytes(1, b'$flag') + field_bytes(2, field_int(2, 0))
        with self.assertRaisesRegex(ValueError, 'duplicated program initial value'):
            inventory.initial_values([(3, 2, value), (3, 2, value)])

    @unittest.skipUnless(Path("/Users/antonkrutov/Documents/Drag'N Wash.app/Contents/Resources/Data/sharedassets1.assets").exists(),
                         'pinned original macOS game is unavailable')
    def test_crest_size_tags_cannot_be_reordered(self):
        root = Path("/Users/antonkrutov/Documents/Drag'N Wash.app/Contents/Resources/Data")
        keys, values, *_ = inventory.versions.load(root, inventory.versions.BUILDS['macos'])
        line_id = 'line:8ee41fdc'
        source = dict(zip(keys, values))[line_id]
        self.assertEqual(inventory.dl.TAGS.findall(source)[:2], ['<size=85%>', '<size=70%>'])
        changed = source.replace('<size=85%>', '<size=TMP>', 1).replace('<size=70%>', '<size=85%>', 1).replace('<size=TMP>', '<size=70%>', 1)
        doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': inventory.dl.OBJECT_HASH,
               'lines': {line_id: {'source': source, 'text': source}}}
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'locale.json'
            path.write_text(json.dumps(doc, ensure_ascii=False))
            self.assertEqual(inventory.dl.read_locale(path, keys, values)[1][line_id], source)
            doc['lines'][line_id]['text'] = changed
            path.write_text(json.dumps(doc, ensure_ascii=False))
            with self.assertRaisesRegex(ValueError, 'markup order differs'):
                inventory.dl.read_locale(path, keys, values)

    @unittest.skipUnless(Path("/Users/antonkrutov/Documents/Drag'N Wash.app/Contents/Resources/Data/sharedassets1.assets").exists(),
                         'pinned original macOS game is unavailable')
    def test_original_group_coverage_and_changed_control_guard(self):
        root = Path("/Users/antonkrutov/Documents/Drag'N Wash.app/Contents/Resources/Data")
        result = inventory.extract(root, 'macos')
        self.assertEqual(result['sourceLineCount'], 77)
        self.assertEqual(len(result['groups']), 7)
        self.assertEqual(result['sharedExit']['conditionVariable'], '$has_asked_question')
        original = inventory.versions.load(root, inventory.versions.BUILDS['macos'])
        keys, values, extras, program, nodes, other = original
        old = b'$Yarn.Internal.Once.line:c2bdc402'
        new = b'$Yarn.Internal.Once.line:c2bdc403'
        self.assertEqual(nodes[inventory.NODE].count(old), 2)
        changed = dict(nodes)
        changed[inventory.NODE] = changed[inventory.NODE].replace(old, new, 1)
        with patch.object(inventory.versions, 'load', return_value=(keys, values, extras, program, changed, other)), \
             patch.object(inventory, 'NODE_SHA', inventory.dl.sha(changed[inventory.NODE])), \
             self.assertRaisesRegex(ValueError, 'unexpected control instruction at 12'):
            inventory.extract(root, 'macos')


if __name__ == '__main__':
    unittest.main()
