import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).parent
TOOL = ROOT / 'work/input-action-source-bin/input-action-source.dll'
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data/Managed/Assembly-CSharp.dll"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data/Managed/Assembly-CSharp.dll')


@unittest.skipUnless(TOOL.is_file() and MAC.is_file() and WIN.is_file(), 'built tool and pinned builds required')
class InputActionSourceTests(unittest.TestCase):
    def test_pinned_constructor_and_source_guard(self):
        expected_json = {
            'macos': '455df1026b374a4310b071daeb8517e68f504a8652d58e17710defa83a57432f',
            'windows': '06bf2f316bc61099bf49a7c654fedaa9918368f856052c729726a771ca8efc34',
        }
        for platform, path in (('macos', MAC), ('windows', WIN)):
            with self.subTest(platform=platform):
                result = subprocess.run(['dotnet', str(TOOL), platform, str(path)],
                                        capture_output=True, text=True, check=True)
                report = json.loads(result.stdout)
                self.assertEqual((report['mapCount'], report['actionCount'], len(report['references'])), (3, 24, 27))
                self.assertEqual(report['jsonLiteral']['utf8Sha256'], expected_json[platform])
                self.assertEqual(report['jsonLiteral']['role'], 'preserve-exactly-input-config')
                self.assertEqual(sum(x['role'] == 'map-key' for x in report['references']), 3)
                self.assertEqual(sum(x['role'] == 'action-key' for x in report['references']), 24)
        bad = subprocess.run(['dotnet', str(TOOL), 'windows', str(MAC)], capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn('Unsupported game assembly', bad.stderr)


if __name__ == '__main__':
    unittest.main()
