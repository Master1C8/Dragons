#!/usr/bin/env python3
"""Bind registered special-scene dependencies to the paired source inventory."""
import argparse
from collections import defaultdict
import json
from pathlib import Path

import dialogue_locale as dl
import yarn_transition_repair as repair
from assemble_source_inventory import INVENTORY_SHA, load_pinned

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE = ROOT / 'localization/evidence'
SOURCE_LINKS = ('sourceInventory', 'sourceGroupInventory', 'sourceAudit',
                'sourceContextMap', 'sourceContextInventory')


def line_id(key):
    return 'yarn:' + key


def case_inputs(case, nodes):
    direct = set(case.get('sourceLineIds', ())) | set(case.get('pivotalChoiceIds', ()))
    direct.update(case.get('lexicalCandidateIds', ()))
    context = set(case.get('contextualLineIds', ()))
    for group in case.get('groups', ()):
        group_ids = set(group['sourceLineIds'])
        node_ids = {row['id'] for row in nodes[group['node']]}
        if not group_ids <= node_ids:
            raise ValueError(f'{case["id"]}: source group does not match its node')
        direct.update(group_ids)
        context.update(node_ids)
    for build in case.get('sourceScopeByBuild', {}).values():
        context.update(build['sourceLineIds'])
    direct.update(row['lineId'] for row in case.get('mappings', ()))
    for transfer in case.get('exactTransfersAndMarkers', ()):
        marker = transfer['matchingEmbeddedTitle']
        direct.add(marker['lineId'])
        direct.update(row['lineId'] for row in marker['adjacentRunLines'])
        host, start = repair.CONTINUATIONS[transfer['target']]
        if host != marker['node']:
            raise ValueError(f'fragment host differs: {host}')
        context.update(row['id'] for row in nodes[host] if row['instructionIndex'] >= start)
    if case.get('node'):
        node_ids = {row['id'] for row in nodes[case['node']]}
        if not direct <= node_ids:
            raise ValueError(f'{case["id"]}: direct dependencies do not match the node')
        context.update(node_ids)
    if not direct:
        raise ValueError(f'case has no explicit source dependencies: {case["id"]}')
    return {line_id(key) for key in direct}, {line_id(key) for key in context - direct}


def input_group(case_id, inputs, records):
    unknown = inputs - records.keys()
    if unknown:
        raise ValueError(f'{case_id}: unknown source IDs {", ".join(sorted(unknown))}')
    return sorted(inputs)


def build(inventory_path):
    inventory = load_pinned(inventory_path, INVENTORY_SHA)
    records = {row['id']: row for row in inventory['entries']}
    if len(records) != len(inventory['entries']):
        raise ValueError('duplicate shared source ID')
    nodes = defaultdict(list)
    for row in records.values():
        if row['family'] == 'yarn':
            nodes[row['node']].append({**row, 'id': row['id'].removeprefix('yarn:')})
    nodes = dict(nodes)
    cases, reports = {}, {}
    for path in sorted(EVIDENCE.glob('special-scenes-*.json')):
        raw = path.read_bytes()
        registry = json.loads(raw, object_pairs_hook=dl.unique_object)
        field, = [key for key in SOURCE_LINKS if key in registry]
        source = registry[field]
        expected = registry[field + 'Sha256']
        load_pinned(ROOT / source, expected)
        relative = path.relative_to(ROOT).as_posix()
        reports[relative] = {'sha256': dl.sha(raw), 'source': source, 'sourceSha256': expected}
        for case in registry['cases']:
            key = case['id']
            if key in cases:
                raise ValueError(f'duplicate special scene: {key}')
            direct, context = case_inputs(case, nodes)
            direct = input_group(key, direct, records)
            context = input_group(key, context, records)
            for option in case.get('pivotalChoiceIds', ()):
                if records[line_id(option)]['kind'] != 'option':
                    raise ValueError(f'{key}: pivotal choice is not an option')
            cases[key] = {'registry': relative, 'directIds': direct, 'contextIds': context}

    # These display values have multiple source occurrences. Keep their runtime
    # and serialized inputs together rather than treating them as separate terms.
    additional = {
        'new-slot-display': (
            9, {'slot-new-label-serialized-candidate', 'slot-new-runtime-text-candidate'},
            {'preserve-exactly-slot-progress-template', 'preserve-exactly-slot-progress-format'},
        ),
        'missing-yarn-line-display': (
            4, {'player-facing-error-fallback-candidate'},
            {'preserve-exactly-unused-provider-fallback', 'preserve-exactly-dialogue-option-template'},
        ),
    }
    evidence = EVIDENCE / 'non-yarn-translation-scope-20261110.md'
    for key, (expected, roles, context_roles) in additional.items():
        ids = {row['id'] for row in records.values() if isinstance(row['role'], str) and row['role'] in roles}
        context = {row['id'] for row in records.values()
                   if isinstance(row['role'], str) and row['role'] in context_roles}
        if key in cases or len(ids) != expected:
            raise ValueError(f'{key}: unexpected runtime text bindings')
        cases[key] = {'registry': evidence.relative_to(ROOT).as_posix(), 'evidenceSha256': dl.sha(evidence.read_bytes()),
                      'directIds': input_group(key, ids, records), 'contextIds': input_group(key, context, records)}
    direct_ids = {id for case in cases.values() for id in case['directIds']}
    all_ids = direct_ids | {id for case in cases.values() for id in case['contextIds']}
    return {'schema': 1, 'status': 'known-source-cases-indexed', 'sharedInventorySha256': INVENTORY_SHA,
            'sourceRegistries': reports, 'caseCount': len(cases), 'uniqueDirectIds': len(direct_ids),
            'uniqueDirectAndContextIds': len(all_ids), 'cases': cases}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    index = build(args.inventory)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(index, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({key: index[key] for key in ('caseCount', 'uniqueDirectIds', 'uniqueDirectAndContextIds')}))


if __name__ == '__main__':
    main()
