#!/usr/bin/env python3
"""Prepare source-pinned Windows setting changes for an asset composition."""
from copy import deepcopy
from pathlib import Path

import UnityPy
import compare_settings_sources as comparison
import dialogue_locale as dl
import inventory_yarn_bindings as bindings
import probe_windows_slot_font as windows_fonts
import settings_locale as settings


def prepare(data, locale_file, requested_locale):
    trees, types = comparison.windows_scan(data)
    records = comparison.collect(trees, types, include_source=True)
    sources, targets, protected = {}, {}, {}
    for path_id, tree in trees.items():
        name = tree['m_Name']
        fields = records[name]['fields']
        for field, record in fields.items():
            key, source = record['id'], record['source']
            target = protected if record['provisionalRole'] == 'preserve-exactly' else sources
            if key in sources or key in protected:
                raise ValueError(f'duplicate Windows setting field: {key}')
            target[key] = source
            if field == 'label':
                targets[key] = (path_id, None)
            elif field.startswith('option:') and field[7:].isdecimal():
                targets[key] = (path_id, int(field[7:]))
            else:
                raise ValueError(f'unsupported Windows setting field: {key}')
    code, translations = dl.read_locale(locale_file, list(sources), list(sources.values()),
                                         windows_fonts.FILES[settings.ASSET], yarn_semantics=False)
    if code != requested_locale:
        raise ValueError('settings and requested locale codes do not match')
    expected = deepcopy(trees)
    for key, value in translations.items():
        path_id, option = targets[key]
        if option is None:
            expected[path_id]['label']['backupString'] = value
        else:
            expected[path_id]['dropdownOptions'][option]['backupString'] = value
    return {'originalTrees': trees, 'expectedTrees': expected, 'protected': protected,
            'locale': code, 'count': len(translations)}


def apply(data, env, objects, baseline, changed, prepared):
    """Modify only settings objects in a separately serialized in-memory asset."""
    root = Path(data).resolve(strict=True)
    env.path = str(root)
    gen = bindings.generator(root, 'windows')
    cache, schemas = {}, {}
    for path_id, updated in prepared['expectedTrees'].items():
        original_tree = prepared['originalTrees'][path_id]
        if updated == original_tree:
            continue
        identity = (path_id, 'MonoBehaviour')
        if identity not in objects or identity in changed:
            raise ValueError(f'overlapping or missing Windows setting object: {path_id}')
        obj = objects[identity]
        head, script, schema = settings.nodes_for(obj, gen, cache)
        if (script.m_Namespace, script.m_ClassName) != ('UnityScriptableSettings', comparison.WINDOWS[path_id]):
            raise ValueError(f'unexpected Windows setting type: {path_id}')
        tree = obj.read_typetree(nodes=schema, check_read=True)
        settings.check_header(tree, head, path_id)
        if tree != original_tree or obj.save_typetree(tree, nodes=schema) != baseline[identity]:
            raise ValueError(f'Windows setting source or no-op bytes changed: {path_id}')
        raw = obj.save_typetree(updated, nodes=schema)
        changed[identity] = raw
        obj.set_raw_data(raw)
        schemas[path_id] = schema
    return schemas


def verify(path, data, prepared, schemas):
    """Decode changed objects from the saved temporary asset before publication."""
    env = UnityPy.load(str(path))
    env.path = str(Path(data).resolve(strict=True))
    objects = {o.path_id: o for o in env.objects}
    if len(objects) != len(env.objects):
        raise ValueError('duplicate saved Windows setting object IDs')
    for path_id, schema in schemas.items():
        if path_id not in objects or objects[path_id].read_typetree(nodes=schema, check_read=True) != prepared['expectedTrees'][path_id]:
            raise ValueError(f'saved Windows setting field differs: {path_id}')
