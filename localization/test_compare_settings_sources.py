import unittest
from unittest.mock import patch

import compare_settings_sources as comparison


class SettingsSourceComparisonTests(unittest.TestCase):
    def test_resolution_options_are_preserved_but_label_is_candidate(self):
        tree = {'m_Name': 'Resolution', 'label': {'backupString': 'Resolution'},
                'dropdownOptions': [{'backupString': '1024x768_60'}]}
        with patch.object(comparison.settings, 'ensure_unbound'):
            record = comparison.collect({12: tree}, {12: 'SettingResolution'}, True)['Resolution']
        self.assertEqual(record['fields']['label']['provisionalRole'], 'candidate')
        self.assertEqual(record['fields']['option:0']['provisionalRole'], 'preserve-exactly')
        self.assertEqual(record['fields']['option:0']['source'], '1024x768_60')

    def test_missing_platform_is_retained(self):
        row = comparison.compare({'Camera': {'type': 'SettingFloat', 'fields': {}}}, {})['Camera']
        self.assertIsNotNone(row['macos'])
        self.assertIsNone(row['windows'])

    def test_mismatched_types_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'setting type differs'):
            comparison.compare({'Camera': {'type': 'A'}}, {'Camera': {'type': 'B'}})

    def test_duplicate_asset_names_are_rejected(self):
        value = {'m_Name': 'Repeat', 'label': {'backupString': ''}}
        with patch.object(comparison.settings, 'ensure_unbound'), \
             self.assertRaisesRegex(ValueError, 'duplicate setting name'):
            comparison.collect({1: value, 2: value}, {1: 'SettingGroup', 2: 'SettingGroup'})


if __name__ == '__main__':
    unittest.main()
