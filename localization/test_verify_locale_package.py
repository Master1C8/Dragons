import tempfile
import unittest
from pathlib import Path
import zipfile

from build_windows_package import zip_member
from verify_locale_package import compare_archive, compare_bundle


class LocalePackageComparisonTests(unittest.TestCase):
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
