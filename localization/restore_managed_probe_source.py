#!/usr/bin/env python3
"""Restore an earlier managed probe source or project descriptor."""

import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile
import zipfile

from restore_probe_assets import read_receipt, sha256
from restore_renderer_assembly import rebuild


CHECKOUT = Path(__file__).resolve().parents[1]


def git_base(blob, destination):
    if not re.fullmatch(r'[0-9a-f]{40}', blob):
        raise ValueError('Expected a full Git base blob ID')
    with destination.open('xb') as stream:
        subprocess.run(['git', '-C', str(CHECKOUT), 'cat-file', 'blob', blob], stdout=stream, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    parser.add_argument('--archive', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    if sha256(args.archive) != receipt['archiveSha256']:
        raise ValueError('Managed source archive fingerprint mismatch')
    row = receipt['outputs'][args.recorded_path]
    with tempfile.TemporaryDirectory(dir=args.output.parent) as directory, zipfile.ZipFile(args.archive) as archive:
        scratch = Path(directory)
        blob = row['basePath']
        git_base(blob, scratch / blob)
        rebuilt = scratch / 'restored'
        rebuild(row, {'git': scratch}, {}, archive, rebuilt)
        rebuilt.chmod(int(row['mode'], 8))
        os.link(rebuilt, args.output)


if __name__ == '__main__':
    main()
