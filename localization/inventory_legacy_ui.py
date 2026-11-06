#!/usr/bin/env python3
"""Export source-pinned legacy Unity UI Text fields for classification."""
import argparse
from collections import Counter
import json
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import inventory_text_assets as inventory
import inventory_yarn_bindings as bindings
import settings_locale as settings


def hierarchy(game_id, transforms, names):
    chain, seen = [], set()
    while game_id:
        if game_id in seen or game_id not in transforms or game_id not in names:
            raise ValueError(f'broken or cyclic GameObject hierarchy: {game_id}')
        seen.add(game_id)
        chain.append(names[game_id])
        game_id = transforms[game_id]
    return list(reversed(chain))


def inspect(root, platform):
    root = Path(root)
    pinned = inventory.inspect(root, platform)
    gen = bindings.generator(root, platform)
    cache, records, unresolved = {}, [], []
    for name in sorted(pinned['assets']):
        env = UnityPy.load(str(root / name))
        env.path = str(root)
        transforms, names, pending = {}, {}, []
        for obj in env.objects:
            if obj.type.name == 'GameObject':
                names[obj.path_id] = obj.read().m_Name
            elif obj.type.name in ('Transform', 'RectTransform'):
                t = obj.read(check_read=False)
                if t.m_GameObject.m_FileID or (t.m_Father.m_FileID and t.m_Father.m_PathID):
                    raise ValueError(f'external transform reference: {name}#{obj.path_id}')
                pending.append((t.m_GameObject.m_PathID, t.m_Father.m_PathID))
        transform_game = {obj.path_id: obj.read(check_read=False).m_GameObject.m_PathID
                          for obj in env.objects if obj.type.name in ('Transform', 'RectTransform')}
        for game_id, father in pending:
            if game_id in transforms or (father and father not in transform_game):
                raise ValueError(f'ambiguous transform hierarchy: {name}#{game_id}')
            transforms[game_id] = transform_game.get(father, 0)
        for obj in env.objects:
            if obj.type.name != 'MonoBehaviour':
                continue
            head = obj.parse_monobehaviour_head()
            try:
                script = head.m_Script.deref().read()
            except Exception:
                unresolved.append(f'{name}#{obj.path_id}')
                continue
            if (script.m_Namespace, script.m_ClassName) != ('UnityEngine.UI', 'Text'):
                continue
            if head.m_GameObject.m_FileID:
                raise ValueError(f'external text GameObject: {name}#{obj.path_id}')
            checked_head, checked_script, schema = settings.nodes_for(obj, gen, cache)
            if (checked_script.m_Namespace, checked_script.m_ClassName) != ('UnityEngine.UI', 'Text'):
                raise ValueError('script identity changed during decoding')
            tree = obj.read_typetree(nodes=schema, check_read=True)
            settings.check_header(tree, checked_head, obj.path_id)
            raw = obj.get_raw_data()
            if obj.save_typetree(tree, nodes=schema) != raw or not isinstance(tree['m_Text'], str):
                raise ValueError(f'text object failed exact schema round-trip: {name}#{obj.path_id}')
            records.append({'asset': name, 'objectId': obj.path_id,
                            'gameObjectId': head.m_GameObject.m_PathID,
                            'hierarchy': hierarchy(head.m_GameObject.m_PathID, transforms, names),
                            'rawSha256': dl.sha(raw), 'text': tree['m_Text'],
                            'textSha256': dl.sha(tree['m_Text'].encode('utf-8'))})
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'assets': pinned['assets'], 'entries': records, 'unresolvedScripts': unresolved,
            'rootCounts': dict(sorted(Counter(r['hierarchy'][0] for r in records).items())),
            'limitations': 'Static legacy UI Text fields only; ancestry and serialized text do not prove runtime reachability or whether code replaces a value. Other classes, dynamic text, bundles and excluded textures need separate classification.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data_dir', type=Path)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    result = inspect(args.data_dir, args.platform)
    with args.output.open('x', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f"Exported {len(result['entries'])} entries; unresolved script references: {len(result['unresolvedScripts'])}")


if __name__ == '__main__':
    main()
