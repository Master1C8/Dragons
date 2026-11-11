#!/usr/bin/env python3
"""Restore a retired Yarn table or its paired structure control."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess

import compare_yarn_versions as versions
import paired_locale
from restore_platform_locale_input import CHECKOUT, load_catalog
from restore_probe_assets import read_receipt


def stock_table(platform, stock_data):
    keys, values, *_ = versions.load(stock_data, versions.BUILDS[platform])
    return dict(zip(keys, values, strict=True))


def project(snapshot, kind, platform, catalog, stock):
    if kind == 'structure-control':
        lines = {}
        for key, row in catalog.items():
            bindings = row['builds']
            sources = {name: binding['source'] for name, binding in bindings.items()}
            lines[key] = (
                {'platforms': sources} if paired_locale.sources_differ(bindings) else next(iter(sources.values()))
            )
        lines.update(snapshot['lines'])
        return {**snapshot, 'lines': lines}

    if kind != 'table':
        raise ValueError(f'Unknown projection: {kind}')
    lines = stock.copy()
    for key, value in snapshot['lines'].items():
        bindings = catalog[key]['builds']
        binding = bindings.get(platform)
        if not binding or binding['file'] != 'dialogue.json':
            continue
        target = binding['key']
        if lines[target] != binding['source']:
            raise ValueError(f'Stock source differs from catalog: {target}')
        text = paired_locale.resolve(key, bindings, value, allow_blank=True).get(platform)
        if text is not None:
            lines[target] = text
    return lines


def read_snapshot(row):
    revision, locale = row['revision'], row['locale']
    if not re.fullmatch(r'[0-9a-f]{40}', revision) or not re.fullmatch(r'[a-z]{2}(?:-[A-Za-z0-9]+)?', locale):
        raise ValueError('Expected a full translation revision and a locale code')
    raw = subprocess.check_output(
        ['git', '-C', str(CHECKOUT), 'show', f'{revision}:localization/{locale}/translation.json'],
    )
    if hashlib.sha256(raw).hexdigest() != row['translationSha256']:
        raise ValueError('Translation snapshot fingerprint mismatch')
    return json.loads(raw)


def rebuild(row, catalog, stock):
    output = project(read_snapshot(row), row['kind'], row.get('platform'), catalog, stock)
    data = (json.dumps(output, ensure_ascii=False, indent=row['indent']) + '\n').encode('utf-8')
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('Restored Yarn projection fingerprint mismatch')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    for option in ('inventory', 'yarn-scope', 'output'):
        parser.add_argument('--' + option, type=Path, required=True)
    parser.add_argument('--stock-data', type=Path)
    args = parser.parse_args()
    row = read_receipt(args.receipt)['outputs'][args.recorded_path]
    stock = None
    if row['kind'] == 'table':
        if args.stock_data is None:
            parser.error('Pass --stock-data for a Yarn table')
        stock = stock_table(row['platform'], args.stock_data)
    _, catalog = load_catalog(args.inventory, args.yarn_scope)
    data = rebuild(row, catalog, stock)
    with args.output.open('xb') as stream:
        stream.write(data)
    args.output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    main()
