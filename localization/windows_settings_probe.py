#!/usr/bin/env python3
"""Build one source-pinned Windows settings probe asset for isolated tests."""
import argparse
from copy import deepcopy
from hashlib import sha256
from importlib.metadata import version
import json
import os
from pathlib import Path

import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
import compare_yarn_versions as versions
import dialogue_locale as dl
import probe_windows_slot_font as font_probe
import settings_locale as settings

TEST_WORK = Path(__file__).resolve().parent / 'work'
ASSET = 'sharedassets0.assets'
PATH_ID = 605
LABEL = f'{ASSET}#{PATH_ID}:label'
OPTION = f'{ASSET}#{PATH_ID}:option:1'


def build(source_data, locale_file, output):
    for package, expected in [('UnityPy', '1.25.4'), ('TypeTreeGeneratorAPI', '0.0.10')]:
        if version(package) != expected:
            raise ValueError(f'unsupported {package} version')
    source_data = Path(source_data).resolve(strict=True)
    output = Path(output)
    root = TEST_WORK.resolve(strict=True)
    if (output.is_symlink() or output.exists() or output.resolve(strict=False).parent != root
            or output.suffix != '.assets'):
        raise ValueError('output must be a fresh .assets file directly in the test work directory')
    if root == source_data or source_data in root.parents:
        raise ValueError('test output must not be inside the source game')
    if dl.sha((source_data / 'globalgamemanagers').read_bytes()) != versions.BUILDS['windows']['globalSha256']:
        raise ValueError('unsupported Windows build identity')
    if dl.sha((source_data / 'globalgamemanagers.assets').read_bytes()) != font_probe.FILES['globalgamemanagers.assets']:
        raise ValueError('unsupported Windows script inventory')
    asset_bytes = (source_data / ASSET).read_bytes()
    if dl.sha(asset_bytes) != font_probe.FILES[ASSET]:
        raise ValueError('unsupported Windows settings asset')
    files = [p for p in sorted((source_data / 'Managed').glob('*.dll')) if not p.name.startswith('Yarn.')]
    inputs = [(p.name, p.read_bytes()) for p in files]
    manifest = [[name, dl.sha(data)] for name, data in inputs]
    if sha256(json.dumps(manifest, separators=(',', ':')).encode()).hexdigest() != font_probe.MANAGED_HASH:
        raise ValueError('unsupported Windows managed schema inputs')
    generator = TypeTreeGenerator('6000.3.14f1')
    for _, data in inputs:
        generator.load_dll(data)
    env = UnityPy.load(asset_bytes)
    env.path = str(source_data)
    objects = {(o.path_id, o.type.name): o for o in env.objects}
    if len(objects) != len(env.objects) or (PATH_ID, 'MonoBehaviour') not in objects:
        raise ValueError('unexpected Windows settings inventory')
    obj = objects[(PATH_ID, 'MonoBehaviour')]
    head, script, nodes = settings.nodes_for(obj, generator, {})
    if (script.m_Namespace, script.m_ClassName) != ('UnityScriptableSettings', 'SettingDropdown'):
        raise ValueError('unexpected Windows dropdown type')
    tree = obj.read_typetree(nodes=nodes, check_read=True)
    settings.check_header(tree, head, PATH_ID)
    if obj.save_typetree(tree, nodes=nodes) != obj.get_raw_data():
        raise ValueError('Windows settings schema failed no-op byte comparison')
    if (tree['label']['backupString'] != 'Anti-aliasing'
            or [o['backupString'] for o in tree['dropdownOptions']] != ['Off', 'On']):
        raise ValueError('unexpected Windows dropdown source')
    settings.ensure_unbound(tree['label'], LABEL)
    settings.ensure_unbound(tree['dropdownOptions'][1], OPTION)
    code, translations = dl.read_locale(locale_file, [LABEL, OPTION], ['Anti-aliasing', 'On'],
                                         font_probe.FILES[ASSET], yarn_semantics=False)
    updated = deepcopy(tree)
    if LABEL in translations:
        updated['label']['backupString'] = translations[LABEL]
    if OPTION in translations:
        updated['dropdownOptions'][1]['backupString'] = translations[OPTION]
    changed = obj.save_typetree(updated, nodes=nodes)
    baseline = {key: value.get_raw_data() for key, value in objects.items()}
    obj.set_raw_data(changed)
    result = env.file.save()
    tmp = output.with_name(output.name + '.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(result)
        saved = UnityPy.load(str(tmp))
        saved.path = str(source_data)
        after = {(o.path_id, o.type.name): o for o in saved.objects}
        if len(after) != len(saved.objects) or after.keys() != objects.keys():
            raise ValueError('saved Windows settings inventory changed')
        for key, value in after.items():
            expected = changed if key == (PATH_ID, 'MonoBehaviour') else baseline[key]
            if value.get_raw_data() != expected:
                raise ValueError(f'saved Windows settings object differs: {key}')
        if after[(PATH_ID, 'MonoBehaviour')].read_typetree(nodes=nodes, check_read=True) != updated:
            raise ValueError('saved Windows settings field differs')
        os.link(tmp, output)
    finally:
        tmp.unlink(missing_ok=True)
    return {'testOnly': True, 'build': versions.BUILDS['windows']['version'], 'locale': code,
            'sourceAssetSha256': font_probe.FILES[ASSET], 'changedSyntheticEntries': len(translations),
            'outputSha256': dl.sha(result), 'output': str(output)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source_data', type=Path)
    p.add_argument('--locale-file', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(build(args.source_data, args.locale_file, args.output), ensure_ascii=False))


if __name__ == '__main__':
    main()
