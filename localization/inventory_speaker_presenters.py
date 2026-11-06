#!/usr/bin/env python3
"""Inventory pinned Yarn line/option presenters and speaker display references."""
import argparse
import json
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import inventory_text_assets as inventory
import inventory_yarn_bindings as bindings
import settings_locale as settings

SELECTED = {('Yarn.Unity', 'LinePresenter'), ('Yarn.Unity', 'OptionsPresenter')}
FIELDS = {
    'LinePresenter': ('lineText', 'showCharacterNameInLine', 'characterNameText', 'characterNameContainer'),
    'OptionsPresenter': ('showsLastLine', 'lastLineText', 'lastLineContainer',
                         'lastLineCharacterNameText', 'lastLineCharacterNameContainer'),
}


def inspect(root, platform):
    root = Path(root)
    pinned = inventory.inspect(root, platform)
    generator, cache, records, unresolved = bindings.generator(root, platform), {}, [], []
    for name in sorted(pinned['assets']):
        env = UnityPy.load(str(root / name))
        env.path = str(root)
        objects = {o.path_id: o for o in env.objects}
        for obj in env.objects:
            if obj.type.name != 'MonoBehaviour':
                continue
            try:
                head = obj.parse_monobehaviour_head()
                script = head.m_Script.deref().read()
            except Exception:
                unresolved.append({'asset': name, 'objectId': obj.path_id})
                continue
            identity = (script.m_Namespace, script.m_ClassName)
            if identity not in SELECTED:
                continue
            head2, script2, schema = settings.nodes_for(obj, generator, cache)
            if (script2.m_Namespace, script2.m_ClassName) != identity:
                raise ValueError(f'presenter script changed: {name}#{obj.path_id}')
            tree = obj.read_typetree(nodes=schema, check_read=True)
            settings.check_header(tree, head2, obj.path_id)
            raw = obj.get_raw_data()
            if obj.save_typetree(tree, nodes=schema) != raw:
                raise ValueError(f'presenter schema failed no-op round-trip: {name}#{obj.path_id}')
            fields = {key: tree[key] for key in FIELDS[script.m_ClassName]}
            targets = {}
            for key, ref in fields.items():
                if not isinstance(ref, dict):
                    continue
                if ref['m_FileID'] != 0:
                    raise ValueError(f'external presenter reference: {name}#{obj.path_id}:{key}')
                target = ref['m_PathID']
                if target and target not in objects:
                    raise ValueError(f'missing presenter reference: {name}#{obj.path_id}:{key}')
                if target and key.endswith('Text'):
                    target_obj = objects[target]
                    if target_obj.type.name != 'MonoBehaviour':
                        raise ValueError(f'unexpected text target type: {name}#{obj.path_id}:{key}')
                    target_script = target_obj.parse_monobehaviour_head().m_Script.deref().read()
                    if (target_script.m_Namespace, target_script.m_ClassName) != ('TMPro', 'TextMeshProUGUI'):
                        raise ValueError(f'unexpected text target script: {name}#{obj.path_id}:{key}')
                    targets[key] = {'objectId': target, 'script': 'TMPro.TextMeshProUGUI',
                                    'rawSha256': dl.sha(target_obj.get_raw_data())}
                elif target:
                    if objects[target].type.name != 'GameObject':
                        raise ValueError(f'unexpected presenter container: {name}#{obj.path_id}:{key}')
                    targets[key] = {'objectId': target, 'type': 'GameObject'}
            records.append({'asset': name, 'objectId': obj.path_id, 'class': script.m_ClassName,
                            'rawSha256': dl.sha(raw), 'fields': fields, 'nonNullTargets': targets})
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'assets': pinned['assets'], 'presenters': records, 'unresolvedScripts': unresolved,
            'limitations': 'Serialized presenter fields in 17 source assets only. Awake can change references, runtime code or other assets may replace presenters, and rendering or event consumers are not established.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data_dir', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
