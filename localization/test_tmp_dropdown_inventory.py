import json
from pathlib import Path
import subprocess
import unittest

import inventory_tmp_dropdowns as dropdowns

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
TOOL = Path(__file__).parent / 'work/text-setter-bin/text-setter-consumers.dll'


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned builds required')
class DropdownInventoryTests(unittest.TestCase):
    def test_serialized_dropdowns_on_both_builds(self):
        for platform, root, object_id in (('macos', MAC, 672), ('windows', WIN, 667)):
            with self.subTest(platform=platform):
                result = dropdowns.inspect(root, platform)
                self.assertFalse(result['unresolvedScripts'])
                self.assertEqual(len(result['assets']), 17)
                self.assertEqual(len(result['dropdowns']), 1)
                item = result['dropdowns'][0]
                self.assertEqual((item['asset'], item['objectId'], item['multiSelect'], item['optionCount']),
                                 ('sharedassets0.assets', object_id, False, 0))

    @unittest.skipUnless(TOOL.is_file(), 'build pinned text-setter-consumers tool first')
    def test_direct_sinks_factory_refs_and_wrong_inventory_guard(self):
        for platform, root, assembly_count in (('macos', MAC, 170), ('windows', WIN, 172)):
            with self.subTest(platform=platform):
                result = subprocess.run(['dotnet', str(TOOL), platform, str(root / 'Managed')],
                                        capture_output=True, text=True, check=True)
                data = json.loads(result.stdout)
                self.assertEqual((data['assemblyCount'], len(data['sites'])), (assembly_count, 249))
                direct = [x for x in data['sites'] if x['assembly'] == 'Assembly-CSharp.dll']
                self.assertEqual(len(direct), 11)
                self.assertEqual(sum(x['preceding'][-1]['operand'] == 'NEW' for x in direct), 3)
                self.assertEqual(len(data['selectedDropdownFieldReferences']), 8)
                self.assertTrue(any(x['opcode'] == 'stfld' and 'set_MultiSelect' in x['method']
                                    for x in data['multiSelectReferences']))
                self.assertFalse(any(x['opcode'] in ('call', 'callvirt') for x in data['multiSelectReferences']))
                self.assertEqual({x['assembly'] for x in data['defaultControlFactoryCallSites']},
                                 {'Unity.TextMeshPro.dll', 'UnityEngine.UI.dll'})
        bad = subprocess.run(['dotnet', str(TOOL), 'windows', str(MAC / 'Managed')],
                             capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)
        self.assertIn('Unsupported managed assembly inventory', bad.stderr)


if __name__ == '__main__':
    unittest.main()
