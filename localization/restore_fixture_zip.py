#!/usr/bin/env python3
"""Restore a recorded historical test ZIP from verified retained members."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import tempfile
import zipfile

from restore_probe_assets import relative_path, sha256


def member_bytes(member, roots):
    source = member['source']
    source_root = roots[source['root']]
    if source_root is None:
        raise ValueError('This fixture requires the extracted components archive')
    path = source_root / relative_path(source['path'])
    if path.resolve() != path or not path.is_file():
        raise ValueError(f'Expected a regular retained source: {path}')
    if 'member' in source:
        with zipfile.ZipFile(path) as archive:
            data = archive.read(source['member'])
    else:
        data = path.read_bytes()
    if len(data) != member['size'] or hashlib.sha256(data).hexdigest() != member['sha256']:
        raise ValueError(f'Fixture source fingerprint mismatch: {path}')
    return data


def restore(receipt, recorded_path, stock, components, output):
    root = Path(__file__).resolve().parents[1]
    roots = {
        'checkout': root,
        'windowsStock': stock.resolve(strict=True),
        'components': components.resolve(strict=True) if components else None,
    }
    records = json.loads(receipt.read_text())['outputs']
    record = next((row for row in records if row['path'] == recorded_path), None)
    if record is None:
        raise ValueError(f'Unknown fixture path: {recorded_path}')
    target = output or root / relative_path(recorded_path)
    if target.resolve() != target or not target.is_relative_to(root / 'localization/work'):
        raise ValueError('Select a destination inside localization/work')
    if target.exists():
        if not target.is_file() or sha256(target) != record['sha256']:
            raise FileExistsError(target)
        print(f'Fixture already matches: {target}')
        return
    with tempfile.TemporaryDirectory(dir=target.parent) as staging:
        restored = Path(staging) / 'restored.zip'
        with zipfile.ZipFile(restored, 'w') as archive:
            archive.comment = bytes.fromhex(record['comment'])
            for member in record['members']:
                relative_path(member['name'])
                info = zipfile.ZipInfo(member['name'], tuple(member['date']))
                info.compress_type = zipfile.ZIP_STORED
                info.create_system = member['createSystem']
                info.create_version = member['createVersion']
                info.extract_version = member['extractVersion']
                info.external_attr = member['modeAttributes']
                info.internal_attr = member['internalAttributes']
                info.extra = bytes.fromhex(member['extra'])
                info.comment = bytes.fromhex(member['comment'])
                archive.writestr(info, member_bytes(member, roots))
        if sha256(restored) != record['sha256']:
            raise ValueError('Restored fixture ZIP fingerprint mismatch')
        restored.chmod(int(record['mode'], 8))
        os.link(restored, target)
    print(f'Restored fixture: {target}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    parser.add_argument('--windows-stock', type=Path, required=True)
    parser.add_argument('--components', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    restore(args.receipt, args.recorded_path, args.windows_stock, args.components, args.output)
