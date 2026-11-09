"""Exercise source identity, exact read-back and failure boundaries for Windows UI."""
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import UnityPy
import compare_yarn_versions as versions
import dialogue_locale as dl
import map_ui_hierarchy as mapping
import windows_ui_locale as adapter

SOURCE = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WORK = Path(__file__).parent / 'work'
READY = SOURCE.is_dir() and MAC.is_dir() and dl.SITE_LOCALES.is_file() and WORK.is_dir()


@unittest.skipUnless(READY, 'pinned Windows/macOS builds and test work directory required')
class WindowsUIAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='windows-ui-adapter-', dir=WORK)
        self.root = Path(self.tmp.name)
        self.locale = self.root / 'ru.json'
        self.output = self.root / 'level1.test'
        self.lines = {
            'level1#3862': {'source': 'Options', 'text': 'ЖЮЯ 101'},
            'level1#3854': {'source': 'Quit', 'text': 'ЖЮЯ 102'},
            'level1#3849': {'source': 'Resume', 'text': 'ЖЮЯ 103'},
            'level1#3863': {'source': 'Pause Menu', 'text': 'ЖЮЯ 104'},
        }
        self.doc = {'schema': 1, 'locale': 'ru',
                    'sourceObjectSha256': mapping.WINDOWS_ASSETS['level1'], 'lines': self.lines}
        self.write_locale()

    def tearDown(self):
        self.tmp.cleanup()

    def write_locale(self):
        self.locale.write_text(json.dumps(self.doc, ensure_ascii=False), encoding='utf-8')

    def test_windows_only_fields_and_other_objects_are_exact(self):
        env, source_rows = adapter.scan(SOURCE, 'level1')
        self.assertEqual(len(source_rows), 18)
        before = {(x.path_id, x.type.name): x.get_raw_data() for x in env.objects}
        result = adapter.build(SOURCE, 'level1', self.locale, 'ru', self.output)
        self.assertEqual((result['availableFields'], result['changedFields']), (18, 4))
        output_bytes = self.output.read_bytes()
        self.assertEqual(dl.sha(output_bytes), result['outputSha256'])
        actual = UnityPy.load(output_bytes)
        after = {(x.path_id, x.type.name): x.get_raw_data() for x in actual.objects}
        self.assertEqual(set(before), set(after))
        for identity, raw in before.items():
            key = f'level1#{identity[0]}'
            if key in self.lines and identity[1] == 'MonoBehaviour':
                text, end = dl.read_string(raw, 88)
                self.assertEqual(text, self.lines[key]['source'])
                self.assertEqual(after[identity], raw[:88] + dl.write_string(self.lines[key]['text']) + raw[end:])
            else:
                self.assertEqual(after[identity], raw, identity)
        with self.assertRaisesRegex(ValueError, 'fresh regular file'):
            adapter.build(SOURCE, 'level1', self.locale, 'ru', self.output)
        self.assertEqual(self.output.read_bytes(), output_bytes)

    def test_all_six_windows_only_pause_scenes(self):
        evidence = json.loads((Path(__file__).parent / 'evidence/ui-hierarchy-versions-20261107.json').read_text())
        expected = {'Options': 'Ж 1', 'Quit': 'Ж 2', 'Resume': 'Ж 3', 'Pause Menu': 'Ж 4'}
        for level in range(1, 7):
            asset = f'level{level}'
            lines = {}
            for row in evidence['entries']:
                if row['asset'] != asset or row['macos'] is not None or row['windows'] is None:
                    continue
                parent = row['hierarchy'][-2]
                value = 'Pause Menu' if parent == 'Container' else parent
                self.assertIn(value, expected)
                lines[row['windows']['id']] = {'source': value, 'text': expected[value]}
            self.assertEqual(len(lines), 4, asset)
            doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': mapping.WINDOWS_ASSETS[asset], 'lines': lines}
            locale = self.root / f'{asset}.json'
            locale.write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
            output = self.root / f'{asset}.asset'
            report = adapter.build(SOURCE, asset, locale, 'ru', output)
            self.assertEqual(report['changedFields'], 4)
            objects = {o.path_id: o for o in UnityPy.load(output.read_bytes()).objects}
            for key, entry in lines.items():
                text, _ = dl.read_string(objects[int(key.split('#')[1])].get_raw_data(), 88)
                self.assertEqual(text, entry['text'], key)

    def test_main_menu_and_shared_assets_are_rebuilt(self):
        samples = {
            'level0': ('level0#5183', 'New'),
            'sharedassets0.assets': ('sharedassets0.assets#661', 'Enter text...'),
            'sharedassets1.assets': ('sharedassets1.assets#11105', 'Option Text'),
        }
        for index, (asset, (key, source)) in enumerate(samples.items()):
            with self.subTest(asset=asset):
                expected = f'ЖЮЯ {index}' if asset == 'level0' else source
                doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': mapping.WINDOWS_ASSETS[asset],
                       'lines': {key: {'source': source, 'text': expected}}}
                locale = self.root / f'sample-{index}.json'
                locale.write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
                output = self.root / f'sample-{index}.asset'
                report = adapter.build(SOURCE, asset, locale, 'ru', output)
                self.assertEqual(report['changedFields'], 1)
                objects = {o.path_id: o for o in UnityPy.load(output.read_bytes()).objects}
                text, _ = dl.read_string(objects[int(key.split('#')[1])].get_raw_data(), 88)
                self.assertEqual(text, expected)

    def make_combined_inputs(self):
        spec = versions.BUILDS['windows']
        keys, values, extras, _, _, _ = versions.load(SOURCE, spec)
        source = dict(zip(keys, values))
        line = 'line:4183ca7e'
        synthetic = "Жж Ъъ Ьь <i>'Drag'n'wash franchise 223'...</i>"
        yarn = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': spec['localizationSha256'],
                'lines': {line: {'source': source[line], 'text': synthetic}}}
        ui = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': spec['assetSha256'],
              'lines': {'sharedassets1.assets#11105': {'source': 'Option Text', 'text': 'Option Text'}}}
        yarn_path, ui_path = self.root / 'yarn.json', self.root / 'shared-ui.json'
        yarn_path.write_text(json.dumps(yarn, ensure_ascii=False), encoding='utf-8')
        ui_path.write_text(json.dumps(ui, ensure_ascii=False), encoding='utf-8')
        return yarn, yarn_path, ui_path, keys, values, extras

    def test_dialogue_and_ui_combine_without_changing_other_objects(self):
        yarn, yarn_path, ui_path, keys, values, extras = self.make_combined_inputs()
        original, rows = adapter.scan(SOURCE, 'sharedassets1.assets')
        before = {(o.path_id, o.type.name): o.get_raw_data() for o in original.objects}
        output = self.root / 'combined.assets'
        result = adapter.build(SOURCE, 'sharedassets1.assets', ui_path, 'ru', output,
                               dialogue_locale_file=yarn_path)
        self.assertEqual((result['changedFields'], result['dialogueFields']), (1, 1))
        actual = UnityPy.load(output.read_bytes())
        after = {(o.path_id, o.type.name): o.get_raw_data() for o in actual.objects}
        self.assertEqual(before.keys(), after.keys())
        spec = versions.BUILDS['windows']
        yarn_id = next(k for k in before if k[0] == spec['localization'])
        ui_id = (11105, 'MonoBehaviour')
        raw = before[yarn_id]
        replacement = [yarn['lines'].get(k, {}).get('text', v) for k, v in zip(keys, values)]
        self.assertEqual(after[yarn_id], dl.encode(raw, keys, replacement, extras))
        self.assertEqual(dl.parse(after[yarn_id]), (keys, replacement, extras))
        self.assertEqual(after[ui_id], before[ui_id])
        for identity, raw in before.items():
            if identity not in (yarn_id, ui_id):
                self.assertEqual(after[identity], raw, identity)
        self.assertEqual(result['outputSha256'], dl.sha(output.read_bytes()))

    def test_dialogue_only_without_ui_locale(self):
        yarn, yarn_path, _, keys, values, extras = self.make_combined_inputs()
        output = self.root / 'dialogue-only.assets'
        report = adapter.build(SOURCE, 'sharedassets1.assets', None, 'ru', output,
                               dialogue_locale_file=yarn_path)
        self.assertEqual((report['changedFields'], report['dialogueFields']), (0, 1))
        spec = versions.BUILDS['windows']
        obj = next(o for o in UnityPy.load(output.read_bytes()).objects if o.path_id == spec['localization'])
        expected = [yarn['lines'].get(k, {}).get('text', v) for k, v in zip(keys, values)]
        self.assertEqual(dl.parse(obj.get_raw_data()), (keys, expected, extras))

    def test_combination_rejects_locale_mismatch_and_wrong_asset(self):
        yarn, yarn_path, ui_path, _, _, _ = self.make_combined_inputs()
        yarn['locale'] = 'fr'
        yarn_path.write_text(json.dumps(yarn, ensure_ascii=False), encoding='utf-8')
        output = self.root / 'combined.assets'
        with self.assertRaisesRegex(ValueError, 'dialogue and UI locale codes do not match'):
            adapter.build(SOURCE, 'sharedassets1.assets', ui_path, 'ru', output,
                          dialogue_locale_file=yarn_path)
        self.assertFalse(output.exists())
        with self.assertRaisesRegex(ValueError, 'dialogue can be combined only'):
            adapter.build(SOURCE, 'level1', self.locale, 'ru', output,
                          dialogue_locale_file=yarn_path)
        self.assertFalse(output.exists())

    def test_combination_rejects_stale_dialogue_source(self):
        yarn, yarn_path, ui_path, _, _, _ = self.make_combined_inputs()
        yarn['lines']['line:4183ca7e']['source'] = 'stale source'
        yarn_path.write_text(json.dumps(yarn, ensure_ascii=False), encoding='utf-8')
        output = self.root / 'stale.assets'
        with self.assertRaisesRegex(ValueError, 'source mismatch'):
            adapter.build(SOURCE, 'sharedassets1.assets', ui_path, 'ru', output,
                          dialogue_locale_file=yarn_path)
        self.assertFalse(output.exists())

    def test_combined_readback_failure_does_not_publish_either_change(self):
        _, yarn_path, ui_path, _, _, _ = self.make_combined_inputs()
        output = self.root / 'failed-combined.assets'
        with patch.object(adapter, 'verify_output', side_effect=ValueError('combined readback failed')):
            with self.assertRaisesRegex(ValueError, 'combined readback failed'):
                adapter.build(SOURCE, 'sharedassets1.assets', ui_path, 'ru', output,
                              dialogue_locale_file=yarn_path)
        self.assertFalse(output.exists())
        self.assertFalse(output.with_name(output.name + '.tmp').exists())

    def make_settings_inputs(self):
        asset = 'sharedassets0.assets'
        ui = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': mapping.WINDOWS_ASSETS[asset],
              'lines': {'sharedassets0.assets#661': {'source': 'Enter text...', 'text': 'Enter text...'}}}
        setting = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': mapping.WINDOWS_ASSETS[asset],
                   'lines': {'sharedassets0.assets#605:label': {'source': 'Anti-aliasing', 'text': 'ЖЮЯ 427'},
                             'sharedassets0.assets#605:option:1': {'source': 'On', 'text': 'ЪъЬь 431'}}}
        ui_path, settings_path = self.root / 'settings-ui.json', self.root / 'settings.json'
        ui_path.write_text(json.dumps(ui, ensure_ascii=False), encoding='utf-8')
        settings_path.write_text(json.dumps(setting, ensure_ascii=False), encoding='utf-8')
        return setting, ui_path, settings_path

    def test_settings_and_ui_compose_with_exact_object_boundaries(self):
        setting, ui_path, settings_path = self.make_settings_inputs()
        original, _ = adapter.scan(SOURCE, 'sharedassets0.assets')
        before = {(o.path_id, o.type.name): o.get_raw_data() for o in original.objects}
        output = self.root / 'combined-settings.assets'
        result = adapter.build(SOURCE, 'sharedassets0.assets', ui_path, 'ru', output,
                               settings_locale_file=settings_path)
        self.assertEqual((result['changedFields'], result['settingsFields']), (1, 2))
        actual = UnityPy.load(str(output))
        actual.path = str(SOURCE)
        objects = {(o.path_id, o.type.name): o for o in actual.objects}
        after = {k: o.get_raw_data() for k, o in objects.items()}
        self.assertEqual(before.keys(), after.keys())
        changed = {k for k in before if before[k] != after[k]}
        self.assertEqual(changed, {(605, 'MonoBehaviour')})
        self.assertEqual(after[(661, 'MonoBehaviour')], before[(661, 'MonoBehaviour')])
        generator = adapter.windows_settings.bindings.generator(SOURCE, 'windows')
        _, _, schema = adapter.windows_settings.settings.nodes_for(objects[(605, 'MonoBehaviour')], generator, {})
        tree = objects[(605, 'MonoBehaviour')].read_typetree(nodes=schema, check_read=True)
        self.assertEqual(tree['label']['backupString'], 'ЖЮЯ 427')
        self.assertEqual([x['backupString'] for x in tree['dropdownOptions']], ['Off', 'ЪъЬь 431'])
        self.assertEqual(before[(615, 'MonoBehaviour')], after[(615, 'MonoBehaviour')])

    def test_settings_only_updates_multiple_setting_classes(self):
        asset = 'sharedassets0.assets'
        lines = {'sharedassets0.assets#604:label': {'source': 'Ambience Volume', 'text': 'ЖЮЯ 601'},
                 'sharedassets0.assets#605:label': {'source': 'Anti-aliasing', 'text': 'ЖЮЯ 602'},
                 'sharedassets0.assets#607:label': {'source': 'Camera FOV', 'text': 'ЖЮЯ 603'}}
        locale = self.root / 'multi-settings.json'
        locale.write_text(json.dumps({'schema': 1, 'locale': 'ru', 'sourceObjectSha256': mapping.WINDOWS_ASSETS[asset],
                                     'lines': lines}, ensure_ascii=False), encoding='utf-8')
        original, _ = adapter.scan(SOURCE, asset)
        before = {(o.path_id, o.type.name): o.get_raw_data() for o in original.objects}
        output = self.root / 'multi-settings.assets'
        result = adapter.build(SOURCE, asset, None, 'ru', output, settings_locale_file=locale)
        self.assertEqual(result['settingsFields'], 3)
        after = {(o.path_id, o.type.name): o.get_raw_data() for o in UnityPy.load(output.read_bytes()).objects}
        self.assertEqual(before.keys(), after.keys())
        self.assertEqual({k for k in before if before[k] != after[k]},
                         {(604, 'MonoBehaviour'), (605, 'MonoBehaviour'), (607, 'MonoBehaviour')})

    def test_settings_only_and_reject_no_inputs(self):
        _, _, settings_path = self.make_settings_inputs()
        output = self.root / 'settings-only.assets'
        result = adapter.build(SOURCE, 'sharedassets0.assets', None, 'ru', output,
                               settings_locale_file=settings_path)
        self.assertEqual((result['changedFields'], result['settingsFields']), (0, 2))
        with self.assertRaisesRegex(ValueError, 'at least one locale input'):
            adapter.build(SOURCE, 'sharedassets0.assets', None, 'ru', self.root / 'none.assets')

    def test_settings_reject_protected_values_wrong_asset_and_locale(self):
        setting, ui_path, settings_path = self.make_settings_inputs()
        output = self.root / 'rejected-settings.assets'
        with self.assertRaisesRegex(ValueError, 'settings can be combined only'):
            adapter.build(SOURCE, 'level1', self.locale, 'ru', output, settings_locale_file=settings_path)
        self.assertFalse(output.exists())
        setting['locale'] = 'fr'
        settings_path.write_text(json.dumps(setting, ensure_ascii=False), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'settings and requested locale codes do not match'):
            adapter.build(SOURCE, 'sharedassets0.assets', ui_path, 'ru', output, settings_locale_file=settings_path)
        self.assertFalse(output.exists())
        setting['locale'] = 'ru'
        setting['lines'] = {'sharedassets0.assets#615:option:0': {'source': '640x480_60', 'text': 'ЖЮЯ'}}
        settings_path.write_text(json.dumps(setting, ensure_ascii=False), encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'unknown line IDs'):
            adapter.build(SOURCE, 'sharedassets0.assets', ui_path, 'ru', output, settings_locale_file=settings_path)
        self.assertFalse(output.exists())

    def test_settings_decode_failure_does_not_publish_combined_asset(self):
        _, ui_path, settings_path = self.make_settings_inputs()
        output = self.root / 'failed-settings.assets'
        with patch.object(adapter.windows_settings, 'verify', side_effect=ValueError('setting readback failed')):
            with self.assertRaisesRegex(ValueError, 'setting readback failed'):
                adapter.build(SOURCE, 'sharedassets0.assets', ui_path, 'ru', output,
                              settings_locale_file=settings_path)
        self.assertFalse(output.exists())
        self.assertFalse(output.with_name(output.name + '.tmp').exists())

    def test_wrong_build_unknown_id_and_locale_are_rejected(self):
        with self.assertRaisesRegex(ValueError, 'unsupported Windows build identity'):
            adapter.build(MAC, 'level1', self.locale, 'ru', self.output)
        self.assertFalse(self.output.exists())
        self.doc['lines'] = {'level1#999999': {'source': 'Options', 'text': 'ЖЮЯ'}}
        self.write_locale()
        with self.assertRaisesRegex(ValueError, 'unknown line IDs'):
            adapter.build(SOURCE, 'level1', self.locale, 'ru', self.output)
        self.assertFalse(self.output.exists())
        self.doc['lines'] = self.lines
        self.write_locale()
        with self.assertRaisesRegex(ValueError, 'requested UI locale does not match'):
            adapter.build(SOURCE, 'level1', self.locale, 'fr', self.output)
        self.assertFalse(self.output.exists())

    def test_readback_failure_does_not_publish_output(self):
        with patch.object(adapter, 'verify_output', side_effect=ValueError('forced readback failure')):
            with self.assertRaisesRegex(ValueError, 'forced readback failure'):
                adapter.build(SOURCE, 'level1', self.locale, 'ru', self.output)
        self.assertFalse(self.output.exists())
        self.assertFalse(self.output.with_name(self.output.name + '.tmp').exists())

    def test_existing_temporary_file_is_preserved(self):
        tmp = self.output.with_name(self.output.name + '.tmp')
        tmp.write_bytes(b'owner-existing-temp')
        with self.assertRaises(FileExistsError):
            adapter.build(SOURCE, 'level1', self.locale, 'ru', self.output)
        self.assertEqual(tmp.read_bytes(), b'owner-existing-temp')
        self.assertFalse(self.output.exists())

    def test_rejects_output_inside_game_directory(self):
        with self.assertRaisesRegex(ValueError, 'outside the installed game'):
            adapter.safe_output(SOURCE, SOURCE.parent / 'must-not-create.test')


if __name__ == '__main__':
    unittest.main()
