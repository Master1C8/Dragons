import unittest
from pathlib import Path

import inventory_level_dialogues as levels

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


class SchemaGuardTests(unittest.TestCase):
    def test_unexpected_schema_is_rejected(self):
        class FakeSchema:
            def to_dict_list(self):
                return [{'m_Level': 1, 'm_Name': 'unexpected', 'm_Type': 'string', 'm_MetaFlag': 0}]
        with self.assertRaisesRegex(ValueError, 'unexpected LevelConfiguration fields'):
            levels.corrected_schema(FakeSchema())

    def test_named_closure_handles_cycles_and_missing_targets(self):
        code = {'a': [(16, [(1, 2, b'b')]), (3, [(1, 2, b'line:11111111')])],
                'b': [(16, [(1, 2, b'a')]), (18, [(1, 2, b'missing')])]}
        result = levels.named_closure({'a'}, code)
        self.assertEqual(result['nodes'], ['a', 'b'])
        self.assertEqual(result['lineIds'], ['line:11111111'])
        self.assertEqual(result['unresolved'], [{'node': 'b', 'instructionIndex': 1, 'target': 'missing'}])
        with self.assertRaisesRegex(ValueError, 'roots include absent node'):
            levels.named_closure({'missing'}, code)


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned game builds required')
class SourceTests(unittest.TestCase):
    def test_configs_and_named_closure_on_both_builds(self):
        for platform, root, node_count, line_count in (
                ('macos', MAC, 108, 1289), ('windows', WIN, 112, 1303)):
            with self.subTest(platform=platform):
                report = levels.inspect(root, platform)
                refs = [ref for item in report['configurations'] for ref in item['dialogueReferences']]
                self.assertEqual(len(report['configurations']), 15)
                self.assertEqual(len(refs), 93)
                self.assertTrue(all(ref['targetPresent'] for ref in refs))
                closure = report['namedTransferClosure']
                self.assertEqual(len(closure['roots']), 83)
                self.assertEqual(len(closure['nodes']), node_count)
                self.assertEqual(len(closure['lineIds']), line_count)
                self.assertNotIn('Start', closure['nodes'])
                expected = [] if platform == 'macos' else [
                    {'node': 'Conrad_Outro', 'instructionIndex': 21, 'target': 'Conrad_OutroDone'}]
                self.assertEqual(closure['unresolved'], expected)
                first = next(x for x in report['configurations'] if x['name'] == 'Alexander_1_3')
                self.assertIn({'field': 'progressDialogs', 'index': 0, 'target': 'Alexander_1_required',
                               'targetPresent': True}, first['dialogueReferences'])


if __name__ == '__main__':
    unittest.main()
