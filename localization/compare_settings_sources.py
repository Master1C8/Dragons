#!/usr/bin/env python3
"""Compare pinned serialized settings fields by asset name across builds."""
import argparse
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path

import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
import compare_yarn_versions as versions
import dialogue_locale as dl
import probe_windows_slot_font as windows_fonts
import settings_locale as settings

WINDOWS = {
    604: 'SettingAudio', 605: 'SettingDropdown', 606: 'SettingGroup',
    607: 'SettingFloatClamped', 608: 'SettingDropdown', 609: 'SettingGroup',
    610: 'SettingGroup', 611: 'SettingDropdown', 612: 'SettingAudio',
    613: 'SettingFloatClamped', 614: 'SettingAudio', 615: 'SettingResolution',
    616: 'SettingFloatClamped', 617: 'SettingAudio', 618: 'SettingFramerateTarget',
    619: 'SettingVSync', 620: 'SettingFullscreenMode',
}


def windows_scan(root):
    root = Path(root)
    if version('UnityPy') != '1.25.4' or version('TypeTreeGeneratorAPI') != '0.0.10':
        raise ValueError('unsupported schema tool versions')
    if dl.sha((root / 'globalgamemanagers').read_bytes()) != versions.BUILDS['windows']['globalSha256']:
        raise ValueError('unsupported Windows build identity')
    if dl.sha((root / 'globalgamemanagers.assets').read_bytes()) != windows_fonts.FILES['globalgamemanagers.assets']:
        raise ValueError('unsupported Windows scripts')
    raw = (root / settings.ASSET).read_bytes()
    if dl.sha(raw) != windows_fonts.FILES[settings.ASSET]:
        raise ValueError('unsupported Windows settings asset')
    inputs = [(p.name, p.read_bytes()) for p in sorted((root / 'Managed').glob('*.dll'))
              if not p.name.startswith('Yarn.')]
    manifest = [[name, dl.sha(data)] for name, data in inputs]
    if sha256(json.dumps(manifest, separators=(',', ':')).encode()).hexdigest() != windows_fonts.MANAGED_HASH:
        raise ValueError('unsupported Windows managed schema inputs')
    generator = TypeTreeGenerator('6000.3.14f1')
    for _, data in inputs:
        generator.load_dll(data)
    env = UnityPy.load(raw)
    env.path = str(root)
    objects = {o.path_id: o for o in env.objects}
    if len(objects) != len(env.objects) or not set(WINDOWS).issubset(objects):
        raise ValueError('unexpected Windows object inventory')
    scripts = UnityPy.load(str(root / 'globalgamemanagers.assets'))
    scripts = {o.path_id: o.read() for o in scripts.objects if o.type.name == 'MonoScript'}
    discovered = {}
    for obj in env.objects:
        if obj.type.name != 'MonoBehaviour':
            continue
        head = obj.parse_monobehaviour_head()
        ref = head.m_Script
        if not 0 < ref.m_FileID <= len(obj.assets_file.externals):
            raise ValueError(f'unresolved settings-asset script reference: {obj.path_id}')
        owner = obj.assets_file.externals[ref.m_FileID-1].path.replace('\\', '/').rsplit('/', 1)[-1].lower()
        script = scripts.get(ref.m_PathID) if owner == 'globalgamemanagers.assets' else None
        if script is None:
            raise ValueError(f'unresolved settings-asset script reference: {obj.path_id}')
        if script.m_Namespace == 'UnityScriptableSettings' and script.m_ClassName.startswith('Setting'):
            discovered[obj.path_id] = script.m_ClassName
    if discovered != WINDOWS:
        raise ValueError('unexpected Windows setting class inventory')
    cache, trees = {}, {}
    for path_id, expected in WINDOWS.items():
        obj = objects[path_id]
        head, script, nodes = settings.nodes_for(obj, generator, cache)
        if script.m_ClassName != expected or script.m_Namespace != 'UnityScriptableSettings':
            raise ValueError(f'unexpected setting type: {path_id}')
        tree = obj.read_typetree(nodes=nodes, check_read=True)
        settings.check_header(tree, head, path_id)
        if obj.save_typetree(tree, nodes=nodes) != obj.get_raw_data():
            raise ValueError(f'settings no-op serialization failed: {path_id}')
        trees[path_id] = tree
    return trees, WINDOWS


def collect(trees, types, include_source=False):
    result = {}
    for object_id, tree in trees.items():
        name = tree['m_Name']
        if not name or name in result:
            raise ValueError('empty or duplicate setting name')
        fields = {}
        values = [('label', tree['label'])] + [(f'option:{i}', x) for i, x in enumerate(tree.get('dropdownOptions', []))]
        for field, value in values:
            key = f'{settings.ASSET}#{object_id}:{field}'
            settings.ensure_unbound(value, key)
            source = value['backupString']
            if not isinstance(source, str):
                raise ValueError(f'non-string source: {key}')
            exact = (field.startswith('option:') and types[object_id] == 'SettingResolution') or not source
            entry = {'id': key, 'sourceSha256': dl.sha(source.encode('utf-8')),
                     'provisionalRole': 'preserve-exactly' if exact else 'candidate',
                     'reason': 'resolution option or empty value' if exact else 'nonempty backup string; display role needs review'}
            if include_source:
                entry['source'] = source
            fields[field] = entry
        result[name] = {'type': types[object_id], 'fields': fields}
    return result


def compare(mac, win):
    result = {}
    for name in sorted(mac.keys() | win.keys()):
        a, b = mac.get(name), win.get(name)
        if a and b and a['type'] != b['type']:
            raise ValueError(f'setting type differs: {name}')
        result[name] = {'macos': a, 'windows': b}
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    p.add_argument('--include-source', action='store_true')
    args = p.parse_args()
    if dl.sha((args.macos_data / 'globalgamemanagers').read_bytes()) != versions.BUILDS['macos']['globalSha256']:
        raise ValueError('unsupported macOS build identity')
    _, _, mac_trees, _, _, _ = settings.scan(args.macos_data)
    win_trees, win_types = windows_scan(args.windows_data)
    records = compare(collect(mac_trees, settings.EXPECTED, args.include_source),
                      collect(win_trees, win_types, args.include_source))
    print(json.dumps({'schema': 1, 'macosAssetSha256': settings.SOURCE_HASH,
                      'windowsAssetSha256': windows_fonts.FILES[settings.ASSET],
                      'settings': records,
                      'limitations': 'Known serialized setting objects only. Asset-name pairing and field hashes do not establish runtime visibility, full semantic equivalence, dynamic options or all settings sources. Candidate roles are provisional.'},
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
