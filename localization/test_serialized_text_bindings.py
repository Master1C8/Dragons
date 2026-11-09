import json
import os
from pathlib import Path
import subprocess
import unittest

import inventory_serialized_text_bindings as bindings

DATA = {
    'macos': Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data",
    'windows': Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data'),
}
TOOL = os.environ.get('DRAGONS_EXTENDED_TEXT_SINKS_TOOL')


@unittest.skipUnless(all(path.is_dir() for path in DATA.values()), 'both pinned game builds required')
class TextRouteTests(unittest.TestCase):
    def test_serialized_locale_route_and_fallback_configuration(self):
        for platform, root in DATA.items():
            with self.subTest(platform=platform):
                report = bindings.inspect(root, platform)
                self.assertEqual(len(report['sourceAssets']), 17)
                self.assertEqual(report['resolvedBehaviours'], 3498 if platform == 'macos' else 3435)
                self.assertEqual(report['nativeTextOrUiObjects'], [])
                self.assertEqual(len(report['selectedScripts']), 2)
                event, = report['localizedStringEvents']
                self.assertFalse(event['enabled'])
                self.assertEqual((event['table'], event['entryId'], event['entryKey'], event['localVariables']),
                                 ('', 0, '', 0))
                self.assertEqual(event['listeners'], [{
                    'target': {'m_FileID': 0, 'm_PathID': 653 if platform == 'macos' else 648},
                    'method': 'set_text',
                }])
                row, = report['localizationDatabases']
                self.assertEqual(row['projectLocale'], 'en')
                database = row['database']
                self.assertEqual(database['m_DefaultTableReference'], {'m_TableCollectionName': ''})
                self.assertEqual(database['m_MissingTranslationState'], 1)
                self.assertEqual(database['m_NoTranslationFoundMessage'],
                                 "No translation found for '{key}' in {table.TableCollectionName}")

    @unittest.skipUnless(TOOL and Path(TOOL).is_file(), 'compiled extended text sink scanner required')
    def test_extended_managed_references_and_wrong_source(self):
        reports = {}
        for platform, root in DATA.items():
            command = ['dotnet', TOOL, platform, str(root / 'Managed'), '--extended']
            result = subprocess.run(command, check=True, capture_output=True, text=True)
            reports[platform] = json.loads(result.stdout)
        self.assertEqual(reports['macos']['extendedSites'], reports['windows']['extendedSites'])
        self.assertEqual(reports['macos']['imguiHandlers'], [])
        self.assertEqual(reports['windows']['imguiHandlers'], [])
        sites = reports['macos']['extendedSites']
        self.assertFalse(any(site['assembly'] == 'Assembly-CSharp.dll' for site in sites))
        self.assertEqual(sum(site['category'] == 'tmp-method' and
                             site['assembly'] == 'Naelstrof.UnityScriptableSettings.dll' for site in sites), 10)
        self.assertEqual(sum(site['category'] == 'unity-missing-translation' for site in sites), 11)
        wrong = subprocess.run(['dotnet', TOOL, 'windows', str(DATA['macos'] / 'Managed'), '--extended'],
                               capture_output=True, text=True)
        self.assertNotEqual(wrong.returncode, 0)
        self.assertIn('Unsupported managed assembly inventory', wrong.stderr)
        self.assertEqual(wrong.stdout, '')
