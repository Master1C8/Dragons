import json
from pathlib import Path
import subprocess
import unittest

import ui_locale
import windows_ui_locale

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
TOOL = Path(__file__).parent / 'work/menu-reason-bin/menu-reason-source.dll'


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned builds required')
class MenuReasonSourceTests(unittest.TestCase):
    def test_confirmation_label_is_a_separate_serialized_field(self):
        for root, adapter, key in ((MAC, ui_locale, 'level0#5208'), (WIN, windows_ui_locale, 'level0#5187')):
            with self.subTest(key=key):
                _, rows = adapter.scan(root, 'level0')
                self.assertEqual(rows[key][2], 'Really Delete Save?')

    @unittest.skipUnless(TOOL.is_file(), 'build pinned menu-reason-source tool first')
    def test_reason_argument_and_source_guard(self):
        for platform, root in (('macos', MAC), ('windows', WIN)):
            with self.subTest(platform=platform):
                result = subprocess.run(['dotnet', str(TOOL), platform, str(root / 'Managed/Assembly-CSharp.dll')],
                                        capture_output=True, text=True, check=True)
                data = json.loads(result.stdout)
                self.assertEqual(data['occurrenceOffsets'], [447, 479, 511])
                self.assertEqual(data['getReasonReferences'], [])
                self.assertEqual(len(data['reasonFieldAccesses']), 2)
        result = subprocess.run(['dotnet', str(TOOL), 'windows', str(MAC / 'Managed/Assembly-CSharp.dll')],
                                capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unsupported source assembly', result.stderr)


if __name__ == '__main__':
    unittest.main()
