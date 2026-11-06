"""Integration checks for the source-pinned settings adapter."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SOURCE = Path(os.environ.get('DRAGNWASH_SOURCE_DATA', str(
    Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data")))
SCRIPT = Path(__file__).with_name('settings_locale.py')
SITE_CATALOG = Path.home() / 'Desktop/SiteForMods/lib/language-data/site-locales.ts'
READY = (SOURCE.is_dir() and SITE_CATALOG.is_file()
         and importlib.util.find_spec('UnityPy') is not None
         and importlib.util.find_spec('TypeTreeGeneratorAPI') is not None)


@unittest.skipUnless(READY, 'pinned game, site catalog, and settings probe dependencies required')
class SettingsAdapterIntegrationTests(unittest.TestCase):
    def run_adapter(self, locale, target):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(SOURCE), '--locale', str(locale),
             '--requested-locale', 'ru', '--output', str(target)],
            text=True, capture_output=True, check=False)

    def write_locale(self, path, key, source, text):
        path.write_text(json.dumps({
            'schema': 1, 'locale': 'ru',
            'sourceObjectSha256': '40713b00ce12582eebc427c0104e59becf438eb15803725b2248be3471a96aeb',
            'lines': {key: {'source': source, 'text': text}},
        }, ensure_ascii=False), encoding='utf-8')

    def test_synthetic_label_matches_the_verified_runtime_probe(self):
        import hashlib
        with tempfile.TemporaryDirectory(prefix='dragnwash-setting-test-') as directory:
            root = Path(directory)
            locale, output = root / 'ru.json', root / 'output.assets'
            self.write_locale(locale, 'sharedassets0.assets#606:label', 'Invert Look Y', 'ЖЮЯ 427')
            result = self.run_adapter(locale, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(),
                             '4a8a8c6bafdfd9a671d48d0a7acde8f8da3f08bbd8dc7da43cc9b38ecfdcb622')
            repeated = self.run_adapter(locale, output)
            self.assertNotEqual(repeated.returncode, 0)
            self.assertIn('FileExistsError', repeated.stderr)
            self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(),
                             '4a8a8c6bafdfd9a671d48d0a7acde8f8da3f08bbd8dc7da43cc9b38ecfdcb622')

    def test_resolution_value_is_rejected_at_the_protected_field_guard(self):
        with tempfile.TemporaryDirectory(prefix='dragnwash-setting-test-') as directory:
            root = Path(directory)
            locale, output = root / 'ru.json', root / 'output.assets'
            self.write_locale(locale, 'sharedassets0.assets#619:option:0', '640x480_60', '640x480_61')
            result = self.run_adapter(locale, output)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('unknown line IDs: sharedassets0.assets#619:option:0', result.stderr)
            self.assertFalse(output.exists())

    def test_option_translation_preserves_index_and_every_other_setting_field(self):
        from copy import deepcopy
        import hashlib
        import UnityPy
        import settings_locale as settings
        with tempfile.TemporaryDirectory(prefix='dragnwash-setting-option-') as directory:
            root = Path(directory)
            locale, output = root / 'ru.json', root / 'output.assets'
            self.write_locale(locale, 'sharedassets0.assets#606:option:1', 'On', 'ЖЮЯ 427')
            result = self.run_adapter(locale, output)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(),
                             '8d42bd11daf40e5ddf0b8fd310b31d27f2201ff2da49b81dbfe22afbf87b96e1')
            _, _, original_trees, schemas, _, _ = settings.scan(SOURCE)
            saved = UnityPy.load(str(output))
            obj = next(o for o in saved.objects if o.path_id == 606)
            after = obj.read_typetree(nodes=schemas[606], check_read=True)
            self.assertEqual(after['dropdownOptions'][1]['backupString'], 'ЖЮЯ 427')
            restored = deepcopy(after)
            restored['dropdownOptions'][1]['backupString'] = 'On'
            self.assertEqual(restored, original_trees[606])

    def test_export_inside_source_directory_is_rejected_before_reading_inputs(self):
        with tempfile.TemporaryDirectory(prefix='dragnwash-setting-source-') as directory:
            source = Path(directory)
            destination = source / 'output.json'
            result = subprocess.run([sys.executable, str(SCRIPT), str(source), '--export', str(destination)],
                                    text=True, capture_output=True, check=False)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('output must be outside the source data directory', result.stderr)
            self.assertFalse(destination.exists())

    def test_ui_and_settings_merge_only_when_the_prior_ui_payload_matches(self):
        import hashlib
        import shutil
        import UnityPy
        import dialogue_locale as dl
        import experimental_settings_layout as layout
        import settings_locale as settings
        import ui_locale as ui
        with tempfile.TemporaryDirectory(prefix='dragnwash-setting-merge-') as directory:
            root = Path(directory)
            settings_file, ui_file, target = root / 'settings.json', root / 'ui.json', root / 'copy.assets'
            self.write_locale(settings_file, 'sharedassets0.assets#606:label', 'Invert Look Y', 'ЖЮЯ 427')
            self.write_locale(ui_file, 'sharedassets0.assets#650', 'LABEL', 'TEST 369')
            shutil.copyfile(SOURCE / 'sharedassets0.assets', target)
            ui.patch_into(SOURCE, 'sharedassets0.assets', ui_file, 'ru', target)
            before_hash = hashlib.sha256(target.read_bytes()).hexdigest()
            prepared = settings.make_asset(SOURCE, settings_file, 'ru')
            with self.assertRaisesRegex(ValueError, r'unexpected settings target object: \(650,'):
                settings.patch_into(SOURCE, target, prepared)
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), before_hash)
            self.assertEqual(settings.patch_into(SOURCE, target, prepared, ui_file), 1)
            after = UnityPy.load(str(target))
            objects = {o.path_id: o for o in after.objects}
            self.assertEqual(dl.read_string(objects[650].get_raw_data(), 88)[0], 'TEST 369')
            self.assertEqual(objects[606].read_typetree(nodes=prepared[4][606], check_read=True)
                             ['label']['backupString'], 'ЖЮЯ 427')
            layout.patch_into(SOURCE, target, 'ru', prior_ui=ui_file, prepared_settings=prepared)
            final = UnityPy.load(str(target))
            objects = {o.path_id: o for o in final.objects}
            self.assertEqual(dl.read_string(objects[650].get_raw_data(), 88)[0], 'TEST 369')
            self.assertEqual(objects[606].read_typetree(nodes=prepared[4][606], check_read=True)
                             ['label']['backupString'], 'ЖЮЯ 427')
            self.assertEqual(objects[478].read_typetree(check_read=True)['m_SizeDelta']['y'], -3.0)

    def test_layout_experiment_requires_exact_prior_settings_and_matches_the_probe(self):
        import hashlib
        import shutil
        import experimental_settings_layout as layout
        import settings_locale as settings
        with tempfile.TemporaryDirectory(prefix='dragnwash-layout-test-') as directory:
            root = Path(directory)
            locale, target = root / 'settings.json', root / 'copy.assets'
            self.write_locale(locale, 'sharedassets0.assets#606:option:1', 'On', 'Жж Ъъ Ьь 427')
            prepared = settings.make_asset(SOURCE, locale, 'ru')
            shutil.copyfile(SOURCE / 'sharedassets0.assets', target)
            self.assertEqual(settings.patch_into(SOURCE, target, prepared), 1)
            before = hashlib.sha256(target.read_bytes()).hexdigest()
            self.assertEqual(before, '96e3f29e601a64f575be6ee60e706eabd8afb47f6b2c6803116a773518ae52fd')
            with self.assertRaisesRegex(ValueError, 'supported non-English locale'):
                layout.patch_into(SOURCE, target, 'zz', prepared_settings=prepared)
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), before)
            with self.assertRaisesRegex(ValueError, r'unexpected layout experiment target object: \(606,'):
                layout.patch_into(SOURCE, target, 'ru')
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), before)
            result = layout.patch_into(SOURCE, target, 'ru', prepared_settings=prepared)
            self.assertEqual(result, 'a06067fa117624a04a5ccb4b2bbfb912d9f0a63ac543f730c2be974acf52ffdf')


if __name__ == '__main__':
    unittest.main()
