import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).parent
SCANNER = ROOT / 'work/speaker-presentation-flow-bin/speaker-presentation-flow.dll'
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data/Managed/YarnSpinner.Unity.dll"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data/Managed/YarnSpinner.Unity.dll')


@unittest.skipUnless(SCANNER.is_file() and MAC.is_file() and WIN.is_file(), 'built scanner and both pinned game DLLs required')
class PresenterFlowTests(unittest.TestCase):
    def run_scanner(self, platform, path):
        return subprocess.run(['dotnet', str(SCANNER), platform, str(path)], capture_output=True, text=True)

    def test_same_bounded_control_flow_in_both_builds(self):
        outputs = []
        for platform, path in [('macos', MAC), ('windows', WIN)]:
            result = self.run_scanner(platform, path)
            self.assertEqual(result.returncode, 0, result.stderr)
            outputs.append(json.loads(result.stdout))
        self.assertEqual(outputs[0]['segments'], outputs[1]['segments'])
        line, options = [{i['offset']: i for i in s['instructions']} for s in outputs[0]['segments']]
        self.assertEqual((line[0x8b]['opcode'], line[0x8b]['operand']), ('brfalse.s', 'IL_00bb'))
        self.assertIn('showCharacterNameInLine', line[0x8e]['operand'])
        self.assertEqual((line[0x93]['opcode'], line[0x93]['operand']), ('brfalse.s', 'IL_00a8'))
        self.assertIn('::get_Text()', line[0x9c]['operand'])
        for offset in (0xaf, 0xc2):
            self.assertIn('::get_TextWithoutCharacterName()', line[offset]['operand'])
        self.assertIn('::get_CharacterName()', line[0x112]['operand'])
        self.assertIn('::set_text(', line[0x117]['operand'])
        self.assertIn('::get_Text()', options[0x208]['operand'])
        self.assertEqual((options[0x21b]['opcode'], options[0x21b]['operand']), ('brfalse.s', 'IL_027c'))
        for offset in (0x243, 0x282):
            self.assertIn('::get_TextWithoutCharacterName()', options[offset]['operand'])
        self.assertIn('::get_CharacterName()', options[0x270]['operand'])
        self.assertIn('::set_text(', options[0x275]['operand'])

    def test_wrong_build_is_rejected_at_source_guard(self):
        result = self.run_scanner('macos', WIN)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unsupported Yarn Unity DLL', result.stderr)
        self.assertEqual(result.stdout, '')


if __name__ == '__main__':
    unittest.main()
