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
import speaker_contrast
import ui_preservation
import map_ui_hierarchy as ui_map
import windows_settings_locale as windows_settings
import yarn_transition_repair as transitions


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


def build(data, asset, locale_file, requested_locale, output, *, dialogue_locale_file=None,
          settings_locale_file=None, restore_yarn_transitions=False, improve_speaker_contrast=False):
    target = safe_output(data, output)
    env, rows = scan(data, asset)
    if (locale_file is None and dialogue_locale_file is None and settings_locale_file is None
            and not improve_speaker_contrast):
        raise ValueError('at least one locale input is required')
    if improve_speaker_contrast and requested_locale not in dl.site_locales():
        raise ValueError('speaker contrast requires a supported locale')
    if locale_file is None:
        code, translations = requested_locale, {}
    else:
        source = {key: row[2] for key, row in rows.items()}
        code, translations = ui_preservation.read_locale(
            'windows', asset, locale_file, source, ui_map.WINDOWS_ASSETS[asset],
        )
        if code != requested_locale:
            raise ValueError('requested UI locale does not match locale file')
    if dialogue_locale_file is not None and asset != 'sharedassets1.assets':
        raise ValueError('dialogue can be combined only with sharedassets1.assets')
    if restore_yarn_transitions and asset != 'sharedassets1.assets':
        raise ValueError('Yarn transition repair requires sharedassets1.assets')
    if settings_locale_file is not None and asset != 'sharedassets0.assets':
        raise ValueError('settings can be combined only with sharedassets0.assets')
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
    if improve_speaker_contrast:
        speaker_contrast.apply('windows', asset, objects, changed)
    dialogue_count = 0
    if dialogue_locale_file is not None:
        spec = versions.BUILDS['windows']
        yarn_keys, yarn_values, yarn_extras, _, _, _ = versions.load(data, spec)
        dialogue_code, dialogue_text = dl.read_locale(dialogue_locale_file, yarn_keys, yarn_values,
                                                      spec['localizationSha256'], yarn_semantics=True)
        if dialogue_code != code:
            raise ValueError('dialogue and UI locale codes do not match')
        identities = [identity for identity in objects if identity[0] == spec['localization']]
        if len(identities) != 1 or identities[0] in changed:
            raise ValueError('unexpected or overlapping Windows Yarn object identity')
        identity = identities[0]
        raw = baseline[identity]
        if dl.sha(raw) != spec['localizationSha256'] or dl.parse(raw) != (yarn_keys, yarn_values, yarn_extras):
            raise ValueError('Windows Yarn source changed during validation')
        replacements = [dialogue_text.get(key, value) for key, value in zip(yarn_keys, yarn_values)]
        encoded = dl.encode(raw, yarn_keys, replacements, yarn_extras)
        if dl.parse(encoded) != (yarn_keys, replacements, yarn_extras):
            raise ValueError('combined Windows Yarn object failed structural read-back')
        changed[identity] = encoded
        objects[identity].set_raw_data(encoded)
        dialogue_count = len(dialogue_text)
    if restore_yarn_transitions:
        identity = (versions.BUILDS['windows']['project'], 'MonoBehaviour')
        if identity not in baseline or identity in changed:
            raise ValueError('unexpected or overlapping Windows YarnProject identity')
        changed[identity] = transitions.repair_project('windows', baseline[identity])
        objects[identity].set_raw_data(changed[identity])
    prepared_settings = None
    setting_schemas = {}
    if settings_locale_file is not None:
        prepared_settings = windows_settings.prepare(data, settings_locale_file, code)
        setting_schemas = windows_settings.apply(data, env, objects, baseline, changed, prepared_settings)
    result = env.file.save()
    tmp = target.with_name(target.name + '.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(result)
        verify_output(tmp, baseline, changed)
        if prepared_settings is not None:
            windows_settings.verify(tmp, data, prepared_settings, setting_schemas)
        # A hard link publishes only the verified file and fails if target exists.
        os.link(tmp, target)
    finally:
        tmp.unlink(missing_ok=True)
    return {'platform': 'windows', 'build': versions.BUILDS['windows']['version'],
            'asset': asset, 'sourceSha256': ui_map.WINDOWS_ASSETS[asset], 'locale': code,
            'availableFields': len(rows), 'changedFields': len(translations),
            'dialogueFields': dialogue_count,
            'restoredYarnTransitions': len(transitions.CONTINUATIONS) if restore_yarn_transitions else 0,
            'settingsFields': prepared_settings['count'] if prepared_settings is not None else 0,
            'speakerContrast': improve_speaker_contrast,
            'outputSha256': dl.sha(result), 'output': str(target),
            'limitations': 'UI plus optional Yarn or settings asset changes only. Source classification, code, fonts, packaging and runtime behavior require separate validation.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source_data', type=Path)
    p.add_argument('asset', choices=sorted(ui_map.WINDOWS_ASSETS))
    p.add_argument('--locale-file', type=Path, help='optional source-bound UI locale')
    p.add_argument('--requested-locale', required=True)
    p.add_argument('--dialogue-locale-file', type=Path, help='optional source-bound Yarn locale for sharedassets1.assets')
    p.add_argument('--settings-locale-file', type=Path, help='optional source-bound settings locale for sharedassets0.assets')
    p.add_argument('--restore-yarn-transitions', action='store_true',
                   help='restore the five missing Yarn nodes and align the Windows Conrad outro route')
    p.add_argument('--speaker-contrast', action='store_true', help='use the audited black speaker label style')
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(build(args.source_data, args.asset, args.locale_file,
                           args.requested_locale, args.output,
                           dialogue_locale_file=args.dialogue_locale_file,
                           settings_locale_file=args.settings_locale_file,
                           restore_yarn_transitions=args.restore_yarn_transitions,
                           improve_speaker_contrast=args.speaker_contrast), ensure_ascii=False))


if __name__ == '__main__':
    main()
