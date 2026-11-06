import hashlib
import json
from pathlib import Path
import subprocess
import unittest
import uuid

ROOT = Path(__file__).parent
WORK = ROOT / 'work'
PATCHER = WORK / 'speaker-line-probe-bin/speaker-line-probe.dll'
HARNESS = WORK / 'speaker-line-runtime-test-bin/speaker-line-runtime-test.dll'
MAPPING = WORK / 'speaker-map-synthetic-20261107.json'
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data/Managed"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data/Managed')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@unittest.skipUnless(all(p.exists() for p in (PATCHER, HARNESS, MAPPING, MAC, WIN)), 'both tools, mapping, and pinned game builds required')
class SpeakerLineTests(unittest.TestCase):
    def test_source_id_and_value_guard_on_both_builds(self):
        for platform, managed, known in [
            ('macos', MAC, WORK / 'YarnSpeakerLineSyntheticMac-v2-20261107.dll'),
            ('windows', WIN, WORK / 'YarnSpeakerLineSyntheticWindows-v2-20261107.dll'),
        ]:
            with self.subTest(platform=platform):
                source = managed / 'YarnSpinner.Unity.dll'
                original_hash = sha(source)
                output = WORK / f'speaker-line-test-{uuid.uuid4().hex}.dll'
                try:
                    result = subprocess.run(['dotnet', str(PATCHER), platform, str(source), str(MAPPING), str(output)],
                                            cwd=ROOT.parent, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    doc = json.loads(result.stdout)
                    self.assertTrue(doc['testOnly'])
                    self.assertEqual(doc['syntheticLineId'], 'line:4b36ea4e')
                    self.assertEqual(len(doc['providerIdBindings']), 2)
                    self.assertEqual(len(doc['changedDisplayCallSites']), 2)
                    self.assertEqual(doc['verifiedExistingMethodBodies'], 717)
                    self.assertEqual(doc['outputSha256'], sha(output))
                    self.assertEqual(sha(output), sha(known))
                    harness = subprocess.run(['dotnet', str(HARNESS), platform, str(managed), str(output), sha(output)],
                                             cwd=ROOT.parent, capture_output=True, text=True)
                    self.assertEqual(harness.returncode, 0, harness.stderr)
                    checks = json.loads(harness.stdout)['checks']
                    self.assertEqual(len(checks), 8)
                    self.assertEqual(checks[0]['display'], 'ЖЪЬ42')
                    self.assertEqual(checks[0]['body'], '')
                    self.assertEqual(checks[1]['display'], checks[1]['identityBefore'])
                    self.assertEqual(checks[2]['display'], 'Different college')
                    self.assertEqual(checks[3]['display'], checks[3]['identityBefore'])
                    self.assertEqual([checks[4]['display'], checks[5]['display']], ['Жж', 'ЪъЬь'])
                    self.assertTrue(all(c['identityBefore'] == c['identityAfter'] for c in checks))
                    self.assertEqual(sha(source), original_hash)
                finally:
                    output.unlink(missing_ok=True)

    def test_wrong_build_rejected_before_output(self):
        output = WORK / f'speaker-line-test-{uuid.uuid4().hex}.dll'
        result = subprocess.run(['dotnet', str(PATCHER), 'macos', str(WIN / 'YarnSpinner.Unity.dll'), str(MAPPING), str(output)],
                                cwd=ROOT.parent, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Unsupported source DLL', result.stderr)
        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
