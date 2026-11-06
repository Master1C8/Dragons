"""Source-pinned Windows synthetic Yarn probe safety checks."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import compare_yarn_versions as versions
import dialogue_locale as dl

SOURCE = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
READY = SOURCE.is_dir() and MAC.is_dir() and dl.SITE_LOCALES.is_file() and importlib.util.find_spec('UnityPy') is not None


@unittest.skipUnless(READY, 'pinned macOS and Windows builds and UnityPy required')
class WindowsProbeTests(unittest.TestCase):
    def test_build_and_reject_wrong_source_or_existing_output(self):
        import windows_dialogue_probe as probe
        loaded = versions.load(SOURCE, probe.SPEC)
        keys, values, *_ = loaded
        original = dict(zip(keys, values))['line:4183ca7e']
        doc = {'schema': 1, 'locale': 'ru', 'sourceObjectSha256': probe.SPEC['localizationSha256'],
               'lines': {'line:4183ca7e': {'source': original,
                        'text': "Жж Ъъ Ьь <i>'Drag'n'wash franchise 223'...</i>"}}}
        with tempfile.TemporaryDirectory(prefix='dragnwash-win-probe-') as folder:
            root = Path(folder)
            locale, out = root / 'probe.json', root / 'probe.assets'
            locale.write_text(json.dumps(doc, ensure_ascii=False), encoding='utf-8')
            with patch.object(probe, 'TEST_WORK', root):
                with self.assertRaisesRegex(ValueError, 'unsupported global game managers'):
                    probe.build(MAC, locale, out)
                self.assertFalse(out.exists())
                result = probe.build(SOURCE, locale, out)
                self.assertTrue(result['testOnly'])
                self.assertEqual(result['translatedSyntheticEntries'], 1)
                self.assertEqual(dl.sha(out.read_bytes()), result['outputSha256'])
                before = out.read_bytes()
                with self.assertRaisesRegex(ValueError, 'fresh .assets'):
                    probe.build(SOURCE, locale, out)
                self.assertEqual(out.read_bytes(), before)
                outside = root.parent / 'not-owned-probe.assets'
                with self.assertRaisesRegex(ValueError, 'directly in the test work directory'):
                    probe.build(SOURCE, locale, outside)
                self.assertEqual(out.read_bytes(), before)
                # Simulate an asset changing after the first version check;
                # the user-owned source is never modified by this test.
                candidate = root / 'changed.assets'
                real_read = Path.read_bytes

                def changed_read(path):
                    if path == SOURCE / 'sharedassets1.assets':
                        return b'changed after initial validation'
                    return real_read(path)

                with patch.object(probe.versions, 'load', return_value=loaded), \
                     patch.object(Path, 'read_bytes', changed_read):
                    with self.assertRaisesRegex(ValueError, 'source asset changed during validation'):
                        probe.build(SOURCE, locale, candidate)
                self.assertFalse(candidate.exists())


if __name__ == '__main__':
    unittest.main()
