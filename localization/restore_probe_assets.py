#!/usr/bin/env python3
"""Restore archived stock assets in a retained Dragons test copy."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def restore(receipt, stock_data, prefix):
    root = Path(__file__).resolve().parents[1]
    work = root / 'localization/work'
    prefix = (root / prefix).resolve(strict=True)
    if not prefix.is_relative_to(work):
        raise ValueError('Select a retained test directory within localization/work')
    inventory = json.loads(receipt.read_text())['files']
    count = 0
    for name, record in inventory.items():
        if Path(name).name != name or name in ('.', '..'):
            raise ValueError(f'Invalid stock filename: {name}')
        for copy in record['copies']:
            target = root / copy['path']
            if not target.is_relative_to(prefix):
                continue
            if target.resolve() != target or target.name != name:
                raise ValueError(f'Unexpected target path: {target}')
            if target.exists():
                if not target.is_file() or sha256(target) != record['sha256']:
                    raise FileExistsError(target)
                continue
            source = stock_data / name
            with tempfile.TemporaryDirectory(dir=target.parent) as staging:
                restored = Path(staging) / name
                shutil.copyfile(source, restored)
                if sha256(restored) != record['sha256']:
                    raise ValueError(f'Stock asset fingerprint mismatch: {name}')
                restored.chmod(int(copy['mode'], 8))
                os.link(restored, target)
            count += 1
    print(f'Restored {count} stock assets in {prefix}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('stock_data', type=Path)
    parser.add_argument('prefix', type=Path)
    args = parser.parse_args()
    restore(args.receipt, args.stock_data, args.prefix)
