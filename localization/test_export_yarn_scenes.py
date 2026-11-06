import unittest
from unittest.mock import patch

import dialogue_locale as dl
import export_yarn_scenes as exporter


class SceneExportTests(unittest.TestCase):
    def fixture(self):
        location = {'node': 'Scene', 'instructionIndex': 4, 'kind': 'option',
                    'substitutionCount': 0, 'destination': 7, 'hasCondition': True}
        record = {'macos': location.copy(), 'windows': location.copy(),
                  'sourceSha256': {'macos': dl.sha(b'new'), 'windows': dl.sha(b'old')}}
        context = {'lineIds': {'line:12345678': record}, 'builds': {}, 'programSha256': {}}
        mac = (['line:12345678'], ['new'])
        win = (['line:12345678'], ['old'])
        return context, mac, win

    def test_distinct_build_texts_and_option_context_are_preserved(self):
        context, mac, win = self.fixture()
        with patch.object(exporter.mapping, 'build', return_value=context), \
             patch.object(exporter.mapping, 'load_platform', side_effect=[mac, win]):
            result = exporter.export('mac', 'windows')
        self.assertEqual(result['sourceLineCount'], 1)
        item = result['scenes']['Scene'][0]
        self.assertEqual(item['source'], {'macos': 'new', 'windows': 'old'})
        self.assertEqual((item['instructionIndex'], item['destination'], item['hasCondition']), (4, 7, True))

    def test_cross_platform_location_change_requires_reconciliation(self):
        context, mac, win = self.fixture()
        context['lineIds']['line:12345678']['windows']['instructionIndex'] = 5
        with patch.object(exporter.mapping, 'build', return_value=context), \
             patch.object(exporter.mapping, 'load_platform', side_effect=[mac, win]), \
             self.assertRaisesRegex(ValueError, 'platform location differs'):
            exporter.export('mac', 'windows')

    def test_changed_source_value_is_rejected(self):
        context, mac, win = self.fixture()
        win = (win[0], ['changed'])
        with patch.object(exporter.mapping, 'build', return_value=context), \
             patch.object(exporter.mapping, 'load_platform', side_effect=[mac, win]), \
             self.assertRaisesRegex(ValueError, 'source text fingerprint differs'):
            exporter.export('mac', 'windows')


if __name__ == '__main__':
    unittest.main()
