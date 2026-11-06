import unittest
from pathlib import Path

import compare_yarn_versions as versions
import export_yarn_instructions as exporter

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


class OperandTests(unittest.TestCase):
    def test_utf8_binary_and_numeric_are_preserved(self):
        self.assertEqual(exporter.operand_record(1, 2, b'$flag'),
                         {'field': 1, 'wire': 2, 'hex': '24666c6167', 'utf8': '$flag'})
        self.assertEqual(exporter.operand_record(1, 2, b'\xff'),
                         {'field': 1, 'wire': 2, 'hex': 'ff'})
        self.assertEqual(exporter.operand_record(2, 0, 42), {'field': 2, 'wire': 0, 'unsigned': 42})


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned builds required')
class SourceExportTests(unittest.TestCase):
    def test_every_source_instruction_and_text_binding(self):
        for platform, root in (('macos', MAC), ('windows', WIN)):
            with self.subTest(platform=platform):
                keys, texts, _, _, nodes, _ = versions.load(root, versions.BUILDS[platform])
                source = dict(zip(keys, texts))
                report = exporter.export_build(root, platform)
                self.assertEqual(report['nodeCount'], 195)
                self.assertEqual(report['lineCount'], 1839)
                observed = {}
                for name, raw_node in nodes.items():
                    node = report['nodes'][name]
                    self.assertEqual(bytes.fromhex(node['nodeHex']), raw_node)
                    original = [v for f, w, v in versions.protobuf_fields(raw_node) if (f, w) == (7, 2)]
                    self.assertEqual([bytes.fromhex(row['encodedHex']) for row in node['instructions']], original)
                    for row in node['instructions']:
                        if 'lineId' in row:
                            self.assertNotIn(row['lineId'], observed)
                            observed[row['lineId']] = row['source']
                self.assertEqual(observed, source)


if __name__ == '__main__':
    unittest.main()
