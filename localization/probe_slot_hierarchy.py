#!/usr/bin/env python3
"""Trace the pinned new-game slot controls to their serialized hierarchy."""
import argparse
import json
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import settings_locale as settings
import ui_locale as ui


def inspect(data):
    data = Path(data)
    if dl.sha((data / 'level0').read_bytes()) != ui.ASSETS['level0']:
        raise ValueError('unsupported level0 source')
    if dl.sha((data / 'globalgamemanagers.assets').read_bytes()) != ui.GLOBAL_HASH:
        raise ValueError('unsupported script inventory')
    generator = settings.make_generator(data)
    env = UnityPy.load(str(data / 'level0'))
    env.path = str(data)
    objects = {obj.path_id: obj for obj in env.objects}
    if len(objects) != len(env.objects):
        raise ValueError('duplicate serialized object ID')
    scripts = UnityPy.load(str(data / 'globalgamemanagers.assets'))
    scripts = {obj.path_id: obj.read() for obj in scripts.objects if obj.type.name == 'MonoScript'}
    candidates = []
    for obj in env.objects:
        if obj.type.name != 'MonoBehaviour':
            continue
        head = obj.parse_monobehaviour_head()
        ref = head.m_Script
        if ref.m_FileID <= 0 or ref.m_FileID > len(obj.assets_file.externals):
            continue
        owner = obj.assets_file.externals[ref.m_FileID - 1].path.replace('\\', '/').rsplit('/', 1)[-1].lower()
        if owner == 'globalgamemanagers.assets' and ref.m_PathID in scripts and scripts[ref.m_PathID].m_ClassName == 'MenuSlotsNew':
            candidates.append(obj)
    if len(candidates) != 1:
        raise ValueError('unexpected new-slot component count')
    obj = candidates[0]
    head, script, schema = settings.nodes_for(obj, generator, {})
    if script.m_ClassName != 'MenuSlotsNew':
        raise ValueError('unexpected script identity')
    tree = obj.read_typetree(nodes=schema, check_read=True)
    settings.check_header(tree, head, obj.path_id)
    if obj.save_typetree(tree, nodes=schema) != obj.get_raw_data():
        raise ValueError('slot component schema failed no-op byte comparison')
    transforms, by_game = {}, {}
    for component in env.objects:
        if component.type.name not in ('Transform', 'RectTransform'):
            continue
        value = component.read(check_read=False)
        if value.m_GameObject.m_FileID != 0 or value.m_Father.m_FileID != 0:
            raise ValueError('external transform reference')
        game_id = value.m_GameObject.m_PathID
        if game_id in by_game:
            raise ValueError('multiple transforms on one game object')
        transforms[component.path_id] = (game_id, value.m_Father.m_PathID)
        by_game[game_id] = component.path_id

    def hierarchy(ref):
        if ref['m_FileID'] != 0 or ref['m_PathID'] not in objects:
            raise ValueError('unexpected slot field reference')
        component = objects[ref['m_PathID']]
        if component.type.name != 'MonoBehaviour':
            raise ValueError('slot field does not refer to a component')
        owner = component.parse_monobehaviour_head().m_GameObject
        if owner.m_FileID != 0 or owner.m_PathID not in by_game:
            raise ValueError('unexpected component owner')
        current, seen, chain = by_game[owner.m_PathID], set(), []
        while current:
            if current in seen or current not in transforms:
                raise ValueError('unresolved or cyclic hierarchy')
            seen.add(current)
            game_id, current = transforms[current]
            game = objects[game_id]
            if game.type.name != 'GameObject':
                raise ValueError('transform owner is not a game object')
            value = game.read()
            chain.append({'id': game_id, 'name': value.m_Name, 'serializedActive': value.m_IsActive})
        return {'componentId': ref['m_PathID'], 'gameObjectChain': chain}

    fields = {}
    for n in range(1, 4):
        for suffix in ('Button', 'DeleteButton', 'Progress'):
            name = f'slot{n}{suffix}'
            fields[name] = hierarchy(tree[name])
    return {'schema': 1, 'level0Sha256': ui.ASSETS['level0'],
            'globalScriptAssetSha256': ui.GLOBAL_HASH, 'componentId': obj.path_id,
            'fields': fields,
            'limitations': 'Serialized ancestry and initial active flags alone do not prove runtime visibility, canvas order, alpha, or accessibility.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_data', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.source_data.resolve(strict=True)), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
