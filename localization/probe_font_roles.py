#!/usr/bin/env python3
"""Inspect representative original macOS dialogue and menu font roles, read-only."""
import argparse
from hashlib import sha256
from importlib.metadata import version
from io import BytesIO
import json
from pathlib import Path

import UnityPy
from fontTools.ttLib import TTFont
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
from UnityPy.helpers.TypeTreeNode import TypeTreeNode

from ui_locale import ASSETS, GLOBAL_HASH

EXPECTED_FILES = {
    'globalgamemanagers.assets': GLOBAL_HASH,
    'sharedassets0.assets': ASSETS['sharedassets0.assets'],
    'sharedassets1.assets': ASSETS['sharedassets1.assets'],
    'level0': ASSETS['level0'],
    'level1': ASSETS['level1'],
    'Managed/Unity.TextMeshPro.dll': 'a25a11167a5a7339d611c364a6525fc172d19fe5caa6aa95d6866fd1d36d0743',
    'Managed/YarnSpinner.Unity.dll': '54953f9c071aa3ca5b52eb8b12b8e0bedc73f7665a506c61acbef0c58ac340ef',
}
RUSSIAN = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя'


def digest(data):
    return sha256(data).hexdigest()


def read_tree(obj, generator):
    """Use the serialized schema or an aligned generated schema with header checks."""
    try:
        tree = obj.read_typetree(check_read=True)
    except (ValueError, EOFError, AssertionError):
        if obj.type.name != 'MonoBehaviour':
            raise
        head = obj.parse_monobehaviour_head()
        script = head.m_Script.deref().read()
        fullname = (script.m_Namespace + '.' if script.m_Namespace else '') + script.m_ClassName
        key = ('aligned', script.m_AssemblyName, fullname)
        nodes = generator.cache.get(key)
        if nodes is None:
            generated = generator.get_nodes_up(script.m_AssemblyName, fullname)
            flat = [{k: v for k, v in row.items() if k != 'm_Children'}
                    for row in generated.to_dict_list()]
            enabled = next(row for row in flat if row['m_Level'] == 1 and row['m_Name'] == 'm_Enabled')
            enabled['m_MetaFlag'] |= 0x4000
            nodes = TypeTreeNode.from_list(flat)
            generator.cache[key] = nodes
        tree = obj.read_typetree(nodes=nodes, check_read=True)
    if obj.type.name == 'MonoBehaviour':
        head = obj.parse_monobehaviour_head()
        if (tree['m_Script'] != {'m_FileID': head.m_Script.m_FileID, 'm_PathID': head.m_Script.m_PathID}
                or tree['m_GameObject'] != {'m_FileID': head.m_GameObject.m_FileID, 'm_PathID': head.m_GameObject.m_PathID}
                or tree['m_Enabled'] != head.m_Enabled or tree['m_Name'] != head.m_Name):
            raise ValueError(f'component header mismatch: {obj.path_id}')
    return tree


