#!/usr/bin/env python3
"""Verify every known exact game component in the built data directory."""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path

import UnityPy

import compare_yarn_versions as versions
import dialogue_locale as dl
from assemble_source_inventory import INVENTORY_SHA, load_pinned


def source_contract(inventory, platform):
    """Summarize the disjoint source-occurrence roles and bind exact components."""
    counts = defaultdict(Counter)
    components = defaultdict(dict)
    component_fields = set()
    for row in inventory['entries']:
        source = row['source'].get(platform)
        if source is None:
            continue
        role = row['role']
        if isinstance(role, dict):
            role = role[platform]
        family = row['family']
        if row.get('preserveExactPrefix'):
            prefix = row['preserveExactPrefix'][platform]
            if not prefix or not source.startswith(prefix):
                raise ValueError(f'source prefix binding differs: {row["id"]}')
            protection = 'exact-prefix-and-display'
        elif row.get('localeInput') == 'speaker-locale':
            if row['preserveExactValue'][platform] != source:
                raise ValueError(f'speaker source binding differs: {row["id"]}')
            protection = 'exact-value-and-display'
        elif role.startswith('preserve-exactly'):
            if 'preserveExactValue' in row and row['preserveExactValue'][platform] != source:
                raise ValueError(f'exact source binding differs: {row["id"]}')
            protection = 'exact-value'
        elif role == 'candidate' or role.endswith('-candidate'):
            protection = 'display'
        else:
            raise ValueError(f'unresolved source role: {row["id"]}')
        counts[family][protection] += 1
        if family != 'game-component':
            continue
        if protection != 'exact-value':
            raise ValueError(f'non-exact serialized game component: {row["id"]}')
        asset, path_id = row['location'][platform].rsplit('#', 1)
        path_id = int(path_id)
        field = (asset, path_id, tuple(row['fieldPath']))
        if field in component_fields:
            raise ValueError(f'duplicate component string field: {row["id"]}')
        component_fields.add(field)
        expected = row['rawObjectSha256']
        if components[asset].setdefault(path_id, expected) != expected:
            raise ValueError(f'conflicting component object digest: {asset}#{path_id}')
    if not components:
        raise ValueError('no exact game components')
    return {family: dict(roles) for family, roles in sorted(counts.items())}, components


def verify_components(candidate, components):
    """Compare complete component bytes using one load per affected asset."""
    candidate = Path(candidate)
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    verified = {}
    for asset, expected in sorted(components.items()):
        file = candidate / asset
        if file.is_symlink() or not file.is_file():
            raise ValueError(f'expected a real candidate asset: {asset}')
        objects = UnityPy.load(str(file)).objects
        index = {obj.path_id: obj for obj in objects}
        if len(index) != len(objects):
            raise ValueError(f'duplicate candidate object identity: {asset}')
        for path_id, digest in expected.items():
            obj = index.get(path_id)
            if obj is None or obj.type.name != 'MonoBehaviour':
                raise ValueError(f'candidate component missing or wrong type: {asset}#{path_id}')
            if dl.sha(obj.get_raw_data()) != digest:
                raise ValueError(f'exact game component changed: {asset}#{path_id}')
        verified[asset] = len(expected)
    return verified


def verify(platform, inventory_path, candidate):
    inventory = load_pinned(inventory_path, INVENTORY_SHA)
    counts, components = source_contract(inventory, platform)
    verified = verify_components(candidate, components)
    return {'schema': 1, 'platform': platform, 'sharedInventorySha256': INVENTORY_SHA,
            'sourceOccurrenceRoles': counts, 'verifiedGameComponentObjects': verified,
            'verifiedGameComponentFields': counts['game-component']['exact-value']}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=tuple(versions.BUILDS))
    parser.add_argument('candidate_data', type=Path)
    parser.add_argument('--inventory', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.platform, args.inventory, args.candidate_data), indent=2))


if __name__ == '__main__':
    main()
