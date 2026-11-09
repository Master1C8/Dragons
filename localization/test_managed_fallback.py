import json
import os
from pathlib import Path
import tempfile
import unittest

import dialogue_locale as dl
import managed_fallback as fallback

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data/Managed" / fallback.ASSEMBLY
WIN = (Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data/Managed')
       / fallback.ASSEMBLY)
TOOL = os.environ.get('DRAGONS_MANAGED_FALLBACK_TOOL')


def write_locale(path, platform, text):
    path.write_text(json.dumps({
        'schema': 1, 'locale': 'ru', 'sourceObjectSha256': fallback.SOURCES[platform],
        'lines': {'yarn-missing-line': {'source': fallback.FALLBACK['yarn-missing-line'], 'text': text}},
    }), encoding='utf-8')


class ManagedFallbackTests(unittest.TestCase):
    def test_wrong_source_is_rejected_before_tool_resolution(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / fallback.ASSEMBLY
            source.write_bytes(b'invalid')
            with self.assertRaisesRegex(ValueError, 'unsupported macos missing-line source assembly'):
                fallback.prepare('macos', source, root / 'missing.json', 'ru', root / 'missing.dll')

    @unittest.skipUnless(TOOL and MAC.is_file() and WIN.is_file(), 'compiled patcher and both source builds required')
    def test_paired_literals_and_nonoverwriting_publication(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for platform, source in (('macos', MAC), ('windows', WIN)):
                with self.subTest(platform=platform):
                    locale = root / f'{platform}.json'
                    output = root / f'{platform}.dll'
                    write_locale(locale, platform, 'Жж\n741')
                    with self.assertRaisesRegex(ValueError, 'single plain-text line'):
                        fallback.build(platform, source, locale, 'ru', TOOL, output)
                    self.assertFalse(output.exists())
                    write_locale(locale, platform, 'Жж Ъъ 741')
                    with self.assertRaisesRegex(ValueError, 'managed locale ru does not match uk'):
                        fallback.build(platform, source, locale, 'uk', TOOL, output)
                    self.assertFalse(output.exists())
                    receipt = fallback.build(platform, source, locale, 'ru', TOOL, output)
                    original_output = output.read_bytes()
                    self.assertEqual(receipt['changedOffsets'], [24, 57])
                    self.assertEqual(receipt['verifiedMethodBodies'], 717)
                    self.assertEqual(receipt['outputSha256'], dl.sha(original_output))
                    write_locale(locale, platform, 'Жж Ъъ 742')
                    with self.assertRaises(FileExistsError):
                        fallback.build(platform, source, locale, 'ru', TOOL, output)
                    self.assertEqual(output.read_bytes(), original_output)
                    self.assertEqual(dl.sha(source.read_bytes()), fallback.SOURCES[platform])
                    write_locale(locale, platform, fallback.FALLBACK['yarn-missing-line'])
                    unchanged, receipt = fallback.prepare(platform, source, locale, 'ru', TOOL)
                    self.assertEqual(unchanged, source.read_bytes())
                    self.assertEqual(receipt['outputSha256'], fallback.SOURCES[platform])

    @unittest.skipUnless(TOOL and MAC.is_file() and WIN.is_file(), 'compiled patcher and both source builds required')
    def test_new_slot_patch_reproduces_both_verified_probes(self):
        expected_outputs = {
            'macos': (2385, 'd5d8c8bd09d81b02d757a730cb87f22fa882e71a677e4c1fecc3b429901c3b4f'),
            'windows': (2328, 'ed2f58e930775be2aad6064ebaa76cc1e915235b1b0cc3810ede3696aa7f8e32'),
        }
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for platform, source in (('macos', MAC), ('windows', WIN)):
                with self.subTest(platform=platform):
                    locale = root / f'{platform}.json'
                    locale.write_text(json.dumps({
                        'schema': 1, 'locale': 'ru', 'sourceObjectSha256': fallback.SLOT_SOURCES[platform],
                        'lines': {'slot-new': {'source': 'NEW', 'text': 'ЖЪЬ42'}},
                    }), encoding='utf-8')
                    source_dll = source.with_name(fallback.SLOT_ASSEMBLY)
                    output, receipt = fallback.prepare(platform, source_dll, locale, 'ru', TOOL, slot_new=True)
                    methods, digest = expected_outputs[platform]
                    self.assertEqual(receipt['changedOffsets'], [133, 257, 380])
                    self.assertEqual(receipt['verifiedMethodBodies'], methods)
                    self.assertEqual(receipt['outputSha256'], digest)
                    self.assertEqual(dl.sha(output), digest)
                    self.assertEqual(dl.sha(source_dll.read_bytes()), fallback.SLOT_SOURCES[platform])
