#!/usr/bin/env python3
"""Inventory Yarn projects and DialogueRunner bindings in pinned serialized assets."""
import argparse
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path

import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
import compare_yarn_versions as builds
import dialogue_locale as dl
import inventory_extra_assets as extra
import map_ui_hierarchy as ui_map
import probe_windows_slot_font as windows_fonts
import settings_locale as settings
import ui_locale as ui

RESOURCES = {'macos': 'fd20278f865e51fba3c1a922777031afb2a5d2d00fc10ee682296e32cc071974',
             'windows': 'e48266e661438a4186de78f4aad660707c57b511153dd6199f293b503f958ae8'}
TARGETS = {('Yarn.Unity', 'YarnProject'), ('Yarn.Unity', 'DialogueRunner')}


def generator(data, platform):
    if platform == 'macos':
        return settings.make_generator(data)
    inputs = [(p.name, p.read_bytes()) for p in sorted((data / 'Managed').glob('*.dll'))
              if not p.name.startswith('Yarn.')]
    manifest = [[name, dl.sha(raw)] for name, raw in inputs]
    if sha256(json.dumps(manifest, separators=(',', ':')).encode()).hexdigest() != windows_fonts.MANAGED_HASH:
        raise ValueError('unsupported Windows managed schema inputs')
    gen = TypeTreeGenerator('6000.3.14f1')
    for _, raw in inputs:
        gen.load_dll(raw)
    return gen


def external_name(obj, file_id):
    if file_id <= 0 or file_id > len(obj.assets_file.externals):
        raise ValueError(f'invalid external reference: {obj.path_id}')
    return obj.assets_file.externals[file_id - 1].path.replace('\\', '/').rsplit('/', 1)[-1]


def inspect(root, platform):
    root = Path(root)
    if platform not in ('macos', 'windows'):
        raise ValueError('unsupported platform')
    if version('UnityPy') != '1.25.4' or version('TypeTreeGeneratorAPI') != '0.0.10':
        raise ValueError('unsupported schema tool versions')
    spec = builds.BUILDS[platform]
    if dl.sha((root / 'globalgamemanagers').read_bytes()) != spec['globalSha256']:
        raise ValueError('unsupported build identity')
    hashes = dict(ui.ASSETS if platform == 'macos' else ui_map.WINDOWS_ASSETS)
    hashes.update({k: v for k, v in extra.EXPECTED['mac' if platform == 'macos' else 'windows'].items()
                   if k.startswith('sharedassets')})
    hashes['resources.assets'] = RESOURCES[platform]
    global_hash = ui.GLOBAL_HASH if platform == 'macos' else ui_map.WINDOWS_GLOBAL
    if dl.sha((root / 'globalgamemanagers.assets').read_bytes()) != global_hash:
        raise ValueError('unsupported global script inventory')
    for name, expected in hashes.items():
        if dl.sha((root / name).read_bytes()) != expected:
            raise ValueError(f'unsupported asset: {name}')
    scripts_env = UnityPy.load(str(root / 'globalgamemanagers.assets'))
    scripts = {o.path_id: o.read() for o in scripts_env.objects if o.type.name == 'MonoScript'}
    target_scripts = {o.path_id: (o.read().m_Namespace, o.read().m_ClassName)
                      for o in scripts_env.objects if o.type.name == 'MonoScript'
                      and (o.read().m_Namespace, o.read().m_ClassName) in TARGETS}
    if len(target_scripts) != len(TARGETS) or set(target_scripts.values()) != TARGETS:
        raise ValueError('unexpected Yarn script identity inventory')
    gen = generator(root, platform)
    cache, projects, runners = {}, [], []
    unresolved = []
    for name in sorted(hashes):
        env = UnityPy.load(str(root / name))
        env.path = str(root)
        if len({o.path_id for o in env.objects}) != len(env.objects):
            raise ValueError(f'duplicate object IDs: {name}')
        for obj in env.objects:
            if obj.type.name != 'MonoBehaviour':
                continue
            head = obj.parse_monobehaviour_head()
            ref = head.m_Script
            try:
                owner = external_name(obj, ref.m_FileID).lower()
            except ValueError:
                unresolved.append(f'{name}#{obj.path_id}')
                continue
            script = scripts.get(ref.m_PathID) if owner == 'globalgamemanagers.assets' else None
            if script is None:
                unresolved.append(f'{name}#{obj.path_id}')
                continue
            identity = (script.m_Namespace, script.m_ClassName)
            if identity not in TARGETS:
                continue
            row = {'asset': name, 'objectId': obj.path_id, 'rawSha256': dl.sha(obj.get_raw_data()),
                   'objectName': head.m_Name, 'gameObjectFileId': head.m_GameObject.m_FileID,
                   'gameObjectId': head.m_GameObject.m_PathID}
            if identity[1] == 'YarnProject':
                projects.append(row)
                continue
            actual_head, actual_script, schema = settings.nodes_for(obj, gen, cache)
            if (actual_script.m_Namespace, actual_script.m_ClassName) != identity:
                raise ValueError(f'runner schema script mismatch: {name}#{obj.path_id}')
            tree = obj.read_typetree(nodes=schema, check_read=True)
            settings.check_header(tree, actual_head, obj.path_id)
            if obj.save_typetree(tree, nodes=schema) != obj.get_raw_data():
                raise ValueError(f'runner no-op serialization failed: {name}#{obj.path_id}')
            project = tree['yarnProject']
            file_id, path_id = project['m_FileID'], project['m_PathID']
            if not path_id:
                target_asset = None
            elif file_id == 0:
                target_asset = name
            else:
                target_asset = external_name(obj, file_id)
            row.update({'projectReference': {'asset': target_asset, 'fileId': file_id, 'pathId': path_id},
                        'serializedAutoStart': bool(tree['autoStart']), 'startNode': tree['startNode']})
            runners.append(row)
    return {'schema': 1, 'platform': platform, 'buildVersion': spec['version'],
            'globalScriptsSha256': global_hash, 'scannedAssets': hashes,
            'projects': projects, 'runners': runners, 'unresolvedScriptReferences': sorted(unresolved),
            'limitations': 'Serialized fields and selected script classes in these fifteen assets only. No runtime changes, dynamic project loading/merging, other asset families, reachability or full game behavior are established.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data_dir', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
