#!/usr/bin/env python3
"""Export or patch pinned Unity settings labels in a separate asset file."""
import argparse
from copy import deepcopy
from importlib.metadata import version
import json
import os
from pathlib import Path

import UnityPy
from UnityPy.helpers.TypeTreeGenerator import TypeTreeGenerator
from UnityPy.helpers.TypeTreeNode import TypeTreeNode

import dialogue_locale as dl
import ui_locale as ui

MANIFEST = Path(__file__).parent / 'evidence/font-roles-choices-20261106.json'
MANIFEST_HASH = 'a2610376c590a4ea28a16b6224fc3c5f11f52ba38db3e0d047ebc537d619ca1b'
ASSET = 'sharedassets0.assets'
SOURCE_HASH = ui.ASSETS[ASSET]
EXPECTED = {
    606: 'SettingDropdown', 608: 'SettingAudio', 609: 'SettingDropdown',
    610: 'SettingGroup', 611: 'SettingFloatClamped', 612: 'SettingDropdown',
    613: 'SettingGroup', 614: 'SettingGroup', 615: 'SettingDropdown',
    616: 'SettingAudio', 617: 'SettingFloatClamped', 618: 'SettingAudio',
    619: 'SettingResolution', 620: 'SettingFloatClamped', 621: 'SettingAudio',
    622: 'SettingFramerateTarget', 623: 'SettingVSync',
    624: 'SettingFullscreenMode', 625: 'SettingDropdown',
}


def make_generator(data):
    if (version('UnityPy') != '1.25.4' or version('TypeTreeGeneratorAPI') != '0.0.10'):
        raise ValueError('unsupported UnityPy or TypeTreeGeneratorAPI version')
    if dl.sha(MANIFEST.read_bytes()) != MANIFEST_HASH:
        raise ValueError('managed assembly manifest changed')
    expected = json.loads(MANIFEST.read_text(encoding='utf-8'))['managedGeneratorInputs']
    files = [p for p in sorted((data / 'Managed').glob('*.dll')) if not p.name.startswith('Yarn.')]
    actual = [[p.name, dl.sha(p.read_bytes())] for p in files]
    if actual != expected:
        raise ValueError('managed assembly inputs differ from pinned schema inputs')
    gen = TypeTreeGenerator('6000.3.14f1')
    for path in files:
        gen.load_dll(path.read_bytes())
    return gen


def nodes_for(obj, gen, cache):
    head = obj.parse_monobehaviour_head()
    script = head.m_Script.deref().read()
    key = (script.m_AssemblyName, script.m_Namespace, script.m_ClassName)
    if key not in cache:
        fullname = (script.m_Namespace + '.' if script.m_Namespace else '') + script.m_ClassName
        generated = gen.get_nodes_up(script.m_AssemblyName, fullname)
        rows = [{k: v for k, v in row.items() if k != 'm_Children'}
                for row in generated.to_dict_list()]
        enabled = next(row for row in rows if row['m_Level'] == 1 and row['m_Name'] == 'm_Enabled')
        enabled['m_MetaFlag'] |= 0x4000
        # This generator emits one managed-reference registry per inherited
        # class. Unity serializes a single registry at the end of these source
        # objects. Keep the last one and verify every resulting object byte for
        # byte on a no-op round trip before trusting this schema.
        registries = [i for i, row in enumerate(rows)
                      if row['m_Level'] == 1 and row['m_Type'] == 'ManagedReferencesRegistry']
        keep = registries[-1] if registries else -1
        cleaned, skip = [], False
        for i, row in enumerate(rows):
            if row['m_Level'] == 1:
                skip = row['m_Type'] == 'ManagedReferencesRegistry' and i != keep
            if not skip:
                cleaned.append(row)
        cache[key] = TypeTreeNode.from_list(cleaned)
    return head, script, cache[key]


def check_header(tree, head, path_id):
    if (tree['m_Script'] != {'m_FileID': head.m_Script.m_FileID, 'm_PathID': head.m_Script.m_PathID}
            or tree['m_GameObject'] != {'m_FileID': head.m_GameObject.m_FileID, 'm_PathID': head.m_GameObject.m_PathID}
            or tree['m_Enabled'] != head.m_Enabled or tree['m_Name'] != head.m_Name):
        raise ValueError(f'setting component header changed: {path_id}')


