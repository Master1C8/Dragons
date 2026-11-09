import json
from pathlib import Path
import tempfile
import unittest

import inventory_non_yarn_scope as scope
import managed_fallback
from assemble_source_inventory import INVENTORY_NAME
import map_ui_hierarchy
import ui_locale

INVENTORY = Path(__file__).parent / 'work/source-inventory-20261107' / INVENTORY_NAME
DATA = {
    'macos': Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data",
    'windows': Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data'),
}


@unittest.skipUnless(INVENTORY.is_file() and all(p.is_dir() for p in DATA.values()),
                     'paired source inventory and pinned game builds required')
class NonYarnScopeTests(unittest.TestCase):
    def test_scope_and_complete_inputs_on_both_builds(self):
        entries = scope.load_pinned(INVENTORY, scope.INVENTORY_SHA)['entries']
        for platform, data in DATA.items():
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                (root / 'ui').mkdir()
                hashes = ui_locale.ASSETS if platform == 'macos' else map_ui_hierarchy.WINDOWS_ASSETS
                report = scope.verify_platform(entries, platform, data)
                self.assertEqual(sum(len(r['translate']) for r in report['ui'].values()), 58 if platform == 'macos' else 82)
                self.assertEqual(sum(len(r['preserve']) for r in report['ui'].values()), 80)
                self.assertEqual(len(report['settings']['translate']), 37 if platform == 'macos' else 31)
                self.assertEqual(len(report['settings']['preserve']), 43)
                self.assertEqual({k: len(v) for k, v in report['managed'].items()}, {'slot-new': 3, 'yarn-missing-line': 2})
                values = {r['location'][platform]: r['source'][platform] for r in entries
                          if r['family'] in ('ui', 'settings') and r['location'][platform] is not None}

                def write(path, digest, rows):
                    path.write_text(json.dumps({'schema': 1, 'locale': 'ru', 'sourceObjectSha256': digest,
                                                'lines': {k: {'source': v, 'text': v} for k, v in rows.items()}}),
                                    encoding='utf-8')

                for asset, group in report['ui'].items():
                    if group['translate']:
                        write(root / 'ui' / f'{asset}.json', hashes[asset], {k: values[k] for k in group['translate']})
                write(root / 'settings.json', hashes['sharedassets0.assets'],
                      {k: values[k] for k in report['settings']['translate']})
                write(root / 'slot-new.json', managed_fallback.SLOT_SOURCES[platform], managed_fallback.SLOT)
                write(root / 'missing-line.json', managed_fallback.SOURCES[platform], managed_fallback.FALLBACK)
                result = scope.verify_platform(entries, platform, data, 'ru', root)
                self.assertEqual(len(result['localeInputSha256']),
                                 3 + sum(bool(r['translate']) for r in report['ui'].values()))
                missing, *rest = report['settings']['translate']
                write(root / 'settings.json', hashes['sharedassets0.assets'], {k: values[k] for k in rest})
                with self.assertRaisesRegex(ValueError, f'missing 1 IDs: {missing}'):
                    scope.verify_platform(entries, platform, data, 'ru', root)
