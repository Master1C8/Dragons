from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

import inventory_speaker_lines as lines
import inventory_speaker_presenters as presenters
import map_yarn_context as mapping

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
TOOL = Path(__file__).parent / 'work/speaker-consumers-bin/speaker-consumers.dll'
EVIDENCE = Path(__file__).parent / 'evidence'


class ColonCaseBindingTests(unittest.TestCase):
    def test_case_bindings_match_context_map(self):
        case_file = json.loads((EVIDENCE / 'special-scenes-alexander-colon-20261107.json').read_text())
        raw = (EVIDENCE / 'yarn-context-map-20261107.json').read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), case_file['sourceInventorySha256'])
        context = json.loads(raw)
        case = case_file['cases'][0]
        for platform in ('macos', 'windows'):
            self.assertEqual(case['nodeSha256'][platform], context['nodeSha256'][platform][case['node']])
            self.assertTrue(all(context['lineIds'][key][platform]['node'] == case['node']
                                for key in case['sourceLineIds']))
            for choice in case['branchControls']:
                actual = context['lineIds'][choice['choiceId']][platform]
                self.assertEqual((actual['instructionIndex'], actual['destination']),
                                 (choice['instructionIndex'], choice['destination']))


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
                keys, values, _, _, locations, _, _ = mapping.load_platform(root, platform)
                source = dict(zip(keys, values))
                self.assertEqual(source['line:4b36ea4e'],
                                 'The most prestigious college hosting prestigious professors like me:')
                self.assertEqual(source['line:f167e3d7'], 'Alexander!')
                self.assertEqual([(locations[k]['node'], locations[k]['instructionIndex'])
                                  for k in ('line:dd06ed39', 'line:4b36ea4e', 'line:f167e3d7', 'line:6757e4a0')],
                                 [('Alexander_2', 13), ('Alexander_2', 14), ('Alexander_2', 15), ('Alexander_2', 16)])
                self.assertEqual([locations[k]['destination'] for k in ('line:7e9389a7', 'line:f64a5b30')], [10, 18])
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
