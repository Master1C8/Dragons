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
import package_inputs
import paired_locale


def build(inventory_path, scope_path, data_paths, draft_root, locale, *, locale_file=None):
    entries = load_pinned(inventory_path, INVENTORY_SHA)['entries']
    scope = load_pinned(scope_path, package_inputs.YARN_SCOPE_SHA)
    cases = index_special_scenes.build(inventory_path)
    builds, rows = paired_locale.catalog(entries, scope)
    translations, shared_hash = {}, None
    if locale_file is not None:
        shared_hash = dl.sha(locale_file.read_bytes())
        translations = paired_locale.read(locale_file, locale, package_inputs.YARN_SCOPE_SHA, rows, complete=False)
        if dl.sha(locale_file.read_bytes()) != shared_hash:
            raise ValueError('shared draft changed during export')

    for platform, data in data_paths.items():
        spec = versions.BUILDS[platform]
        keys, values, *_ = versions.load(data, spec)
        source = dict(zip(keys, values))
        non_yarn.verify_platform(entries, platform, data)
        for row in entries:
            if row['family'] == 'yarn':
                key = row['id'].removeprefix('yarn:')
                if row['source'][platform] != source[key]:
                    raise ValueError(f'{platform}: source text differs for {key}')

        bindings = {key: row['builds'][platform] for key, row in rows.items()
                    if platform in row['builds']}
        draft, draft_hash = {}, shared_hash
        if draft_root is not None:
            draft_path = draft_root / platform / 'dialogue.json'
            draft_hash = dl.sha(draft_path.read_bytes())
            code, draft = dl.read_locale(draft_path, keys, values, spec['localizationSha256'])
            dialogue_keys = {row['key'] for row in bindings.values() if row['file'] == 'dialogue.json'}
            if code != locale or draft.keys() - dialogue_keys or dl.sha(draft_path.read_bytes()) != draft_hash:
                raise ValueError(f'{platform}: draft locale, scope or snapshot differs')
        count = 0
        for key, binding in bindings.items():
            if key in translations:
                binding['draft'] = translations[key][platform]
            elif binding['file'] == 'dialogue.json' and binding['key'] in draft:
                binding['draft'] = draft[binding['key']]
            count += 'draft' in binding
        builds[platform].update(draftSha256=draft_hash, draftCount=count)

    return {'schema': 1, 'status': 'authoring-inputs-only', 'locale': locale,
            'sharedInventorySha256': INVENTORY_SHA, 'yarnScopeSha256': package_inputs.YARN_SCOPE_SHA,
            'builds': builds, 'specialScenes': cases, 'rows': list(rows.values())}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--yarn-scope', type=Path, required=True)
    drafts = parser.add_mutually_exclusive_group()
    drafts.add_argument('--draft-root', type=Path)
    drafts.add_argument('--locale-file', type=Path)
    parser.add_argument('--locale', required=True)
    parser.add_argument('--output', type=Path, required=True)
    for platform in versions.BUILDS:
        parser.add_argument(f'--{platform}-data', type=Path, required=True)
    args = parser.parse_args()
    data = {p: getattr(args, f'{p}_data') for p in versions.BUILDS}
    result = build(args.inventory, args.yarn_scope, data, args.draft_root, args.locale,
                   locale_file=args.locale_file)
    with args.output.open('x', encoding='utf-8') as out:
        json.dump(result, out, ensure_ascii=False, indent=2)
        out.write('\n')
    print(f'{len(result["rows"])} authoring IDs, SHA-256 {dl.sha(args.output.read_bytes())}')


if __name__ == '__main__':
    main()
