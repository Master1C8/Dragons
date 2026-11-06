#!/usr/bin/env python3
"""Bind serialized version components to their colocated TMP text fields."""
import argparse
import json
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import inventory_text_assets as inventory
import settings_locale as settings
import inventory_yarn_bindings as bindings


def inspect(root, platform):
    root = Path(root)
    pinned = inventory.inspect(root, platform)
    generator, cache, rows, unresolved = bindings.generator(root, platform), {}, [], []
    for name in sorted(pinned['assets']):
        env = UnityPy.load(str(root / name))
        env.path = str(root)
        objects = {obj.path_id: obj for obj in env.objects}
        if len(objects) != len(env.objects):
            raise ValueError('duplicate serialized object identity')
        for obj in env.objects:
            if obj.type.name != 'MonoBehaviour':
                continue
            try:
                head = obj.parse_monobehaviour_head()
                script = head.m_Script.deref().read()
            except Exception:
                unresolved.append({'asset': name, 'objectId': obj.path_id})
                continue
            if (script.m_Namespace, script.m_ClassName) != ('', 'VersionNumber'):
                continue
            head, verified, schema = settings.nodes_for(obj, generator, cache)
            tree = obj.read_typetree(nodes=schema, check_read=True)
            settings.check_header(tree, head, obj.path_id)
            if obj.save_typetree(tree, nodes=schema) != obj.get_raw_data():
                raise ValueError('version component no-op serialization failed')
            ref = tree['m_GameObject']
            if ref['m_FileID'] != 0 or ref['m_PathID'] not in objects:
                raise ValueError('version component has unresolved GameObject')
            go = objects[ref['m_PathID']].read()
            text_components = []
            for entry in go.m_Component:
                pointer = entry.component
                if pointer.m_FileID != 0 or pointer.m_PathID not in objects:
                    raise ValueError('external or missing GameObject component')
                component = objects[pointer.m_PathID]
                if component.type.name != 'MonoBehaviour':
                    continue
                text_head = component.parse_monobehaviour_head()
                text_script = text_head.m_Script.deref().read()
                if (text_script.m_Namespace, text_script.m_ClassName) not in (('TMPro', 'TextMeshProUGUI'), ('TMPro', 'TextMeshPro')):
                    continue
                header, _, text_schema = settings.nodes_for(component, generator, cache)
                data = component.read_typetree(nodes=text_schema, check_read=True)
                settings.check_header(data, header, component.path_id)
                if component.save_typetree(data, nodes=text_schema) != component.get_raw_data():
                    raise ValueError('text component no-op serialization failed')
                text_components.append({'objectId': component.path_id,
                                        'class': text_script.m_ClassName,
                                        'textSha256': dl.sha(data['m_text'].encode('utf-8')),
                                        'rawSha256': dl.sha(component.get_raw_data())})
            if len(text_components) != 1:
                raise ValueError(f'ambiguous colocated TMP text: {name}#{obj.path_id}')
            rows.append({'asset': name, 'componentId': obj.path_id,
                         'gameObjectId': ref['m_PathID'], 'gameObjectName': go.m_Name,
                         'componentRawSha256': dl.sha(obj.get_raw_data()), 'text': text_components[0]})
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'assets': pinned['assets'], 'versionDisplays': rows, 'unresolvedScripts': unresolved,
            'limitations': 'Colocated serialized components only. GetComponent resolution, execution timing, runtime mutation and visibility remain unverified.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.data, args.platform), indent=2))


if __name__ == '__main__':
    main()
