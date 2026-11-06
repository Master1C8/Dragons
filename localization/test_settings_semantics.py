import json
from pathlib import Path
import subprocess
import unittest

import compare_settings_sources as comparison
import settings_locale as settings

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
TOOL = Path(__file__).parent / 'work/settings-semantics-bin/settings-semantics.dll'


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned builds required')
class SettingsSemanticsTests(unittest.TestCase):
    def test_pinned_option_sources_are_indexed_and_resolution_preserved(self):
        _, _, mac_trees, _, _, _ = settings.scan(MAC)
        win_trees, win_types = comparison.windows_scan(WIN)
        a = comparison.collect(mac_trees, settings.EXPECTED, include_source=True)
        b = comparison.collect(win_trees, win_types, include_source=True)
        for values in (a, b):
            options = values['CrouchControl']['fields']
            self.assertEqual([options[f'option:{i}']['source'] for i in range(3)], ['Tap/Hold', 'Toggle', 'Hold'])
            fullscreen = values['WindowMode']['fields']
            self.assertEqual([fullscreen[f'option:{i}']['source'] for i in range(4)],
                             ['Exclusive', 'Fullscreen', 'Maxed Window', 'Windowed'])
            resolution = values['Resolution']['fields']
            self.assertEqual(len(resolution) - 1, 42)
            self.assertTrue(all(v['provisionalRole'] == 'preserve-exactly' for k, v in resolution.items() if k != 'label'))
            self.assertEqual(values['MasterVolume']['fields']['label']['source'], '')

    @unittest.skipUnless(TOOL.is_file(), 'build pinned settings-semantics tool first')
    def test_both_builds_and_wrong_build_rejection(self):
        for platform, root in (('macos', MAC), ('windows', WIN)):
            with self.subTest(platform=platform):
                result = subprocess.run(['dotnet', str(TOOL), platform, str(root / 'Managed/Naelstrof.UnityScriptableSettings.dll')],
                                        capture_output=True, text=True, check=True)
                report = json.loads(result.stdout)
                self.assertEqual(len(report['methods']), 7)
                resolution = next(x for x in report['methods'] if 'SettingResolution::GetLocalizedDropdowns' in x['signature'])
                refs = [x['operand'] for x in resolution['instructions']]
                self.assertIn('UnityEngine.Resolution[] UnityEngine.Screen::get_resolutions()', refs)
                self.assertFalse(any(isinstance(ref, str) and '::dropdownOptions' in ref for ref in refs))
        wrong = subprocess.run(['dotnet', str(TOOL), 'windows', str(MAC / 'Managed/Naelstrof.UnityScriptableSettings.dll')],
                               capture_output=True, text=True)
        self.assertNotEqual(wrong.returncode, 0)
        self.assertIn('Unsupported settings assembly', wrong.stderr)


if __name__ == '__main__':
    unittest.main()
