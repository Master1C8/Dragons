import json
from pathlib import Path
import tempfile
import unittest
import zipfile

import build_windows_package as windows
import cjk_font_fallback as cjk
import dialogue_locale as dl


class WindowsPackageArchiveTests(unittest.TestCase):
    def test_cjk_license_is_bound_to_the_archive_receipt(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            license = b'license fixture'
            manifest = {'files': {}, 'cjkFallback': {'licenseSha256': dl.sha(license)}}
            with self.assertRaisesRegex(ValueError, 'receipt and license are required together'):
                windows.archive_payload(root / 'missing.zip', root, manifest)
            with self.assertRaisesRegex(ValueError, 'license differs'):
                windows.archive_payload(root / 'wrong.zip', root, manifest, font_license=b'wrong')
            archive = root / 'verified.zip'
            windows.archive_payload(archive, root, manifest, font_license=license)
            with zipfile.ZipFile(archive) as package:
                self.assertEqual(package.namelist(), ['manifest.json', cjk.LICENSE])
                self.assertEqual(package.read(cjk.LICENSE), license)

    def test_archive_readback_requires_verified_payload_and_is_reproducible(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            payload = root / 'payload'
            payload.mkdir()
            member = payload / 'level0'
            original = 'ЖЪЬ 527'.encode()
            member.write_bytes(original)
            manifest = {'files': {'level0': {'sourceSha256': 'original', 'outputSha256': dl.sha(original)}}}
            first, second = root / 'first.zip', root / 'second.zip'
            windows.archive_payload(first, payload, manifest)
            windows.archive_payload(second, payload, manifest)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            with zipfile.ZipFile(first) as package:
                self.assertEqual(package.namelist(), ['manifest.json', 'DragNWash_Data/level0'])
                self.assertEqual(json.loads(package.read('manifest.json')), manifest)
                self.assertEqual(package.read('DragNWash_Data/level0'), original)
            member.write_bytes(b'unverified')
            with self.assertRaisesRegex(ValueError, 'ZIP member differs from verified output'):
                windows.archive_payload(root / 'corrupt.zip', payload, manifest)
            self.assertEqual(first.read_bytes(), second.read_bytes())
