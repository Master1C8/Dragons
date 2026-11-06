import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import uuid

WORK = Path(__file__).parent / 'work'
PROBE = WORK / 'speaker-display-bin/speaker-display-probe.dll'
RUNTIME = WORK / 'speaker-display-runtime-bin/speaker-display-runtime-test.dll'
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data/Managed"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data/Managed')
READY = MAC.is_dir() and WIN.is_dir() and PROBE.is_file() and RUNTIME.is_file() and WORK.is_dir()


@unittest.skipUnless(READY, 'both pinned builds and built synthetic probe tools required')
class SpeakerDisplayProbeTests(unittest.TestCase):
    def test_actual_dlls_runtime_identity_and_failure_boundaries(self):
        with tempfile.TemporaryDirectory(prefix='speaker-input-', dir=WORK) as folder:
            root = Path(folder)
            mapping = root / 'synthetic.json'
            mapping.write_text(json.dumps({'schema': 1, 'locale': 'ru', 'map': {'Ryan': 'Жж', 'Conrad': 'ЪъЬь'}},
                                          ensure_ascii=False), encoding='utf-8')
            outputs = []
            try:
                for platform, managed in (('macos', MAC), ('windows', WIN)):
                    with self.subTest(platform=platform):
                        output = WORK / f'speaker-unittest-{uuid.uuid4().hex}.dll'
                        outputs.append(output)
                        source = managed / 'YarnSpinner.Unity.dll'
                        cmd = ['dotnet', str(PROBE), platform, str(source), str(mapping), str(output)]
                        built = subprocess.run(cmd, capture_output=True, text=True, check=True)
                        info = json.loads(built.stdout)
                        self.assertTrue(info['testOnly'])
                        self.assertEqual(info['verifiedExistingMethodBodies'], 717)
                        self.assertEqual(len(info['changedDisplayCallSites']), 2)
                        self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), info['outputSha256'])
                        runtime = subprocess.run(['dotnet', str(RUNTIME), platform, str(managed), str(output), info['outputSha256']],
                                                 capture_output=True, text=True, check=True)
                        check = json.loads(runtime.stdout)
                        self.assertEqual(len(check['checks']), 7)
                        self.assertTrue(all(c['identityBefore'] == c['identityAfter'] for c in check['checks']))
                        unusual = next(c for c in check['checks'] if c['source'].startswith('The most prestigious college'))
                        self.assertEqual(unusual['body'], '')
                        self.assertEqual(unusual['display'], unusual['source'][:-1])
                        digest = hashlib.sha256(output.read_bytes()).hexdigest()
                        collision = subprocess.run(cmd, capture_output=True, text=True)
                        self.assertNotEqual(collision.returncode, 0)
                        self.assertEqual(hashlib.sha256(output.read_bytes()).hexdigest(), digest)
                invalid = root / 'invalid.json'
                invalid.write_text('{"schema":1,"locale":"ru","map":{"Ryan":"Ж","Ryan":"Х","Conrad":"Ъ"}}', encoding='utf-8')
                new_output = WORK / f'speaker-unittest-{uuid.uuid4().hex}.dll'
                outputs.append(new_output)
                bad = subprocess.run(['dotnet', str(PROBE), 'macos', str(MAC / 'YarnSpinner.Unity.dll'), str(invalid), str(new_output)],
                                     capture_output=True, text=True)
                self.assertNotEqual(bad.returncode, 0)
                self.assertIn('Invalid or duplicate source speaker', bad.stderr)
                self.assertFalse(new_output.exists())
                wrong = subprocess.run(['dotnet', str(PROBE), 'windows', str(MAC / 'YarnSpinner.Unity.dll'), str(mapping), str(new_output)],
                                       capture_output=True, text=True)
                self.assertNotEqual(wrong.returncode, 0)
                self.assertIn('Unsupported source DLL', wrong.stderr)
                self.assertFalse(new_output.exists())
                outside = root / 'not-allowed.dll'
                denied = subprocess.run(['dotnet', str(PROBE), 'macos', str(MAC / 'YarnSpinner.Unity.dll'), str(mapping), str(outside)],
                                        capture_output=True, text=True)
                self.assertNotEqual(denied.returncode, 0)
                self.assertIn('Output must be a fresh DLL directly in project work', denied.stderr)
                self.assertFalse(outside.exists())
            finally:
                for path in outputs:
                    path.unlink(missing_ok=True)


if __name__ == '__main__':
    unittest.main()
