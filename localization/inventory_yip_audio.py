#!/usr/bin/env python3
"""Trace the pinned level-one Yarn SFX lookup to the serialized yip clip."""
import argparse
from importlib.metadata import version
import json
from pathlib import Path

import UnityPy
import compare_yarn_versions as builds
import dialogue_locale as dl
import inventory_yarn_bindings as bindings
import map_ui_hierarchy as ui_map
import settings_locale as settings
import ui_locale as ui

RESOURCE_SHA = '69c42882282a0f9ed62579ca232970fb5c2834b990e09b99a65aa37c1d11f871'
CLIP_OBJECT_SHA = '878d43a3bc3b3a37301405984de7961b09261cde25dff88ef94f421804964475'
CLIP_DATA_SHA = 'f0c374c547a26c57b0920d1a3527196b637c2a65cd4158564cbb7821322c8514'
EXPECTED_IDS = {'macos': {'scene': 3910, 'clip': 828}, 'windows': {'scene': 3865, 'clip': 821}}


def inspect(root, platform):
    root = Path(root)
    if platform not in EXPECTED_IDS:
        raise ValueError('unsupported platform')
    if version('UnityPy') != '1.25.4' or version('TypeTreeGeneratorAPI') != '0.0.10':
        raise ValueError('unsupported schema tool versions')
    spec = builds.BUILDS[platform]
    global_hash = ui.GLOBAL_HASH if platform == 'macos' else ui_map.WINDOWS_GLOBAL
    scene_hash = ui.ASSETS['level1'] if platform == 'macos' else ui_map.WINDOWS_ASSETS['level1']
    required = {'globalgamemanagers': spec['globalSha256'], 'globalgamemanagers.assets': global_hash,
                'level1': scene_hash, 'sharedassets1.assets': spec['assetSha256'],
                'sharedassets1.resource': RESOURCE_SHA}
    for name, expected in required.items():
        if dl.sha((root / name).read_bytes()) != expected:
            raise ValueError(f'unsupported source: {name}')
    gen = bindings.generator(root, platform)
    env = UnityPy.load(str(root / 'level1'))
    env.path = str(root)
    ids = EXPECTED_IDS[platform]
    matches = [o for o in env.objects if o.path_id == ids['scene'] and o.type.name == 'MonoBehaviour']
    if len(matches) != 1:
        raise ValueError('scene state component missing or ambiguous')
    obj = matches[0]
    head, script, schema = settings.nodes_for(obj, gen, {})
    if (script.m_Namespace, script.m_ClassName) != ('', 'WalkNWashSceneState'):
        raise ValueError('unexpected scene state script')
    tree = obj.read_typetree(nodes=schema, check_read=True)
    settings.check_header(tree, head, obj.path_id)
    if obj.save_typetree(tree, nodes=schema) != obj.get_raw_data():
        raise ValueError('scene state schema failed no-op comparison')
    refs = tree['yarnSFX']
    if len(refs) != 1 or refs[0]['m_PathID'] != ids['clip']:
        raise ValueError('unexpected Yarn sound array')
    ref = refs[0]
    source_asset = bindings.external_name(obj, ref['m_FileID'])
    if source_asset != 'sharedassets1.assets':
        raise ValueError('unexpected sound reference asset')
    assets = UnityPy.load(str(root / source_asset))
    clip_matches = [o for o in assets.objects if o.path_id == ids['clip'] and o.type.name == 'AudioClip']
    if len(clip_matches) != 1:
        raise ValueError('audio clip missing or ambiguous')
    clip_obj = clip_matches[0]
    if dl.sha(clip_obj.get_raw_data()) != CLIP_OBJECT_SHA:
        raise ValueError('audio object fingerprint differs')
    clip = clip_obj.read()
    resource = clip.m_Resource
    if clip.m_Name != 'yip' or resource.m_Source != 'sharedassets1.resource':
        raise ValueError('unexpected audio name or resource')
    payload = (root / resource.m_Source).read_bytes()
    start, length = resource.m_Offset, resource.m_Size
    if start < 0 or length <= 0 or start + length > len(payload):
        raise ValueError('invalid audio resource range')
    segment_hash = dl.sha(payload[start:start+length])
    if segment_hash != CLIP_DATA_SHA:
        raise ValueError('audio resource segment differs')
    return {'schema': 1, 'platform': platform, 'buildVersion': spec['version'],
            'sourceHashes': required, 'sceneComponentId': obj.path_id,
            'sceneComponentSha256': dl.sha(obj.get_raw_data()),
            'yarnSfxReference': {'fileId': ref['m_FileID'], 'pathId': ref['m_PathID'], 'asset': source_asset},
            'clip': {'name': clip.m_Name, 'type': clip_obj.type.name, 'objectSha256': CLIP_OBJECT_SHA,
                     'resource': resource.m_Source, 'offset': start, 'length': length,
                     'encodedBytesSha256': segment_hash},
            'limitations': 'Serialized level1 lookup and pinned audio bytes only. No sound decoding, playback, other scenes, dynamic replacement, reachability or translated-audio decision is established.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=EXPECTED_IDS)
    p.add_argument('data_dir', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
