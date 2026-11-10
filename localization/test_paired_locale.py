import json
from pathlib import Path
import tempfile
import unittest

import paired_locale


class PairedLocaleTests(unittest.TestCase):
    def test_shared_and_platform_specific_values(self):
        same = {'macos': {'source': 'Yes'}, 'windows': {'source': 'Yes'}}
        different = {'macos': {'source': 'Yes'}, 'windows': {'source': 'Okay'}}
        self.assertEqual(paired_locale.resolve('both', same, 'Да'), {'macos': 'Да', 'windows': 'Да'})
        self.assertEqual(paired_locale.resolve('only', {'macos': same['macos']}, 'Да'), {'macos': 'Да'})
        split = {'macos': 'Да', 'windows': 'Хорошо'}
        self.assertEqual(paired_locale.resolve('both', different, {'platforms': split}), split)
        confirmed = {'text': 'Хорошо', 'sharedAcrossSourceVariants': True}
        self.assertEqual(paired_locale.resolve('both', different, confirmed),
                         {'macos': 'Хорошо', 'windows': 'Хорошо'})
        with self.assertRaisesRegex(ValueError, 'explicit confirmation'):
            paired_locale.resolve('both', different, 'Да')
        with self.assertRaisesRegex(ValueError, 'must match source platforms'):
            paired_locale.resolve('both', different, {'platforms': {'macos': 'Да'}})

    def test_coverage_and_materialization_keep_platform_source_and_destination(self):
        bindings = {
            'macos': {'file': 'dialogue.json', 'key': 'mac-key', 'source': 'Yes'},
            'windows': {'file': 'dialogue.json', 'key': 'win-key', 'source': 'Okay'},
        }
        rows = {'both': {'builds': bindings}, 'only': {'builds': {'macos': {
            'file': 'dialogue.json', 'key': 'exclusive', 'source': 'Maybe',
        }}}}
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = root / 'shared.json'
            doc = paired_locale.template('uk', 'scope', rows)
            self.assertEqual(doc['lines'], {'both': {'platforms': {'macos': '', 'windows': ''}}, 'only': ''})
            path.write_text(json.dumps(doc), encoding='utf-8')
            self.assertEqual(paired_locale.read(path, 'uk', 'scope', rows, complete=False),
                             {'both': {}, 'only': {}})
            with self.assertRaisesRegex(ValueError, 'both: translation must be nonempty'):
                paired_locale.read(path, 'uk', 'scope', rows)

            doc['lines']['both']['platforms']['windows'] = 'Гаразд'
            path.write_text(json.dumps(doc), encoding='utf-8')
            self.assertEqual(paired_locale.read(path, 'uk', 'scope', rows, complete=False)['both'],
                             {'windows': 'Гаразд'})

            doc['lines']['both']['platforms']['macos'] = 'Так'
            del doc['lines']['only']
            path.write_text(json.dumps(doc), encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'missing 1 shared locale IDs: only'):
                paired_locale.read(path, 'uk', 'scope', rows)
            doc['lines']['only'] = 'Можливо'
            path.write_text(json.dumps(doc), encoding='utf-8')
            translations = paired_locale.read(path, 'uk', 'scope', rows)
            target = root / 'windows'
            paired_locale.materialize(target, 'windows', 'uk', {
                'sourceFingerprints': {'dialogue.json': 'windows-hash'},
            }, rows, translations)
            self.assertEqual(json.loads((target / 'dialogue.json').read_bytes()), {
                'schema': 1, 'locale': 'uk', 'sourceObjectSha256': 'windows-hash',
                'lines': {'win-key': {'source': 'Okay', 'text': 'Гаразд'}},
            })
