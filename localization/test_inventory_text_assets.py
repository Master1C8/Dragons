import unittest

import dialogue_locale as dl
import inventory_text_assets as inventory


class TextAssetParsingTests(unittest.TestCase):
    def test_unicode_payload_and_name_round_trip(self):
        raw = dl.write_string('LineBreaking') + dl.write_string('«Ъь»\n')
        self.assertEqual(inventory.parse_text_asset(raw), ('LineBreaking', '«Ъь»\n'))

    def test_trailing_bytes_are_not_silently_ignored(self):
        raw = dl.write_string('Name') + dl.write_string('Text') + b'\0\0\0\0'
        with self.assertRaisesRegex(ValueError, 'did not round-trip exactly'):
            inventory.parse_text_asset(raw)

    def test_truncated_payload_is_rejected(self):
        raw = dl.write_string('Name') + dl.write_string('Text')[:-1]
        with self.assertRaisesRegex(ValueError, 'invalid string length'):
            inventory.parse_text_asset(raw)


if __name__ == '__main__':
    unittest.main()
