#!/usr/bin/env python3
"""Inspect selected pinned Windows slot and dialogue font roles, read-only."""
import argparse
from hashlib import sha256
from importlib.metadata import version
from io import BytesIO
import json
from pathlib import Path

import UnityPy
from fontTools.ttLib import TTFont
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
import compare_yarn_versions as builds
import probe_font_roles as fonts

FILES = {'globalgamemanagers.assets': '910358d16b824bfd4b8398fea8c0295b5660471bb13a6708655096097bb0f018',
         'level0': '55a296caa23347190faa063efdaab4cf5a37e00bdbffa455729b4aa346cddae0',
         'level1': '203725518656d04df3341248a7d24bc27551ebd6c03e582977869f0acfc5a459',
         'sharedassets1.assets': builds.BUILDS['windows']['assetSha256'],
         'sharedassets0.assets': 'c8ce3f2e8f52bb5d191c773e6f5f2a4e23d6c6c6ee8893aa7ac7a784cb1c7ac3'}
MANAGED_HASH = '11ababb69686eb17c8a608ade69a1540e33e3138f7f7f485f55e125a649e8e63'


def digest(b):
    return sha256(b).hexdigest()


def inspect(data):
    data = Path(data)
    for package, expected in [('UnityPy', '1.25.4'), ('TypeTreeGeneratorAPI', '0.0.10'), ('fonttools', '4.60.1')]:
        if version(package) != expected:
            raise ValueError(f'unsupported {package} version')
    if digest((data / 'globalgamemanagers').read_bytes()) != builds.BUILDS['windows']['globalSha256']:
        raise ValueError('unsupported Windows build identity')
    for name, expected in FILES.items():
        if digest((data / name).read_bytes()) != expected:
            raise ValueError(f'unsupported source file: {name}')
    selected = [p for p in sorted((data / 'Managed').glob('*.dll')) if not p.name.startswith('Yarn.')]
    managed = [[p.name, digest(p.read_bytes())] for p in selected]
    if digest(json.dumps(managed, separators=(',', ':')).encode()) != MANAGED_HASH:
        raise ValueError('unsupported managed schema inputs')
    generator = TypeTreeGenerator('6000.3.14f1')
    for path in selected:
        generator.load_dll(path.read_bytes())
    envs = {}
    for name in ('level0', 'level1', 'sharedassets0.assets', 'sharedassets1.assets'):
        env = UnityPy.load(str(data / name))
        env.path = str(data)
        objects = {obj.path_id: obj for obj in env.objects}
        if len(objects) != len(env.objects):
            raise ValueError('duplicate serialized object ID')
        envs[name] = objects

    def tree(name, path_id):
        obj = envs[name][path_id]
        value = fonts.read_tree(obj, generator)
        nodes = None
        if obj.type.name == 'MonoBehaviour':
            script = obj.parse_monobehaviour_head().m_Script.deref().read()
            fullname = (script.m_Namespace + '.' if script.m_Namespace else '') + script.m_ClassName
            nodes = generator.cache.get(('aligned', script.m_AssemblyName, fullname))
        if obj.save_typetree(value, nodes=nodes) != obj.get_raw_data():
            raise ValueError(f'{name}#{path_id}: schema failed no-op round trip')
        return value

    def role(name, path_id):
        obj = envs[name][path_id]
        value = tree(name, path_id)
        ref = value['m_fontAsset']
        if ref['m_FileID'] <= 0 or ref['m_FileID'] > len(obj.assets_file.externals):
            raise ValueError('unexpected font asset reference')
        owner = obj.assets_file.externals[ref['m_FileID'] - 1].path.replace('\\', '/').rsplit('/', 1)[-1]
        if owner != 'sharedassets0.assets' or ref['m_PathID'] != 622:
            raise ValueError('unexpected selected font')
        return {'asset': name, 'pathId': path_id, 'fontAsset': owner, 'fontPathId': ref['m_PathID'],
                'fontSize': value['m_fontSize'], 'autoSizing': value['m_enableAutoSizing']}
    primary, fallback = tree('sharedassets0.assets', 622), tree('sharedassets0.assets', 621)
    if primary['m_FallbackFontAssetTable'] != [{'m_FileID': 0, 'm_PathID': 621}]:
        raise ValueError('unexpected fallback chain')
    if fallback['m_SourceFontFile'] != {'m_FileID': 0, 'm_PathID': 299}:
        raise ValueError('unexpected fallback source font')
    font = tree('sharedassets0.assets', 299)
    raw = bytes(font['m_FontData'])
    cmap = TTFont(BytesIO(raw)).getBestCmap()
    roles = [role('level0', i) for i in (5180, 5183, 5184, 5186, 5189, 5191)]
    presenter, options = tree('level1', 3964), tree('level1', 4228)
    if (presenter['lineText'] != {'m_FileID': 0, 'm_PathID': 3851}
            or presenter['characterNameText'] != {'m_FileID': 0, 'm_PathID': 3852}
            or options['lastLineText'] != {'m_FileID': 0, 'm_PathID': 3859}):
        raise ValueError('unexpected dialogue presenter links')
    option_ref = options['optionViewPrefab']
    externals = envs['level1'][4228].assets_file.externals
    if option_ref['m_FileID'] <= 0 or option_ref['m_FileID'] > len(externals):
        raise ValueError('unexpected option prefab reference')
    option_owner = externals[option_ref['m_FileID'] - 1].path.replace('\\', '/').rsplit('/', 1)[-1]
    if option_owner != 'sharedassets1.assets' or option_ref['m_PathID'] != 10882:
        raise ValueError('unexpected option prefab link')
    option_item = tree('sharedassets1.assets', 10882)
    if option_item['text'] != {'m_FileID': 0, 'm_PathID': 11105}:
        raise ValueError('unexpected option text link')
    dialogue_roles = [role('level1', i) for i in (3851, 3852, 3859)] + [role('sharedassets1.assets', 11105)]
    return {'schema': 1, 'build': builds.BUILDS['windows']['version'], 'sourceHashes': FILES,
            'managedGeneratorInputs': managed, 'managedManifestSha256': MANAGED_HASH, 'roles': roles,
            'dialogueRoles': dialogue_roles,
            'presenter': {'pathId': 3964, 'lineText': 3851, 'characterNameText': 3852},
            'optionsPresenter': {'pathId': 4228, 'lastLineText': 3859,
                                 'optionPrefabPathId': 10882, 'optionTextPathId': 11105},
            'primary': {'pathId': 622, 'name': primary['m_Name'], 'populationMode': primary['m_AtlasPopulationMode']},
            'fallback': {'pathId': 621, 'name': fallback['m_Name'], 'populationMode': fallback['m_AtlasPopulationMode']},
            'sourceFont': {'pathId': 299, 'name': font['m_Name'], 'sha256': digest(raw),
                           'russianAlphabetMissing': ''.join(c for c in fonts.RUSSIAN if ord(c) not in cmap)},
            'limitation': 'Selected serialized font relationships and cmap only. No runtime rendering, visual layout, other text roles or Windows package compatibility established.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_data', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.source_data.resolve(strict=True)), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