def ensure_unbound(value, key):
    ref = value['localizedString']
    entry = ref['m_TableEntryReference']
    if (ref['m_TableReference']['m_TableCollectionName'] or entry['m_KeyId'] or entry['m_Key']
            or ref['m_LocalVariables']):
        raise ValueError(f'{key}: active localization reference requires separate handling')


def scan(data):
    data = Path(data)
    if dl.sha((data / ASSET).read_bytes()) != SOURCE_HASH or dl.sha((data / 'globalgamemanagers.assets').read_bytes()) != ui.GLOBAL_HASH:
        raise ValueError('unsupported or modified settings source asset')
    gen = make_generator(data)
    env = UnityPy.load(str(data / ASSET))
    env.path = str(data)
    objects = {o.path_id: o for o in env.objects if o.path_id in EXPECTED}
    if set(objects) != set(EXPECTED):
        raise ValueError('settings object inventory changed')
    cache, trees, nodes, lines, protected = {}, {}, {}, {}, {}
    for path_id, expected_class in EXPECTED.items():
        obj = objects[path_id]
        if obj.type.name != 'MonoBehaviour':
            raise ValueError(f'{path_id}: unexpected object type')
        head, script, schema = nodes_for(obj, gen, cache)
        if script.m_ClassName != expected_class:
            raise ValueError(f'{path_id}: unexpected settings class')
        raw = obj.get_raw_data()
        tree = obj.read_typetree(nodes=schema, check_read=True)
        check_header(tree, head, path_id)
        encoded = obj.save_typetree(tree, nodes=schema)
        if encoded != raw:
            raise ValueError(f'{path_id}: settings schema failed no-op byte comparison')
        trees[path_id], nodes[path_id] = tree, schema
        label = tree['label']
        label_key = f'{ASSET}#{path_id}:label'
        ensure_unbound(label, label_key)
        if label['backupString']:
            lines[label_key] = label['backupString']
        else:
            protected[label_key] = label['backupString']
        for i, value in enumerate(tree.get('dropdownOptions', [])):
            key = f'{ASSET}#{path_id}:option:{i}'
            ensure_unbound(value, key)
            # Resolution strings are option values used by the engine, not
            # arbitrary prose. Retain them exactly until a source contract
            # demonstrates a separate display-only representation.
            target = protected if expected_class == 'SettingResolution' or not value['backupString'] else lines
            target[key] = value['backupString']
    return env, objects, trees, nodes, lines, protected


def make_asset(data, locale_file, requested):
    env, objects, trees, nodes, lines, protected = scan(data)
    locale, translations = dl.read_locale(locale_file, list(lines), list(lines.values()), SOURCE_HASH, yarn_semantics=False)
    if locale != requested:
        raise ValueError(f'locale file identifies {locale}, not requested {requested}')
    before = {(o.path_id, o.type.name): o.get_raw_data() for o in env.objects}
    if len(before) != len(env.objects):
        raise ValueError('duplicate source object identities')
    expected_trees = deepcopy(trees)
    for key, text in translations.items():
        tail = key.split('#', 1)[1].split(':')
        path_id = int(tail[0])
        if tail[1] == 'label' and len(tail) == 2:
            expected_trees[path_id]['label']['backupString'] = text
        elif tail[1] == 'option' and len(tail) == 3:
            expected_trees[path_id]['dropdownOptions'][int(tail[2])]['backupString'] = text
        else:
            raise ValueError(f'invalid settings key: {key}')
    changed = {}
    for path_id, tree in expected_trees.items():
        if tree != trees[path_id]:
            changed[path_id] = objects[path_id].save_typetree(tree, nodes=nodes[path_id])
    return env.file.save(), before, changed, expected_trees, nodes, locale, translations, protected


