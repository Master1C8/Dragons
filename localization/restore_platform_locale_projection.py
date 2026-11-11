#!/usr/bin/env python3
"""Restore historical platform input rows from Git translations and stock text."""

import argparse
import hashlib
import json
from pathlib import Path

from restore_platform_locale_input import load_catalog, load_translation
from restore_probe_assets import read_receipt


def rebuild(row, builds, catalog, snapshots):
    platform, member = row['platform'], row['member']
    source_fingerprint = builds[platform]['sourceFingerprints'][member]
    bindings = {}
    for key, entry in catalog.items():
        binding = entry['builds'].get(platform)
        if binding and binding['file'] == member:
            bindings[binding['key']] = (key, binding['source'])

    translations = []
    for source in row['sources']:
        cache_key = (source['revision'], source['sha256'], row['locale'])
        if cache_key not in snapshots:
            snapshots[cache_key] = load_translation(*cache_key, catalog)
        translations.append(snapshots[cache_key])

    if row['ordering'] == 'explicit':
        keys = row['keys']
    else:
        selected = set(row.get('include', bindings)) - set(row.get('exclude', ()))
        keys = [key for key in bindings if key in selected]
        if row['ordering'] == 'translation':
            positions = {key: index for index, key in enumerate(translations[0])}
            keys.sort(key=lambda key: positions.get(bindings[key][0], len(catalog)))

    overrides = {
        key: int(index) for index, changed in row.get('overrides', {}).items() for key in changed
    }
    source_text = set(row.get('sourceText', ()))
    lines = {}
    for key in keys:
        authoring_id, source = bindings[key]
        if key in source_text:
            translation = source
        else:
            translation = translations[overrides.get(key, 0)][authoring_id][platform]
        lines[key] = {'source': source, 'text': translation}
    doc = {'schema': 1, 'locale': row['locale'], 'sourceObjectSha256': source_fingerprint, 'lines': lines}
    indent, ascii_only, suffix = row.get('style', (2, False, '\n'))
    output = (json.dumps(doc, ensure_ascii=ascii_only, indent=indent) + suffix).encode('utf-8')
    if len(output) != row['bytes'] or hashlib.sha256(output).hexdigest() != row['sha256']:
        raise ValueError('Restored platform projection fingerprint mismatch')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    for option in ('inventory', 'yarn-scope', 'output'):
        parser.add_argument('--' + option, type=Path, required=True)
    args = parser.parse_args()
    row = read_receipt(args.receipt)['outputs'][args.recorded_path]
    data = rebuild(row, *load_catalog(args.inventory, args.yarn_scope), {})
    with args.output.open('xb') as stream:
        stream.write(data)
    args.output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    main()
