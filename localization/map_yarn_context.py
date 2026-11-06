#!/usr/bin/env python3
"""Bind pinned Yarn line IDs to compiled node and instruction positions."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

import UnityPy
import compare_yarn_versions as source
import dialogue_locale as dl

YARN_DLL_SHA = 'd10c640b1b0b3664241b19137d3f0c27ffa8ba75e0fcf5dac183bbcc89b78f7e'
LINE_ID = re.compile(r'line:[0-9a-f]{8}\Z')
ID_BYTES = re.compile(rb'line:[0-9a-f]{8}')


def map_nodes(nodes, table_ids):
    """Read the pinned game's generated protobuf layout, failing closed on ambiguity."""
    table_ids = list(table_ids)
    if len(set(table_ids)) != len(table_ids):
        raise ValueError('duplicate table ID')
    found, node_hashes = {}, {}
    for name, body in nodes.items():
        node_hashes[name] = dl.sha(body)
        node_fields = list(source.protobuf_fields(body))
        names = [v.decode('utf-8', errors='strict') for n, w, v in node_fields if (n, w) == (1, 2)]
        if names != [name] or any((n, w) not in {(1, 2), (6, 2), (7, 2)} for n, w, _ in node_fields):
            raise ValueError(f'unexpected node structure: {name}')
        instructions = [v for n, w, v in node_fields if (n, w) == (7, 2)]
        for index, instruction in enumerate(instructions):
            fields = list(source.protobuf_fields(instruction))
            if len(fields) != 1 or fields[0][1] != 2 or not 1 <= fields[0][0] <= 23:
                raise ValueError(f'unexpected instruction: {name}#{index}')
            op, _, payload = fields[0]
            if op not in (3, 5):
                continue
            operands = list(source.protobuf_fields(payload))
            allowed = {(1, 2), (2, 0)} if op == 3 else {(1, 2), (2, 0), (3, 0), (4, 0)}
            if any((n, w) not in allowed for n, w, _ in operands):
                raise ValueError(f'unexpected line operands: {name}#{index}')
            if len({n for n, _, _ in operands}) != len(operands):
                raise ValueError(f'duplicate line operands: {name}#{index}')
            ids = [v.decode('utf-8', errors='strict') for n, w, v in operands if (n, w) == (1, 2)]
            if len(ids) != 1 or not LINE_ID.fullmatch(ids[0]) or ids[0] in found:
                raise ValueError(f'invalid or duplicated line ID: {name}#{index}')
            numbers = {n: v for n, w, v in operands if w == 0}
            found[ids[0]] = {'node': name, 'instructionIndex': index,
                              'kind': 'line' if op == 3 else 'option',
                              'substitutionCount': numbers.get(2 if op == 3 else 3, 0)}
            if op == 5:
                found[ids[0]]['destination'] = numbers.get(2, 0)
                found[ids[0]]['hasCondition'] = bool(numbers.get(4, 0))
                if numbers.get(4, 0) not in (0, 1):
                    raise ValueError(f'invalid option condition flag: {name}#{index}')
    if set(found) != set(table_ids):
        raise ValueError(f'line inventory mismatch: {len(set(table_ids)-set(found))} missing, {len(set(found)-set(table_ids))} unknown')
    return found, node_hashes


def load_platform(root, platform):
    root = Path(root)
    if dl.sha((root / 'Managed/YarnSpinner.dll').read_bytes()) != YARN_DLL_SHA:
        raise ValueError('unsupported Yarn runtime schema')
    keys, values, extras, program, nodes, _ = source.load(root, source.BUILDS[platform])
    locations, hashes = map_nodes(nodes, keys)
    raw_ids = Counter(x.decode() for x in ID_BYTES.findall(program))
    missing = Counter(keys) - raw_ids
    if missing:
        raise ValueError('parsed line IDs absent from raw program')
    # Additional ID occurrences are not discarded: some belong to state keys.
    # This raw scan cannot classify their role or provide a complete operand map.
    extra_occurrences = dict(sorted((raw_ids - Counter(keys)).items()))
    return keys, values, extras, program, locations, hashes, extra_occurrences


def build(mac, windows):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    a = load_platform(mac, 'macos')
    b = load_platform(windows, 'windows')
    if a[0] != b[0]:
        raise ValueError('builds have different ordered line IDs')
    records = {}
    for key, av, bv in zip(a[0], a[1], b[1]):
        records[key] = {'macos': a[4][key], 'windows': b[4][key],
                        'sourceSha256': {'macos': dl.sha(av.encode('utf-8')),
                                         'windows': dl.sha(bv.encode('utf-8'))}}
    return {'schema': 1, 'yarnRuntimeSha256': YARN_DLL_SHA,
            'builds': source.BUILDS,
            'programSha256': {'macos': dl.sha(a[3]), 'windows': dl.sha(b[3])},
            'nodeSha256': {'macos': a[5], 'windows': b[5]},
            'additionalRawIdOccurrences': {'macos': a[6], 'windows': b[6]},
            'lineIds': records,
            'limitations': 'Instruction binding is static. RunLine and AddOption are instruction types, not proof of reachability or final visible-text classification. Headers, commands, operands, substitutions, branching and special-scene context still require review. Program hashes bind all compiled bytes; this report is not a standalone preserve-exactly validator.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    result = build(args.macos_data, args.windows_data)
    # Keep each line-ID record on one line for compact, reviewable diffs.
    print('{')
    for key, value in result.items():
        if key == 'lineIds':
            print('  \"lineIds\": {')
            for index, (line_id, record) in enumerate(value.items()):
                comma = ',' if index + 1 < len(value) else ''
                print('    ' + json.dumps(line_id) + ': ' + json.dumps(record, ensure_ascii=False, separators=(',', ':')) + comma)
            print('  },')
        else:
            comma = '' if key == 'limitations' else ','
            print('  ' + json.dumps(key) + ': ' + json.dumps(value, ensure_ascii=False, separators=(',', ':')) + comma)
    print('}')


if __name__ == '__main__':
    main()
