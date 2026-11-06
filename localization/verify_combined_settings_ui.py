#!/usr/bin/env python3
"""Compare a combined settings/UI asset against source-bound locale inputs."""
import argparse
from copy import deepcopy
import json
from pathlib import Path

import UnityPy
import compare_settings_sources as comparison
import compare_yarn_versions as versions
import dialogue_locale as dl
import inventory_yarn_bindings as bindings
import settings_locale as settings
import ui_locale as mac_ui
import windows_ui_locale as win_ui


def object_map(env):
    objects = {(obj.path_id, obj.type.name): obj for obj in env.objects}
    if len(objects) != len(env.objects):
        raise ValueError('duplicate Unity object identity')
    return objects


def verify(platform, source_data, candidate, requested, settings_locale, ui_locale):
    if UnityPy.__version__ != '1.25.4' or platform not in versions.BUILDS:
        raise ValueError('unsupported UnityPy version or platform')
    if settings_locale is None and ui_locale is None:
        raise ValueError('at least one locale input is required')
    source_data, candidate = Path(source_data), Path(candidate)
    if dl.sha((source_data / 'globalgamemanagers').read_bytes()) != versions.BUILDS[platform]['globalSha256']:
        raise ValueError('unsupported build identity')
    asset = settings.ASSET
    adapter = mac_ui if platform == 'macos' else win_ui
    source_env, ui_rows = adapter.scan(source_data, asset)
    source_env.path = str(source_data.resolve(strict=True))
    source_objects = object_map(source_env)
    candidate_env = UnityPy.load(str(candidate))
    candidate_env.path = str(source_data.resolve(strict=True))
    actual = object_map(candidate_env)
    if source_objects.keys() != actual.keys():
        raise ValueError('candidate Unity object inventory changed')
    before = {k: o.get_raw_data() for k, o in source_objects.items()}
    expected = {}
    counts = {'settings': 0, 'ui': 0}
    asset_hash = mac_ui.ASSETS[asset] if platform == 'macos' else win_ui.ui_map.WINDOWS_ASSETS[asset]
    if settings_locale is not None:
        if platform == 'macos':
            _, _, trees, schemas, _, _ = settings.scan(source_data)
            types = settings.EXPECTED
        else:
            trees, types = comparison.windows_scan(source_data)
            generator = bindings.generator(source_data, 'windows')
            cache, schemas = {}, {}
            for path_id in trees:
                obj = source_objects[(path_id, 'MonoBehaviour')]
                head, script, schema = settings.nodes_for(obj, generator, cache)
                if (script.m_Namespace, script.m_ClassName) != ('UnityScriptableSettings', types[path_id]):
                    raise ValueError(f'unexpected setting type: {path_id}')
                settings.check_header(trees[path_id], head, path_id)
                if obj.save_typetree(trees[path_id], nodes=schema) != before[(path_id, 'MonoBehaviour')]:
                    raise ValueError(f'settings source no-op differs: {path_id}')
                schemas[path_id] = schema
        records = comparison.collect(trees, types, include_source=True)
        sources, targets = {}, {}
        for setting in records.values():
            for field, row in setting['fields'].items():
                if row['provisionalRole'] == 'preserve-exactly':
                    continue
                key = row['id']
                if key in sources:
                    raise ValueError('duplicate setting field')
                path_id = int(key.split('#', 1)[1].split(':', 1)[0])
                sources[key] = row['source']
                targets[key] = (path_id, field)
        code, translations = dl.read_locale(settings_locale, list(sources), list(sources.values()), asset_hash, yarn_semantics=False)
        if code != requested:
            raise ValueError('settings locale does not match requested locale')
        trees_after = deepcopy(trees)
        for key, text in translations.items():
            path_id, field = targets[key]
            if field == 'label':
                trees_after[path_id]['label']['backupString'] = text
            elif field.startswith('option:') and field[7:].isdecimal():
                trees_after[path_id]['dropdownOptions'][int(field[7:])]['backupString'] = text
            else:
                raise ValueError(f'unsupported setting field: {field}')
        for path_id, tree in trees_after.items():
            if tree == trees[path_id]:
                continue
            identity = (path_id, 'MonoBehaviour')
            obj = source_objects[identity]
            expected[identity] = obj.save_typetree(tree, nodes=schemas[path_id])
            if actual[identity].read_typetree(nodes=schemas[path_id], check_read=True) != tree:
                raise ValueError(f'candidate setting tree differs: {path_id}')
        counts['settings'] = len(translations)
    if ui_locale is not None:
        ui_keys = list(ui_rows)
        ui_values = [ui_rows[k][2] for k in ui_keys]
        code, translations = dl.read_locale(ui_locale, ui_keys, ui_values, asset_hash, yarn_semantics=False)
        if code != requested:
            raise ValueError('UI locale does not match requested locale')
        for key, text in translations.items():
            obj, raw, _, end = ui_rows[key]
            identity = (obj.path_id, obj.type.name)
            if identity not in before or before[identity] != raw or identity in expected:
                raise ValueError('UI source object missing, changed or overlaps settings')
            expected[identity] = raw[:88] + dl.write_string(text) + raw[end:]
        counts['ui'] = len(translations)
    for identity, raw in before.items():
        if actual[identity].get_raw_data() != expected.get(identity, raw):
            raise ValueError(f'candidate object differs from expected: {identity}')
    return {'schema': 1, 'platform': platform, 'build': versions.BUILDS[platform]['version'],
            'locale': requested, 'sourceAssetSha256': asset_hash,
            'settingsLocaleSha256': dl.sha(Path(settings_locale).read_bytes()) if settings_locale else None,
            'uiLocaleSha256': dl.sha(Path(ui_locale).read_bytes()) if ui_locale else None,
            'candidateAssetSha256': dl.sha(candidate.read_bytes()), 'expectedEntries': counts,
            'verifiedObjects': len(before),
            'limitations': 'Exact object comparison for one settings/UI asset only. Not a complete source, semantic, runtime, installation, save or restoration check.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=tuple(versions.BUILDS))
    parser.add_argument('source_data', type=Path)
    parser.add_argument('candidate_asset', type=Path)
    parser.add_argument('--locale', required=True)
    parser.add_argument('--settings-locale', type=Path)
    parser.add_argument('--ui-locale', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.platform, args.source_data, args.candidate_asset, args.locale,
                            args.settings_locale, args.ui_locale), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
