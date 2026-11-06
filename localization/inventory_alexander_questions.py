#!/usr/bin/env python3
"""Trace source-bound Alexander question groups and their state identities."""
import argparse
import json
from pathlib import Path

import UnityPy
import audit_yarn_targets as audit
import compare_yarn_versions as versions
import dialogue_locale as dl

NODE = 'Alexander_questions'
NODE_SHA = '5b7ca45c949d907f6cfa9471d6b79ccb8ee07dca83cf008509cbfb755b606ef2'
GROUPS = [
    ('teaching', 'line:fc7aaaa0', 3, 34, 69),
    ('purple', 'line:daa040eb', 7, 69, 112),
    ('size', 'line:21c0526b', 11, 112, 140),
    ('number-seven-taste', 'line:c2bdc402', 15, 140, 182),
    ('impression', 'line:838cdf1b', 19, 182, 225),
    ('happiness', 'line:72a9b5bb', 23, 225, 256),
    ('family-crest', 'line:a5a8a9d5', 27, 256, 290),
]


def expect(rows, index, opcode, operands):
    if not 0 <= index < len(rows) or rows[index] != (opcode, operands):
        raise ValueError(f'unexpected control instruction at {index}')


def initial_values(other):
    values = {}
    for field, wire, data in other:
        if (field, wire) != (3, 2):
            continue
        parts = list(versions.protobuf_fields(data))
        keys = [v.decode('utf-8', errors='strict') for n, w, v in parts if (n, w) == (1, 2)]
        operands = [v for n, w, v in parts if (n, w) == (2, 2)]
        if len(keys) != 1 or len(operands) != 1 or keys[0] in values:
            raise ValueError('invalid or duplicated program initial value')
        values[keys[0]] = list(versions.protobuf_fields(operands[0]))
    return values


