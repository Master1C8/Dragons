#!/usr/bin/env python3
"""Trace two language-dependent Alexander dialogue groups in both pinned builds."""
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
    'proletarian-register': ('Alexander_1_required', ['line:73e4789c', 'line:e5d47feb',
        'line:8512365e', 'line:74c9c07b', 'line:e2f9c70c', 'line:13223129', 'line:a97338b0']),
    'teacher-professor-correction': ('Alexander_1_intro', ['line:9aa97614', 'line:393c128a',
        'line:155d1c64', 'line:af0c15fd', 'line:836d1b13', 'line:1270a483']),
}


def choice(rows, index, key, destination):
    checks.expect(rows, index, 5, [(1, 2, key.encode()), (2, 0, destination)])


def inspect(root, platform):
    root = Path(root)
    if UnityPy.__version__ != '1.25.4' or dl.sha((root / 'Managed/YarnSpinner.dll').read_bytes()) != mapping.YARN_DLL_SHA:
        raise ValueError('unsupported Yarn runtime schema')
    keys, values, _, program, nodes, _ = versions.load(root, versions.BUILDS[platform])
    locations, _ = mapping.map_nodes(nodes, keys)
    source = dict(zip(keys, values))
    code = audit.instruction_records({node: nodes[node] for node, _ in GROUPS.values()})
    required, intro = code['Alexander_1_required'], code['Alexander_1_intro']
    choice(required, 5, 'line:e5d47feb', 11)
    choice(required, 6, 'line:8512365e', 15)
    checks.expect(required, 14, 1, [(1, 0, 23)])
    checks.expect(required, 22, 1, [(1, 0, 23)])
    choice(intro, 19, 'line:393c128a', 25)
    choice(intro, 20, 'line:155d1c64', 30)
    checks.expect(intro, 29, 1, [(1, 0, 35)])
    checks.expect(intro, 34, 1, [(1, 0, 35)])
    groups = {}
    for name, (node, ids) in GROUPS.items():
        lines = []
        for key in ids:
            if key not in source or locations[key]['node'] != node:
                raise ValueError(f'group source binding changed: {key}')
            lines.append({'id': key, 'instructionIndex': locations[key]['instructionIndex'],
                          'sourceSha256': dl.sha(source[key].encode('utf-8'))})
        groups[name] = {'node': node, 'nodeSha256': dl.sha(nodes[node]), 'lines': lines}
    return {'build': versions.BUILDS[platform], 'programSha256': dl.sha(program), 'groups': groups}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    report = {'schema': 1, 'builds': {'macos': inspect(args.macos_data, 'macos'),
                                      'windows': inspect(args.windows_data, 'windows')},
              'limitations': 'Static source bindings and two specific choice paths; no natural reachability, runtime behavior, complete semantic discovery or target wording is established.'}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
