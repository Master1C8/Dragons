import json
from pathlib import Path
import shutil
import tempfile
import unittest

import UnityPy
import dialogue_locale as dl
import settings_locale as settings
import ui_locale as mac_ui
import windows_ui_locale as win_ui
import verify_combined_settings_ui as verifier

ROOT = Path(__file__).parent
WORK = ROOT / 'work'
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir() and WORK.is_dir(), 'both pinned builds required')
class CombinedSettingsVerificationTests(unittest.TestCase):
    def test_combined_assets_and_corruption_controls(self):
        with tempfile.TemporaryDirectory(prefix='settings-verifier-', dir=WORK) as directory:
            root = Path(directory)
            for platform, source in [('macos', MAC), ('windows', WIN)]:
                with self.subTest(platform=platform):
                    asset = settings.ASSET
                    digest = mac_ui.ASSETS[asset] if platform == 'macos' else win_ui.ui_map.WINDOWS_ASSETS[asset]
                    setting_id, ui_id = (609, 666) if platform == 'macos' else (605, 661)
                    option_id = f'{asset}#{setting_id}:option:1'
                    ui_key = f'{asset}#{ui_id}'
                    setting_doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': digest,
                                   'lines': {option_id: {'source': 'On', 'text': 'ЖЮЯ 427'}}}
                    ui_doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': digest,
                              'lines': {ui_key: {'source': 'Enter text...', 'text': 'Enter text...'}}}
                    setting, ui, candidate = (root / f'{platform}-{x}' for x in ('settings.json', 'ui.json', 'candidate.assets'))
                    setting.write_text(json.dumps(setting_doc, ensure_ascii=False), encoding='utf-8')
                    ui.write_text(json.dumps(ui_doc, ensure_ascii=False), encoding='utf-8')
                    if platform == 'windows':
                        win_ui.build(source, asset, ui, 'ru', candidate, settings_locale_file=setting)
                    else:
                        shutil.copyfile(source / asset, candidate)
                        mac_ui.patch_into(source, asset, ui, 'ru', candidate)
                        settings.patch_into(source, candidate, settings.make_asset(source, setting, 'ru'), prior_ui=ui)
                    report = verifier.verify(platform, source, candidate, 'ru', setting, ui)
                    self.assertEqual(report['expectedEntries'], {'settings': 1, 'ui': 1})
                    self.assertEqual(report['candidateAssetSha256'], dl.sha(candidate.read_bytes()))
                    settings_only = verifier.verify(platform, source, candidate, 'ru', setting, None)
                    self.assertEqual(settings_only['expectedEntries'], {'settings': 1, 'ui': 0})
                    wrong_ui = root / f'{platform}-wrong-ui.json'
                    ui_doc['lines'][ui_key]['text'] = 'ЖЮЯ 502'
                    wrong_ui.write_text(json.dumps(ui_doc, ensure_ascii=False), encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'protected UI text must remain exact'):
                        verifier.verify(platform, source, candidate, 'ru', setting, wrong_ui)
                    with self.assertRaisesRegex(ValueError, 'settings locale does not match requested locale'):
                        verifier.verify(platform, source, candidate, 'uk', setting, ui)
                    wrong_setting = root / f'{platform}-wrong-settings.json'
                    setting_doc['lines'][option_id]['text'] = 'ЖЮЯ 428'
                    wrong_setting.write_text(json.dumps(setting_doc, ensure_ascii=False), encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'candidate setting tree differs'):
                        verifier.verify(platform, source, candidate, 'ru', wrong_setting, ui)
                    invalid = root / f'{platform}-protected.json'
                    resolution_id = 619 if platform == 'macos' else 615
                    protected_key = f'{asset}#{resolution_id}:option:0'
                    setting_doc['lines'] = {protected_key: {'source': '640x480_60', 'text': '640x480_61'}}
                    invalid.write_text(json.dumps(setting_doc, ensure_ascii=False), encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'unknown line IDs'):
                        verifier.verify(platform, source, candidate, 'ru', invalid, ui)
                    corrupted = root / f'{platform}-corrupted.assets'
                    env = UnityPy.load(str(candidate))
                    target = next(o for o in env.objects if (o.path_id, o.type.name) not in
                                  ((setting_id, 'MonoBehaviour'), (ui_id, 'MonoBehaviour')) and o.get_raw_data())
                    raw = target.get_raw_data()
                    target.set_raw_data(raw[:-1] + bytes([raw[-1] ^ 1]))
                    corrupted.write_bytes(env.file.save())
                    with self.assertRaisesRegex(ValueError, 'candidate object differs from expected'):
                        verifier.verify(platform, source, corrupted, 'ru', setting, ui)

    def test_missing_input_rejected(self):
        with self.assertRaisesRegex(ValueError, 'at least one locale input'):
            verifier.verify('macos', MAC, MAC / settings.ASSET, 'ru', None, None)


if __name__ == '__main__':
    unittest.main()
