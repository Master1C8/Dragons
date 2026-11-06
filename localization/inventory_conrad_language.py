#!/usr/bin/env python3
"""Trace three Conrad language-dependent source groups in pinned builds."""
import argparse
import json
from pathlib import Path

import UnityPy
import audit_yarn_targets as audit
import compare_yarn_versions as versions
import dialogue_locale as dl
import inventory_alexander_questions as checks
import map_yarn_context as mapping

GROUPS = {
    'dirty-double-meaning': ('Conrad_placed_mount_3', 'b7d05b632985f5a4ea1927e08976f1e6f75c8c04a20b4f7decf8771f03ba2893'),
    'professional-double-meaning': ('Conrad_finished_jerkoff_3', '0b4e6056d35c6455a65aa7ec0ba2332a84b41b9ccd53ec05796a3e853c3be193'),
    'big-c-nickname': ('Conrad_5_outro_ryan_romanced', 'a929cdaf300353f0bea49442b7fbb09b86bd200c3bb7c84e1ea05e6dbe264f0c'),
}
CHOICES = {
    'dirty-double-meaning': [(12, 'line:31fa3bdf', 18), (13, 'line:0372e0d1', 49), (29, 'line:8bab3246', 34)],
    'professional-double-meaning': [(23, 'line:50a559bb', 29), (24, 'line:5788e15c', 34),
                                    (69, 'line:bf977a7e', 75), (70, 'line:05c673e7', 77)],
    'big-c-nickname': [(0, 'line:f57fc630', 6), (1, 'line:f2527ed7', 11),
                       (28, 'line:982fd3c7', 34), (29, 'line:255362b9', 40)],
}


def inspect(root, platform):
    root = Path(root)
    if UnityPy.__version__ != '1.25.4' or dl.sha((root / 'Managed/YarnSpinner.dll').read_bytes()) != mapping.YARN_DLL_SHA:
        raise ValueError('unsupported Yarn runtime schema')
    keys, values, _, program, nodes, _ = versions.load(root, versions.BUILDS[platform])
    locations, _ = mapping.map_nodes(nodes, keys)
    source = dict(zip(keys, values))
    code = audit.instruction_records({node: nodes[node] for node, _ in GROUPS.values()})
    groups = {}
    for name, (node, expected_hash) in GROUPS.items():
        if dl.sha(nodes[node]) != expected_hash:
            raise ValueError(f'unexpected source node: {node}')
        rows = code[node]
        for index, key, destination in CHOICES[name]:
            checks.expect(rows, index, 5, [(1, 2, key.encode()), (2, 0, destination)])
        lines = []
        for index, (op, operands) in enumerate(rows):
            if op not in (3, 5):
                continue
            key = audit.one_string(operands, f'{node}#{index}')
            if key not in source or locations[key]['node'] != node or locations[key]['instructionIndex'] != index:
                raise ValueError(f'source binding mismatch: {key}')
            lines.append({'id': key, 'instructionIndex': index, 'kind': 'line' if op == 3 else 'option',
                          'sourceSha256': dl.sha(source[key].encode('utf-8'))})
        groups[name] = {'node': node, 'nodeSha256': expected_hash, 'lines': lines,
                        'choiceDestinations': [{'instructionIndex': i, 'id': k, 'destination': d}
                                               for i, k, d in CHOICES[name]]}
    checks.expect(code['Conrad_placed_mount_3'], 19, 13, [(1, 2, b'$conrad_jerked_off_3')])
    checks.expect(code['Conrad_finished_jerkoff_3'], 15, 14, [(1, 2, b'$conrad_jerked_off_3')])
    return {'build': versions.BUILDS[platform], 'programSha256': dl.sha(program), 'groups': groups}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    report = {'schema': 1, 'builds': {'macos': inspect(args.macos_data, 'macos'),
                                      'windows': inspect(args.windows_data, 'windows')},
              'limitations': 'Three static source nodes and selected branch controls only. Runtime reachability, gameplay, full source discovery, target wording and editorial acceptance remain unverified.'}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
