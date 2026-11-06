#!/usr/bin/env python3
"""Export paired source texts grouped by verified Yarn node and instruction order."""
import argparse
from collections import defaultdict
import json
from pathlib import Path

import map_yarn_context as mapping


def export(mac, windows):
    context = mapping.build(mac, windows)
    a = mapping.load_platform(mac, 'macos')
    b = mapping.load_platform(windows, 'windows')
    if a[0] != b[0] or set(a[0]) != set(context['lineIds']):
        raise ValueError('source and context inventories differ')
    scenes = defaultdict(list)
    for key, mac_text, win_text in zip(a[0], a[1], b[1]):
        record = context['lineIds'][key]
        if record['macos'] != record['windows']:
            raise ValueError(f'platform location differs for {key}; explicit reconciliation required')
        loc = record['macos']
        if (mapping.dl.sha(mac_text.encode('utf-8')) != record['sourceSha256']['macos'] or
                mapping.dl.sha(win_text.encode('utf-8')) != record['sourceSha256']['windows']):
            raise ValueError(f'source text fingerprint differs for {key}')
        scenes[loc['node']].append({'id': key, **{k: v for k, v in loc.items() if k != 'node'},
                                    'source': {'macos': mac_text, 'windows': win_text}})
    ordered = {node: sorted(lines, key=lambda x: x['instructionIndex'])
               for node, lines in sorted(scenes.items())}
    for node, lines in ordered.items():
        if len({x['instructionIndex'] for x in lines}) != len(lines):
            raise ValueError(f'duplicate instruction position: {node}')
    if sum(map(len, ordered.values())) != len(a[0]):
        raise ValueError('scene export lost source entries')
    return {'schema': 1, 'builds': context['builds'], 'programSha256': context['programSha256'],
            'sceneCountWithLines': len(ordered), 'sourceLineCount': len(a[0]), 'scenes': ordered,
            'limitations': 'Static grouped source texts; commands, conditions, non-line instructions, complete runtime context and visibility are not included or classified. Do not use as a standalone translation-ready inventory.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    result = export(args.macos_data, args.windows_data)
    # Exclusive creation prevents overwriting an existing source snapshot or game file.
    with args.output.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f"Exported {result['sourceLineCount']} source IDs in {result['sceneCountWithLines']} nodes; further classification required.")


if __name__ == '__main__':
    main()
