#!/usr/bin/env python3
"""Scan pinned serialized assets for objective displays and 3D TMP text."""
import argparse
import json
from pathlib import Path

import UnityPy
import inventory_text_assets as inventory

TARGETS = {('', 'ObjectiveDisplay'), ('', 'ObjectiveManager'), ('TMPro', 'TextMeshPro')}


def selected(namespace, name):
    return (namespace, name) in TARGETS


def inspect(root, platform):
    root = Path(root)
    pinned = inventory.inspect(root, platform)
    matches, unresolved = [], []
    for name in sorted(pinned['assets']):
        env = UnityPy.load(str(root / name))
        env.path = str(root)
        for obj in env.objects:
            if obj.type.name != 'MonoBehaviour':
                continue
            try:
                head = obj.parse_monobehaviour_head()
                script = head.m_Script.deref().read()
            except Exception:
                unresolved.append({'asset': name, 'objectId': obj.path_id})
                continue
            if selected(script.m_Namespace, script.m_ClassName):
                matches.append({'asset': name, 'objectId': obj.path_id,
                                'namespace': script.m_Namespace, 'class': script.m_ClassName})
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'assets': pinned['assets'], 'matches': matches, 'unresolvedScriptReferences': unresolved,
            'limitations': 'Only three selected script identities in these 17 serialized files. Other bundles, dynamic creation, subclasses, non-MonoBehaviour text and runtime visibility remain unexamined.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data_dir', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
