import json
from pathlib import Path
import shutil
import tempfile
import unittest

import UnityPy
import credit_name_preservation as credits
import dialogue_locale as dl
import ui_locale as mac_ui
import windows_ui_locale as windows_ui
import map_ui_hierarchy as ui_map

ROOT = Path(__file__).parent
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


class CreditManifestTests(unittest.TestCase):
    def test_manifest_matches_complete_pinned_role_report(self):
        manifest = json.loads(credits.MANIFEST.read_text())
        report_path = ROOT / 'evidence/ui-source-roles-20261107.json'
        self.assertEqual(dl.sha(report_path.read_bytes()), manifest['sourceRoleReportSha256'])
        report = json.loads(report_path.read_text())
        candidates = [row for row in report['entries']
                      if row['provisionalRole'] == 'credit-name-preserve-candidate']
        self.assertEqual(len(candidates), 34)
        expected = {(tuple(row['hierarchy']), row['macos']['id'], row['windows']['id'],
                     row['macos']['sourceTextSha256'], row['windows']['sourceTextSha256'])
                    for row in candidates}
        actual = {(tuple(row['hierarchy']), row['ids']['macos'], row['ids']['windows'],
                   row['sourceSha256'], dl.sha(row['source'].encode('utf-8')))
                  for row in manifest['entries']}
        self.assertEqual(len(expected), 34)
        self.assertEqual(len(actual), 34)
        self.assertEqual(actual, expected)


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned game builds required')
class CreditNameTests(unittest.TestCase):
    def test_exact_names_and_unrelated_description(self):
        manifest = json.loads(credits.MANIFEST.read_text())
        for platform, source, scanner in (('macos', MAC, mac_ui.scan), ('windows', WIN, windows_ui.scan)):
            with self.subTest(platform=platform):
                _, rows = scanner(source, 'level2')
                values = {k: value[2] for k, value in rows.items()}
                credits.validate(platform, 'level2', values, {})
                first = manifest['entries'][0]
                key = first['ids'][platform]
                credits.validate(platform, 'level2', values, {key: first['source']})
                with self.assertRaisesRegex(ValueError, 'credit name must remain exact'):
                    credits.validate(platform, 'level2', values, {key: first['source'] + 'x'})
                bad_source = dict(values)
                bad_source[key] += 'x'
                with self.assertRaisesRegex(ValueError, 'credit-name source mismatch'):
                    credits.validate(platform, 'level2', bad_source, {})
                description = next(k for k, v in values.items() if v == 'GDC Bundle Part 4')
                credits.validate(platform, 'level2', values, {description: 'Other description'})

    def test_both_actual_adapters_reject_name_before_output(self):
        first = json.loads(credits.MANIFEST.read_text())['entries'][0]
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for platform, source in (('macos', MAC), ('windows', WIN)):
                with self.subTest(platform=platform):
                    digest = mac_ui.ASSETS['level2'] if platform == 'macos' else ui_map.WINDOWS_ASSETS['level2']
                    key = first['ids'][platform]
                    locale = root / f'{platform}.json'
                    locale.write_text(json.dumps({'schema': 1, 'locale': 'ru', 'sourceObjectSha256': digest,
                                                  'lines': {key: {'source': first['source'], 'text': first['source'] + 'x'}}}),
                                      encoding='utf-8')
                    output = root / f'{platform}.assets'
                    with self.assertRaisesRegex(ValueError, 'credit name must remain exact'):
                        if platform == 'macos':
                            mac_ui.patch_into(source, 'level2', locale, 'ru', output)
                        else:
                            windows_ui.build(source, 'level2', locale, 'ru', output)
                    self.assertFalse(output.exists())

    def test_both_adapters_allow_non_name_and_preserve_all_names(self):
        names = json.loads(credits.MANIFEST.read_text())['entries']
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for platform, source, scanner in (('macos', MAC, mac_ui.scan), ('windows', WIN, windows_ui.scan)):
                with self.subTest(platform=platform):
                    _, rows = scanner(source, 'level2')
                    target_id = next(k for k, v in rows.items() if v[2] == 'Sound Attribution\n')
                    digest = mac_ui.ASSETS['level2'] if platform == 'macos' else ui_map.WINDOWS_ASSETS['level2']
                    locale = root / f'positive-{platform}.json'
                    locale.write_text(json.dumps({'schema': 1, 'locale': 'ru', 'sourceObjectSha256': digest,
                                                  'lines': {target_id: {'source': 'Sound Attribution\n', 'text': 'SYNTHETIC'}}}),
                                      encoding='utf-8')
                    output = root / f'positive-{platform}.assets'
                    if platform == 'macos':
                        shutil.copyfile(source / 'level2', output)
                        mac_ui.patch_into(source, 'level2', locale, 'ru', output)
                    else:
                        windows_ui.build(source, 'level2', locale, 'ru', output)
                    env = UnityPy.load(str(output))
                    objects = {o.path_id: o for o in env.objects}
                    changed_id = int(target_id.split('#')[1])
                    self.assertEqual(dl.read_string(objects[changed_id].get_raw_data(), 88)[0], 'SYNTHETIC')
                    for row in names:
                        obj_id = int(row['ids'][platform].split('#')[1])
                        self.assertEqual(dl.read_string(objects[obj_id].get_raw_data(), 88)[0], row['source'])


if __name__ == '__main__':
    unittest.main()
