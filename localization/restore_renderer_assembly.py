#!/usr/bin/env python3
"""Restore a historical renderer assembly from its verified delta chain."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

from restore_probe_assets import read_receipt, relative_path, sha256


def rebuild(row, stock, recovered, archive, destination):
    if row['base'] == 'earlier-output':
        base = recovered[row['baseSha256']]
    else:
        base = stock[row['base']] / relative_path(row['basePath'])
    if sha256(base) != row['baseSha256']:
        raise ValueError('Renderer assembly base fingerprint mismatch')

    with tempfile.TemporaryDirectory(dir=destination.parent) as scratch:
        patch = Path(scratch) / 'assembly.zst'
        with archive.open(row['archiveMember']) as source, patch.open('xb') as output:
            shutil.copyfileobj(source, output)
        if sha256(patch) != row['patchSha256']:
            raise ValueError('Renderer assembly delta fingerprint mismatch')
        rebuilt = Path(scratch) / 'assembly.dll'
        subprocess.run(['zstd', '-q', '-d', '--patch-from=' + str(base),
                        str(patch), '-o', str(rebuilt)], check=True)
        if rebuilt.stat().st_size != row['bytes'] or sha256(rebuilt) != row['sha256']:
            raise ValueError('Restored renderer assembly fingerprint mismatch')
        os.link(rebuilt, destination)
    recovered[row['sha256']] = destination


def restore(receipt, recorded_path, archive_path, stock, output):
    rows = receipt['outputs']
    selected = next(((row, file) for row in rows for file in row['files']
                     if file['path'] == recorded_path), None)
    if selected is None:
        raise ValueError(f'Unknown renderer assembly: {recorded_path}')
    if sha256(archive_path) != receipt['archiveSha256']:
        raise ValueError('Renderer assembly archive fingerprint mismatch')
    target, file = selected
    with tempfile.TemporaryDirectory(dir=output.parent) as staging, zipfile.ZipFile(archive_path) as archive:
        recovered = {}
        for row in rows:
            if row['family'] != target['family']:
                continue
            destination = Path(staging) / (row['sha256'] + '.dll')
            rebuild(row, stock, recovered, archive, destination)
            if row is target:
                destination.chmod(int(file['mode'], 8))
                os.link(destination, output)
                break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    for option in ('archive', 'macos-stock', 'windows-stock', 'output'):
        parser.add_argument('--' + option, type=Path, required=True)
    args = parser.parse_args()
    restore(read_receipt(args.receipt), args.recorded_path, args.archive,
            {'macos': args.macos_stock, 'windows': args.windows_stock}, args.output)
