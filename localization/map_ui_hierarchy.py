#!/usr/bin/env python3
"""Bind pinned TMP text fields to serialized object ancestry, not visibility."""
import argparse
import json
from pathlib import Path

import UnityPy
import compare_yarn_versions as versions
import dialogue_locale as dl
import ui_locale as ui


WINDOWS_ASSETS = {
    "level0": "55a296caa23347190faa063efdaab4cf5a37e00bdbffa455729b4aa346cddae0",
    "level1": "203725518656d04df3341248a7d24bc27551ebd6c03e582977869f0acfc5a459",
    "level2": "d8b5b6b96a2372e36087edb0a5e3e1fa6ccc2e0d1684698be2221771f02f438e",
    "level3": "2443af34e7c6f2136ca58b0aa712a1c35ce13e60567e963ac7224575fa9d4eb1",
    "level4": "2253e49bca20fa74c12d90eb6c9bd4eadf9ca83f36bcb451f41d7e71fd9bbc28",
    "level5": "ecbae7085b8126e5a77087e1b60a9fb3568032bbae0818106f22640d0242530e",
    "level6": "7312f5011f3222b623e0f06acc5107bcdc72a8487780d9fd5249446fd42be608",
    "sharedassets0.assets": "c8ce3f2e8f52bb5d191c773e6f5f2a4e23d6c6c6ee8893aa7ac7a784cb1c7ac3",
    "sharedassets1.assets": "aff0c9a7b017a4b8cd5fa7ee069fa49331703c54bff9e7a2e398fa04b646d231",
}
WINDOWS_GLOBAL = "910358d16b824bfd4b8398fea8c0295b5660471bb13a6708655096097bb0f018"


def inspect(data, platform):
    data = Path(data)
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    if platform not in ('macos', 'windows'):
        raise ValueError('unsupported platform')
    spec = versions.BUILDS[platform]
    if dl.sha((data / 'globalgamemanagers').read_bytes()) != spec['globalSha256']:
        raise ValueError('unsupported build identity')
    expected_global = ui.GLOBAL_HASH if platform == 'macos' else WINDOWS_GLOBAL
    expected_assets = dict(ui.ASSETS if platform == 'macos' else WINDOWS_ASSETS)
    if dl.sha((data / 'globalgamemanagers.assets').read_bytes()) != expected_global:
        raise ValueError('unsupported global script inventory')
    script_env = UnityPy.load(str(data / 'globalgamemanagers.assets'))
    scripts = {obj.path_id: obj.read() for obj in script_env.objects if obj.type.name == 'MonoScript'}
    result = {}
    for asset in sorted(expected_assets):
        old_global, old_hash = ui.GLOBAL_HASH, ui.ASSETS[asset]
        try:
            ui.GLOBAL_HASH, ui.ASSETS[asset] = expected_global, expected_assets[asset]
            env, rows = ui.scan(data, asset)
        finally:
            ui.GLOBAL_HASH, ui.ASSETS[asset] = old_global, old_hash
        objects = {obj.path_id: obj for obj in env.objects}
        if len(objects) != len(env.objects):
            raise ValueError(f'duplicate object IDs in {asset}')
        transforms, by_game = {}, {}
        for obj in env.objects:
            if obj.type.name not in ('Transform', 'RectTransform'):
                continue
            t = obj.read(check_read=False)
            if t.m_GameObject.m_FileID != 0 or t.m_Father.m_FileID != 0:
                raise ValueError(f'external transform reference: {asset}#{obj.path_id}')
            game_id = t.m_GameObject.m_PathID
            if game_id in by_game:
                raise ValueError(f'multiple transforms: {asset}#{game_id}')
            transforms[obj.path_id] = (game_id, t.m_Father.m_PathID)
            by_game[game_id] = obj.path_id

        def describe_game(game_id):
            obj = objects.get(game_id)
            if obj is None or obj.type.name != 'GameObject':
                raise ValueError(f'missing game object: {asset}#{game_id}')
            game = obj.read()
            components = []
            for pair in game.m_Component:
                ref = pair.component
                if ref.m_FileID != 0 or ref.m_PathID not in objects:
                    raise ValueError(f'external or missing component: {asset}#{game_id}')
                component = objects[ref.m_PathID]
                entry = {'id': ref.m_PathID, 'type': component.type.name}
                if component.type.name == 'MonoBehaviour':
                    head = component.parse_monobehaviour_head()
                    sr = head.m_Script
                    if not 0 < sr.m_FileID <= len(component.assets_file.externals):
                        raise ValueError(f'unresolved script: {asset}#{component.path_id}')
                    owner = component.assets_file.externals[sr.m_FileID-1].path.replace('\\', '/').rsplit('/', 1)[-1].lower()
                    script = scripts.get(sr.m_PathID) if owner == 'globalgamemanagers.assets' else None
                    if script is None:
                        raise ValueError(f'unresolved script: {asset}#{component.path_id}')
                    entry.update({'script': (script.m_Namespace + '.' if script.m_Namespace else '') + script.m_ClassName,
                                  'serializedEnabled': bool(head.m_Enabled)})
                components.append(entry)
            return {'id': game_id, 'name': game.m_Name, 'serializedActive': bool(game.m_IsActive),
                    'components': components}

        for key, (obj, _, text, _) in rows.items():
            owner = obj.parse_monobehaviour_head().m_GameObject
            if owner.m_FileID != 0 or owner.m_PathID not in by_game:
                raise ValueError(f'unresolved text owner: {key}')
            chain, seen, current = [], set(), by_game[owner.m_PathID]
            while current:
                if current in seen or current not in transforms:
                    raise ValueError(f'cyclic or missing transform: {key}')
                seen.add(current)
                game_id, current = transforms[current]
                chain.append(describe_game(game_id))
            if not chain:
                raise ValueError(f'empty hierarchy: {key}')
            result[key] = {'sourceTextSha256': dl.sha(text.encode('utf-8')), 'gameObjectChain': chain}
    return {'schema': 1, 'platform': platform, 'globalScriptAssetSha256': expected_global, 'sourceAssets': expected_assets,
            'objects': result,
            'limitations': 'Serialized hierarchy, active/enabled flags and attached components do not establish runtime visibility, text consumers, scene reachability, canvas order or localization role. Cross-platform identity and semantics require separate comparison.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('source_data', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.source_data, args.platform), ensure_ascii=False, separators=(',', ':')))


if __name__ == '__main__':
    main()
