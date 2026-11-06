#!/usr/bin/env python3
"""Audit static named Yarn node transfers and suspicious embedded source markers."""
import argparse
import json
from pathlib import Path

import UnityPy
import compare_yarn_versions as source
import dialogue_locale as dl


def instruction_records(nodes):
    out = {}
    for name, node in nodes.items():
        rows = []
        for field, wire, value in source.protobuf_fields(node):
            if (field, wire) != (7, 2):
                continue
            operands = list(source.protobuf_fields(value))
            if len(operands) != 1 or operands[0][1] != 2 or not 1 <= operands[0][0] <= 23:
                raise ValueError(f'unknown instruction: {name}#{len(rows)}')
            op, _, payload = operands[0]
            rows.append((op, list(source.protobuf_fields(payload))))
        out[name] = rows
    return out


def one_string(operands, name):
    values = [v for n, w, v in operands if (n, w) == (1, 2)]
    if len(values) != 1:
        raise ValueError(f'invalid string operand: {name}')
    return values[0].decode('utf-8', errors='strict')


def inspect_program(nodes, texts):
    rows = instruction_records(nodes)
    markers, targets = {}, []
    for node, instructions in rows.items():
        for index, (op, operands) in enumerate(instructions):
            if op == 3:
                line_id = one_string(operands, f'{node}#{index}')
                if line_id not in texts:
                    raise ValueError(f'unknown RunLine ID: {line_id}')
                text = texts[line_id]
                if text.startswith('title: '):
                    name = text[len('title: '):]
                    if not name or name in markers:
                        raise ValueError(f'empty or duplicate title marker: {name}')
                    adjacent = []
                    for other in (index - 1, index + 1):
                        if 0 <= other < len(instructions) and instructions[other][0] == 3:
                            adjacent_id = one_string(instructions[other][1], f'{node}#{other}')
                            if adjacent_id not in texts:
                                raise ValueError(f'unknown adjacent RunLine ID: {adjacent_id}')
                            adjacent.append({'instructionIndex': other, 'lineId': adjacent_id,
                                             'sourceSha256': dl.sha(texts[adjacent_id].encode('utf-8'))})
                    markers[name] = {'node': node, 'instructionIndex': index, 'lineId': line_id,
                                     'sourceSha256': dl.sha(text.encode('utf-8')), 'adjacentRunLines': adjacent}
            elif op in (16, 18):
                if len(operands) != 1 or operands[0][:2] != (1, 2):
                    raise ValueError(f'unexpected node-transfer operands: {node}#{index}')
                name = one_string(operands, f'{node}#{index}')
                if not name:
                    raise ValueError(f'empty node-transfer target: {node}#{index}')
                targets.append({'node': node, 'instructionIndex': index,
                                'kind': 'RunNode' if op == 16 else 'DetourToNode',
                                'target': name, 'targetPresent': name in nodes})
    for target in targets:
        target['matchingEmbeddedTitle'] = markers.get(target['target'])
    return targets, markers


def inspect(data, platform):
    keys, values, _, program, nodes, _ = source.load(data, source.BUILDS[platform])
    targets, markers = inspect_program(nodes, dict(zip(keys, values)))
    return {'build': source.BUILDS[platform], 'programSha256': dl.sha(program),
            'nodeCount': len(nodes), 'namedTransfers': targets, 'embeddedTitleMarkers': markers}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    result = {'schema': 1, 'builds': {'macos': inspect(args.macos_data, 'macos'),
                                      'windows': inspect(args.windows_data, 'windows')},
              'limitations': 'Static named RunNode and DetourToNode targets in one extracted Yarn project only. Other programs may be loaded or merged; reachability, dynamic jumps, conditions and game-level error handling are not established. Embedded title-like lines are source evidence, not permission to rewrite the program.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
