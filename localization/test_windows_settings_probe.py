"""Safety checks for the isolated Windows dropdown probe."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import dialogue_locale as dl

SOURCE = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
READY = (SOURCE.is_dir() and MAC.is_dir() and dl.SITE_LOCALES.is_file()
         and importlib.util.find_spec('UnityPy') is not None
         and importlib.util.find_spec('TypeTreeGeneratorAPI') is not None
         and importlib.util.find_spec('fontTools') is not None)


@unittest.skipUnless(READY, 'pinned Windows and macOS builds and probe dependencies required')
class WindowsSettingsProbeTests(unittest.TestCase):
    def test_only_selected_dropdown_fields_are_changed(self):
        import windows_settings_probe as probe
        doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': probe.font_probe.FILES[probe.ASSET],
               'lines': {probe.LABEL: {'source': 'Anti-aliasing', 'text': 'ЖЮЯ 427'},
                         probe.OPTION: {'source': 'On', 'text': 'ЪъЬь 431'}}}
        with tempfile.TemporaryDirectory(prefix='dragnwash-win-settings-') as folder:
            root = Path(folder)
            locale, out = root / 'locale.json', root / 'settings.assets'
            locale.write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
            with patch.object(probe, 'TEST_WORK', root):
                with self.assertRaisesRegex(ValueError, 'unsupported Windows build identity'):
                    probe.build(MAC, locale, out)
                self.assertFalse(out.exists())
                result = probe.build(SOURCE, locale, out)
                self.assertTrue(result['testOnly'])
                self.assertEqual(result['changedSyntheticEntries'], 2)
                self.assertEqual(result['outputSha256'], 'a057e84687993682f91a850f62c0e5b81d21c0d76a6fd8afde55959e49a10f1c')
                before = out.read_bytes()
                with self.assertRaisesRegex(ValueError, 'fresh .assets'):
                    probe.build(SOURCE, locale, out)
                self.assertEqual(out.read_bytes(), before)
                doc['lines'] = {'sharedassets0.assets#605:option:0': {'source': 'Off', 'text': 'ТЕСТ'}}
                locale.write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'unknown'):
                    probe.build(SOURCE, locale, root / 'invalid.assets')
                self.assertFalse((root / 'invalid.assets').exists())


if __name__ == '__main__':
    unittest.main()
