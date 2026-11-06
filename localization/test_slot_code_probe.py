import hashlib
import json
from pathlib import Path
import subprocess
import unittest
import uuid

ROOT = Path(__file__).parent
WORK = ROOT / 'work'
TOOL = WORK / 'slot-code-probe-bin/slot-code-probe.dll'
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data/Managed/Assembly-CSharp.dll"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data/Managed/Assembly-CSharp.dll')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@unittest.skipUnless(TOOL.is_file() and MAC.is_file() and WIN.is_file(), 'built probe and both pinned game assemblies required')
class SlotCodeProbeTests(unittest.TestCase):
    def invoke(self, platform, source, output):
        return subprocess.run(['dotnet', str(TOOL), platform, str(source), str(output)],
                              cwd=ROOT.parent, capture_output=True, text=True)

    def test_separate_synthetic_build_and_original_preservation(self):
        for platform, source in [('macos', MAC), ('windows', WIN)]:
            with self.subTest(platform=platform):
                output = WORK / f'slot-code-test-{uuid.uuid4().hex}.dll'
                original = sha(source)
                try:
                    result = self.invoke(platform, source, output)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    report = json.loads(result.stdout)
                    self.assertTrue(report['testOnly'])
                    self.assertEqual(report['changedOffsets'], [0x85, 0x101, 0x17c])
                    self.assertGreater(report['verifiedExistingMethodBodies'], 100)
                    self.assertEqual(report['sourceSha256'], original)
                    self.assertEqual(report['outputSha256'], sha(output))
                    self.assertNotEqual(sha(output), original)
                    self.assertEqual(sha(source), original)
                    again = self.invoke(platform, source, output)
                    self.assertNotEqual(again.returncode, 0)
                    self.assertIn('Output already exists', again.stderr)
                    self.assertEqual(sha(output), report['outputSha256'])
                finally:
                    output.unlink(missing_ok=True)

    def test_wrong_build_and_outside_destination_rejected(self):
        output = WORK / f'slot-code-test-{uuid.uuid4().hex}.dll'
        result = self.invoke('macos', WIN, output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unsupported source assembly', result.stderr)
        self.assertFalse(output.exists())
        outside = ROOT / f'slot-code-test-{uuid.uuid4().hex}.dll'
        result = self.invoke('macos', MAC, outside)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Output must be a fresh DLL directly in project work', result.stderr)
        self.assertFalse(outside.exists())


if __name__ == '__main__':
    unittest.main()
