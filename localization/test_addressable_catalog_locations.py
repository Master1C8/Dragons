import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).parent
WORK = ROOT / 'work'
TOOL = WORK / 'addressable-catalog-locations-bin/addressable-catalog-locations.dll'
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
PREFIX = '{UnityEngine.AddressableAssets.Addressables.RuntimePath}'


def relative(path):
    if not path.startswith(PREFIX):
        raise ValueError('not a catalog runtime path')
    return path[len(PREFIX):].replace('\\', '/').lstrip('/')


@unittest.skipUnless(TOOL.is_file() and MAC.is_dir() and WIN.is_dir(), 'built scanner and both pinned game builds required')
class CatalogLocationTests(unittest.TestCase):
    def run_tool(self, platform, source):
        return subprocess.run(['dotnet', str(TOOL), platform, str(source)], capture_output=True, text=True)

    def test_locations_reproduce_and_correspond_to_inspected_bundles(self):
        for platform, source in [('macos', MAC), ('windows', WIN)]:
            with self.subTest(platform=platform):
                result = self.run_tool(platform, source)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout.encode(), (WORK / f'catalog-locations-{platform}-20261107.json').read_bytes())
                report = json.loads(result.stdout)
                self.assertEqual((report['locationCount'], report['nativeHashExceptions']), (13, 3))
                self.assertEqual((report['diagnosticMemoryCopyCalls'], report['diagnosticLoggerCalls']), (13, 10))
                prior = json.loads((ROOT / f'evidence/addressables-{platform}-20261107.json').read_text())
                self.assertEqual(report['catalogSha256'], prior['files']['catalog.bin'])
                bundles = {b['file']: b for b in prior['bundles']}
                rows = report['locations']
                bundle_locations = [r for r in rows if r['resourceType'].endswith('.IAssetBundleResource')]
                self.assertEqual({relative(r['internalId']) for r in bundle_locations}, set(bundles))
                self.assertEqual(len(bundle_locations), 3)
                self.assertTrue(all(not row['dataAvailable'] for row in bundle_locations))
                locale = next(r for r in rows if r['resourceType'] == 'UnityEngine.Localization.Locale')
                self.assertEqual(locale['primaryKey'], 'English (en)')
                locale_deps = {relative(d) for d in locale['dependencies']}
                self.assertEqual(len(locale_deps), 2)
                self.assertTrue(locale_deps <= bundles.keys())
                locale_bundle = next(bundles[d] for d in locale_deps if 'localization-locales_assets_all.bundle' in d)
                self.assertIn(locale['internalId'], [c['path'] for c in locale_bundle['containers']])
                shaders = [r for r in rows if r['resourceType'] == 'UnityEngine.ComputeShader']
                self.assertEqual(len(shaders), 9)
                for shader in shaders:
                    self.assertEqual(len(shader['dependencies']), 1)
                    bundle = bundles[relative(shader['dependencies'][0])]
                    self.assertIn(shader['internalId'], [c['path'] for c in bundle['containers']])

    def test_wrong_build_and_altered_catalog_rejected_at_guards(self):
        wrong = self.run_tool('macos', WIN)
        self.assertNotEqual(wrong.returncode, 0)
        self.assertIn('Unsupported managed inventory', wrong.stderr)
        self.assertEqual(wrong.stdout, '')
        with tempfile.TemporaryDirectory(prefix='catalog-locations-negative-', dir=WORK) as temp:
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
