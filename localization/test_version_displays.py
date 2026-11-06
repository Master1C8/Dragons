import json
from pathlib import Path
import subprocess
import unittest

import inventory_version_displays as inventory

ROOT = Path(__file__).parent
MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
TOOL = ROOT / 'work/text-setter-bin/text-setter-consumers.dll'


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned builds required')
class VersionDisplaysTests(unittest.TestCase):
    def test_serialized_text_components_match_previously_mapped_fields(self):
        mapped = json.loads((ROOT / 'evidence/ui-source-roles-20261107.json').read_text())['entries']
        for platform, source in (('macos', MAC), ('windows', WIN)):
            with self.subTest(platform=platform):
                report = inventory.inspect(source, platform)
                self.assertFalse(report['unresolvedScripts'])
                rows = report['versionDisplays']
                self.assertEqual(len(rows), 7)
                found = {(f"{r['asset']}#{r['text']['objectId']}", r['text']['textSha256']) for r in rows}
                expected = {(r[platform]['id'], r[platform]['sourceTextSha256']) for r in mapped
                            if r['provisionalRole'] == 'version-display-needs-consumer-review'}
                self.assertEqual(found, expected)
                self.assertTrue(all(r['gameObjectName'] == 'VersionText' for r in rows))
                self.assertEqual({r['text']['class'] for r in rows}, {'TextMeshProUGUI'})

    @unittest.skipUnless(TOOL.is_file(), 'build pinned text-setter-consumers first')
    def test_direct_version_setter_path_on_both_builds(self):
        for platform, source in (('macos', MAC), ('windows', WIN)):
            with self.subTest(platform=platform):
                result = subprocess.run(['dotnet', str(TOOL), platform, str(source / 'Managed')],
                                        capture_output=True, text=True, check=True)
                report = json.loads(result.stdout)
                hits = [s for s in report['sites'] if s['assembly'] == 'Assembly-CSharp.dll'
                        and s['method'] == 'System.Void VersionNumber::Start()']
                self.assertEqual(len(hits), 1)
                self.assertEqual(hits[0]['setter'], 'System.Void TMPro.TMP_Text::set_text(System.String)')
                self.assertEqual([x['operand'] for x in hits[0]['preceding']], [
                    None, '!!0 UnityEngine.Component::GetComponent<TMPro.TMP_Text>()',
                    'System.String UnityEngine.Application::get_version()'])


if __name__ == '__main__':
    unittest.main()
