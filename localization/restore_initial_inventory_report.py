#!/usr/bin/env python3
"""Recover the exact serialization of an early Dragons inventory report."""

import argparse
import hashlib
import json
from pathlib import Path
import re

from restore_probe_assets import read_receipt, sha256


def project(text, row):
    layout = row['layout']
    removed = row.get('removeFields', [])
    replacement = row.get('replaceLimitations')
    if layout == 'original':
        return text
    if layout == 'dotnet':
        parts = re.split(r'(?=^  "[^"]+": )', text, flags=re.MULTILINE)
        prefixes = tuple(f'  "{field}": ' for field in removed)
        result = ''.join(part for part in parts if not part.startswith(prefixes))
        if replacement:
            before, after = (json.dumps(value) for value in replacement)
            if result.count(before) != 1:
                raise ValueError('Expected one historical limitations field')
            result = result.replace(before, after, 1)
        return result

    document = json.loads(text)
    for field in removed:
        del document[field]
    if replacement:
        before, after = replacement
        if document['limitations'] != before:
            raise ValueError('Unexpected limitations field')
        document['limitations'] = after
    if layout == 'compact':
        return json.dumps(document, ensure_ascii=False, separators=(',', ':')) + '\n'
    if layout == 'indented':
        return json.dumps(document, ensure_ascii=False, indent=2) + '\n'
    raise ValueError(f'Unknown historical JSON layout: {layout}')


def restore(row, base, output):
    if sha256(base) != row['baseSha256']:
        raise ValueError('Base inventory report fingerprint mismatch')
    data = project(base.read_bytes().decode('utf-8'), row).encode('utf-8')
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('Restored inventory report fingerprint mismatch')
    with output.open('xb') as stream:
        stream.write(data)
    output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    parser.add_argument('--base', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    selected = next(row for row in read_receipt(args.receipt)['outputs']
                    if row['path'] == args.recorded_path)
    restore(selected, args.base, args.output)
