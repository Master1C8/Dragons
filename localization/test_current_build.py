from copy import deepcopy
import unittest

from current_build import relative_path, replace_checked


class CurrentBuildTests(unittest.TestCase):
    def test_leaf_edit_preserves_new_game_fields_and_other_options(self):
        current = {'label': {'backupString': 'Audio', 'newGameField': 42},
                   'dropdownOptions': [{'backupString': 'Off'}, {'backupString': 'On'}]}
        expected = deepcopy(current)
        expected['label']['backupString'] = 'Звук'
        replace_checked(current, ['label', 'backupString'], 'Audio', 'Звук')
        self.assertEqual(current, expected)
        replace_checked(current, ['dropdownOptions', 1, 'backupString'], 'On', 'Вкл.')
        self.assertEqual(current['dropdownOptions'][0], {'backupString': 'Off'})

    def test_changed_source_is_rejected_before_the_leaf_is_overwritten(self):
        current = {'label': {'backupString': 'Master Volume', 'newGameField': 42}}
        before = deepcopy(current)
        with self.assertRaisesRegex(ValueError, 'Source value changed'):
            replace_checked(current, ['label', 'backupString'], 'Audio', 'Звук')
        self.assertEqual(current, before)
        replace_checked(current, ['label', 'backupString'], 'Master Volume', 'Общая громкость')
        self.assertEqual(current['label']['newGameField'], 42)

    def test_input_paths_reject_escape_and_ambiguous_spelling(self):
        self.assertEqual(str(relative_path('Managed/Assembly-CSharp.dll')), 'Managed/Assembly-CSharp.dll')
        for value in ('../outside', '/absolute', 'a/../b', 'a//b', './a', 'C:/game', 'a\\b', ''):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, 'Unsafe build input path'):
                relative_path(value)


if __name__ == '__main__':
    unittest.main()
