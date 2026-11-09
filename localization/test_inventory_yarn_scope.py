import json
from pathlib import Path
import tempfile
import unittest

import compare_yarn_versions as versions
import inventory_yarn_scope as scope
import managed_fallback
from assemble_source_inventory import INVENTORY_NAME
from speaker_locale import ALEXANDER

INVENTORY = Path(__file__).parent / 'work/source-inventory-20261107' / INVENTORY_NAME
DATA = {
    'macos': Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data",
    'windows': Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data'),
}


@unittest.skipUnless(INVENTORY.is_file() and all(path.is_dir() for path in DATA.values()),
                     'pinned paired source inventory and installed builds required')
class YarnScopeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = scope.build(INVENTORY, DATA)

    def test_repaired_graph_and_conservative_locale_scope(self):
        self.assertEqual(self.report['localeInputCounts'], {
            'dialogue-locale': 1823, 'exact-only': 15, 'speaker-locale': 1,
        })
        for platform, build in self.report['builds'].items():
            self.assertEqual(sum(build['rootClasses'].values()), 123)
            self.assertEqual(len(build['roots']), 95)
            self.assertEqual(len(build['original']['allUnresolvedTargets']), 5)
            self.assertEqual(build['original']['reachableTextCount'], 1593 if platform == 'macos' else 1607)
            self.assertEqual(build['repaired']['reachableTextCount'], 1593)
            self.assertEqual(build['repaired']['allUnresolvedTargets'], [])
        rows = self.report['rows']
        self.assertEqual(sum('preserveExactValue' in row for row in rows), 16)
        self.assertEqual(sum('preserveExactPrefix' in row for row in rows), 18)
        self.assertEqual(sum(row.get('platformSourceDiffers', False) for row in rows), 25)
        special = next(row for row in rows if row['id'] == ALEXANDER)
        self.assertEqual(special['localeInput'], 'speaker-locale')
        self.assertEqual(special['repairedNamedReachableOn'], [])

    def test_complete_structure_requires_unrooted_dialogue_and_special_body(self):
        platform = 'macos'
        data = DATA[platform]
        spec = versions.BUILDS[platform]
        keys, values, _, _, _, _ = versions.load(data, spec)
        source = dict(zip(keys, values))
        rows = self.report['rows']
        ordinary = {r['id']: {'source': source[r['id']], 'text': source[r['id']]}
                    for r in rows if r['localeInput'] == 'dialogue-locale'}
        unrooted = next(r['id'] for r in rows if r['id'] in ordinary and not r['repairedNamedReachableOn'])
        exact = next(r['id'] for r in rows if r['localeInput'] is None)
        names = {'speaker-ryan': {'source': 'Ryan', 'text': 'Жж'},
                 'speaker-conrad': {'source': 'Conrad', 'text': 'Ъъ'}}
        with tempfile.TemporaryDirectory() as folder:
            dialogue = Path(folder) / 'dialogue.json'
            speakers = Path(folder) / 'speakers.json'

            def write(path, digest, lines):
                path.write_text(json.dumps({'schema': 1, 'locale': 'ru', 'sourceObjectSha256': digest,
                                            'lines': lines}), encoding='utf-8')

            def validate():
                return scope.validate_complete(self.report, platform, data, 'ru', dialogue, speakers)

            write(dialogue, spec['localizationSha256'], ordinary)
            write(speakers, managed_fallback.SOURCES[platform], names)
            with self.assertRaisesRegex(ValueError, f'missing {ALEXANDER} in the speaker locale'):
                validate()
            write(speakers, managed_fallback.SOURCES[platform],
                  names | {ALEXANDER: {'source': source[ALEXANDER], 'text': 'ЖЪЬ:'}})
            receipt = validate()
            self.assertEqual((receipt['dialogueIds'], receipt['specialDisplayIds'], receipt['speakerNames']),
                             (1823, 1, 2))
            self.assertEqual(set(receipt['inputSha256']), {'dialogue', 'speakers'})
            write(dialogue, spec['localizationSha256'], {k: v for k, v in ordinary.items() if k != unrooted})
            with self.assertRaisesRegex(ValueError, f'missing 1 dialogue IDs: {unrooted}'):
                validate()
            write(dialogue, spec['localizationSha256'],
                  ordinary | {exact: {'source': source[exact], 'text': 'Changed'}})
            with self.assertRaisesRegex(ValueError, exact):
                validate()
