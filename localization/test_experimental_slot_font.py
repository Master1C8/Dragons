"""Exercise the isolated slot-font candidate on a pinned copied game asset."""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest

import dialogue_locale as dl
import ui_locale as ui

SOURCE = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
READY = (SOURCE.is_dir() and dl.SITE_LOCALES.is_file()
         and importlib.util.find_spec('UnityPy') is not None
         and importlib.util.find_spec('TypeTreeGeneratorAPI') is not None
         and importlib.util.find_spec('fontTools') is not None)


@unittest.skipUnless(READY, 'pinned macOS game and font probe dependencies required')
class SlotFontExperimentTests(unittest.TestCase):
    def test_merges_only_matching_ui_and_reproduces_reviewed_candidate(self):
        import experimental_slot_font as experiment
        with tempfile.TemporaryDirectory(prefix='dragnwash-slot-font-test-') as folder:
            root = Path(folder)
            target, locale = root / 'level0', root / 'locale.json'
            shutil.copyfile(SOURCE / 'level0', target)
            lines = {f'level0#{i}': {'source': 'New', 'text': 'ЖжЪъЬ'} for i in (5204, 5205, 5207)}
            locale.write_text(json.dumps({'schema': 1, 'locale': 'ru',
                                          'sourceObjectSha256': ui.ASSETS['level0'], 'lines': lines},
                                         ensure_ascii=False), encoding='utf-8')
            ui.patch_into(SOURCE, 'level0', locale, 'ru', target)
            before = hashlib.sha256(target.read_bytes()).hexdigest()
            self.assertEqual(before, 'f487e03d62ba7c7d2e655cdbc9d3986ebc7db5d8d4744a4d9732a034820a5e0b')
            with self.assertRaisesRegex(ValueError, 'supported non-English locale'):
                experiment.patch_into(SOURCE, target, 'zz', prior_ui=locale)
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), before)
            with self.assertRaisesRegex(ValueError, 'unexpected slot font target object'):
                experiment.patch_into(SOURCE, target, 'ru')
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), before)
            result = experiment.patch_into(SOURCE, target, 'ru', prior_ui=locale)
            self.assertEqual(result, '57198148633e8919609fd45428a6824d1f5ed89defb319f6fc1efd4875b74cb3')
            with self.assertRaisesRegex(ValueError, 'unexpected slot font target object'):
                experiment.patch_into(SOURCE, target, 'ru', prior_ui=locale)
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), result)


if __name__ == '__main__':
    unittest.main()
