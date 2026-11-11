#!/usr/bin/env python3
"""Rebuild a historical source inventory from retained exports and Git."""

import argparse
import io
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

from restore_probe_assets import read_receipt, relative_path, sha256


def git_archive(checkout, revision, paths, destination):
    archive = subprocess.check_output(
        ['git', '-C', str(checkout), 'archive', revision, *paths]
    )
    with tarfile.open(fileobj=io.BytesIO(archive)) as tar:
        for member in tar:
            if member.isfile():
                path = destination / relative_path(member.name)
                path.parent.mkdir(parents=True, exist_ok=True)
                with tar.extractfile(member) as source:
                    path.write_bytes(source.read())


def restore(receipt, filename, exports, output):
    checkout = Path(__file__).resolve().parents[1]
    records = read_receipt(receipt)
    row = next((item for item in records['outputs'] if item['name'] == filename), None)
    if row is None:
        raise ValueError(f'Unknown inventory: {filename}')
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    for name, digest in row['inputs'].items():
        source = exports / relative_path(name)
        if sha256(source) != digest:
            raise ValueError(f'Source export fingerprint mismatch: {source}')

    with tempfile.TemporaryDirectory(dir=output.parent) as staging:
        scratch = Path(staging)
        paths = [p for p in row['toolFiles'] if not p.startswith('localization/evidence/')]
        git_archive(checkout, row['sourceRevision'], [*paths, 'localization/evidence'], scratch)
        git_archive(checkout, records['supportRevision'], ['localization/managed_fallback.py'], scratch)
        tools = scratch / 'localization'
        rebuilt = scratch / 'rebuilt.json'
        subprocess.run(
            [
                sys.executable, '-B', str(tools / 'assemble_source_inventory.py'),
                '--work', str(exports.resolve(strict=True)),
                '--ui-roles', str(tools / 'evidence/ui-source-roles-20261107.json'),
                '--output', str(rebuilt),
            ],
            check=True,
        )
        if sha256(rebuilt) != row['sha256']:
            raise ValueError('Rebuilt inventory fingerprint mismatch')
        os.link(rebuilt, output)
    print(f'Restored source inventory: {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('filename')
    parser.add_argument('--exports', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    restore(args.receipt, args.filename, args.exports, args.output)
