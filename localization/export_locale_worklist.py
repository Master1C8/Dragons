#!/usr/bin/env python3
"""Export a paired authoring worklist from the pinned package input scopes."""

import argparse
import json
from pathlib import Path

from assemble_source_inventory import INVENTORY_SHA, load_pinned
import compare_yarn_versions as versions
import dialogue_locale as dl
import index_special_scenes
import inventory_non_yarn_scope as non_yarn
import managed_fallback
import map_ui_hierarchy
import package_inputs
import settings_locale
import speaker_locale
import ui_locale


def build(inventory_path, scope_path, data_paths, draft_root, locale):
    entries = load_pinned(inventory_path, INVENTORY_SHA)['entries']
    scope = load_pinned(scope_path, package_inputs.YARN_SCOPE_SHA)
    cases = index_special_scenes.build(inventory_path)
    if scope['sharedInventorySha256'] != INVENTORY_SHA:
        raise ValueError('Yarn scope does not match the shared inventory')
    yarn = {row['id']: row for row in scope['rows']}
    rows, builds = {}, {}

    for platform, data in data_paths.items():
        spec = versions.BUILDS[platform]
        keys, values, *_ = versions.load(data, spec)
        source = dict(zip(keys, values))
        other = non_yarn.verify_platform(entries, platform, data)
        hashes = ui_locale.ASSETS if platform == 'macos' else map_ui_hierarchy.WINDOWS_ASSETS
        managed = managed_fallback.SOURCES[platform]
        files = {
            'dialogue.json': spec['localizationSha256'],
            'speakers.json': managed,
            'settings.json': hashes[settings_locale.ASSET],
            'slot-new.json': managed_fallback.SLOT_SOURCES[platform],
            'missing-line.json': managed,
        }
        files.update({f'ui/{asset}.json': hashes[asset] for asset, roles in other['ui'].items()
                      if roles['translate']})
        draft_path = draft_root / platform / 'dialogue.json'
        draft_hash = dl.sha(draft_path.read_bytes())
        code, draft = dl.read_locale(draft_path, keys, values, spec['localizationSha256'])
        if (code != locale or any(yarn[key]['localeInput'] != 'dialogue-locale' for key in draft)
                or dl.sha(draft_path.read_bytes()) != draft_hash):
            raise ValueError(f'{platform}: draft locale, scope or snapshot differs')

        destinations = set()

        def add(row_id, group, filename, key, text, source_ids, **context):
            destination = (filename, key)
            if filename not in files or destination in destinations:
                raise ValueError(f'{platform}: invalid or repeated input destination {destination}')
            destinations.add(destination)
            row = rows.setdefault(row_id, {'id': row_id, 'group': group, **context, 'builds': {}})
            row['builds'][platform] = {
                'file': filename, 'key': key, 'source': text, 'sourceIds': source_ids,
            }
            if filename == 'dialogue.json' and key in draft:
                row['builds'][platform]['draft'] = draft[key]

        for row in entries:
            row_id = row['id']
            family = row['family']
            if family == 'yarn':
                key = row_id.removeprefix('yarn:')
                if row['source'][platform] != source[key]:
                    raise ValueError(f'{platform}: source text differs for {key}')
                kind = yarn[key]['localeInput']
                if kind in ('dialogue-locale', 'speaker-locale'):
                    filename = 'dialogue.json' if kind == 'dialogue-locale' else 'speakers.json'
                    add(row_id, row['node'], filename, key, source[key], [row_id],
                        kind=row['kind'], instructionIndex=row['instructionIndex'],
                        preserveExactPrefix=row['preserveExactPrefix'])
            elif family == 'ui':
                key = row['location'][platform]
                asset = row['asset']
                if key in other['ui'][asset]['translate']:
                    add(row_id, f'UI/{asset}', f'ui/{asset}.json', key, row['source'][platform], [row_id])
            elif family == 'settings':
                key = row['location'][platform]
                if key in other['settings']['translate']:
                    add(row_id, 'Settings', 'settings.json', key, row['source'][platform], [row_id])

        for filename, sources, _, _ in non_yarn.MANAGED_INPUTS.values():
            key, value = next(iter(sources.items()))
            add(f'display:{key}', 'Managed display', f'{filename}.json', key, value, other['managed'][key])
        for key, value in speaker_locale.SOURCE_NAMES.items():
            source_ids = [r['id'] for r in entries if r['family'] == 'yarn' and
                          (r['preserveExactPrefix'] or {}).get(platform) == value + ': ']
            add(f'display:{key}', 'Speaker labels', 'speakers.json', key, value, source_ids)
        builds[platform] = {'inputCount': len(destinations), 'sourceFingerprints': files,
                            'draftSha256': draft_hash, 'draftCount': len(draft)}

    return {'schema': 1, 'status': 'authoring-inputs-only', 'locale': locale,
            'sharedInventorySha256': INVENTORY_SHA, 'yarnScopeSha256': package_inputs.YARN_SCOPE_SHA,
            'builds': builds, 'specialScenes': cases, 'rows': list(rows.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--yarn-scope', type=Path, required=True)
    parser.add_argument('--draft-root', type=Path, required=True)
    parser.add_argument('--locale', required=True)
    parser.add_argument('--output', type=Path, required=True)
    for platform in versions.BUILDS:
        parser.add_argument(f'--{platform}-data', type=Path, required=True)
    args = parser.parse_args()
    data = {p: getattr(args, f'{p}_data') for p in versions.BUILDS}
    result = build(args.inventory, args.yarn_scope, data, args.draft_root, args.locale)
    with args.output.open('x', encoding='utf-8') as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        out.write('\n')
    print(f'{len(result["rows"])} authoring IDs, SHA-256 {dl.sha(args.output.read_bytes())}')


if __name__ == '__main__':
    main()
