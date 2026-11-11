#!/usr/bin/env python3
"""Restore historical test files from verified stock or retained ZIP members."""

import argparse
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

from restore_probe_assets import read_receipt, relative_path, sha256


def stage(row, roots, destination):
    source_root = roots[row['root']]
    if source_root is None:
        raise ValueError(f"Supply the {row['root']} recovery directory")
    source = source_root / relative_path(row['source'])
    if source.resolve() != source or not source.is_file():
        raise ValueError(f'Unexpected recovery source: {source}')
    if 'member' in row:
        with zipfile.ZipFile(source) as archive, archive.open(row['member']) as member:
            with destination.open('xb') as stream:
                shutil.copyfileobj(member, stream)
    else:
        shutil.copyfile(source, destination)
    if destination.stat().st_size != row['bytes'] or sha256(destination) != row['sha256']:
        raise ValueError(f'Recovery source fingerprint mismatch: {source}')


def restore(receipt, prefix, macos_stock, windows_stock, accepted):
    checkout = Path(__file__).resolve().parents[1]
    work = checkout / 'localization/work'
    prefix = (checkout / prefix).resolve(strict=True)
    if not prefix.is_relative_to(work):
        raise ValueError('Select a test directory inside localization/work')
    roots = {
        'checkout': checkout,
        'macosStock': macos_stock,
        'windowsStock': windows_stock,
        'releasedInstaller': accepted,
    }
    roots = {name: path.resolve(strict=True) if path else None for name, path in roots.items()}
    count = 0
    for row in read_receipt(receipt)['outputs']:
        target = checkout / relative_path(row['path'])
        if not target.is_relative_to(prefix):
            continue
        if target.resolve() != target:
            raise ValueError(f'Unexpected recovery path: {target}')
        if target.exists():
            if not target.is_file() or sha256(target) != row['sha256']:
                raise FileExistsError(target)
            continue
        with tempfile.TemporaryDirectory(dir=target.parent) as staging:
            recovered = Path(staging) / 'recovered'
            stage(row, roots, recovered)
            recovered.chmod(int(row['mode'], 8))
            os.link(recovered, target)
        count += 1
    print(f'Restored {count} archived files in {prefix}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('prefix', type=Path)
    parser.add_argument('--macos-stock', type=Path)
    parser.add_argument('--windows-stock', type=Path)
    parser.add_argument('--accepted', type=Path)
    args = parser.parse_args()
    restore(args.receipt, args.prefix, args.macos_stock, args.windows_stock, args.accepted)
