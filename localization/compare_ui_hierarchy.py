#!/usr/bin/env python3
"""Compare source-bound TMP object hierarchies in the two game builds."""
import argparse
import json
from pathlib import Path

import map_ui_hierarchy as mapping


def keyed(objects):
    result = {}
    for object_id, record in objects.items():
        asset, separator, path_id = object_id.partition('#')
        if not separator or not asset or not path_id.isdecimal():
            raise ValueError(f'invalid object ID: {object_id}')
        chain = record['gameObjectChain']
        if not chain:
            raise ValueError(f'empty hierarchy: {object_id}')
        path = (asset, tuple(obj['name'] for obj in reversed(chain)))
        if path in result:
            raise ValueError(f'ambiguous same-name hierarchy: {asset}: {path[1]}')
        result[path] = {'id': object_id, 'sourceTextSha256': record['sourceTextSha256']}
    return result


def compare_records(mac, windows):
    a, b = keyed(mac), keyed(windows)
    entries = []
    for asset, path in sorted(a.keys() | b.keys()):
        key = (asset, path)
        left, right = a.get(key), b.get(key)
        entries.append({'asset': asset, 'hierarchy': list(path), 'macos': left, 'windows': right,
                        'sameText': None if left is None or right is None else
                            left['sourceTextSha256'] == right['sourceTextSha256']})
    return entries


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    mac = mapping.inspect(args.macos_data, 'macos')
    win = mapping.inspect(args.windows_data, 'windows')
    entries = compare_records(mac['objects'], win['objects'])
    result = {'schema': 1, 'builds': {'macos': {'globalScriptAssetSha256': mac['globalScriptAssetSha256'],
                                                'sourceAssets': mac['sourceAssets']},
                                      'windows': {'globalScriptAssetSha256': win['globalScriptAssetSha256'],
                                                  'sourceAssets': win['sourceAssets']}},
              'entries': entries,
              'limitations': 'Exact serialized object-name paths and text fingerprints only. Matching paths do not prove equivalent consumers, reachability, visible text or behavior. Unmatched objects remain in scope for their build.'}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
