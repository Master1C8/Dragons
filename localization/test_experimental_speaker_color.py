import hashlib
from pathlib import Path
import shutil
import tempfile
import unittest

import UnityPy
import experimental_speaker_color as experiment
import settings_locale as settings
import probe_font_roles as fonts

SOURCE = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"


@unittest.skipUnless(SOURCE.is_dir(), 'pinned macOS game required')
class SpeakerColorExperimentTests(unittest.TestCase):
    def test_exact_color_fields_and_repeated_application_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / 'level1'
            shutil.copyfile(SOURCE / 'level1', target)
            original = hashlib.sha256(target.read_bytes()).hexdigest()
            with self.assertRaisesRegex(ValueError, 'supported tools and locale'):
                experiment.patch_into(SOURCE, target, 'zz')
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), original)
            result = experiment.patch_into(SOURCE, target, 'ru')
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), result)
            original_env = UnityPy.load(str(SOURCE / 'level1')); original_env.path = str(SOURCE)
            after_env = UnityPy.load(str(target)); after_env.path = str(SOURCE)
            before = {(o.path_id, o.type.name): o for o in original_env.objects}
            after = {(o.path_id, o.type.name): o for o in after_env.objects}
            self.assertEqual(before.keys(), after.keys())
            self.assertEqual([k for k in before if before[k].get_raw_data() != after[k].get_raw_data()], [(3900, 'MonoBehaviour')])
            generator = settings.make_generator(SOURCE)
            original_tree = fonts.read_tree(before[(3900, 'MonoBehaviour')], generator)
            changed_tree = fonts.read_tree(after[(3900, 'MonoBehaviour')], generator)
            self.assertEqual(changed_tree['m_fontColor'], experiment.BLACK)
            self.assertEqual(changed_tree['m_fontColor32'], {'rgba': 4278190080})
            changed_tree['m_fontColor'] = original_tree['m_fontColor']
            changed_tree['m_fontColor32'] = original_tree['m_fontColor32']
            self.assertEqual(changed_tree, original_tree)
            with self.assertRaisesRegex(ValueError, 'unexpected speaker color target object'):
                experiment.patch_into(SOURCE, target, 'ru')
            self.assertEqual(hashlib.sha256(target.read_bytes()).hexdigest(), result)

    def test_original_target_rejected(self):
        with self.assertRaisesRegex(ValueError, 'separate regular copied asset'):
            experiment.patch_into(SOURCE, SOURCE / 'level1', 'ru')


if __name__ == '__main__':
    unittest.main()
