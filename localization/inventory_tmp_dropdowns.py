#!/usr/bin/env python3
"""Read source-pinned TMP dropdown configuration; no runtime claims."""
import argparse
import json
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import inventory_text_assets as inventory
import inventory_yarn_bindings as bindings
import settings_locale as settings


def inspect(root, platform):
    root = Path(root)
    pinned = inventory.inspect(root, platform)
    generator, cache, records, unresolved = bindings.generator(root, platform), {}, [], []
    for name in sorted(pinned['assets']):
        env = UnityPy.load(str(root / name))
        env.path = str(root)
        for obj in env.objects:
            if obj.type.name != 'MonoBehaviour':
                continue
            try:
                script = obj.parse_monobehaviour_head().m_Script.deref().read()
            except Exception:
                unresolved.append({'asset': name, 'objectId': obj.path_id})
                continue
            if (script.m_Namespace, script.m_ClassName) != ('TMPro', 'TMP_Dropdown'):
                continue
            head, checked_script, schema = settings.nodes_for(obj, generator, cache)
            if (checked_script.m_Namespace, checked_script.m_ClassName) != ('TMPro', 'TMP_Dropdown'):
                raise ValueError('dropdown script identity changed')
            tree = obj.read_typetree(nodes=schema, check_read=True)
            settings.check_header(tree, head, obj.path_id)
            raw = obj.get_raw_data()
            if obj.save_typetree(tree, nodes=schema) != raw:
                raise ValueError(f'dropdown schema failed no-op: {name}#{obj.path_id}')
            mode = tree['m_MultiSelect']
            if mode not in (0, 1):
                raise ValueError('invalid serialized multiselect value')
            records.append({'asset': name, 'objectId': obj.path_id,
                            'rawSha256': dl.sha(raw), 'multiSelect': bool(mode),
                            'value': tree['m_Value'], 'optionCount': len(tree['m_Options']['m_Options']),
                            'captionText': tree['m_CaptionText']})
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'assets': pinned['assets'], 'dropdowns': records, 'unresolvedScripts': unresolved,
            'limitations': 'Serialized TMP_Dropdown components in the 17 pinned files only; runtime instantiation, mutation, localization, and reachability are not established.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=('macos', 'windows'))
    parser.add_argument('data', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.data, args.platform), indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
