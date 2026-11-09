#!/usr/bin/env python3
"""Validate the known serialized and managed non-Yarn localization inputs."""
import argparse
from collections import defaultdict
import json
from pathlib import Path

import compare_settings_sources as settings_sources
import compare_yarn_versions as versions
import dialogue_locale as dl
import managed_fallback
import map_ui_hierarchy
import settings_locale
import ui_locale
import ui_preservation
import verify_managed_assemblies as managed
import windows_ui_locale
from assemble_source_inventory import INVENTORY_SHA, load_pinned

MANAGED_INPUTS = {
    'slot-new-runtime-text-candidate': ('slot-new', managed_fallback.SLOT, True, 3),
    'player-facing-error-fallback-candidate': ('missing-line', managed_fallback.FALLBACK, False, 2),
}


def require_keys(label, expected, actual):
    missing = expected - actual
    if missing:
        raise ValueError(f'{label}: missing {len(missing)} IDs: {", ".join(sorted(missing)[:10])}')


def verify_platform(entries, platform, data, locale=None, inputs=None):
    adapter, hashes = (ui_locale, ui_locale.ASSETS) if platform == 'macos' else (
        windows_ui_locale, map_ui_hierarchy.WINDOWS_ASSETS)
    if (locale is None) != (inputs is None):
        raise ValueError('complete input validation needs a locale and input directory')
    receipts = {}

    def read(path, reader):
        digest = dl.sha(path.read_bytes())
        result = reader()
        if dl.sha(path.read_bytes()) != digest:
            raise ValueError(f'{path.name}: locale input changed during validation')
        receipts[path.relative_to(inputs).as_posix()] = digest
        return result

    ui_groups = defaultdict(dict)
    for row in entries:
        if row['family'] == 'ui' and row['location'][platform] is not None:
            ui_groups[row['asset']][row['location'][platform]] = (row['source'][platform], row['role'])
    if ui_groups.keys() != hashes.keys():
        raise ValueError(f'{platform}: serialized UI asset scope changed')
    if inputs is not None:
        required_files = {f'{asset}.json' for asset, rows in ui_groups.items()
                          if any(role.endswith('-candidate') for _, role in rows.values())}
        supplied_files = {path.name for path in (inputs / 'ui').iterdir()}
        if supplied_files != required_files:
            raise ValueError(f'{platform}: UI locale asset files differ from scope')
    ui_scope = {}
    for asset, rows in sorted(ui_groups.items()):
        _, scanned = adapter.scan(data, asset)
        source = {key: row[2] for key, row in scanned.items()}
        if source != {key: value for key, (value, _) in rows.items()}:
            raise ValueError(f'{platform}: serialized UI scope changed for {asset}')
        ui_preservation.validate(platform, asset, source, {})
        expected = {key for key, (_, role) in rows.items() if role.endswith('-candidate')}
        protected = {key for key, (_, role) in rows.items() if role.startswith('preserve-exactly-')}
        if expected | protected != source.keys() or expected & protected:
            raise ValueError(f'{platform}: unresolved serialized UI role in {asset}')
        ui_scope[asset] = {'translate': sorted(expected), 'preserve': sorted(protected)}
        if inputs is not None and expected:
            path = inputs / 'ui' / f'{asset}.json'
            code, actual = read(path, lambda: ui_preservation.read_locale(platform, asset, path, source, hashes[asset]))
            if code != locale:
                raise ValueError(f'{platform}: UI locale mismatch in {asset}')
            require_keys(f'{platform} {asset}', expected, actual.keys())

    if platform == 'macos':
        _, _, trees, _, _, _ = settings_locale.scan(data)
        types = settings_locale.EXPECTED
    else:
        trees, types = settings_sources.windows_scan(data)
    scanned = settings_sources.collect(trees, types, include_source=True)
    fields = {r['id']: (r['source'], r['provisionalRole']) for item in scanned.values()
              for r in item['fields'].values()}
    recorded = {r['location'][platform]: (r['source'][platform], r['role'][platform]) for r in entries
                if r['family'] == 'settings' and r['location'][platform] is not None}
    if fields != recorded:
        raise ValueError(f'{platform}: settings scope changed')
    settings = {key: text for key, (text, role) in fields.items() if role == 'candidate'}
    exact_settings = {key for key, (_, role) in fields.items() if role == 'preserve-exactly'}
    if settings.keys() | exact_settings != fields.keys():
        raise ValueError(f'{platform}: unresolved settings role')
    if inputs is not None:
        path = inputs / 'settings.json'
        code, actual = read(path, lambda: dl.read_locale(
            path, list(settings), list(settings.values()), hashes[settings_locale.ASSET], yarn_semantics=False))
        if code != locale:
            raise ValueError(f'{platform}: settings locale mismatch')
        require_keys(f'{platform} settings', settings.keys(), actual.keys())

    assemblies = managed.scan(data / 'Managed')
    manifest = managed.validate_source(platform, assemblies)
    candidates = defaultdict(list)
    for row in entries:
        if row['family'] == 'managed' and platform in row['source'] and not row['role'].startswith('preserve-exactly-'):
            candidates[row['role']].append(row)
    if candidates.keys() != MANAGED_INPUTS.keys():
        raise ValueError(f'{platform}: unresolved managed text role')
    managed_scope = {}
    for role, (filename, source, is_slot, count) in MANAGED_INPUTS.items():
        assembly = managed_fallback.SLOT_ASSEMBLY if is_slot else managed_fallback.ASSEMBLY
        key, value = next(iter(source.items()))
        rows = candidates[role]
        if len(rows) != count or any(row['source'][platform] != value or row['assemblySha256'] != assemblies[assembly]
                                    for row in rows):
            raise ValueError(f'{platform}: managed display binding differs for {key}')
        managed_scope[key] = [row['id'] for row in rows]
        if inputs is not None:
            path = inputs / f'{filename}.json'
            read(path, lambda: managed_fallback.read_replacement(path, locale, assemblies[assembly], slot_new=is_slot))

    return {'ui': ui_scope, 'settings': {'translate': sorted(settings), 'preserve': sorted(exact_settings)},
            'managed': managed_scope, 'sourceManagedManifestSha256': manifest, 'localeInputSha256': receipts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--locale')
    for platform in versions.BUILDS:
        parser.add_argument(f'--{platform}-data', type=Path, required=True)
        parser.add_argument(f'--{platform}-inputs', type=Path)
    args = parser.parse_args()
    folders = {p: getattr(args, f'{p}_inputs') for p in versions.BUILDS}
    if any((args.locale is None) != (folder is None) for folder in folders.values()):
        parser.error('complete validation needs --locale and both platform input directories')
    entries = load_pinned(args.inventory, INVENTORY_SHA)['entries']
    builds = {p: verify_platform(entries, p, getattr(args, f'{p}_data'), args.locale, folders[p])
              for p in versions.BUILDS}
    with args.output.open('x', encoding='utf-8') as file:
        json.dump({'schema': 1, 'scope': 'known-non-yarn-inputs', 'sharedInventorySha256': INVENTORY_SHA,
                   'locale': args.locale, 'builds': builds}, file, indent=2)
        file.write('\n')
    print(dl.sha(args.output.read_bytes()))


if __name__ == '__main__':
    main()