def extract(data, platform):
    keys, values, _, program, nodes, other = versions.load(data, versions.BUILDS[platform])
    if NODE not in nodes or dl.sha(nodes[NODE]) != NODE_SHA:
        raise ValueError('unsupported Alexander question bytecode')
    source = dict(zip(keys, values))
    rows = audit.instruction_records({NODE: nodes[NODE]})[NODE]
    if len(rows) != 294:
        raise ValueError('unexpected Alexander instruction count')
    initials = initial_values(other)
    if initials.get('$has_asked_question') != [(2, 0, 0)]:
        raise ValueError('unexpected initial question-state value')
    expect(rows, 28, 13, [(1, 2, b'$has_asked_question')])
    expect(rows, 29, 5, [(1, 2, b'line:66fb84fe'), (2, 0, 290), (4, 0, 1)])
    expect(rows, 30, 6, [])
    expect(rows, 31, 10, [(1, 0, 293)])
    expect(rows, 32, 11, [])
    expect(rows, 33, 2, [])
    expect(rows, 290, 11, [])
    expect(rows, 291, 16, [(1, 2, b'Alexander_3_required_end')])
    expect(rows, 292, 1, [(1, 0, 293)])
    expect(rows, 293, 20, [])
    if 'Alexander_3_required_end' not in nodes:
        raise ValueError('question exit node missing')
    ending = audit.instruction_records({'end': nodes['Alexander_3_required_end']})['end']
    expect(ending, 0, 9, [])  # protobuf default false
    expect(ending, 1, 14, [(1, 2, b'$has_asked_question')])
    expect(ending, 2, 11, [])
    groups, seen = [], {'line:66fb84fe'}
    for name, line_id, option_index, start, end in GROUPS:
        variable = '$Yarn.Internal.Once.' + line_id
        if initials.get(variable) != [(2, 0, 0)]:
            raise ValueError(f'unexpected initial once-state: {line_id}')
        expect(rows, option_index - 3, 13, [(1, 2, variable.encode())])
        expect(rows, option_index - 2, 8, [(1, 5, b'\x00\x00\x80?')])
        expect(rows, option_index - 1, 12, [(1, 2, b'Bool.Not')])
        expect(rows, option_index, 5, [(1, 2, line_id.encode()), (2, 0, start), (4, 0, 1)])
        expect(rows, start, 11, [])
        expect(rows, start + 1, 9, [(1, 0, 1)])
        expect(rows, start + 2, 14, [(1, 2, variable.encode())])
        expect(rows, end - 5, 9, [(1, 0, 1)])
        expect(rows, end - 4, 14, [(1, 2, b'$has_asked_question')])
        expect(rows, end - 3, 11, [])
        expect(rows, end - 2, 16, [(1, 2, NODE.encode())])
        expect(rows, end - 1, 1, [(1, 0, 293)])
        if line_id not in source or line_id in seen:
            raise ValueError(f'unknown or duplicate group option: {line_id}')
        seen.add(line_id)
        lines, commands = [], []
        for index in range(start, end):
            op, operands = rows[index]
            if op in (3, 5):
                child_id = audit.one_string(operands, f'{NODE}#{index}')
                if child_id not in source or child_id in seen:
                    raise ValueError(f'unknown or duplicate group line: {child_id}')
                if op == 5:
                    destinations = [v for n, w, v in operands if (n, w) == (2, 0)]
                    if len(destinations) != 1 or not start <= destinations[0] < end:
                        raise ValueError(f'option leaves group: {child_id}')
                seen.add(child_id)
                lines.append({'id': child_id, 'instructionIndex': index,
                              'kind': 'line' if op == 3 else 'option',
                              'sourceSha256': dl.sha(source[child_id].encode('utf-8'))})
            elif op in (1, 10):
                destinations = [v for n, w, v in operands if (n, w) == (1, 0)]
                if len(destinations) != 1 or not (start <= destinations[0] < end or destinations[0] == 293):
                    raise ValueError(f'jump leaves group: {NODE}#{index}')
            elif op == 16 and index != end - 2:
                raise ValueError(f'unexpected node transfer in group: {NODE}#{index}')
            elif op == 4:
                commands.append({'instructionIndex': index, 'text': audit.one_string(operands, f'{NODE}#{index}')})
        groups.append({'id': name, 'questionId': line_id,
                       'questionSourceSha256': dl.sha(source[line_id].encode('utf-8')),
                       'optionInstructionIndex': option_index, 'destination': start,
                       'bodyEndExclusive': end, 'onceVariable': variable, 'bodyLines': lines,
                       'commands': commands})
    all_node_ids = {audit.one_string(operands, f'{NODE}#{i}')
                    for i, (op, operands) in enumerate(rows) if op in (3, 5)}
    if seen != all_node_ids or len(seen) != 77:
        raise ValueError('question groups do not cover exactly the node line IDs')
    return {'programSha256': dl.sha(program), 'nodeSha256': NODE_SHA,
            'endNodeSha256': dl.sha(nodes['Alexander_3_required_end']), 'groups': groups,
            'sharedExit': {'optionId': 'line:66fb84fe', 'sourceSha256': dl.sha(source['line:66fb84fe'].encode('utf-8')),
                           'conditionVariable': '$has_asked_question', 'destination': 290,
                           'targetNode': 'Alexander_3_required_end'},
            'sourceLineCount': len(seen)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    mac, win = extract(args.macos_data, 'macos'), extract(args.windows_data, 'windows')
    if mac['groups'] != win['groups'] or mac['sharedExit'] != win['sharedExit']:
        raise ValueError('Alexander source groups differ across builds')
    print(json.dumps({'schema': 1, 'macosProgramSha256': mac['programSha256'],
                      'windowsProgramSha256': win['programSha256'], 'nodeSha256': NODE_SHA,
                      'endNodeSha256': {'macos': mac['endNodeSha256'], 'windows': win['endNodeSha256']},
                      'sourceLineCount': mac['sourceLineCount'], 'groups': mac['groups'],
                      'sharedExit': mac['sharedExit'],
                      'limitations': 'Static bytecode and text bindings only. Actual reachability, all callers, variable persistence, dynamic command execution, visual typography and locale adaptation require separate review.'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
