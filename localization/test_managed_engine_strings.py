import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).parent
SCANNER = ROOT / 'work/managed-strings-unity-bin/managed-strings.dll'
WORK = ROOT / 'work/source-inventory-20261107'
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data/Managed"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data/Managed')


@unittest.skipUnless(SCANNER.is_file() and MAC.is_dir() and WIN.is_dir(), 'scanner and both pinned managed directories required')
class EngineStringTests(unittest.TestCase):
    def invoke(self, selector, source):
        return subprocess.run(['dotnet', str(SCANNER), selector, str(source)], capture_output=True)

    def test_all_source_occurrences_reproduce(self):
        for platform, root in [('macos', MAC), ('windows', WIN)]:
            for suffix, dll, count in [('tmp', 'Unity.TextMeshPro.dll', 368), ('unity-ui', 'UnityEngine.UI.dll', 210)]:
                with self.subTest(platform=platform, assembly=dll):
                    result = self.invoke(f'{platform}-{suffix}', root / dll)
                    self.assertEqual(result.returncode, 0, result.stderr.decode(errors='replace'))
                    doc = json.loads(result.stdout)
                    self.assertEqual(doc['sourceInstructionCount'], count)
                    self.assertEqual(len(doc['strings']), count)
                    self.assertEqual(len({row['id'] for row in doc['strings']}), count)
                    self.assertEqual(result.stdout, (WORK / f'managed-strings-v2-{platform}-{suffix}.json').read_bytes())

    def test_wrong_platform_rejected_before_output(self):
        for suffix, dll in [('tmp', 'Unity.TextMeshPro.dll'), ('unity-ui', 'UnityEngine.UI.dll')]:
            with self.subTest(assembly=dll):
                result = self.invoke(f'macos-{suffix}', WIN / dll)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(b'Unsupported or modified game assembly', result.stderr)
                self.assertEqual(result.stdout, b'')


if __name__ == '__main__':
    unittest.main()
