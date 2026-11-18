#!/usr/bin/env python3
"""Rebuild current game assets from reviewed historical text and a bounded delta."""
import argparse
import json
from pathlib import Path
import struct
import tempfile

from assemble_source_inventory import INVENTORY_SHA, load_pinned
from current_build import Build, digest, relative_path
import dialogue_locale as dialogue
import package_inputs
import paired_locale
import managed_fallback
import cjk_font_fallback as cjk
import complex_text
import current_font
from rebuild_release_packages import archived_file
import speaker_locale
import yarn_transition_repair


ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(Path(path).read_text(), object_pairs_hook=dialogue.unique_object)


def validate_overlay(path, locale, source_sha, source, edits, *, yarn=True):
    doc = {'schema': 1, 'locale': locale, 'sourceObjectSha256': source_sha,
           'lines': {key: {'source': source[key], 'text': value} for key, value in edits.items()}}
    path.write_text(json.dumps(doc, ensure_ascii=False) + '\n')
    actual, result = dialogue.read_locale(path, list(source), list(source.values()), source_sha,
                                          yarn_semantics=yarn)
    if actual != locale or result != edits:
        raise ValueError('Validated locale differs from the explicitly requested values')


def build(args):
    locale = args.locale
    if locale not in dialogue.site_locales():
        raise ValueError('An explicit supported non-English locale is required')
    profile = load(args.profile)
    delta = load(args.delta)
    if (delta['schemaVersion'] != 1 or delta['locale'] != locale or
            delta['gameVersion'] != profile['gameVersion']):
        raise ValueError('Locale delta does not match the selected game build')
    inputs = Build(args.source, args.profile)
    inputs.verify()
    platform = profile['platform']
    settings_fallback = None
    if 'sharedSettingsWith' in profile:
        shared = profile['sharedSettingsWith']
        reference = ROOT / relative_path(shared['path'])
        if digest(reference.read_bytes()) != shared['sha256']:
            raise ValueError('Shared settings source-profile fingerprint changed')
        other = load(reference)
        def semantic_settings(value):
            return {(r['name'], r['class'], r['label'], tuple(r['options'])) for r in value['settings']}
        if semantic_settings(profile) != semantic_settings(other):
            raise ValueError('Current platform settings differ from the shared text source')
        settings_fallback = other['platform']
    config_path = args.accepted / 'PackageConfig.json'
    if digest(config_path.read_bytes()) != profile['acceptedConfigSha256']:
        raise ValueError('Accepted release configuration fingerprint mismatch')
    config = load(config_path)
    accepted = next(row for row in config['languages'] if row['siteLocale'] == locale)
    archived = args.accepted / 'LocalizationPayload'
    runtime, runtime_sha = archived_file(archived, accepted, speaker_locale.COMPANION)
    license_dir = archived / 'Licenses' / locale
    resource = None
    if locale in cjk.FONTS:
        if not args.fonts:
            raise ValueError('The pinned CJK recovery inputs are required')
        resource = cjk.prepare(locale, args.fonts / 'cjk' / f'{locale}.otf', license_dir / cjk.LICENSE)
    roster = load(ROOT / 'installer/App/LocalePackages.json')['locales']
    pin = next(row for row in roster if row['siteLocale'] == locale)
    authored = ROOT / 'localization' / locale / 'translation.json'
    if digest(authored.read_bytes()) != pin['translationSha256']:
        raise ValueError('Historical authoring differs from its reviewed release binding')
    inventory = load_pinned(args.inventory, INVENTORY_SHA)
    scope = load_pinned(args.scope, package_inputs.YARN_SCOPE_SHA)
    builds, rows = paired_locale.catalog(inventory['entries'], scope)
    translations = paired_locale.read(authored, locale, package_inputs.YARN_SCOPE_SHA, rows)
    if args.output.exists():
        raise FileExistsError(args.output)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.current-locale-', dir=args.output.parent) as temporary:
        stage = Path(temporary)
        shaping = None
        if locale in complex_text.FONTS:
            from current_shaping import prepare
            shaping = prepare(args, stage, authored, rows, translations, delta, archived, accepted)
            resource = shaping.font
        old_inputs = stage / 'historical-inputs'
        paired_locale.materialize(old_inputs, platform, locale, builds[platform], rows, translations)
        old_ui = {p.stem: load(p) for p in (old_inputs / 'ui').glob('*.json')}
        output = stage / 'payload'
        output.mkdir()
        files, ui_counts = {}, {}
        font_receipt = None
        asset_names = {key.split('#')[0] for key in profile['ui']}
        asset_names |= {row['asset'] for row in profile['settings']} | {profile['yarn']['asset']}
        for name in sorted(asset_names):
            asset = inputs.asset(name)
            binding = {int(key.split('#')[1]): row for key, row in profile['ui'].items()
                       if key.split('#')[0] == name}
            actual = asset.text_bindings()
            if actual.keys() != binding.keys() or any(
                    actual[key]['source'] != row['source'] or
                    list(actual[key]['hierarchy']) != row['hierarchy'] for key, row in binding.items()):
                raise ValueError(f'Current UI inventory differs from its reviewed binding: {name}')
            edits = {}
            slot_labels = {key for key, row in binding.items()
                           if row['hierarchy'][1:4] == ['Menu_SlotsLoad', 'Container', 'LoadSlotSelect']
                           and row['hierarchy'][-1] == 'SlotProgress'}
            if name == 'level1' and len(slot_labels) != 3:
                raise ValueError('Unexpected save-slot plaque inventory')
            for path_id, row in binding.items():
                policy = row['policy']
                if policy == 'delta':
                    edits[str(path_id)] = delta['ui'][row['source']]
                elif policy == 'inherited':
                    old_asset, old_id = row['oldId'].split('#')
                    old = old_ui[old_asset]['lines'][f'{old_asset}#{old_id}']
                    if old['source'] != row['source']:
                        raise ValueError('Historical UI source differs from the current source')
                    edits[str(path_id)] = old['text']
                elif policy != 'preserve':
                    raise ValueError('Unreviewed UI preservation policy')
            if edits:
                sources = {str(key): row['source'] for key, row in binding.items()}
                validate_overlay(stage / 'ui-check.json', locale, profile['files'][name]['sha256'],
                                 sources, edits, yarn=False)
                for key, target in edits.items():
                    row = binding[int(key)]
                    title = row['hierarchy'][1:] == ['Menu_Options', 'Container', 'Panel', 'TitlePlaque', 'Title']
                    asset.text(int(key), sources[key], target, fit_width=80.0 if title else None)
            for path_id in sorted(slot_labels):
                source = binding[path_id]['source']
                asset.text(path_id, source, source, fit_width=24.0)
            for path_id, row in binding.items():
                if row.get('speakerContrast'):
                    asset.speaker_colour(path_id)
            for row in profile['settings']:
                if row['asset'] != name:
                    continue
                fields = []
                for suffix, source in [('label', row['label']), *[
                        (f'option:{i}', value) for i, value in enumerate(row['options'])]]:
                    key = row['name'] + ':' + suffix
                    if key in delta['settings']:
                        item = delta['settings'][key]
                        if item['source'] != source:
                            raise ValueError('New setting source differs from the reviewed delta')
                        text = item['text']
                    else:
                        # Historical setting IDs are storage IDs; resolve the
                        # semantic setting name through the reviewed catalog.
                        shared = translations.get('settings:' + key, {})
                        text = shared.get(platform)
                        if text is None and settings_fallback is not None:
                            text = shared.get(settings_fallback)
                        if text is None:
                            if row['class'] == 'SettingResolution' and suffix.startswith('option:'):
                                continue
                            if not source:
                                continue
                            raise ValueError(f'Untranslated setting: {key}')
                    field = ['label', 'backupString'] if suffix == 'label' else [
                        'dropdownOptions', int(suffix.split(':')[1]), 'backupString']
                    fields.append((field, source, text))
                if fields:
                    asset.setting(row['id'], row['name'], fields)
            if name == profile['yarn']['asset']:
                spec = profile['yarn']
                original = asset.original[spec['localization']]
                keys, values, _ = dialogue.parse(original)
                current = dict(zip(keys, values))
                old = load(old_inputs / 'dialogue.json')['lines']
                changed = {key for key, row in old.items() if row['source'] != current[key]}
                if changed != set(spec['sourceTextChanges']) or delta['yarn'].keys() - changed:
                    raise ValueError('Source text changes differ from the reviewed Yarn delta')
                edited = {key: row['text'] for key, row in old.items()}
                reused_variants = []
                for key in sorted(changed - delta['yarn'].keys()):
                    source_platform = spec.get('sharedSourcePlatform')
                    shared_id = 'yarn:' + key
                    shared_row = rows[shared_id]['builds'].get(source_platform)
                    if shared_row is None or shared_row['source'] != current[key]:
                        raise ValueError(f'No exact reviewed source variant for changed Yarn line: {key}')
                    edited[key] = translations[shared_id][source_platform]
                    reused_variants.append({'id': key, 'sourcePlatform': source_platform,
                                            'sourceSha256': digest(current[key].encode()),
                                            'targetSha256': digest(edited[key].encode())})
                for key, row in delta['yarn'].items():
                    if row['source'] != current[key]:
                        raise ValueError(f'Current Yarn delta source mismatch: {key}')
                    edited[key] = row['text']
                validate_overlay(stage / 'yarn-check.json', locale, digest(original), current, edited)
                asset.yarn(spec['localization'], {key: (current[key], text) for key, text in edited.items()})
                old_source = args.old_source / spec['oldAsset']
                old_env = __import__('UnityPy').load(str(old_source))
                old_project = next(o for o in old_env.objects if o.path_id == spec['oldProject']).get_raw_data()
                repaired = yarn_transition_repair.repair_project(
                    spec.get('transitionSourcePlatform', platform), old_project)
                size = struct.unpack_from('<I', old_project, 40)[0]
                if digest(old_project[44:44 + size]) != spec['programSha256']:
                    raise ValueError('Historical and current dialogue programs differ')
                size = struct.unpack_from('<I', repaired, 40)[0]
                asset.program(spec['project'], spec['programSha256'], repaired[44:44 + size])
            if name == cjk.ASSET and resource:
                font_receipt = current_font.add(asset, resource)
            if asset.changed:
                files[name] = asset.save(output / name)
            ui_counts[name] = {'objects': len(binding), 'translated': len(edits),
                               'protected': sum(row['policy'] == 'preserve' for row in binding.values())}
        managed = output / 'Managed'
        managed.mkdir()
        slot_source = inputs.data / 'Managed/Assembly-CSharp.dll'
        slot_hash = digest(inputs.read('Managed/Assembly-CSharp.dll'))
        slot_text = translations['display:slot-new'][platform]
        validate_overlay(stage / 'current-slot.json', locale, slot_hash,
                         managed_fallback.CURRENT_SLOT, {'slot-new': slot_text}, yarn=False)
        slot_raw, slot_receipt = managed_fallback.prepare(
            platform, slot_source, stage / 'current-slot.json', locale,
            args.slot_tool, slot_new=True, current_build=True)
        (managed / 'Assembly-CSharp.dll').write_bytes(slot_raw)
        files['Managed/Assembly-CSharp.dll'] = {'sourceSha256': slot_hash,
                                               'outputSha256': digest(slot_raw)}
        # Current Yarn/TMP inputs retain the exact historical fingerprints.
        # Rebuild the speaker/fallback patch instead of shipping a stale game DLL.
        speaker_source = inputs.data / 'Managed/YarnSpinner.Unity.dll'
        inputs.read('Managed/YarnSpinner.Unity.dll')
        patched, speaker_receipt = speaker_locale.prepare(
            platform, speaker_source, old_inputs / 'speakers.json', locale,
            args.speaker_tool, runtime, runtime_sha, fallback_locale=old_inputs / 'missing-line.json')
        complex_receipt = None
        if shaping:
            rendered, complex_receipt = shaping.patch(inputs.data / 'Managed',
                                                       patched[complex_text.YARN], speaker_receipt)
            patched.update(rendered)
        for name, raw in patched.items():
            (managed / name).write_bytes(raw)
            old = inputs.profile['files'].get('Managed/' + name)
            files['Managed/' + name] = {'sourceSha256': old['sha256'] if old else None,
                                      'outputSha256': digest(raw)}
        inputs.verify()
        manifest = {'schema': 1, 'kind': 'current-build-localization-replacements', 'platform': platform,
                    'locale': locale, 'build': profile['gameVersion'],
                    'sourceGlobalManagersSha256': profile['files']['globalgamemanagers']['sha256'],
                    'sourceGlobalScriptsSha256': profile['files']['globalgamemanagers.assets']['sha256'],
                    'buildProfileSha256': digest(Path(args.profile).read_bytes()),
                    'authoringSha256': digest(authored.read_bytes()), 'deltaSha256': digest(args.delta.read_bytes()),
                    'files': files, 'uiCoverage': ui_counts, 'speakerPatch': speaker_receipt,
                    'reusedYarnSourceVariants': reused_variants, 'slotPatch': slot_receipt}
        if resource:
            if font_receipt is None:
                raise ValueError('Locale font was not written')
            font_receipt['assetSha256'] = files[cjk.ASSET]['outputSha256']
            if complex_receipt:
                complex_receipt['fontFallback'] = font_receipt
                manifest['complexText'] = complex_receipt
                license_name = complex_text.LICENSE
            else:
                manifest['cjkFallback'] = font_receipt
                license_name = cjk.LICENSE
            (output / license_name).write_bytes(resource.license)
        (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
        # Only complete, verified output is exposed. The task owns a fresh
        # destination; an existing result is never replaced.
        if args.output.exists():
            raise FileExistsError(args.output)
        output.rename(args.output)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--locale', required=True)
    for name in ('source', 'old-source', 'profile', 'delta', 'accepted', 'inventory', 'scope', 'speaker-tool', 'slot-tool', 'output'):
        parser.add_argument('--' + name, type=Path, required=True)
    for name in ('fonts', 'shaping-source', 'shaper', 'icu', 'shaping-tool'):
        parser.add_argument('--' + name, type=Path)
    result = build(parser.parse_args())
    print(json.dumps({'locale': result['locale'], 'files': len(result['files']), 'uiCoverage': result['uiCoverage']}))


if __name__ == '__main__':
    main()
