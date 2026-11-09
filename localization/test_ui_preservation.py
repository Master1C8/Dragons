import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import map_ui_hierarchy as ui_map
import ui_locale as mac_ui
import ui_preservation
import windows_ui_locale as windows_ui

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


class UiPreservationTests(unittest.TestCase):
    def test_changed_manifest_fails_before_processing_roles(self):
        with tempfile.TemporaryDirectory() as folder:
            report = Path(folder) / 'roles.json'
            report.write_text('{"entries": []}', encoding='utf-8')
            with patch.object(ui_preservation, 'ROLES', report):
                with self.assertRaisesRegex(ValueError, 'UI preservation report fingerprint mismatch'):
                    ui_preservation.validate('macos', 'level0', {}, {})

    @unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned game builds required')
    def test_both_adapters_reject_edits_to_each_protected_ui_family(self):
        examples = (
            ('level0', 'version-display-needs-consumer-review', 'Version\n'),
            ('level1', 'dialogue-presenter-template-needs-consumer-review', 'Character Name'),
            ('sharedassets0.assets', 'settings-prefab-template-needs-consumer-review', 'LABEL'),
            ('level2', 'cheat-menu-text-needs-visibility-review', 'DELETE SAVE'),
        )
        report = json.loads(ui_preservation.ROLES.read_bytes())
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            for platform, source, scanner, hashes in (
                    ('macos', MAC, mac_ui.scan, mac_ui.ASSETS),
                    ('windows', WIN, windows_ui.scan, ui_map.WINDOWS_ASSETS)):
                for asset, role, value in examples:
                    with self.subTest(platform=platform, role=role):
                        _, objects = scanner(source, asset)
                        source_text = {k: v[2] for k, v in objects.items()}
                        key = next(row[platform]['id'] for row in report['entries']
                                   if row['asset'] == asset and row['provisionalRole'] == role
                                   and source_text[row[platform]['id']] == value)
                        ui_preservation.validate(platform, asset, source_text, {key: value})
                        locale = root / f'{platform}-{asset}.json'
                        locale.write_text(json.dumps({
                            'schema': 1, 'locale': 'ru', 'sourceObjectSha256': hashes[asset],
                            'lines': {key: {'source': value, 'text': value + ' SYNTHETIC'}},
                        }), encoding='utf-8')
                        output = root / f'{platform}-{asset}.out'
                        with self.assertRaisesRegex(ValueError, f'protected UI text must remain exact: {key}'):
                            if platform == 'macos':
                                mac_ui.patch_into(source, asset, locale, 'ru', output)
                            else:
                                windows_ui.build(source, asset, locale, 'ru', output)
                        self.assertFalse(output.exists())
