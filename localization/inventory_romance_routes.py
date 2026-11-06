#!/usr/bin/env python3
"""Trace pivotal route choices and source-bound static Yarn dependencies."""
import argparse
import json
from pathlib import Path

import UnityPy
import audit_yarn_targets as audit
import compare_yarn_versions as versions
import dialogue_locale as dl
import inventory_alexander_questions as checks

FLAGS = ('$alexander_romanced', '$suggested_ryan_to_conrad', '$ryan_conrad_romanced',
         '$ryan_romanced', '$conrad_romanced')
ROOTS = ('Alexander_5_romance_route', 'Conrad_Outro_3', 'ryan_food_dialogue')


def assert_choice(rows, position, line, dest, conditional=False):
    operands = [(1, 2, line.encode()), (2, 0, dest)]
    if conditional:
        operands.append((4, 0, 1))
    checks.expect(rows, position, 5, operands)


def assert_write(rows, bool_index, name, value):
    checks.expect(rows, bool_index, 9, [(1, 0, 1)] if value else [])
    checks.expect(rows, bool_index + 1, 14, [(1, 2, name.encode())])


def extract(root, platform):
    keys, values, _, program, nodes, other = versions.load(root, versions.BUILDS[platform])
    source = dict(zip(keys, values))
    if len(source) != len(keys):
        raise ValueError('duplicate source IDs')
    code = audit.instruction_records(nodes)
    if not set(ROOTS).issubset(code):
        raise ValueError('missing route decision node')
    initial = checks.initial_values(other)
    if any(initial.get(flag) != [(2, 0, 0)] for flag in FLAGS):
        raise ValueError('unexpected initial romance state')
    alex, conrad, ryan = (code[x] for x in ROOTS)
    assert_choice(alex, 58, 'line:a0e49f02', 64)
    assert_choice(alex, 59, 'line:0371fb9c', 75)
    assert_write(alex, 71, '$alexander_romanced', True)
    assert_choice(conrad, 15, 'line:36ff6bd9', 21)
    assert_choice(conrad, 16, 'line:7e9d40e6', 66)
    assert_write(conrad, 22, '$suggested_ryan_to_conrad', True)
    assert_write(conrad, 67, '$suggested_ryan_to_conrad', False)
    checks.expect(ryan, 104, 13, [(1, 2, b'$suggested_ryan_to_conrad')])
    checks.expect(ryan, 105, 9, [(1, 0, 1)])
    checks.expect(ryan, 106, 8, [(1, 5, b'\x00\x00\x00@')])
    checks.expect(ryan, 107, 12, [(1, 2, b'Bool.EqualTo')])
    assert_choice(ryan, 108, 'line:bedc761d', 119, True)
    assert_choice(ryan, 109, 'line:e104b8e4', 183)
    checks.expect(ryan, 110, 13, [(1, 2, b'$suggested_ryan_to_conrad')])
    checks.expect(ryan, 111, 9, [])
    checks.expect(ryan, 112, 8, [(1, 5, b'\x00\x00\x00@')])
    checks.expect(ryan, 113, 12, [(1, 2, b'Bool.EqualTo')])
    assert_choice(ryan, 114, 'line:f5a81524', 229, True)
    assert_write(ryan, 120, '$ryan_conrad_romanced', True)
    assert_write(ryan, 184, '$ryan_romanced', True)
    assert_write(ryan, 230, '$conrad_romanced', True)
    references = {flag: [] for flag in FLAGS}
    transfers = {}
    direct = set(ROOTS)
    for node, instructions in code.items():
        transfers[node] = []
        for index, (op, operands) in enumerate(instructions):
            if op in (13, 14):
                variable = audit.one_string(operands, f'{node}#{index}')
                if variable in references:
                    references[variable].append({'node': node, 'instructionIndex': index,
                                                 'operation': 'read' if op == 13 else 'write'})
                    direct.add(node)
            elif op in (16, 18):
                target = audit.one_string(operands, f'{node}#{index}')
                transfers[node].append({'instructionIndex': index, 'target': target,
                                        'kind': 'RunNode' if op == 16 else 'DetourToNode',
                                        'targetPresent': target in nodes})
    closure, pending, missing = set(direct), list(direct), []
    while pending:
        node = pending.pop()
        for edge in transfers[node]:
            target = edge['target']
            if target not in nodes:
                missing.append({'node': node, **edge})
            elif target not in closure:
                closure.add(target)
                pending.append(target)
    selected, seen = {}, set()
    for node in sorted(closure):
        lines = []
        for index, (op, operands) in enumerate(code[node]):
            if op not in (3, 5):
                continue
            line = audit.one_string(operands, f'{node}#{index}')
            if line not in source or line in seen:
                raise ValueError(f'unknown or duplicate route source ID: {line}')
            seen.add(line)
            lines.append({'id': line, 'instructionIndex': index,
                          'kind': 'line' if op == 3 else 'option',
                          'sourceSha256': dl.sha(source[line].encode('utf-8'))})
        selected[node] = {'nodeSha256': dl.sha(nodes[node]), 'lines': lines,
                          'namedTransfers': transfers[node]}
    return {'build': versions.BUILDS[platform], 'programSha256': dl.sha(program),
            'initialValues': {flag: False for flag in FLAGS}, 'directNodes': sorted(direct),
            'flagReferences': references, 'staticTransferClosure': selected,
            'unresolvedNamedTargets': sorted(missing, key=lambda x: (x['node'], x['instructionIndex'])),
            'sourceLineCount': len(seen)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    result = {'schema': 1, 'pivotalChoiceIds': ['line:a0e49f02', 'line:0371fb9c', 'line:36ff6bd9',
                                               'line:7e9d40e6', 'line:bedc761d', 'line:e104b8e4',
                                               'line:f5a81524'],
              'builds': {'macos': extract(args.macos_data, 'macos'),
                         'windows': extract(args.windows_data, 'windows')},
              'limitations': 'Static named transfers and explicit reads/writes of five selected Yarn variables only. Dynamic dispatch, code-side state, reachability, all consumers, texture/audio dependencies and natural gameplay require separate investigation.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
