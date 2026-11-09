import json
from pathlib import Path
import shutil
import tempfile
import unittest

import UnityPy

import inventory_yarn_bindings as bindings
import map_ui_hierarchy
import probe_font_roles as fonts
import speaker_contrast as contrast
import ui_locale as mac_ui
import windows_ui_locale as win_ui

SOURCES = {
    'macos': Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data",
    'windows': Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data'),
}
NAME_IDS = {
    'macos': {'level1': 3900, 'level3': 1494, 'level5': 1519, 'level6': 1491},
    'windows': {'level1': 3852, 'level3': 1449, 'level5': 1474, 'level6': 1446},
}


def objects(path, source):
    env = UnityPy.load(str(path))
    env.path = str(source)
    return {(obj.path_id, obj.type.name): obj for obj in env.objects}


@unittest.skipUnless(all(path.is_dir() for path in SOURCES.values()), 'both pinned game builds required')
class SpeakerContrastTests(unittest.TestCase):
    def test_paired_scene_fields_and_ui_composition(self):
        for platform, source in SOURCES.items():
            generator = bindings.generator(source, platform)
            with tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                for asset, path_id in NAME_IDS[platform].items():
                    with self.subTest(platform=platform, asset=asset):
                        locale = None
                        text_id = None
                        if asset == 'level1':
                            text_id, source_text, asset_hash = (
                                (3903, 'LOADING...', mac_ui.ASSETS[asset]) if platform == 'macos'
                                else (3862, 'Options', map_ui_hierarchy.WINDOWS_ASSETS[asset])
                            )
                            locale = root / 'ui.json'
                            locale.write_text(json.dumps({
                                'schema': 1, 'locale': 'ru', 'sourceObjectSha256': asset_hash,
                                'lines': {f'{asset}#{text_id}': {'source': source_text, 'text': 'ЖЮЯ'}},
                            }), encoding='utf-8')
                        target = root / asset
                        if platform == 'macos':
                            shutil.copyfile(source / asset, target)
                            mac_ui.patch_into(source, asset, locale, 'ru', target, improve_speaker_contrast=True)
                        else:
                            win_ui.build(source, asset, locale, 'ru', target, improve_speaker_contrast=True)
                        before, after = objects(source / asset, source), objects(target, source)
                        self.assertEqual(before.keys(), after.keys())
                        name = (path_id, 'MonoBehaviour')
                        expected = {name}
                        if text_id is not None:
                            text = (text_id, 'MonoBehaviour')
                            expected.add(text)
                            self.assertEqual(fonts.read_tree(after[text], generator)['m_text'], 'ЖЮЯ')
                        self.assertEqual({key for key in before
                                          if before[key].get_raw_data() != after[key].get_raw_data()}, expected)
                        original = fonts.read_tree(before[name], generator)
                        updated = fonts.read_tree(after[name], generator)
                        self.assertEqual(original['m_fontColor'], {'r': 1., 'g': 1., 'b': 1., 'a': 1.})
                        self.assertEqual(updated, original | {
                            'm_fontColor': {'r': 0., 'g': 0., 'b': 0., 'a': 1.},
                            'm_fontColor32': {'rgba': 4278190080},
                        })

    def test_already_black_scene_is_outside_patch_scope(self):
        self.assertNotIn('level4', contrast.ASSETS)
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder) / 'level4'
            with self.assertRaisesRegex(ValueError, 'no audited speaker contrast patch'):
                win_ui.build(SOURCES['windows'], 'level4', None, 'ru', output, improve_speaker_contrast=True)
            self.assertFalse(output.exists())
