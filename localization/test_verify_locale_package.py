import tempfile
import unittest
from pathlib import Path
import struct
import zipfile

from build_windows_package import zip_member
from verify_locale_package import compare_archive, compare_bundle
from verify_serialized_metadata import HEADER, OBJECT, compare_metadata


class LocalePackageComparisonTests(unittest.TestCase):
    def test_serialized_metadata_allows_relocation_and_rejects_external_change(self):
        def asset(payload, external=b'other.assets'):
            types = struct.pack('<iBi', 2, 0, 1) + struct.pack('<iBh', 1, 0, -1) + bytes(16)
            prefix = b'6000.3.14f1\0' + types + struct.pack('<i', 2)
            prefix += bytes((-len(prefix)) % 4)
            padded = payload + bytes((-len(payload)) % 8)
            objects = OBJECT.pack(1, 0, len(payload), 0) + OBJECT.pack(2, len(padded), 4, 0)
            references = (struct.pack('<ii', 0, 1) + b'\0' + bytes(16) + struct.pack('<i', 2)
                          + external + b'\0' + struct.pack('<i', 0) + b'\0')
            metadata = prefix + objects + references
            data_offset = (HEADER.size + len(metadata) + 15) & ~15
            data = padded + b'tail'
            header = HEADER.pack(0, 0, 22, 0, 0, bytes(3), len(metadata), data_offset + len(data),
                                 data_offset, 0)
            return header + metadata + bytes(data_offset - HEADER.size - len(metadata)) + data

        original = asset(b'old')
        relocated = asset(b'new longer text')
        self.assertEqual(compare_metadata(original, relocated)['objects'], 2)
        with self.assertRaisesRegex(ValueError, 'serialized metadata differs'):
            compare_metadata(original, asset(b'new longer text', b'wrong.assets'))
        with self.assertRaisesRegex(ValueError, 'invalid Unity object extent or padding'):
            compare_metadata(original, asset(b'old').replace(b'old\0', b'old!'))

    def test_archive_compares_payload_with_matching_inventory_and_receipt(self):
        member = 'DragNWash_Data/sharedassets1.assets'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference = root / 'reference.zip'
            matching = root / 'matching.zip'
            changed = root / 'changed.zip'
            for path, payload in ((reference, b'expected'), (matching, b'expected'), (changed, b'replaced')):
                with zipfile.ZipFile(path, 'x') as archive:
                    archive.writestr(zip_member('manifest.json'), b'{}')
                    archive.writestr(zip_member(member), payload)

            self.assertEqual(compare_archive(reference, matching), {'verifiedArchiveMembers': 2})
            with self.assertRaisesRegex(ValueError, f'archive member differs from verified rebuild: {member}'):
                compare_archive(reference, changed)

    def test_bundle_checks_bytes_even_outside_localized_assets(self):
        name = 'Contents/Resources/Data/boot.config'
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            reference = root / 'reference.app'
            candidate = root / 'candidate.app'
            for bundle in (reference, candidate):
                file = bundle / name
                file.parent.mkdir(parents=True)
                file.write_bytes(b'stock')

            self.assertEqual(compare_bundle(reference, candidate), {'verifiedBundleFiles': 1})
            (candidate / name).write_bytes(b'other')
            with self.assertRaisesRegex(ValueError, f'bundle entry differs from verified rebuild: {name}'):
                compare_bundle(reference, candidate)
