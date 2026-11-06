#!/usr/bin/env python3
"""Inventory TextAsset payloads and TMP line-break bindings in pinned builds."""
import argparse
import json
from pathlib import Path

import UnityPy
import compare_yarn_versions as versions
import dialogue_locale as dl
import inventory_extra_assets as extra
import inventory_yarn_bindings as bindings
import map_ui_hierarchy as ui_map
import settings_locale as settings
import ui_locale as ui

EXPECTED = {19: 'PerformanceTestRunSettings', 20: 'LineBreaking Leading Characters',
            21: 'PerformanceTestRunInfo', 22: 'LineBreaking Following Characters'}


def parse_text_asset(raw):
    name, p = dl.read_string(raw, 0)
    value, end = dl.read_string(raw, p)
    if end != len(raw) or dl.write_string(name) + dl.write_string(value) != raw:
        raise ValueError('TextAsset did not round-trip exactly')
    return name, value


def inspect(root, platform):
    root = Path(root)
    if platform not in ('macos', 'windows') or UnityPy.__version__ != '1.25.4':
        raise ValueError('unsupported platform or UnityPy version')
    spec = versions.BUILDS[platform]
    global_scripts = ui.GLOBAL_HASH if platform == 'macos' else ui_map.WINDOWS_GLOBAL
    assets = dict(ui.ASSETS if platform == 'macos' else ui_map.WINDOWS_ASSETS)
    assets.update({n: h for n, h in extra.EXPECTED['mac' if platform == 'macos' else 'windows'].items()
                   if n.startswith('sharedassets')})
    assets['resources.assets'] = bindings.RESOURCES[platform]
    assets['globalgamemanagers.assets'] = global_scripts
    assets['globalgamemanagers'] = spec['globalSha256']
    for name, expected in assets.items():
        if dl.sha((root / name).read_bytes()) != expected:
            raise ValueError(f'unsupported source: {name}')
    records = []
    for name in sorted(assets):
        env = UnityPy.load(str(root / name))
        if len({o.path_id for o in env.objects}) != len(env.objects):
            raise ValueError(f'duplicate object IDs: {name}')
        for obj in env.objects:
            if obj.type.name != 'TextAsset':
                continue
            raw = obj.get_raw_data()
            object_name, value = parse_text_asset(raw)
            read = obj.read()
            if (object_name, value) != (read.m_Name, read.m_Script):
                raise ValueError(f'TextAsset reader mismatch: {name}#{obj.path_id}')
            role = ('line-break-configuration' if name == 'resources.assets' and obj.path_id in (20, 22)
                    else 'diagnostic-metadata-needs-consumer-review')
            records.append({'asset': name, 'objectId': obj.path_id, 'name': object_name,
                            'rawSha256': dl.sha(raw), 'payloadSha256': dl.sha(value.encode('utf-8')),
                            'payloadBytes': len(value.encode('utf-8')), 'provisionalRole': role,
                            'preserveExactly': True})
    identities = {(r['asset'], r['objectId']): r['name'] for r in records}
    if identities != {('resources.assets', i): n for i, n in EXPECTED.items()}:
        raise ValueError('unexpected TextAsset inventory')
    env = UnityPy.load(str(root / 'resources.assets'))
    env.path = str(root)
    matches = [o for o in env.objects if o.path_id == 1388 and o.type.name == 'MonoBehaviour']
    if len(matches) != 1:
        raise ValueError('TMP Settings object missing or ambiguous')
    obj = matches[0]
    gen = bindings.generator(root, platform)
    head, script, schema = settings.nodes_for(obj, gen, {})
    if (script.m_Namespace, script.m_ClassName, head.m_Name) != ('TMPro', 'TMP_Settings', 'TMP Settings'):
        raise ValueError('unexpected TMP Settings script or name')
    tree = obj.read_typetree(nodes=schema, check_read=True)
    settings.check_header(tree, head, obj.path_id)
    if obj.save_typetree(tree, nodes=schema) != obj.get_raw_data():
        raise ValueError('TMP Settings schema failed exact round-trip')
    leading, following = tree['m_leadingCharacters'], tree['m_followingCharacters']
    if leading != {'m_FileID': 0, 'm_PathID': 20} or following != {'m_FileID': 0, 'm_PathID': 22}:
        raise ValueError('unexpected TMP line-break resource references')
    return {'schema': 1, 'platform': platform, 'buildVersion': spec['version'], 'assets': assets,
            'textAssets': sorted(records, key=lambda x: (x['asset'], x['objectId'])),
            'tmpSettings': {'asset': 'resources.assets', 'objectId': obj.path_id,
                            'rawSha256': dl.sha(obj.get_raw_data()), 'leading': leading, 'following': following,
                            'modernHangulRule': bool(tree['m_UseModernHangulLineBreakingRules'])},
            'limitations': 'Only TextAsset objects in these seventeen serialized assets. Runtime use, diagnostic metadata consumers, managed strings, streaming/addressable contents and other resource types need separate review.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data_dir', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
