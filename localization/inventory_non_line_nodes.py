#!/usr/bin/env python3
"""Inventory compiled Yarn nodes without line or option instructions."""
import argparse
from collections import Counter
import json
from pathlib import Path

import UnityPy
import audit_yarn_targets as audit
import compare_yarn_versions as versions
import dialogue_locale as dl
import map_yarn_context as mapping


def inspect_nodes(nodes):
    parsed = audit.instruction_records(nodes)
    result = []
    for name in sorted(nodes):
        rows = parsed[name]
        if any(op in (3, 5) for op, _ in rows):
            continue
        targets = []
        for index, (op, operands) in enumerate(rows):
            if op in (16, 18):
                if len(operands) != 1 or operands[0][:2] != (1, 2):
                    raise ValueError(f'unexpected node-transfer operands: {name}#{index}')
                target = audit.one_string(operands, f'{name}#{index}')
                if not target:
                    raise ValueError('empty node-transfer target')
                targets.append({'instructionIndex': index, 'kind': 'RunNode' if op == 16 else 'DetourToNode',
                                'target': target, 'targetPresent': target in nodes})
        result.append({'node': name, 'nodeSha256': dl.sha(nodes[name]), 'instructionCount': len(rows),
                       'opcodeCounts': {str(k): v for k, v in sorted(Counter(op for op, _ in rows).items())},
                       'namedTransfers': targets})
    return result


def inspect(root, platform):
    root = Path(root)
    if UnityPy.__version__ != '1.25.4' or dl.sha((root / 'Managed/YarnSpinner.dll').read_bytes()) != mapping.YARN_DLL_SHA:
        raise ValueError('unsupported Yarn runtime schema')
    keys, values, _, program, nodes, _ = versions.load(root, versions.BUILDS[platform])
    mapping.map_nodes(nodes, keys)
    return {'build': versions.BUILDS[platform], 'programSha256': dl.sha(program),
            'totalNodeCount': len(nodes), 'noLineNodes': inspect_nodes(nodes)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    print(json.dumps({'schema': 1, 'builds': {'macos': inspect(args.macos_data, 'macos'),
                                              'windows': inspect(args.windows_data, 'windows')},
        'limitations': 'Static nodes lacking RunLine/AddOption in these pinned programs. Named transfers may lead to displayed text; dynamic jumps, runtime behavior, other programs and source-role completeness are unverified.'}, indent=2))


if __name__ == '__main__':
    main()
