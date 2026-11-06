import unittest

import compare_ui_hierarchy as comparison


def item(name, digest):
    return {'sourceTextSha256': digest, 'gameObjectChain': [{'name': name}]}


class UIHierarchyComparisonTests(unittest.TestCase):
    def test_same_path_can_have_different_source_text(self):
        rows = comparison.compare_records({'level1#1': item('Title', 'a')},
                                          {'level1#2': item('Title', 'b')})
        self.assertEqual(len(rows), 1)
        self.assertFalse(rows[0]['sameText'])
        self.assertEqual(rows[0]['macos']['id'], 'level1#1')
        self.assertEqual(rows[0]['windows']['id'], 'level1#2')

    def test_windows_only_fields_remain_in_output(self):
        rows = comparison.compare_records({}, {'level1#2': item('Title', 'b')})
        self.assertIsNone(rows[0]['macos'])
        self.assertIsNone(rows[0]['sameText'])
        self.assertEqual(rows[0]['windows']['id'], 'level1#2')

    def test_ambiguous_name_path_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'ambiguous same-name hierarchy'):
            comparison.compare_records({'level1#1': item('Title', 'a'),
                                        'level1#2': item('Title', 'b')}, {})

    def test_same_path_in_different_assets_is_not_merged(self):
        rows = comparison.compare_records({'level1#1': item('Title', 'a'),
                                           'level2#1': item('Title', 'a')}, {})
        self.assertEqual(len(rows), 2)


if __name__ == '__main__':
    unittest.main()
