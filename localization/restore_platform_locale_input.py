#!/usr/bin/env python3
"""Restore a platform package input from the corresponding Git translation."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile

import package_inputs
import paired_locale
from restore_probe_assets import read_receipt, relative_path


CHECKOUT = Path(__file__).resolve().parents[1]


def load_catalog(inventory, scope):
    entries = package_inputs.load_pinned(inventory, package_inputs.INVENTORY_SHA)['entries']
    scope_data = package_inputs.load_pinned(scope, package_inputs.YARN_SCOPE_SHA)
    return paired_locale.catalog(entries, scope_data)


def rebuild(row, builds, catalog):
    revision = row['translationRevision']
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Expected a full translation revision')
    locale, platform = row['locale'], row['platform']
    member = relative_path(row['member']).as_posix()
    blob = f'{revision}:localization/{locale}/translation.json'
    raw = subprocess.check_output(['git', '-C', str(CHECKOUT), 'show', blob])
    if hashlib.sha256(raw).hexdigest() != row['translationSha256']:
        raise ValueError('Translation snapshot fingerprint mismatch')
    with tempfile.TemporaryDirectory() as temporary:
        scratch = Path(temporary)
        snapshot = scratch / 'translation.json'
        snapshot.write_bytes(raw)
        translations = paired_locale.read(snapshot, locale, package_inputs.YARN_SCOPE_SHA, catalog, complete=False)
        orders = {'catalog': catalog, 'translation': translations}
        rows = {}
        for key in orders[row['ordering']]:
            if platform in translations.get(key, {}) and catalog[key]['builds'][platform]['file'] == member:
                rows[key] = catalog[key]
        source = builds[platform]['sourceFingerprints'][member]
        destination = scratch / 'materialized'
        paired_locale.materialize(destination, platform, locale, {'sourceFingerprints': {member: source}},
                                  rows, translations)
        data = (destination / member).read_bytes()
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('Restored platform input fingerprint mismatch')
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    for option in ('inventory', 'yarn-scope', 'output'):
        parser.add_argument('--' + option, type=Path, required=True)
    args = parser.parse_args()
    rows = read_receipt(args.receipt)['outputs']
    selected = next(((row, file) for row in rows for file in row['files']
                     if file['path'] == args.recorded_path), None)
    if selected is None:
        parser.error(f'Unknown platform input: {args.recorded_path}')
    row, file = selected
    data = rebuild(row, *load_catalog(args.inventory, args.yarn_scope))
    with args.output.open('xb') as out:
        out.write(data)
    os.chmod(args.output, int(file['mode'], 8))
