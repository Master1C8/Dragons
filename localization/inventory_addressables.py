#!/usr/bin/env python3
"""Inspect pinned local Addressables bundles and the English Locale object."""
import argparse
from collections import Counter
import json
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import inventory_text_assets as inventory
import inventory_yarn_bindings as bindings
import settings_locale as settings

COMMON = {'AddressablesLink/link.xml': 'b78c3cbab27ece6465e4bcc4da74f12b070a6e68b2c9ec36838d6f88cfa9842d'}
FILES = {
    'macos': {
        'settings.json': '9f3d6bd6e67eac3ff2fb4437ade10917197594f1664c31c9cdfa7f0efce9ffd8',
        'catalog.bin': '3d7c6f7c9e89b3604293cdead97988638c85edece345682c69b61cf7b283994c',
        'catalog.hash': '1b9ddb598f497b6017ebb58d39bf2eb16603b5560b6991ef75b69a2c57e4ddff',
        'StandaloneOSX/333908e17138c6bc348493caa4a1dab8_monoscripts_e368a6bbd9e65e516f776fec53f7147a.bundle': 'de52ec4cf82ca5d48562830294ba9c10fd173b2a0b11f4765093148490f96c79',
        'StandaloneOSX/localization-locales_assets_all.bundle': '02f8b06d25ed3ff6b73c107fb642d395570eb4373390d04a4109115337ec73d7',
        'StandaloneOSX/unifiedraytracing_assets_all_909468e4da11be4f9133fe65d7bc7304.bundle': '56fad1163d20e72ec1ad5c5cdfa84c4ca9b53c9c4e7e730d99841a6921c9ea18',
    },
    'windows': {
        'settings.json': 'ce0bb681a7e624b7db3df40a631ea89affe0e20387975b264bc2948a1cd376e6',
        'catalog.bin': '3c384566fa98c6c20ba6d790424c97734532fb0be4403822f3a0b629d8b839fa',
        'catalog.hash': '6c17d41c27621743ef111e1282db058c7bb799031e4ae2f7a52cae424161add9',
        'StandaloneWindows64/333908e17138c6bc348493caa4a1dab8_monoscripts_e368a6bbd9e65e516f776fec53f7147a.bundle': 'a900ba604d8f8b3ad8cbf8adc2e0fcf3a3a72f08952ac2653bbd4de096e02ce6',
        'StandaloneWindows64/localization-locales_assets_all.bundle': 'c859f8997d105b84d0ef8cbc3e1849e987f7c30048eea542f031b9124f361723',
        'StandaloneWindows64/unifiedraytracing_assets_all_478cdda9ad8977ca6a223e37a17c1e28.bundle': 'd41a972160df62c90428d9f1e302b4ca14ac09500446af5799f0f73d532c350a',
    },
}


def inspect(root, platform):
    root = Path(root)
    pinned = inventory.inspect(root, platform)
    base = root / 'StreamingAssets' / 'aa'
    expected = {**COMMON, **FILES[platform]}
    files = {p.relative_to(base).as_posix(): p for p in base.rglob('*') if p.is_file()}
    if set(files) != set(expected):
        raise ValueError('Addressables file inventory changed')
    for name, path in files.items():
        if dl.sha(path.read_bytes()) != expected[name]:
            raise ValueError(f'Addressables input changed: {name}')
    config = json.loads(files['settings.json'].read_text(encoding='utf-8'))
    bundles = sorted(name for name in expected if name.endswith('.bundle'))
    summaries = []
    for name in bundles:
        env = UnityPy.load(str(files[name]))
        counts = Counter(obj.type.name for obj in env.objects)
        containers = []
        for obj in env.objects:
            if obj.type.name == 'AssetBundle':
                value = obj.read()
                containers.extend({'path': path, 'fileId': item.asset.m_FileID,
                                   'pathId': item.asset.m_PathID} for path, item in value.m_Container)
        summaries.append({'file': name, 'objectTypes': dict(sorted(counts.items())),
                          'containers': containers})
    env = UnityPy.load(*(str(files[name]) for name in bundles))
    locale = [obj for obj in env.objects if obj.type.name == 'MonoBehaviour']
    if len(locale) != 1 or locale[0].path_id != -1847119570001700535:
        raise ValueError('unexpected locale object inventory')
    obj = locale[0]
    head, script, schema = settings.nodes_for(obj, bindings.generator(root, platform), {})
    if (script.m_AssemblyName, script.m_Namespace, script.m_ClassName) != ('Unity.Localization', 'UnityEngine.Localization', 'Locale'):
        raise ValueError('unexpected locale script')
    tree = obj.read_typetree(nodes=schema, check_read=True)
    settings.check_header(tree, head, obj.path_id)
    if obj.save_typetree(tree, nodes=schema) != obj.get_raw_data():
        raise ValueError('locale object did not round-trip exactly')
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'files': dict(sorted(expected.items())), 'settings': config,
            'bundles': summaries, 'locale': {'objectId': obj.path_id,
                'rawSha256': dl.sha(obj.get_raw_data()), 'fields': tree},
            'limitations': 'Only the pinned local aa directory and decoded bundle objects. The binary catalog is hashed but not decoded; remote or dynamically loaded content, runtime lookup, other StreamingAssets and other resource families are not covered.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data_dir', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
