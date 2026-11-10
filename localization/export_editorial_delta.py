#!/usr/bin/env python3
"""Bind an editorial correction and its review scope to the paired v42 corpus."""
import argparse
from collections import defaultdict
import json
from pathlib import Path

import assemble_source_inventory as inventory
import dialogue_locale as dialogue
import index_special_scenes
import package_inputs
import paired_locale


def snapshot(path):
    raw = path.read_bytes()
    return json.loads(raw, object_pairs_hook=dialogue.unique_object), dialogue.sha(raw)


def sha_json(value):
    return dialogue.sha((json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode())


def source_ids_for_edit(key, edit, scenes):
    contexts = set()
    for span in edit['sceneSpans']:
        node, start, end = span['node'], span['firstInstruction'], span['lastInstruction']
        selected = [row for row in scenes[node] if start <= row['instructionIndex'] <= end]
        if (not selected or selected[0]['instructionIndex'] != start
                or selected[-1]['instructionIndex'] != end):
            raise ValueError(f'{key}: scene span does not bind exact source boundaries')
        contexts.update('yarn:' + row['id'] for row in selected)
    if key.startswith('yarn:') and key not in contexts:
        raise ValueError(f'{key}: correction is absent from its scene context')
    return contexts


def export(inventory_path, scope_path, scenes_path, before_path, after_path, recipe_path, locale):
    source = inventory.load_pinned(inventory_path, inventory.INVENTORY_SHA)['entries']
    scope = inventory.load_pinned(scope_path, package_inputs.YARN_SCOPE_SHA)
    scenes = inventory.load_pinned(scenes_path, inventory.FILES['yarn-paired-scenes.json'])['scenes']
    _, rows = paired_locale.catalog(source, scope)
    _, before_hash = snapshot(before_path)
    _, after_hash = snapshot(after_path)
    before = paired_locale.read(before_path, locale, package_inputs.YARN_SCOPE_SHA, rows)
    after = paired_locale.read(after_path, locale, package_inputs.YARN_SCOPE_SHA, rows)
    if dialogue.sha(before_path.read_bytes()) != before_hash or dialogue.sha(after_path.read_bytes()) != after_hash:
        raise ValueError('locale changed during delta export')
    recipe, recipe_hash = snapshot(recipe_path)
    if (recipe.keys() != {'schema', 'locale', 'beforeSha256', 'afterSha256', 'edits'}
            or recipe['schema'] != 1 or recipe['locale'] != locale
            or (recipe['beforeSha256'], recipe['afterSha256']) != (before_hash, after_hash)):
        raise ValueError('editorial delta recipe does not bind the two locale snapshots')
    changed = {key for key in rows if before[key] != after[key]}
    if not changed or changed != recipe['edits'].keys():
        raise ValueError('correction decisions must match the effective locale diff')

    source_targets = defaultdict(set)
    for key, row in rows.items():
        for binding in row['builds'].values():
            for source_id in binding['sourceIds']:
                source_targets[source_id].add(key)

    components = {name: set() for name in ('scene', 'repetitions', 'glossaryReferents', 'runtime', 'regression')}
    for key, edit in recipe['edits'].items():
        if edit.keys() != {'sceneSpans', 'glossaryReferentSourceIds', 'runtimeSourceIds', 'reason'} or not edit['reason']:
            raise ValueError(f'{key}: expected reviewed dependency decisions')
        components['scene'].update(source_ids_for_edit(key, edit, scenes))
        components['glossaryReferents'].update(edit['glossaryReferentSourceIds'])
        components['runtime'].update(edit['runtimeSourceIds'])

    cases = index_special_scenes.build(inventory_path)['cases']
    components['regression'].update(source_id for case in cases.values() for source_id in case['directIds'])
    source_map = {row['id']: row for row in source}
    components['regression'].update(row['id'] for row in source if row['role'] in (
        'preserve-exactly-credit-name', 'preserve-exactly-slot-progress-template',
    ))
    retained = set()
    resolved = {}
    for group, dependencies in components.items():
        unknown = dependencies - source_map.keys()
        if unknown:
            raise ValueError(f'{group}: unknown dependency source ID: {min(unknown)}')
        targets = {key for source_id in dependencies for key in source_targets.get(source_id, ())}
        retained.update(dependencies - source_targets.keys())
        resolved[group] = targets
    # Check exact source and target repetitions. Inflection or contextual
    # variants belong to the reviewed glossary/referent dependency list.
    for key in changed:
        originals = {b['source'] for b in rows[key]['builds'].values()}
        translations = set(before[key].values()) | set(after[key].values())
        for other, row in rows.items():
            if other in changed:
                continue
            other_sources = {binding['source'] for binding in row['builds'].values()}
            other_targets = set(before[other].values()) | set(after[other].values())
            if originals & other_sources or translations & other_targets:
                resolved['repetitions'].add(other)
    resolved['regression'].update(key for key in rows if not key.startswith('yarn:'))
    review = changed.union(*resolved.values())
    changed_ids = [key for key in rows if key in changed]
    closure_ids = [key for key in rows if key in review]
    protected = [row for row in source if row['id'] in retained]
    lists = {name: [key for key in rows if key in values] for name, values in resolved.items()}
    return {'schema': 1, 'locale': locale, 'beforeSha256': before_hash, 'afterSha256': after_hash,
            'sharedInventorySha256': inventory.INVENTORY_SHA, 'yarnScopeSha256': package_inputs.YARN_SCOPE_SHA,
            'sceneSourceSha256': inventory.FILES['yarn-paired-scenes.json'], 'recipeSha256': recipe_hash,
            'changedIds': changed_ids, 'closureIds': closure_ids, 'components': lists,
            'componentSourceIds': {name: [key for key in source_map if key in ids] for name, ids in components.items()},
            'componentSha256': {name: sha_json(ids) for name, ids in lists.items()},
            'changedIdsSha256': sha_json(changed_ids), 'closureIdsSha256': sha_json(closure_ids),
            'protectedContextSha256': sha_json(protected), 'protectedContext': protected,
            'reviewRows': [{**rows[key], 'before': before[key], 'after': after[key]} for key in closure_ids]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('inventory', 'yarn-scope', 'paired-scenes', 'before', 'after', 'recipe', 'output'):
        parser.add_argument(f'--{name}', type=Path, required=True)
    parser.add_argument('--locale', required=True)
    args = parser.parse_args()
    result = export(args.inventory, args.yarn_scope, args.paired_scenes, args.before,
                    args.after, args.recipe, args.locale)
    with args.output.open('x', encoding='utf-8') as output:
        json.dump(result, output, ensure_ascii=False, indent=2)
        output.write('\n')


if __name__ == '__main__':
    main()
