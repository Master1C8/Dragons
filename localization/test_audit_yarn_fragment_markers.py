import json
from pathlib import Path
import unittest

import audit_yarn_fragment_markers as markers

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')
REPORT = Path(__file__).parent / 'evidence/yarn-fragment-markers-20261110.json'


class MarkerBoundaryTests(unittest.TestCase):
    def test_marker_target_is_rejected_after_matching_control(self):
        suffix = [(20, [])]
        text = {'open': '==', 'title': 'title: Next', 'close': '---'}
        host = [(1, [(1, 0, 1)]), (15, []),
                *((3, [(1, 2, key.encode())]) for key in text), *suffix]
        self.assertEqual(markers.prove_block(host, suffix, 5, 'Next', text)['ids'], list(text))
        host[0] = (1, [(1, 0, 2)])
        with self.assertRaisesRegex(ValueError, 'local target can enter the embedded block at 2'):
            markers.prove_block(host, suffix, 5, 'Next', text)

    @unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned original builds are required')
    def test_real_programs_reproduce_pinned_marker_blocks(self):
        receipt = json.loads(REPORT.read_bytes())
        for platform, path in [('macos', MAC), ('windows', WIN)]:
            with self.subTest(platform=platform):
                blocks, programs = markers.inspect(path, platform)
                self.assertEqual(blocks, receipt['blocks'])
                self.assertEqual(programs, receipt['builds'][platform])
                self.assertEqual(sum(len(block['ids']) for block in blocks.values()), 15)
