import tempfile
import unittest
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import inventory_text_assets as inventory
import inventory_yarn_bindings as bindings
import settings_locale as settings
import verify_text_assets as verifier

SOURCE = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WORK = Path(__file__).parent / 'work'
READY = SOURCE.is_dir() and WORK.is_dir()


class SnapshotComparisonTests(unittest.TestCase):
    def test_exact_bytes_and_identity_are_required(self):
        verifier.compare_snapshots({'asset#1': b'original'}, {'asset#1': b'original'})
        with self.assertRaisesRegex(ValueError, 'preserve-exact mismatch: asset#1'):
            verifier.compare_snapshots({'asset#1': b'original'}, {'asset#1': b'changed'})
        with self.assertRaisesRegex(ValueError, 'TextAsset identity mismatch'):
            verifier.compare_snapshots({'asset#1': b'original'}, {'asset#2': b'original'})


@unittest.skipUnless(READY, 'pinned macOS game and test work directory required')
class TextAssetPreservationTests(unittest.TestCase):
    def setUp(self):
        self.source_report = inventory.inspect(SOURCE, 'macos')
        self.tmp = tempfile.TemporaryDirectory(prefix='text-preserve-', dir=WORK)
        self.root = Path(self.tmp.name)
        for name in self.source_report['assets']:
            (self.root / name).symlink_to(SOURCE / name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_changed_resources(self, mutate):
        env = UnityPy.load(str(SOURCE / 'resources.assets'))
        env.path = str(SOURCE)
        mutate(env)
        path = self.root / 'resources.assets'
        path.unlink()  # Only the symlink created by this fixture.
        path.write_bytes(env.file.save())

    def test_changed_line_break_payload_is_rejected(self):
        self.assertEqual(verifier.verify(SOURCE, self.root, 'macos')['exactTextAssets'], 4)
        def mutate(env):
            obj = next(o for o in env.objects if o.path_id == 20 and o.type.name == 'TextAsset')
            name, value = inventory.parse_text_asset(obj.get_raw_data())
            obj.set_raw_data(dl.write_string(name) + dl.write_string(value + 'X'))
        self.write_changed_resources(mutate)
        with self.assertRaisesRegex(ValueError, 'preserve-exact mismatch: resources.assets#20'):
            verifier.verify(SOURCE, self.root, 'macos')

    def test_changed_line_break_reference_is_rejected(self):
        self.assertEqual(verifier.verify(SOURCE, self.root, 'macos')['lineBreakReferences'], 'unchanged')
        def mutate(env):
            obj = next(o for o in env.objects if o.path_id == 1388 and o.type.name == 'MonoBehaviour')
            gen = bindings.generator(SOURCE, 'macos')
            _, _, schema = settings.nodes_for(obj, gen, {})
            tree = obj.read_typetree(nodes=schema, check_read=True)
            self.assertEqual(obj.save_typetree(tree, nodes=schema), obj.get_raw_data())
            tree['m_leadingCharacters']['m_PathID'] = 22
            obj.set_raw_data(obj.save_typetree(tree, nodes=schema))
        self.write_changed_resources(mutate)
        with self.assertRaisesRegex(ValueError, 'TMP line-break references changed'):
            verifier.verify(SOURCE, self.root, 'macos')

    def test_changed_line_break_mode_is_rejected(self):
        self.assertEqual(verifier.verify(SOURCE, self.root, 'macos')['lineBreakMode'], 'unchanged')
        def mutate(env):
            obj = next(o for o in env.objects if o.path_id == 1388 and o.type.name == 'MonoBehaviour')
            gen = bindings.generator(SOURCE, 'macos')
            _, _, schema = settings.nodes_for(obj, gen, {})
            tree = obj.read_typetree(nodes=schema, check_read=True)
            self.assertEqual(obj.save_typetree(tree, nodes=schema), obj.get_raw_data())
            self.assertEqual(tree['m_UseModernHangulLineBreakingRules'], 0)
            tree['m_UseModernHangulLineBreakingRules'] = 1
            obj.set_raw_data(obj.save_typetree(tree, nodes=schema))
        self.write_changed_resources(mutate)
        with self.assertRaisesRegex(ValueError, 'TMP line-break mode changed'):
            verifier.verify(SOURCE, self.root, 'macos')

    def test_source_directory_cannot_be_its_own_result(self):
        with self.assertRaisesRegex(ValueError, 'separate game data directory'):
            verifier.verify(SOURCE, SOURCE, 'macos')


if __name__ == '__main__':
    unittest.main()
