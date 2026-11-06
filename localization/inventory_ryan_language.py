#!/usr/bin/env python3
"""Trace selected Ryan language-dependent groups in both pinned builds."""
import argparse
import json
from pathlib import Path

import UnityPy
import audit_yarn_targets as audit
import compare_yarn_versions as versions
import dialogue_locale as dl
import inventory_alexander_questions as checks
import map_yarn_context as mapping

SPECS = {
    'editor-route-prompt': ('Ryan_4_intro', '89398eaf5f98938c30d9217f95837c3bb1ab994b61482108c11f47c18c8308b6', [(4, 28)],
        [(10, 'line:4ab6c5a9', 16), (11, 'line:dc86c2de', 21)]),
    'mouth-full-speech': ('Ryan_4_intro', '89398eaf5f98938c30d9217f95837c3bb1ab994b61482108c11f47c18c8308b6', [(28, 60)],
        [(30, 'line:390f05be', 36), (31, 'line:af3f02c9', 38), (47, 'line:b6fb6fce', 53), (48, 'line:0caa6657', 55)]),
    'salmon-guy-dragon': ('Ryan_5_Required_ryan_romanced', '8ac6ebc619846e1db9c7d878ba29b4ad61723b6fb4bb32649d64fd0363213fc1', [(0, 11), (47, 73)],
        [(7, 'line:81905be1', 47), (50, 'line:e5937e30', 56), (51, 'line:fc571337', 65)]),
    'movie-title-choices': ('Ryan_5_Required_ryan_romanced', '8ac6ebc619846e1db9c7d878ba29b4ad61723b6fb4bb32649d64fd0363213fc1', [(0, 11), (84, 125)],
        [(9, 'line:bd66082e', 84), (92, 'line:962abe27', 99), (93, 'line:f1c14f75', 107), (94, 'line:7e352505', 115)]),
    'conrad-height-euphemism': ('ryan_food_dialogue', '03bf2da4fb5edb2f1eda00716d1848aa555fec665f366c4004862da8255127e5', [(128, 161), (238, 270)],
        [(129, 'line:31281c6d', 135), (130, 'line:a7181b1a', 137), (140, 'line:a035a3fd', 146), (141, 'line:69dd6a73', 154),
         (239, 'line:48d4a45a', 245), (240, 'line:dee4a32d', 247), (250, 'line:2f3f5508', 256), (251, 'line:a0cb3f78', 264)]),
}


def inspect(root, platform):
    root = Path(root)
    if UnityPy.__version__ != '1.25.4' or dl.sha((root / 'Managed/YarnSpinner.dll').read_bytes()) != mapping.YARN_DLL_SHA:
        raise ValueError('unsupported Yarn runtime schema')
    keys, values, _, program, nodes, _ = versions.load(root, versions.BUILDS[platform])
    locations, _ = mapping.map_nodes(nodes, keys)
    source = dict(zip(keys, values))
    code = audit.instruction_records({node: nodes[node] for node, _, _, _ in SPECS.values()})
    groups = {}
    for name, (node, expected_hash, spans, choices) in SPECS.items():
        if dl.sha(nodes[node]) != expected_hash:
            raise ValueError(f'unexpected source node: {node}')
        rows = code[node]
        for index, key, destination in choices:
            checks.expect(rows, index, 5, [(1, 2, key.encode()), (2, 0, destination)])
        lines = []
        for index, (op, operands) in enumerate(rows):
            if op not in (3, 5) or not any(start <= index < end for start, end in spans):
                continue
            key = audit.one_string(operands, f'{node}#{index}')
            if key not in source or locations[key]['node'] != node or locations[key]['instructionIndex'] != index:
                raise ValueError(f'source binding mismatch: {key}')
            lines.append({'id': key, 'instructionIndex': index, 'kind': 'line' if op == 3 else 'option',
                          'sourceSha256': dl.sha(source[key].encode('utf-8'))})
        groups[name] = {'node': node, 'nodeSha256': expected_hash, 'instructionSpans': spans, 'lines': lines,
                        'choiceDestinations': [{'instructionIndex': i, 'id': k, 'destination': d} for i, k, d in choices]}
    intro = code['Ryan_4_intro']
    checks.expect(intro, 4, 13, [(1, 2, b'$isEditor')])
    checks.expect(intro, 8, 10, [(1, 0, 27)])
    checks.expect(intro, 17, 9, [(1, 0, 1)])
    checks.expect(intro, 18, 14, [(1, 2, b'$suggested_ryan_to_conrad')])
    checks.expect(intro, 22, 9, [])
    checks.expect(intro, 23, 14, [(1, 2, b'$suggested_ryan_to_conrad')])
    return {'build': versions.BUILDS[platform], 'programSha256': dl.sha(program), 'groups': groups}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    report = {'schema': 1, 'builds': {'macos': inspect(args.macos_data, 'macos'),
                                      'windows': inspect(args.windows_data, 'windows')},
              'limitations': 'Selected static scene spans and branch controls only. Surrounding route conditions, runtime reachability, other sources, target wording and editorial review remain open.'}
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
