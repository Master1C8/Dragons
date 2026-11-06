#!/usr/bin/env python3
"""Build a separately written, version-pinned Windows TMP UI asset.

This is a source-bound asset adapter, not a complete installer or a release.
Source classification, other text paths, fonts and runtime validation remain separate.
"""
import argparse
import json
import os
from pathlib import Path

import UnityPy
import compare_yarn_versions as versions
import dialogue_locale as dl
import map_ui_hierarchy as ui_map


def scan(data, asset):
    root = Path(data).resolve(strict=True)
    if UnityPy.__version__ != '1.25.4' or asset not in ui_map.WINDOWS_ASSETS:
        raise ValueError('unsupported UnityPy version or Windows UI asset')
    manager = (root / 'globalgamemanagers').read_bytes()
    scripts_bytes = (root / 'globalgamemanagers.assets').read_bytes()
    asset_bytes = (root / asset).read_bytes()
    if dl.sha(manager) != versions.BUILDS['windows']['globalSha256']:
        raise ValueError('unsupported Windows build identity')
    if dl.sha(scripts_bytes) != ui_map.WINDOWS_GLOBAL:
        raise ValueError('unsupported Windows script inventory')
    if dl.sha(asset_bytes) != ui_map.WINDOWS_ASSETS[asset]:
        raise ValueError(f'unsupported Windows UI source: {asset}')
    scripts_env = UnityPy.load(scripts_bytes)
    scripts = {o.path_id: o.read() for o in scripts_env.objects if o.type.name == 'MonoScript'}
    env = UnityPy.load(asset_bytes)
    if len({o.path_id for o in env.objects}) != len(env.objects):
        raise ValueError('duplicate source object IDs')
    rows = {}
    for obj in env.objects:
        if obj.type.name != 'MonoBehaviour':
            continue
        head = obj.parse_monobehaviour_head()
        ref = head.m_Script
        if not 0 < ref.m_FileID <= len(obj.assets_file.externals):
            raise ValueError(f'unresolved source script reference: {obj.path_id}')
        owner = obj.assets_file.externals[ref.m_FileID - 1].path.replace('\\', '/').rsplit('/', 1)[-1].lower()
        script = scripts.get(ref.m_PathID) if owner == 'globalgamemanagers.assets' else None
        if script is None:
            raise ValueError(f'unresolved source script reference: {obj.path_id}')
        if (script.m_Namespace, script.m_ClassName) != ('TMPro', 'TextMeshProUGUI'):
            continue
        raw = obj.get_raw_data()
        text, end = dl.read_string(raw, 88)
        if raw[88:end] != dl.write_string(text):
            raise ValueError(f'unexpected UI text encoding: {asset}#{obj.path_id}')
        key = f'{asset}#{obj.path_id}'
        rows[key] = (obj, raw, text, end)
    return env, rows


def safe_output(data, output):
    root = Path(data).resolve(strict=True)
    target = Path(output)
    if not target.name or target.is_symlink() or target.exists():
        raise ValueError('output must be a fresh regular file')
    parent = target.parent.resolve(strict=True)
    game_root = root.parent
    if parent == game_root or game_root in parent.parents:
        raise ValueError('output must be outside the installed game directory')
    return parent / target.name


def verify_output(path, baseline, changed):
    reopened = UnityPy.load(str(path))
    objects = {(o.path_id, o.type.name): o for o in reopened.objects}
    if len(objects) != len(reopened.objects) or objects.keys() != baseline.keys():
        raise ValueError('saved Windows UI object inventory changed')
    for identity, obj in objects.items():
        if obj.get_raw_data() != changed.get(identity, baseline[identity]):
            raise ValueError(f'saved Windows UI object differs: {identity}')


def build(data, asset, locale_file, requested_locale, output):
    target = safe_output(data, output)
    env, rows = scan(data, asset)
    keys = list(rows)
    values = [rows[k][2] for k in keys]
    code, translations = dl.read_locale(locale_file, keys, values,
                                         ui_map.WINDOWS_ASSETS[asset], yarn_semantics=False)
    if code != requested_locale:
        raise ValueError('requested UI locale does not match locale file')
    objects = {(o.path_id, o.type.name): o for o in env.objects}
    if len(objects) != len(env.objects):
        raise ValueError('duplicate source object identity')
    baseline = {identity: obj.get_raw_data() for identity, obj in objects.items()}
    changed = {}
    for key, value in translations.items():
        obj, raw, _, end = rows[key]
        identity = (obj.path_id, obj.type.name)
        replacement = raw[:88] + dl.write_string(value) + raw[end:]
        changed[identity] = replacement
        obj.set_raw_data(replacement)
    result = env.file.save()
    tmp = target.with_name(target.name + '.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(result)
        verify_output(tmp, baseline, changed)
        # A hard link publishes only the verified file and fails if target exists.
        os.link(tmp, target)
    finally:
        tmp.unlink(missing_ok=True)
    return {'platform': 'windows', 'build': versions.BUILDS['windows']['version'],
            'asset': asset, 'sourceSha256': ui_map.WINDOWS_ASSETS[asset], 'locale': code,
            'availableFields': len(rows), 'changedFields': len(translations),
            'outputSha256': dl.sha(result), 'output': str(target),
            'limitations': 'Serialized TMP strings only. Source classification, dialogue, settings, code, fonts, packaging and runtime behavior require separate validation.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source_data', type=Path)
    p.add_argument('asset', choices=sorted(ui_map.WINDOWS_ASSETS))
    p.add_argument('--locale-file', required=True, type=Path)
    p.add_argument('--requested-locale', required=True)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(build(args.source_data, args.asset, args.locale_file,
                           args.requested_locale, args.output), ensure_ascii=False))


if __name__ == '__main__':
    main()
