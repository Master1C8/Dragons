#!/usr/bin/env python3
"""Recreate an earlier worklist report from a verified baseline."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

from restore_probe_assets import read_receipt, sha256


CHECKOUT = Path(__file__).resolve().parents[1]


def rebuild(baseline, row, recipe):
    if sha256(baseline) != row['baselineSha256']:
        raise ValueError('Worklist baseline fingerprint mismatch')
    report = read_receipt(baseline)
    locale = report['locale']
    revision = recipe['revision']
    if not re.fullmatch(r'[0-9a-f]{40}', revision) or not re.fullmatch(r'[a-z]{2}(?:-[A-Za-z0-9]+)?', locale):
        raise ValueError('Expected a full translation revision and a locale code')
    source = subprocess.check_output([
        'git', '-C', str(CHECKOUT), 'show', f'{revision}:localization/{locale}/translation.json',
    ])
    if hashlib.sha256(source).hexdigest() != recipe['translationSha256']:
        raise ValueError('Historical translation fingerprint mismatch')
    lines = json.loads(source)['lines']
    selected = set(recipe['ids'])
    overrides = recipe.get('overrides', {})
    for entry in report['rows']:
        key = entry['id']
        if key not in selected:
            continue
        value = overrides[key] if key in overrides else lines[key]
        for platform, binding in entry['builds'].items():
            if isinstance(value, str):
                draft = value
            elif 'text' in value:
                draft = value['text']
            else:
                draft = value['platforms'][platform]
            binding['draft'] = draft
    for build in report['builds'].values():
        build.update(draftSha256=recipe['recordedDraftSha256'], draftCount=len(selected))
    data = (json.dumps(report, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('Restored worklist report fingerprint mismatch')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    for option in ('baseline', 'metadata', 'output'):
        parser.add_argument('--' + option, type=Path, required=True)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    if sha256(args.metadata) != receipt['metadataSha256']:
        raise ValueError('Worklist recovery metadata fingerprint mismatch')
    recipe = read_receipt(args.metadata)[args.recorded_path]
    row = receipt['outputs'][args.recorded_path]
    raw = rebuild(args.baseline, row, recipe)
    with args.output.open('xb') as out:
        out.write(raw)
    args.output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    main()
