#!/usr/bin/env python3
"""Inventory selected text-bearing object classes in five pinned Unity assets.

This is a discovery probe, not a complete text or reachability classifier.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import UnityPy

EXPECTED = {
    'mac': {
        'globalgamemanagers.assets': '391640e8e7df097a0d377c7a16552975d4821688841ea3460ec99587f4061d9e',
        'sharedassets2.assets': '82300da2892d572a7dac2602489874c130e93cd093112450dc1c03948c15872e',
        'sharedassets3.assets': '22f6f6316b9ff73a5ff3042b82ada4af70fc80ce24a02f26d69b613f0a18d158',
        'sharedassets4.assets': '00f71e4e71abefa25cd13cb9d99f5678e7b257ece9910c7face27a56d37ad8f7',
        'sharedassets5.assets': 'ffdfdeeeb4f793e6cc2425810f182a322e8bf41da7dfac32dddda1aab1bbd9a1',
        'sharedassets6.assets': '38f5e76e01b5f5bae985b7c7b45477ff1888ec7a62265b2393911e59dcceaffc',
    },
    'windows': {
        'globalgamemanagers.assets': '910358d16b824bfd4b8398fea8c0295b5660471bb13a6708655096097bb0f018',
        'sharedassets2.assets': '53589194e2754251d918167309117c038e4e0f9acd0e3c571940c979a6d73f7b',
        'sharedassets3.assets': '87cbffdff5f7018d80f54df3eecf39f4b73f048dcfd4dca6a09a8e64b5d24ded',
        'sharedassets4.assets': '0d055aac49c3344a50e68632b197d6c5fce701a8236a55a90d620b38978b8681',
        'sharedassets5.assets': 'a95e106be4a3fe2438a7b12e43f14d3d5efa4ce0d32fc20209e634657587c2b9',
        'sharedassets6.assets': '11becb0784a1fbd113181c918937ecb7df0701bd6422ef4e04f610626aa1a169',
    },
}
SELECTED = {('TMPro', 'TextMeshProUGUI'), ('TMPro', 'TextMeshPro'),
            ('UnityEngine.UI', 'Text'),
            ('UnityEngine.Localization.Components', 'LocalizeStringEvent'),
            ('UnityScriptableSettings', 'ScriptableSettingSpawner')}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(root, platform):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    root = Path(root)
    for name, expected in EXPECTED[platform].items():
        if digest(root / name) != expected:
            raise ValueError(f'unsupported or modified source: {name}')
    global_env = UnityPy.load(str(root / 'globalgamemanagers.assets'))
    scripts = {obj.path_id: obj.read() for obj in global_env.objects if obj.type.name == 'MonoScript'}
    assets = {}
    for name in sorted(EXPECTED[platform]):
        if name == 'globalgamemanagers.assets':
            continue
        env = UnityPy.load(str(root / name))
        if len({obj.path_id for obj in env.objects}) != len(env.objects):
            raise ValueError(f'duplicate object identifiers: {name}')
        counts, selected, unresolved = Counter(), Counter(), []
        for obj in env.objects:
            counts[obj.type.name] += 1
            if obj.type.name != 'MonoBehaviour':
                continue
            ref = obj.parse_monobehaviour_head().m_Script
            if not 0 < ref.m_FileID <= len(obj.assets_file.externals):
                unresolved.append(obj.path_id)
                continue
            owner = obj.assets_file.externals[ref.m_FileID - 1].path.replace('\\', '/').rsplit('/', 1)[-1].lower()
            script = scripts.get(ref.m_PathID) if owner == 'globalgamemanagers.assets' else None
            if script is None:
                unresolved.append(obj.path_id)
                continue
            key = (script.m_Namespace, script.m_ClassName)
            if key in SELECTED:
                selected['.'.join(key)] += 1
        assets[name] = {'sha256': EXPECTED[platform][name], 'objectCounts': dict(sorted(counts.items())),
                        'selectedComponentCounts': dict(sorted(selected.items())),
                        'unresolvedScriptReferenceIds': sorted(unresolved)}
    return {'schema': 1, 'platform': platform,
            'globalScriptAssetSha256': EXPECTED[platform]['globalgamemanagers.assets'],
            'unityPyVersion': UnityPy.__version__, 'assets': assets,
            'limitations': 'Selected classes and serialized object types only. Other MonoBehaviour fields, dynamic and generated text, texture text, runtime reachability and other asset families are not classified.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=EXPECTED)
    parser.add_argument('data_dir', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
