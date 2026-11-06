import copy
from pathlib import Path
import tempfile
import unittest

import verify_streaming_assets as check

ROOT = Path(__file__).parent
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
MAC_COPY = ROOT / 'work/DragNWash-SpeakerRuntimeLogProbe.app/Contents/Resources/Data'
WIN_COPY = ROOT / 'work/WindowsSettingsCombinedGame/DragNWash_Data'


class StreamingComparisonTests(unittest.TestCase):
    def test_changed_added_and_symlink_files_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            a, b = root / 'a', root / 'b'
            a.mkdir(); b.mkdir()
            (a / 'file.bytes').write_bytes(b'one')
            (b / 'file.bytes').write_bytes(b'one')
            original = check.scan(a)
            check.compare(original, check.scan(b))
            (b / 'file.bytes').write_bytes(b'two')
            with self.assertRaisesRegex(ValueError, 'candidate StreamingAssets file changed: file.bytes'):
                check.compare(original, check.scan(b))
            (b / 'file.bytes').write_bytes(b'one')
            (b / 'extra').write_bytes(b'extra')
            with self.assertRaisesRegex(ValueError, 'candidate StreamingAssets paths changed'):
                check.compare(original, check.scan(b))
            (b / 'extra').unlink()
            (b / 'link').symlink_to(a / 'file.bytes')
            with self.assertRaisesRegex(ValueError, 'unsafe StreamingAssets file'):
                check.scan(b)


@unittest.skipUnless(all(p.is_dir() for p in (MAC, WIN, MAC_COPY, WIN_COPY)), 'both source builds and isolated copies required')
class ActualStreamingTests(unittest.TestCase):
    def test_actual_copies_and_source_guard(self):
        for platform, source, candidate in (('macos', MAC, MAC_COPY), ('windows', WIN, WIN_COPY)):
            with self.subTest(platform=platform):
                report = check.verify(platform, source, candidate)
                self.assertEqual(report['verifiedFiles'], 31)
                original = check.scan(source / 'StreamingAssets')
                check.validate_source(original, platform)
                modified = copy.deepcopy(original)
                name = next(k for k in modified if k.startswith('APVStreamingAssets/'))
                modified[name]['sha256'] = '0' * 64
                with self.assertRaisesRegex(ValueError, 'unsupported APV inventory or bytes'):
                    check.validate_source(modified, platform)
                modified = copy.deepcopy(original)
                name = next(k for k in modified if k.startswith('aa/'))
                modified[name]['sha256'] = '0' * 64
                with self.assertRaisesRegex(ValueError, 'unsupported Addressables inventory or bytes'):
                    check.validate_source(modified, platform)


if __name__ == '__main__':
    unittest.main()
