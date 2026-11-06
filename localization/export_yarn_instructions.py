#!/usr/bin/env python3
"""Export source-bound Yarn instruction context for scene review."""
import argparse
from collections import Counter
import json
from pathlib import Path

import UnityPy
import audit_yarn_targets as audit
import compare_yarn_versions as versions
import dialogue_locale as dl
import map_yarn_context as mapping


def operand_record(field, wire, value):
    row = {'field': field, 'wire': wire}
    if wire == 0:
        row['unsigned'] = value
    else:
        row['hex'] = value.hex()
        if wire == 2:
            try:
                decoded = value.decode('utf-8', errors='strict')
                if decoded.isprintable():
                    row['utf8'] = decoded
            except UnicodeDecodeError:
                pass
    return row


def export_build(root, platform):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    root = Path(root)
    if dl.sha((root / 'Managed/YarnSpinner.dll').read_bytes()) != mapping.YARN_DLL_SHA:
        raise ValueError('unsupported Yarn runtime schema')
    keys, values, _, program, nodes, other = versions.load(root, versions.BUILDS[platform])
    locations, _ = mapping.map_nodes(nodes, keys)
    texts = dict(zip(keys, values))
    result, seen, counts = {}, set(), Counter()
    for name, body in sorted(nodes.items()):
        fields = list(versions.protobuf_fields(body))
        instructions = [v for n, w, v in fields if (n, w) == (7, 2)]
        rows = []
        for index, raw in enumerate(instructions):
            wrapper = list(versions.protobuf_fields(raw))
            if len(wrapper) != 1 or wrapper[0][1] != 2 or not 1 <= wrapper[0][0] <= 23:
                raise ValueError(f'unexpected instruction: {name}#{index}')
            op, _, payload = wrapper[0]
            operands = list(versions.protobuf_fields(payload))
            row = {'index': index, 'opcodeField': op, 'encodedHex': raw.hex(),
                   'operands': [operand_record(*operand) for operand in operands]}
            counts[op] += 1
            if op in (3, 5):
                line = audit.one_string(operands, f'{name}#{index}')
                if line in seen or line not in texts or locations[line]['node'] != name or locations[line]['instructionIndex'] != index:
                    raise ValueError(f'invalid source binding: {name}#{index}')
                row['lineId'] = line
                row['kind'] = 'line' if op == 3 else 'option'
                row['source'] = texts[line]
                seen.add(line)
            rows.append(row)
        result[name] = {'nodeSha256': dl.sha(body), 'nodeHex': body.hex(), 'instructions': rows}
    if seen != set(keys):
        raise ValueError('instruction export does not cover the source table')
    return {'platform': platform, 'build': versions.BUILDS[platform],
            'programSha256': dl.sha(program), 'programOtherFields': [operand_record(*x) for x in other],
            'nodeCount': len(nodes), 'lineCount': len(seen),
            'instructionCounts': {str(k): counts[k] for k in sorted(counts)}, 'nodes': result}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data_dir', type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    report = export_build(args.data_dir, args.platform)
    report['limitations'] = ('Encoded protobuf fields and source strings are static review material. '
        'Numeric opcode/operand fields are not a complete semantic disassembly; conditions, dynamic '
        'substitutions, reachability, consumer behavior and non-Yarn sources remain to be reviewed.')
    with args.output.open('x', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f"Exported {report['nodeCount']} nodes and {report['lineCount']} text IDs")


if __name__ == '__main__':
    main()
