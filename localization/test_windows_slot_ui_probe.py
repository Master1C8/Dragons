"""Source and object safety for the Windows new-slot UI probe."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import dialogue_locale as dl

SOURCE = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
READY = SOURCE.is_dir() and MAC.is_dir() and dl.SITE_LOCALES.is_file() and importlib.util.find_spec('UnityPy') is not None


@unittest.skipUnless(READY, 'pinned macOS and Windows builds and UnityPy required')
class WindowsSlotProbeTests(unittest.TestCase):
    def test_selected_labels_and_refuses_wrong_targets(self):
        import windows_slot_ui_probe as probe
        with tempfile.TemporaryDirectory(prefix='dragnwash-win-slot-') as folder:
            root = Path(folder)
            locale, output = root / 'locale.json', root / 'slot.assets'
            doc = {'schema': 1, 'locale': 'ru',
                   'sourceObjectSha256': '55a296caa23347190faa063efdaab4cf5a37e00bdbffa455729b4aa346cddae0',
                   'lines': {f'level0#{i}': {'source': 'New', 'text': 'ЪъЬь'} for i in (5183, 5184, 5186)}}
            locale.write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
            with patch.object(probe, 'TEST_WORK', root):
                with self.assertRaisesRegex(ValueError, 'unsupported build identity'):
                    probe.build(MAC, locale, output)
                self.assertFalse(output.exists())
                result = probe.build(SOURCE, locale, output)
                self.assertTrue(result['testOnly'])
                self.assertEqual(result['changedSyntheticEntries'], 3)
                self.assertEqual(result['outputSha256'], '050d4c3450ab7aed852678d3a607375e1f91f18824cd0102ff68aa8843f8dc0e')
                before = output.read_bytes()
                with self.assertRaisesRegex(ValueError, 'fresh .assets'):
                    probe.build(SOURCE, locale, output)
                self.assertEqual(output.read_bytes(), before)
                doc['lines'] = {'level0#5191': {'source': 'New', 'text': 'ЪъЬь'}}
                locale.write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
                with self.assertRaisesRegex(ValueError, 'unknown'):
                    probe.build(SOURCE, locale, root / 'greyed.assets')
                self.assertFalse((root / 'greyed.assets').exists())


if __name__ == '__main__':
    unittest.main()