def inspect(data):
    for package, expected in [('UnityPy', '1.25.4'), ('TypeTreeGeneratorAPI', '0.0.10'), ('fonttools', '4.60.1')]:
        if version(package) != expected:
            raise ValueError(f'unsupported {package} version')
    for name, expected in EXPECTED_FILES.items():
        if digest((data / name).read_bytes()) != expected:
            raise ValueError(f'unsupported source file: {name}')
    generator = TypeTreeGenerator('6000.3.14f1')
    managed = sorted((data / 'Managed').glob('*.dll'))
    # Yarn's prefixed dependency copies have duplicate internal assembly names.
    # They are not needed for the Unity TMP and YarnSpinner.Unity schemas here.
    selected = [p for p in managed if not p.name.startswith('Yarn.')]
    manifest = []
    for path in selected:
        raw = path.read_bytes()
        manifest.append([path.name, digest(raw)])
        generator.load_dll(raw)
    envs = {}
    for name in ('sharedassets0.assets', 'sharedassets1.assets', 'level0', 'level1'):
        envs[name] = UnityPy.load(str(data / name))
        envs[name].path = str(data)

    def obj(name, path_id):
        matches = [o for o in envs[name].objects if o.path_id == path_id]
        if len(matches) != 1:
            raise ValueError(f'object identity mismatch: {name}#{path_id}')
        return matches[0]

    def role(name, path_id):
        item = obj(name, path_id)
        tree = read_tree(item, generator)
        pointer = tree['m_fontAsset']
        file_id = pointer['m_FileID']
        if file_id < 0 or file_id > len(item.assets_file.externals):
            raise ValueError(f'invalid font external reference: {name}#{path_id}')
        owner = name if file_id == 0 else item.assets_file.externals[file_id - 1].path.replace('\\', '/').rsplit('/', 1)[-1]
        return {'asset': name, 'pathId': path_id, 'fontAsset': owner,
                'fontPathId': pointer['m_PathID'], 'fontSize': tree['m_fontSize'],
                'autoSizing': tree['m_enableAutoSizing'], 'overflowMode': tree['m_overflowMode']}

    primary = read_tree(obj('sharedassets0.assets', 627), generator)
    fallback = read_tree(obj('sharedassets0.assets', 626), generator)
    font_obj = obj('sharedassets0.assets', 300)
    font = font_obj.read_typetree(check_read=True)
    font_bytes = bytes(font['m_FontData'])
    cmap = TTFont(BytesIO(font_bytes)).getBestCmap()
    presenter = read_tree(obj('level1', 4011), generator)
    if (presenter['lineText'] != {'m_FileID': 0, 'm_PathID': 3899}
            or presenter['characterNameText'] != {'m_FileID': 0, 'm_PathID': 3900}):
        raise ValueError('dialogue presenter links changed')
    options_obj = obj('level1', 4284)
    options = read_tree(options_obj, generator)
    prefab = options['optionViewPrefab']
    if prefab['m_FileID'] <= 0 or prefab['m_FileID'] > len(options_obj.assets_file.externals):
        raise ValueError('choice prefab external reference changed')
    prefab_owner = options_obj.assets_file.externals[prefab['m_FileID'] - 1].path.replace('\\', '/').rsplit('/', 1)[-1]
    option_item = read_tree(obj('sharedassets1.assets', 10894), generator)
    if (prefab_owner != 'sharedassets1.assets' or prefab['m_PathID'] != 10894
            or options['lastLineText'] != {'m_FileID': 0, 'm_PathID': 3906}
            or option_item['text'] != {'m_FileID': 0, 'm_PathID': 11117}):
        raise ValueError('choice presenter links changed')
    roles = ([role('level0', i) for i in range(5201, 5213)]
             + [role('level1', i) for i in (3899, 3900, 3906)]
             + [role('sharedassets1.assets', 11117)])
    return {
        'schema': 1, 'unityVersion': '6000.3.14f1', 'sourceHashes': EXPECTED_FILES,
        'managedGeneratorInputs': manifest,
        'presenter': {'asset': 'level1', 'pathId': 4011, 'lineText': 3899, 'characterNameText': 3900},
        'optionsPresenter': {'asset': 'level1', 'pathId': 4284, 'lastLineText': 3906,
                             'optionPrefabAsset': prefab_owner, 'optionPrefabPathId': 10894,
                             'optionTextPathId': 11117},
        'roles': roles,
        'primary': {'pathId': 627, 'name': primary['m_Name'], 'populationMode': primary['m_AtlasPopulationMode'],
                    'characterCount': len(primary['m_CharacterTable']), 'fallbacks': primary['m_FallbackFontAssetTable']},
        'fallback': {'pathId': 626, 'name': fallback['m_Name'], 'populationMode': fallback['m_AtlasPopulationMode'],
                     'sourceFont': fallback['m_SourceFontFile'], 'initialCharacterCount': len(fallback['m_CharacterTable'])},
        'sourceFont': {'pathId': 300, 'name': font['m_Name'], 'sha256': digest(font_bytes),
                       'russianAlphabetMissing': ''.join(c for c in RUSSIAN if ord(c) not in cmap)},
        'limitation': 'Static mapping and cmap only; in-game glyph readability, clipping and progression require separate verification.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_data', type=Path, help='original game Contents/Resources/Data directory')
    args = parser.parse_args()
    print(json.dumps(inspect(args.source_data.resolve(strict=True)), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
