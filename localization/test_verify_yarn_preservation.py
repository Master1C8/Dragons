from pathlib import Path
import tempfile
import unittest

import UnityPy
import compare_yarn_versions as versions
import dialogue_locale as dl
import verify_yarn_preservation as check

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
WORK = Path(__file__).parent / 'work'


class ExactObjectComparisonTests(unittest.TestCase):
    def test_changed_project_metadata_and_inventory_rejected(self):
        loc = (10, 'MonoBehaviour')
        project = (20, 'MonoBehaviour')
        other = (30, 'TextAsset')
        before = {loc: b'old locale', project: b'compiled branch', other: b'untouched'}
        good = {loc: b'new locale', project: b'compiled branch', other: b'untouched'}
        self.assertEqual(check.compare_objects(before, good, 10, b'new locale'), loc)
        for key, value in ((project, b'compiled brancH'), (loc, b'new localE'), (other, b'changed')):
            with self.subTest(key=key):
                bad = dict(good)
                bad[key] = value
                with self.assertRaisesRegex(ValueError, 'candidate object differs from expected'):
                    check.compare_objects(before, bad, 10, b'new locale')
        missing = dict(good)
        del missing[other]
        with self.assertRaisesRegex(ValueError, 'candidate Unity object inventory changed'):
            check.compare_objects(before, missing, 10, b'new locale')

    def test_real_localization_metadata_is_compared_byte_for_byte(self):
        # Parser/encoder fixture models the real object format without loading a game.
        header = bytearray(36)
        header[28:36] = b'\x02\0\0\0en\0\0'
        keys = [f'line:{i:08x}' for i in range(1839)]
        values = ['TEST'] * len(keys)
        extras = [bytes(24)] * len(keys)
        source = dl.encode(bytes(header), keys, values, extras)
        changed = dl.encode(source, keys, values, [b'\x01' + bytes(23), *extras[1:]])
        loc = (10, 'MonoBehaviour')
        with self.assertRaisesRegex(ValueError, 'candidate object differs from expected'):
            check.compare_objects({loc: source}, {loc: changed}, 10, source)
        self.assertEqual(check.compare_objects({loc: source}, {loc: source}, 10, source), loc)


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned original builds required')
class ActualAssetTests(unittest.TestCase):
    def test_source_pinned_synthetic_yarn_outputs(self):
        samples = [
            ('macos', MAC, WORK / 'DragNWash-SpeakerRuntimeLogProbe.app/Contents/Resources/Data/sharedassets1.assets',
             WORK / 'atomic-builder-synthetic-20261107.json'),
            ('windows', WIN, WORK / 'windows-preservation-synthetic-20261107.assets',
             WORK / 'windows-preservation-synthetic-20261107.json'),
        ]
        for platform, source, candidate, locale in samples:
            if not candidate.is_file() or not locale.is_file():
                self.skipTest('specific isolated synthetic artifacts required')
            with self.subTest(platform=platform):
                report = check.verify(platform, source, candidate, locale)
                self.assertEqual(report['sourceProjectObjectSha256'], versions.BUILDS[platform]['projectSha256'])
                self.assertEqual(report['expectedEntries'], 1)
                self.assertGreater(report['verifiedObjects'], 11000)

    def test_real_compiled_program_change_is_rejected(self):
        candidate = WORK / 'DragNWash-SpeakerRuntimeLogProbe.app/Contents/Resources/Data/sharedassets1.assets'
        locale = WORK / 'atomic-builder-synthetic-20261107.json'
        if not candidate.is_file() or not locale.is_file():
            self.skipTest('specific isolated synthetic artifact required')
        env = UnityPy.load(str(candidate))
        project_id = versions.BUILDS['macos']['project']
        obj = next(o for o in env.objects if o.path_id == project_id)
        raw = bytearray(obj.get_raw_data())
        raw[50] ^= 1
        obj.set_raw_data(bytes(raw))
        with tempfile.TemporaryDirectory(prefix='yarn-preserve-', dir=WORK) as folder:
            altered = Path(folder) / 'altered.assets'
            altered.write_bytes(env.file.save())
            with self.assertRaisesRegex(ValueError, 'candidate object differs from expected.*10719'):
                check.verify('macos', MAC, altered, locale)


if __name__ == '__main__':
    unittest.main()
