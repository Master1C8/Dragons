import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).parent
WORK = ROOT / 'work'
TOOL = WORK / 'addressable-catalog-keys-bin/addressable-catalog-keys.dll'
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


@unittest.skipUnless(TOOL.is_file() and MAC.is_dir() and WIN.is_dir(), 'built scanner and both pinned game builds required')
class CatalogKeyTests(unittest.TestCase):
    def run_tool(self, platform, source):
        return subprocess.run(['dotnet', str(TOOL), platform, str(source)], capture_output=True, text=True)

    def test_both_catalogs_reproduce_and_include_known_keys(self):
        reports = []
        for platform, source in [('macos', MAC), ('windows', WIN)]:
            with self.subTest(platform=platform):
                result = self.run_tool(platform, source)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.encode(), (WORK / f'catalog-keys-{platform}-20261107.json').read_bytes())
                doc = json.loads(result.stdout)
                self.assertEqual((doc['keyCount'], doc['diagnosticMemoryCopyCalls']), (24, 13))
                self.assertEqual(len(set(doc['keys'])), 24)
                self.assertIn('English (en)', doc['keys'])
                self.assertIn('Locale', doc['keys'])
                self.assertEqual(sum(k.endswith('.compute') for k in doc['keys']), 9)
                self.assertEqual(sum(k.endswith('.bundle') for k in doc['keys']), 3)
                reports.append(doc)
        self.assertEqual(reports[0]['keys'][:2], reports[1]['keys'][:2])
        self.assertEqual(reports[0]['keys'][3:], reports[1]['keys'][3:])
        self.assertNotEqual(reports[0]['keys'][2], reports[1]['keys'][2])

    def test_wrong_build_and_altered_catalog_are_rejected(self):
        wrong = self.run_tool('macos', WIN)
        self.assertNotEqual(wrong.returncode, 0)
        self.assertIn('Unsupported managed inventory', wrong.stderr)
        self.assertEqual(wrong.stdout, '')
        with tempfile.TemporaryDirectory(prefix='catalog-negative-', dir=WORK) as temp:
            root = Path(temp)
            (root / 'Managed').symlink_to(MAC / 'Managed', target_is_directory=True)
            aa = root / 'StreamingAssets/aa'
            aa.mkdir(parents=True)
            raw = bytearray((MAC / 'StreamingAssets/aa/catalog.bin').read_bytes())
            raw[-1] ^= 1
            (aa / 'catalog.bin').write_bytes(raw)
            altered = self.run_tool('macos', root)
            self.assertNotEqual(altered.returncode, 0)
            self.assertIn('Unsupported catalog', altered.stderr)
            self.assertEqual(altered.stdout, '')


if __name__ == '__main__':
    unittest.main()
