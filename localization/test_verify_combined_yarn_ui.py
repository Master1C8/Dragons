import json
from pathlib import Path
import tempfile
import unittest

import UnityPy
import compare_yarn_versions as versions
import dialogue_locale as dl
import ui_locale as mac_ui
import windows_ui_locale as win_ui
import verify_combined_yarn_ui as verifier

ROOT = Path(__file__).parent
WORK = ROOT / 'work'
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir() and WORK.is_dir(), 'both pinned builds required')
class CombinedVerificationTests(unittest.TestCase):
    def test_combined_assets_and_corruption_controls(self):
        with tempfile.TemporaryDirectory(prefix='combined-verifier-', dir=WORK) as directory:
            root = Path(directory)
            for platform, source in [('macos', MAC), ('windows', WIN)]:
                with self.subTest(platform=platform):
                    spec = versions.BUILDS[platform]
                    keys, values, extras, _, _, _ = versions.load(source, spec)
                    line = 'line:4183ca7e'
                    yarn_doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': spec['localizationSha256'],
                                'lines': {line: {'source': dict(zip(keys, values))[line],
                                                 'text': "Жж Ъъ Ьь <i>'Drag'n'wash franchise 223'...</i>"}}}
                    ui_key = 'sharedassets1.assets#11117' if platform == 'macos' else 'sharedassets1.assets#11105'
                    ui_doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': spec['assetSha256'],
                              'lines': {ui_key: {'source': 'Option Text', 'text': 'ЖЮЯ 501'}}}
                    yarn, ui, candidate = (root / f'{platform}-{x}' for x in ('yarn.json', 'ui.json', 'candidate.assets'))
                    yarn.write_text(json.dumps(yarn_doc, ensure_ascii=False), encoding='utf-8')
                    ui.write_text(json.dumps(ui_doc, ensure_ascii=False), encoding='utf-8')
                    if platform == 'windows':
                        win_ui.build(source, 'sharedassets1.assets', ui, 'ru', candidate, dialogue_locale_file=yarn)
                    else:
                        env, obj, raw, _, _, _ = dl.load_asset(source / 'sharedassets1.assets')
                        _, updates = dl.read_locale(yarn, keys, values, spec['localizationSha256'])
                        encoded = dl.encode(raw, keys, [updates.get(k, v) for k, v in zip(keys, values)], extras)
                        obj.set_raw_data(encoded)
                        candidate.write_bytes(env.file.save())
                        mac_ui.patch_into(source, 'sharedassets1.assets', ui, 'ru', candidate, dialogue_object=encoded)
                    report = verifier.verify(platform, source, candidate, 'ru', yarn, ui)
                    self.assertEqual(report['expectedEntries'], {'yarn': 1, 'ui': 1})
                    self.assertEqual(report['candidateAssetSha256'], dl.sha(candidate.read_bytes()))
                    with self.assertRaisesRegex(ValueError, 'candidate object differs from expected'):
                        verifier.verify(platform, source, candidate, 'ru', yarn, None)
                    wrong_ui = root / f'{platform}-wrong-ui.json'
                    ui_doc['lines'][ui_key]['text'] = 'ЖЮЯ 502'
                    wrong_ui.write_text(json.dumps(ui_doc, ensure_ascii=False), encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'candidate object differs from expected'):
                        verifier.verify(platform, source, candidate, 'ru', yarn, wrong_ui)
                    wrong_yarn = root / f'{platform}-wrong-yarn.json'
                    yarn_doc['lines'][line]['text'] = "Яя Ъъ Ьь <i>'Drag'n'wash franchise 223'...</i>"
                    wrong_yarn.write_text(json.dumps(yarn_doc, ensure_ascii=False), encoding='utf-8')
                    with self.assertRaisesRegex(ValueError, 'candidate object differs from expected'):
                        verifier.verify(platform, source, candidate, 'ru', wrong_yarn, ui)
                    with self.assertRaisesRegex(ValueError, 'Yarn locale does not match requested locale'):
                        verifier.verify(platform, source, candidate, 'uk', yarn, ui)
                    corrupted = root / f'{platform}-corrupted.assets'
                    env = UnityPy.load(str(candidate))
                    project = next(o for o in env.objects if o.path_id == spec['project'])
                    original = project.get_raw_data()
                    project.set_raw_data(original[:-1] + bytes([original[-1] ^ 1]))
                    corrupted.write_bytes(env.file.save())
                    with self.assertRaisesRegex(ValueError, 'candidate object differs from expected'):
                        verifier.verify(platform, source, corrupted, 'ru', yarn, ui)

    def test_missing_input_rejected(self):
        with self.assertRaisesRegex(ValueError, 'at least one locale input'):
            verifier.verify('macos', MAC, MAC / 'sharedassets1.assets', 'ru', None, None)


if __name__ == '__main__':
    unittest.main()
