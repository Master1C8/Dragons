#!/usr/bin/env python3
"""Recreate the historical gallery capture from the published image bytes."""

import argparse
import base64
import hashlib
import json
from pathlib import Path
import zipfile

from restore_probe_assets import read_receipt, sha256


def restore(receipt, metadata_archive, export, output):
    row = receipt['capture']
    if sha256(metadata_archive) != receipt['metadataArchiveSha256']:
        raise ValueError('Gallery metadata archive fingerprint mismatch')
    with zipfile.ZipFile(metadata_archive) as archive:
        metadata = {}
        for item in receipt['metadata']:
            member = item['archiveMember']
            data = archive.read(member)
            if hashlib.sha256(data).hexdigest() != item['sha256']:
                raise ValueError(f'Gallery metadata fingerprint mismatch: {member}')
            metadata[member] = json.loads(data)

    inventory = metadata['gallery/inventory.json']
    files = []
    for item in metadata['gallery/downloads.json']:
        filename = item['filename']
        if filename != item['sha256'] + '.webp':
            raise ValueError('Unexpected gallery filename')
        data = (export / filename).read_bytes()
        if len(data) != item['sizeBytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise ValueError(f'Published gallery fingerprint mismatch: {filename}')
        files.append({
            'url': item['url'],
            'sha256': item['sha256'],
            'sizeBytes': item['sizeBytes'],
            'dataBase64': base64.b64encode(data).decode('ascii'),
        })
    fields = list(inventory.items())
    fields.insert(row['privateFilesIndex'], ('privateFiles', files))
    body = json.dumps(dict(fields), ensure_ascii=False, separators=(',', ':')).encode()
    capture = base64.b64decode(row['logHeaderBase64'], validate=True)
    capture += b'\nVNREVIVAL_SCREENSHOT_INVENTORY=' + body + b'\n'
    if hashlib.sha256(capture).hexdigest() != row['sha256']:
        raise ValueError('Restored gallery capture fingerprint mismatch')
    with output.open('xb') as file:
        file.write(capture)
    output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('receipt', 'metadata_archive', 'export', 'output'):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    restore(read_receipt(args.receipt), args.metadata_archive, args.export, args.output)
