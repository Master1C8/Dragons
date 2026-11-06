import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))
spec = importlib.util.spec_from_file_location('run_game', Path(__file__).with_name('run_game.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.app = Path(self.temp.name) / 'Fixture.app'
        exe = self.app / 'Contents/MacOS/DragNWash'
        exe.parent.mkdir(parents=True)
        exe.write_bytes(b'fixture')
        (exe.parent / 'steam_appid.txt').write_bytes(b'1234')
        marker = self.app / 'Contents/Resources/vn-localization-build.json'
        marker.parent.mkdir(parents=True)
        marker.write_text(json.dumps({'schema': 1, 'locale': 'ru',
                                      'sourceAssetSha256': module.dl.ASSET_HASH,
                                      'steamFileSha256': hashlib.sha256(b'1234').hexdigest()}))
        self.root_file = self.app / 'steam_appid.txt'

    def tearDown(self):
        self.temp.cleanup()

    def test_cleanup_only_the_expected_generated_file(self):
        root_file = self.root_file
        class Process:
            pid = 123
            def wait(self):
                root_file.write_bytes(b'1234')
                return 0
        with patch.object(module.subprocess, 'run') as verify, patch.object(module.subprocess, 'Popen', return_value=Process()):
            self.assertEqual(module.run(self.app, []), 0)
            self.assertEqual(verify.call_count, 2)
        self.assertFalse(self.root_file.exists())

    def test_unexpected_postlaunch_file_is_preserved(self):
        root_file = self.root_file
        class Process:
            pid = 123
            def wait(self):
                root_file.write_bytes(b'owner-data')
                return 0
        with patch.object(module.subprocess, 'run'), patch.object(module.subprocess, 'Popen', return_value=Process()):
            with self.assertRaisesRegex(RuntimeError, 'preserved'):
                module.run(self.app, [])
        self.assertEqual(self.root_file.read_bytes(), b'owner-data')

    def test_preexisting_file_prevents_launch(self):
        self.root_file.write_bytes(b'owner-data')
        with patch.object(module.subprocess, 'Popen') as launch:
            with self.assertRaisesRegex(ValueError, 'before launch'):
                module.run(self.app, [])
            launch.assert_not_called()
        self.assertEqual(self.root_file.read_bytes(), b'owner-data')


if __name__ == '__main__':
    unittest.main()
