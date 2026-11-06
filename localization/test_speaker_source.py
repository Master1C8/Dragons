from collections import Counter
import json
from pathlib import Path
import subprocess
import unittest

import inventory_speaker_lines as lines
import inventory_speaker_presenters as presenters

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
TOOL = Path(__file__).parent / 'work/speaker-consumers-bin/speaker-consumers.dll'


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned builds required')
class SpeakerSourceTests(unittest.TestCase):
    def test_delimiters_and_all_known_presenters(self):
        for platform, root in (('macos', MAC), ('windows', WIN)):
            with self.subTest(platform=platform):
                result = lines.inspect(root, platform)
                candidates = result['implicitSpeakerCandidates']
                self.assertEqual(Counter(x['provisionalRole'] for x in candidates),
                                 {'known-character-prefix': 18, 'embedded-title-like-source-marker': 5,
                                  'nonstandard-prefix-needs-review': 1})
                unusual = next(x for x in candidates if x['provisionalRole'] == 'nonstandard-prefix-needs-review')
                self.assertEqual((unusual['id'], unusual['bodyCharacters']), ('line:4b36ea4e', 0))
                data = presenters.inspect(root, platform)
                self.assertFalse(data['unresolvedScripts'])
                self.assertEqual(Counter(x['class'] for x in data['presenters']), {'LinePresenter': 5, 'OptionsPresenter': 5})
                for p in data['presenters']:
                    fields = p['fields']
                    if p['class'] == 'LinePresenter':
                        self.assertEqual(fields['showCharacterNameInLine'], 1)
                        self.assertNotEqual(fields['characterNameText']['m_PathID'], 0)
                        self.assertEqual(p['nonNullTargets']['characterNameText']['script'], 'TMPro.TextMeshProUGUI')
                    else:
                        self.assertEqual(fields['showsLastLine'], 0)
                        self.assertEqual(fields['lastLineCharacterNameText']['m_PathID'], 0)

    @unittest.skipUnless(TOOL.is_file(), 'build pinned speaker-consumers tool first')
    def test_getter_consumers_and_wrong_inventory_guard(self):
        for platform, root, count in (('macos', MAC, 170), ('windows', WIN, 172)):
            with self.subTest(platform=platform):
                result = subprocess.run(['dotnet', str(TOOL), platform, str(root / 'Managed')],
                                        check=True, capture_output=True, text=True)
                report = json.loads(result.stdout)
                self.assertEqual(report['assemblyCount'], count)
                hits = report['directCharacterNameGetterReferences']
                self.assertEqual(len(hits), 4)
                self.assertTrue(all(x['assembly'] == 'YarnSpinner.Unity.dll' for x in hits))
                self.assertEqual(sorted(x['offset'] for x in hits), [224, 274, 547, 624])
                self.assertEqual(sum(x['nextOperand'] == 'System.Void TMPro.TMP_Text::set_text(System.String)' for x in hits), 2)
                self.assertEqual(sum(x['nextOperand'] == 'System.Boolean System.String::IsNullOrWhiteSpace(System.String)' for x in hits), 2)
                setup = report['awakeNameSetup']
                self.assertTrue(any(x['opcode'] == 'stfld' and x['operand'] ==
                                    'UnityEngine.GameObject Yarn.Unity.LinePresenter::characterNameContainer' for x in setup))
        bad = subprocess.run(['dotnet', str(TOOL), 'windows', str(MAC / 'Managed')], capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn('Unsupported managed assembly inventory', bad.stderr)


if __name__ == '__main__':
    unittest.main()
