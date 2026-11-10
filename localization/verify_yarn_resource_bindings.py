#!/usr/bin/env python3
"""Verify that the pinned Yarn projects bind only their stock English text."""
import argparse
import json
from importlib.metadata import version
from pathlib import Path

import UnityPy

import compare_yarn_versions as builds
import dialogue_locale as dialogue
import inventory_game_components as components
import inventory_render_components as render
import inventory_yarn_bindings as bindings
import map_ui_hierarchy as ui_map
import settings_locale as settings
import ui_locale as ui


def read_tree(obj, expected_class, generator):
    head, script, schema = settings.nodes_for(obj, generator, {})
    if (script.m_AssemblyName, script.m_Namespace, script.m_ClassName) != (
            'YarnSpinner.Unity', 'Yarn.Unity', expected_class):
        raise ValueError(f'unexpected Yarn script: {obj.path_id}')
    schema = render.correct_string_arrays(components.flat_nodes(schema))
    tree, round_trip = components.read_component(obj, schema, {})
    settings.check_header(tree, head, obj.path_id)
    if not round_trip:
        raise ValueError(f'Yarn object failed byte round trip: {obj.path_id}')
    return tree


def verify_entries(localization, keys, values):
    if (localization['m_Name'] != 'en' or localization['_containsLocalizedAssets'] != 0
            or localization['_usesAddressableAssets'] != 0):
        raise ValueError('unexpected Yarn localization mode or asset flags')
    entries = localization['entries']
    if entries['m_keys'] != keys or len(entries['m_values']) != len(values):
        raise ValueError('Yarn localization entry inventory differs from source')
    for key, value, entry in zip(keys, values, entries['m_values'], strict=True):
        if entry != {
            'localizedString': value,
            'localizedAsset': {'m_FileID': 0, 'm_PathID': 0},
            'localizedAssetReference': {
                'm_AssetGUID': '', 'm_SubObjectName': '', 'm_SubObjectType': '',
            },
        }:
            raise ValueError(f'Yarn entry text or asset binding differs: {key}')


def inspect(root, platform):
    if version('UnityPy') != '1.25.4' or version('TypeTreeGeneratorAPI') != '0.0.10':
        raise ValueError('unsupported schema tool versions')
    spec = builds.BUILDS[platform]
    keys, values, _, program, _, _ = builds.load(root, spec)
    scripts_hash = ui.GLOBAL_HASH if platform == 'macos' else ui_map.WINDOWS_GLOBAL
    if dialogue.sha((root / 'globalgamemanagers.assets').read_bytes()) != scripts_hash:
        raise ValueError('unsupported global script inventory')
    env = UnityPy.load(str(root / 'sharedassets1.assets'))
    env.path = str(root)
    objects = {obj.path_id: obj for obj in env.objects}
    generator = bindings.generator(root, platform)
    localization = read_tree(objects[spec['localization']], 'Localization', generator)
    project = read_tree(objects[spec['project']], 'YarnProject', generator)
    pointer = {'m_FileID': 0, 'm_PathID': spec['localization']}
    if (project['m_Name'] != 'Project' or project['localizationType'] != 0
            or project['baseLocalization'] != pointer
            or project['localizations'] != {'m_keys': ['en'], 'm_values': [pointer]}
            or bytes(project['compiledYarnProgram']) != program):
        raise ValueError('unexpected Yarn project bindings')
    verify_entries(localization, keys, values)
    metadata = project['lineMetadata']['_lineMetadata']
    tags = metadata['m_values']
    if (len(metadata['m_keys']) != len(tags) or len(set(metadata['m_keys'])) != len(tags)
            or not set(metadata['m_keys']).issubset(keys) or any(tag != 'lastline' for tag in tags)):
        raise ValueError('unexpected Yarn line metadata')
    return {'platform': platform, 'buildVersion': spec['version'], 'projectId': spec['project'],
            'projectSha256': spec['projectSha256'], 'englishLocalizationId': spec['localization'],
            'localizationSha256': spec['localizationSha256'], 'entries': len(keys),
            'compiledProgramSha256': dialogue.sha(program), 'lastLineMetadataCount': len(tags)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=builds.BUILDS)
    parser.add_argument('game_data', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.game_data, args.platform), indent=2))


if __name__ == '__main__':
    main()