def patch_into(source_data, target, prepared, prior_ui=None):
    """Merge verified settings edits into a separate copied asset, optionally after UI edits."""
    _, before, changed, trees, nodes, locale, translations, _ = prepared
    source_data, target = Path(source_data), Path(target)
    resolved_source = source_data.resolve(strict=True)
    resolved_target = target.resolve(strict=False)
    if (target.is_symlink() or not target.is_file() or resolved_target == resolved_source
            or resolved_source in resolved_target.parents):
        raise ValueError('settings target must be a separate regular asset file')
    expected_before = dict(before)
    if prior_ui is not None:
        _, rows = ui.scan(source_data, ASSET)
        keys = list(rows)
        code, ui_text = dl.read_locale(prior_ui, keys, [rows[k][2] for k in keys], SOURCE_HASH, yarn_semantics=False)
        if code != locale:
            raise ValueError('prior UI locale does not match settings locale')
        for key, text in ui_text.items():
            obj, raw, _, end = rows[key]
            identity = (obj.path_id, obj.type.name)
            if obj.path_id in changed:
                raise ValueError(f'UI and settings changes overlap: {identity}')
            expected_before[identity] = raw[:88] + dl.write_string(text) + raw[end:]
    current = UnityPy.load(str(target))
    current.path = str(source_data)
    current_objects = {(o.path_id, o.type.name): o for o in current.objects}
    if len(current_objects) != len(current.objects) or current_objects.keys() != expected_before.keys():
        raise ValueError('settings target object inventory changed')
    for key, raw in expected_before.items():
        if current_objects[key].get_raw_data() != raw:
            raise ValueError(f'unexpected settings target object: {key}')
    expected_after = dict(expected_before)
    for path_id, raw in changed.items():
        key = (path_id, 'MonoBehaviour')
        current_objects[key].set_raw_data(raw)
        expected_after[key] = raw
    result = current.file.save()
    tmp = target.with_name(target.name + '.settings-localized.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(result)
        reopened = UnityPy.load(str(tmp))
        reopened.path = str(source_data)
        after = {(o.path_id, o.type.name): o for o in reopened.objects}
        if len(after) != len(reopened.objects) or after.keys() != expected_after.keys():
            raise ValueError('saved settings target object inventory changed')
        for key, raw in expected_after.items():
            if after[key].get_raw_data() != raw:
                raise ValueError(f'saved settings target object differs: {key}')
        for path_id in changed:
            if after[(path_id, 'MonoBehaviour')].read_typetree(nodes=nodes[path_id], check_read=True) != trees[path_id]:
                raise ValueError(f'setting field read-back differs: {path_id}')
        os.replace(tmp, target)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return len(translations)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_data', type=Path)
    parser.add_argument('--export', type=Path)
    parser.add_argument('--locale', type=Path)
    parser.add_argument('--requested-locale')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    if bool(args.export) == bool(args.locale) or bool(args.locale) != bool(args.output) or bool(args.locale) != bool(args.requested_locale):
        parser.error('use --export FILE or --locale FILE --requested-locale CODE --output FILE')
    source = args.source_data.resolve(strict=True)
    destination = (args.export or args.output).resolve(strict=False)
    if destination == source or source in destination.parents:
        raise ValueError('output must be outside the source data directory')
    if args.export:
        _, _, _, _, lines, protected = scan(args.source_data)
        with args.export.open('x', encoding='utf-8') as f:
            json.dump({'schema': 1, 'sourceObjectSha256': SOURCE_HASH, 'lines': lines,
                       'preserveExactly': protected}, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'Exported {len(lines)} candidate fields and {len(protected)} exact-preserve fields; classification is still required.')
        return
    data, before, changed, trees, nodes, locale, translations, _ = make_asset(args.source_data, args.locale, args.requested_locale)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(data)
        reopened = UnityPy.load(str(args.output))
        reopened.path = str(args.source_data)
        after = {(o.path_id, o.type.name): o for o in reopened.objects}
        if len(after) != len(reopened.objects) or before.keys() != after.keys():
            raise ValueError('saved settings asset object inventory changed')
        for key, raw in before.items():
            expected_raw = changed.get(key[0], raw) if key[1] == 'MonoBehaviour' else raw
            if after[key].get_raw_data() != expected_raw:
                raise ValueError(f'saved settings object differs: {key}')
        for path_id, raw in changed.items():
            obj = after[(path_id, 'MonoBehaviour')]
            if obj.get_raw_data() != raw or obj.read_typetree(nodes=nodes[path_id], check_read=True) != trees[path_id]:
                raise ValueError(f'setting field read-back differs: {path_id}')
    except BaseException:
        args.output.unlink(missing_ok=True)
        raise
    print(f'Built {locale}: {len(translations)} settings fields; SHA-256 {dl.sha(data)}. Runtime and complete source classification remain unverified.')


if __name__ == '__main__':
    main()
