#!/usr/bin/env python3
"""Restore a historical editorial recipe from its committed successor."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from restore_probe_assets import read_receipt, relative_path, sha256


CHECKOUT = Path(__file__).resolve().parents[1]


def rebuild(row, delta):
    revision = row['recipeBaseRevision']
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Expected a full recipe base revision')
    path = relative_path(row['recipeBasePath'])
    raw = subprocess.check_output(
        ['git', '-C', str(CHECKOUT), 'show', f'{revision}:{path.as_posix()}'],
    )
    if hashlib.sha256(raw).hexdigest() != row['recipeBaseSha256']:
        raise ValueError('Editorial recipe base fingerprint mismatch')
    recipe = json.loads(raw)
    recipe['afterSha256'] = row['afterSha256']
    for key in delta.get('omitEdits', ()):
        del recipe['edits'][key]
    for key, changes in delta.get('updateEdits', {}).items():
        recipe['edits'][key].update(changes)
    data = (json.dumps(recipe, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if hashlib.sha256(data).hexdigest() != row['recipeSha256']:
        raise ValueError('Restored editorial recipe fingerprint mismatch')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    parser.add_argument('--metadata', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    if sha256(args.metadata) != receipt['metadataSha256']:
        raise ValueError('Editorial recipe metadata fingerprint mismatch')
    data = rebuild(receipt['outputs'][args.recorded_path], read_receipt(args.metadata)[args.recorded_path])
    with args.output.open('xb') as out:
        out.write(data)


if __name__ == '__main__':
    main()
