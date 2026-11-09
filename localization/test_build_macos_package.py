from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import build_macos_package as macos
import package_inputs


class MacosPackageTests(unittest.TestCase):
    def test_validation_gates_app_build_and_uses_the_same_snapshot(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory).resolve()
            source, inputs, output = (root / name for name in ('Original.app', 'inputs', 'Output.app'))
            source.mkdir()
            (inputs / 'ui').mkdir(parents=True)
            for name in package_inputs.LOCALE_FILES:
                (inputs / name).write_text(name)
            tools = dict(managed_tool=root / 'managed.dll', speaker_tool=root / 'speaker.dll',
                         speaker_runtime=root / 'runtime.dll', speaker_runtime_sha='test')
            args = (source, inputs, 'ru', root / 'inventory.json', root / 'scope.json', output)
            with patch.object(package_inputs, 'validate', side_effect=ValueError('missing dialogue ID')), \
                 patch.object(macos.build_game, 'build') as build:
                with self.assertRaisesRegex(ValueError, 'missing dialogue ID'):
                    macos.build(*args, **tools)
                build.assert_not_called()
                self.assertFalse(output.exists())

            def validate(platform, data, locale, local, inventory, scope):
                self.assertEqual((platform, data, locale, inventory, scope),
                                 ('macos', source / macos.build_game.ASSET_RELATIVE.parent, 'ru', *args[3:5]))
                self.assertNotEqual(local, inputs)
                self.assertEqual((local / 'dialogue.json').read_text(), 'dialogue.json')
                (inputs / 'dialogue.json').write_text('changed after snapshot')
                return {'localeInputSha256': {'dialogue.json': 'verified'}}, set()

            def build_app(*args, **kwargs):
                self.assertEqual(args[1].read_text(), 'dialogue.json')
                self.assertEqual(args[3], output)
                self.assertTrue(kwargs['restore_yarn_transitions'])
                self.assertTrue(kwargs['improve_speaker_contrast'])
                self.assertEqual(kwargs['package_receipt']['localeInputSha256'], {'dialogue.json': 'verified'})
                return {'output': str(output)}

            with patch.object(package_inputs, 'validate', side_effect=validate), \
                 patch.object(macos.build_game, 'build', side_effect=build_app):
                self.assertEqual(macos.build(*args, **tools), {'output': str(output)})
