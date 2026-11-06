#!/usr/bin/env python3
"""Verify exact TextAsset preservation and line-break references in a game copy."""
import argparse
import json
from pathlib import Path

import UnityPy
import inventory_text_assets as inventory
import inventory_yarn_bindings as bindings
import settings_locale as settings


def snapshot(root, names):
    root = Path(root)
    out = {}
    for name in sorted(names):
        env = UnityPy.load(str(root / name))
        if len({o.path_id for o in env.objects}) != len(env.objects):
            raise ValueError(f'duplicate object IDs: {name}')
        for obj in env.objects:
            if obj.type.name != 'TextAsset':
                continue
            key = f'{name}#{obj.path_id}'
            if key in out:
                raise ValueError(f'duplicate TextAsset identity: {key}')
            raw = obj.get_raw_data()
            inventory.parse_text_asset(raw)
            out[key] = raw
    return out


def compare_snapshots(source, result):
    if source.keys() != result.keys():
        missing = sorted(source.keys() - result.keys())
        extra = sorted(result.keys() - source.keys())
        raise ValueError(f'TextAsset identity mismatch: missing={missing}, extra={extra}')
    for key, raw in source.items():
        if result[key] != raw:
            raise ValueError(f'preserve-exact mismatch: {key}')


def verify(source_data, result_data, platform):
    source_root = Path(source_data).resolve(strict=True)
    result_root = Path(result_data).resolve(strict=True)
    if source_root == result_root:
        raise ValueError('result must be a separate game data directory')
    source = inventory.inspect(source_root, platform)
    before = snapshot(source_root, source['assets'])
    after = snapshot(result_root, source['assets'])
    compare_snapshots(before, after)
    env = UnityPy.load(str(result_root / 'resources.assets'))
    env.path = str(result_root)
    matches = [o for o in env.objects if o.path_id == 1388 and o.type.name == 'MonoBehaviour']
    if len(matches) != 1:
        raise ValueError('result TMP Settings object missing or ambiguous')
    obj = matches[0]
    gen = bindings.generator(source_root, platform)
    head, script, schema = settings.nodes_for(obj, gen, {})
    if (script.m_Namespace, script.m_ClassName, head.m_Name) != ('TMPro', 'TMP_Settings', 'TMP Settings'):
        raise ValueError('unexpected result TMP Settings script or name')
    tree = obj.read_typetree(nodes=schema, check_read=True)
    settings.check_header(tree, head, obj.path_id)
    if obj.save_typetree(tree, nodes=schema) != obj.get_raw_data():
        raise ValueError('result TMP Settings failed no-op round-trip')
    if tree['m_leadingCharacters'] != source['tmpSettings']['leading'] or tree['m_followingCharacters'] != source['tmpSettings']['following']:
        raise ValueError('TMP line-break references changed')
    if bool(tree['m_UseModernHangulLineBreakingRules']) != source['tmpSettings']['modernHangulRule']:
        raise ValueError('TMP line-break mode changed')
    return {'platform': platform, 'comparedAssets': len(source['assets']),
            'exactTextAssets': len(before), 'lineBreakReferences': 'unchanged', 'lineBreakMode': 'unchanged',
            'limitations': 'Only TextAsset objects, two TMP Settings references and line-break mode in these selected assets. Other protected values, language content, rendering, runtime and packaging require separate validation.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('source_data', type=Path)
    p.add_argument('result_data', type=Path)
    args = p.parse_args()
    print(json.dumps(verify(args.source_data, args.result_data, args.platform), ensure_ascii=False))


if __name__ == '__main__':
    main()
