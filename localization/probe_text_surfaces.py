#!/usr/bin/env python3
"""Count selected text component types in pinned macOS assets, without extracting text."""
import argparse
from collections import Counter
import json
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import ui_locale as ui

RESOURCE_HASH = 'fd20278f865e51fba3c1a922777031afb2a5d2d00fc10ee682296e32cc071974'
SELECTED = {
    ('TMPro', 'TextMeshProUGUI'), ('TMPro', 'TextMeshPro'),
    ('UnityEngine.UI', 'Text'),
    ('UnityEngine.Localization.Components', 'LocalizeStringEvent'),
    ('UnityScriptableSettings', 'ScriptableSettingSpawner'),
}


def inspect(data):
    data = Path(data)
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    if dl.sha((data / 'globalgamemanagers.assets').read_bytes()) != ui.GLOBAL_HASH:
        raise ValueError('unsupported script inventory')
    expected = {'resources.assets': RESOURCE_HASH, **ui.ASSETS}
    for name, digest in expected.items():
        if dl.sha((data / name).read_bytes()) != digest:
            raise ValueError(f'unsupported source asset: {name}')
    scripts_env = UnityPy.load(str(data / 'globalgamemanagers.assets'))
    scripts = {o.path_id: o.read() for o in scripts_env.objects if o.type.name == 'MonoScript'}
    result = {}
    for name in sorted(expected):
        env = UnityPy.load(str(data / name))
        env.path = str(data)
        objects = {o.path_id: o for o in env.objects}
        if len(objects) != len(env.objects):
            raise ValueError(f'duplicate object ID in {name}')
        counts, unresolved, legacy, transforms, game_to_transform = Counter(), 0, [], {}, {}
        for obj in env.objects:
            if obj.type.name in ('Transform', 'RectTransform') and name == 'resources.assets':
                t = obj.read(check_read=False)
                if t.m_GameObject.m_FileID != 0 or (t.m_Father.m_FileID != 0 and t.m_Father.m_PathID):
                    raise ValueError('external transform reference in legacy resource probe')
                transforms[obj.path_id] = (t.m_GameObject.m_PathID, t.m_Father.m_PathID)
                if t.m_GameObject.m_PathID in game_to_transform:
                    raise ValueError('multiple transforms on one object')
                game_to_transform[t.m_GameObject.m_PathID] = obj.path_id
            if obj.type.name == 'TextMesh':
                counts['UnityEngine.TextMesh'] += 1
            if obj.type.name != 'MonoBehaviour':
                continue
            head = obj.parse_monobehaviour_head()
            ref = head.m_Script
            if ref.m_FileID <= 0 or ref.m_FileID > len(obj.assets_file.externals):
                unresolved += 1
                continue
            owner = obj.assets_file.externals[ref.m_FileID - 1].path.replace('\\', '/').rsplit('/', 1)[-1].lower()
            if owner != 'globalgamemanagers.assets' or ref.m_PathID not in scripts:
                unresolved += 1
                continue
            script = scripts[ref.m_PathID]
            key = (script.m_Namespace, script.m_ClassName)
            if key in SELECTED:
                counts['.'.join(key)] += 1
                if key == ('UnityEngine.UI', 'Text') and name == 'resources.assets':
                    legacy.append((obj.path_id, head.m_GameObject.m_PathID))
        roots, missing = Counter(), []
        for path_id, game_id in legacy:
            current = game_to_transform.get(game_id)
            visited, chain = set(), []
            while current in transforms and current not in visited:
                visited.add(current)
                game_id, current = transforms[current]
                game = objects.get(game_id)
                if game is None or game.type.name != 'GameObject':
                    break
                chain.append(game.read().m_Name)
            if not chain or current:
                missing.append(path_id)
            else:
                roots[chain[-1]] += 1
        result[name] = {'sourceSha256': expected[name], 'selectedComponentCounts': dict(sorted(counts.items())),
                        'unresolvedScriptReferences': unresolved}
        if name == 'resources.assets':
            result[name]['legacyTextRootNames'] = dict(sorted(roots.items()))
            result[name]['legacyTextUnresolvedHierarchyIds'] = sorted(missing)
    return {'schema': 1, 'globalScriptAssetSha256': ui.GLOBAL_HASH, 'assets': result,
            'limitations': 'Only selected component classes in these pinned serialized assets were counted. Resource presence and DebugUI ancestry do not prove runtime reachability. Addressables, code-generated strings, other classes and texture text were not inventoried.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_data', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.source_data.resolve(strict=True)), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
