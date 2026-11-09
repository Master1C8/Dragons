#!/usr/bin/env python3
"""Create a separate macOS game copy with a selected dialogue locale."""
import argparse
import ctypes
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

import dialogue_locale as dl
import managed_fallback
import speaker_contrast
import speaker_locale as speakers
import ui_locale as ui
import ui_preservation
import verify_managed_assemblies as managed
import verify_preserved_components as protected
import yarn_transition_repair as transitions

ASSET_RELATIVE = Path('Contents/Resources/Data/sharedassets1.assets')
MANAGED_RELATIVE = ASSET_RELATIVE.parent / 'Managed'


def rename_exclusive(source, destination):
    """Publish a verified directory atomically without replacing an existing path."""
    if sys.platform != 'darwin':
        raise RuntimeError('exclusive app publication requires macOS renamex_np')
    libc = ctypes.CDLL(None, use_errno=True)
    rename = libc.renamex_np
    rename.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_uint]
    rename.restype = ctypes.c_int
    if rename(os.fsencode(source), os.fsencode(destination), 0x00000004) != 0:
        error = ctypes.get_errno()
        raise OSError(error, os.strerror(error), str(destination))


def bundle_paths(source, destination):
    source = source.resolve(strict=True)
    destination = destination.absolute()
    if source.suffix != '.app' or destination.suffix != '.app' or not source.is_dir():
        raise ValueError('source and destination must be macOS .app bundles')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('destination already exists')
    resolved = destination.resolve(strict=False)
    if source == resolved or source in resolved.parents or resolved in source.parents:
        raise ValueError('source and destination must not overlap')
    return source, destination


def build(source, locale_file, requested, destination, ui_dir=None, settings_file=None,
          test_profile_code=None, test_caption_layout=False, test_slot_font=False,
          restore_yarn_transitions=False, *, fallback_locale=None, fallback_tool=None, slot_new_locale=None,
          speaker_locale=None, speaker_tool=None, speaker_runtime=None, speaker_runtime_sha=None,
          improve_speaker_contrast=False, package_receipt=None, preservation_inventory=None):
    source, destination = bundle_paths(source, destination)
    if (package_receipt is None) != (preservation_inventory is None):
        raise ValueError('complete package receipt and preservation inventory are required together')
    if test_caption_layout and test_profile_code is None:
        raise ValueError('experimental settings layout requires an isolated test profile')
    if test_slot_font and test_profile_code is None:
        raise ValueError('experimental slot font requires an isolated test profile')
    destination.parent.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.localization-build-', dir=destination.parent))
    try:
        staged_app = stage / destination.name
        report = _build_unpublished(source, locale_file, requested, staged_app, ui_dir, settings_file,
                                    test_profile_code, test_caption_layout, test_slot_font,
                                    restore_yarn_transitions, fallback_locale=fallback_locale,
                                    fallback_tool=fallback_tool, slot_new_locale=slot_new_locale,
                                    speaker_locale=speaker_locale, speaker_tool=speaker_tool,
                                    speaker_runtime=speaker_runtime, speaker_runtime_sha=speaker_runtime_sha,
                                    improve_speaker_contrast=improve_speaker_contrast,
                                    package_receipt=package_receipt)
        if preservation_inventory is not None:
            report['componentPreservation'] = protected.verify(
                'macos', preservation_inventory, staged_app / ASSET_RELATIVE.parent,
            )
        rename_exclusive(staged_app, destination)
    finally:
        shutil.rmtree(stage)
    # This check concerns the actual published path, not the staging copy.
    # If it fails, retain the published result for diagnosis; do not delete it.
    subprocess.run(['codesign', '--verify', '--deep', '--strict', str(destination)], check=True)
    report['output'] = str(destination)
    print(json.dumps(report, ensure_ascii=False))
    if package_receipt is None:
        print('Build complete. No game was installed or launched; UI coverage and font support remain unverified.')
    return report


def _build_unpublished(source, locale_file, requested, destination, ui_dir=None, settings_file=None,
                       test_profile_code=None, test_caption_layout=False, test_slot_font=False,
                       restore_yarn_transitions=False, *, fallback_locale=None, fallback_tool=None, slot_new_locale=None,
                       speaker_locale=None, speaker_tool=None, speaker_runtime=None, speaker_runtime_sha=None,
                       improve_speaker_contrast=False, package_receipt=None):
    source = source.resolve(strict=True)
    destination = destination.absolute()
    if source.suffix != '.app' or destination.suffix != '.app' or not source.is_dir():
        raise ValueError('source and destination must be macOS .app bundles')
    if test_caption_layout and test_profile_code is None:
        raise ValueError('experimental settings layout requires an isolated test profile')
    if test_slot_font and test_profile_code is None:
        raise ValueError('experimental slot font requires an isolated test profile')
    if destination.exists() or destination.is_symlink():
        raise FileExistsError('destination already exists')
    # Do not put outputs inside the source or recursively copy a parent of the source.
    dest_resolved = destination.resolve(strict=False)
    if source == dest_resolved or source in dest_resolved.parents or dest_resolved in source.parents:
        raise ValueError('source and destination must not overlap')
    for directory, subdirs, files in os.walk(source, followlinks=False):
        for name in subdirs + files:
            if (Path(directory) / name).is_symlink():
                raise ValueError('source app contains a symlink; refusing to sign a potentially external target')
    source_steam = source / 'steam_appid.txt'
    if not source_steam.is_file() or not source_steam.read_bytes():
        raise ValueError('source app is missing its Steam identifier')
    asset = source / ASSET_RELATIVE
    if asset.is_symlink() or not asset.is_file() or source not in asset.resolve().parents:
        raise ValueError('source asset must be a regular file')
    env, obj, raw, keys, values, extras = dl.load_asset(asset)
    locale, translations = dl.read_locale(locale_file, keys, values, yarn_semantics=True)
    if locale != requested:
        raise ValueError(f'locale file identifies {locale}, not requested {requested}')
    global_scripts = ASSET_RELATIVE.with_name('globalgamemanagers.assets')
    if dl.sha((source / global_scripts).read_bytes()) != ui.GLOBAL_HASH:
        raise ValueError('unsupported macOS global scripts and localization settings')
    source_assemblies = managed.scan(source / MANAGED_RELATIVE)
    managed_digest = managed.validate_source('macos', source_assemblies)
    speaker_inputs = (speaker_locale, speaker_tool, speaker_runtime, speaker_runtime_sha)
    if any(item is not None for item in speaker_inputs) and not all(item is not None for item in speaker_inputs):
        raise ValueError('speaker locale, tool, runtime and runtime SHA-256 must be supplied together')
    standalone_fallback = fallback_locale if speaker_locale is None else None
    if (standalone_fallback is not None or slot_new_locale is not None) != (fallback_tool is not None):
        raise ValueError('a managed text locale and tool must be supplied together')
    managed_replacements = {}
    speaker_files, speaker_report = {}, None
    if speaker_locale is not None:
        speaker_files, speaker_report = speakers.prepare(
            'macos', source / MANAGED_RELATIVE / managed_fallback.ASSEMBLY, speaker_locale, requested,
            speaker_tool, speaker_runtime, speaker_runtime_sha, fallback_locale=fallback_locale,
        )
    for assembly, file in ((managed_fallback.ASSEMBLY, standalone_fallback), (managed_fallback.SLOT_ASSEMBLY, slot_new_locale)):
        if file is not None:
            managed_replacements[assembly] = managed_fallback.prepare(
                'macos', source / MANAGED_RELATIVE / assembly, file, requested, fallback_tool,
                slot_new=assembly == managed_fallback.SLOT_ASSEMBLY,
            )
    replacement = [translations.get(k, v) for k, v in zip(keys, values)]
    changed = dl.encode(raw, keys, replacement, extras)
    if dl.parse(changed) != (keys, replacement, extras):
        raise ValueError('rebuilt dialogue object failed read-back')
    ui_files = {}
    if ui_dir is not None:
        ui_dir = Path(ui_dir)
        if not ui_dir.is_dir():
            raise ValueError('UI locale path must be a directory')
        for file in ui_dir.iterdir():
            name = file.name.removesuffix('.json')
            if file.is_symlink() or not file.is_file() or file.suffix != '.json' or name not in ui.ASSETS:
                raise ValueError(f'unexpected UI locale file: {file.name}')
            _, rows = ui.scan(source / 'Contents/Resources/Data', name)
            ui_source = {key: row[2] for key, row in rows.items()}
            code, _ = ui_preservation.read_locale('macos', name, file, ui_source, ui.ASSETS[name])
            if code != requested:
                raise ValueError(f'UI locale {code} does not match {requested}')
            ui_files[name] = file
    settings = None
    prepared_settings = None
    if settings_file is not None:
        import settings_locale as settings
        prepared_settings = settings.make_asset(source / 'Contents/Resources/Data', settings_file, requested)
    profile_tool = None
    prepared_profile = None
    if test_profile_code is not None:
        import isolated_profile as profile_tool
        prepared_profile = profile_tool.prepare(source, test_profile_code)
    if test_caption_layout:
        if dl.sha((source / 'Contents/Resources/Data/sharedassets0.assets').read_bytes()) != ui.ASSETS['sharedassets0.assets']:
            raise ValueError('unsupported settings layout experiment source')
    replacements = {(obj.path_id, obj.type.name): changed}
    repaired_project = None
    if restore_yarn_transitions:
        import compare_yarn_versions as versions
        project_id = versions.BUILDS['macos']['project']
        projects = [o for o in env.objects if (o.path_id, o.type.name) == (project_id, 'MonoBehaviour')]
        if len(projects) != 1:
            raise ValueError('expected one macOS YarnProject for transition repair')
        project = projects[0]
        repaired_project = transitions.repair_project('macos', project.get_raw_data())
        project.set_raw_data(repaired_project)
        replacements[(project_id, project.type.name)] = repaired_project
    obj.set_raw_data(changed)
    data = env.file.save()
    destination.parent.mkdir(parents=True, exist_ok=True)
    # copytree creates the destination exclusively and never modifies the input.
    shutil.copytree(source, destination, symlinks=True)
    target = destination / ASSET_RELATIVE
    if target.is_symlink() or destination.resolve() not in target.resolve().parents or dl.sha(target.read_bytes()) != dl.ASSET_HASH:
        raise ValueError('copied source asset changed')
    temporary = target.with_name('sharedassets1.localized.tmp')
    with temporary.open('xb') as f:
        f.write(data)
    os.replace(temporary, target)
    import UnityPy
    reopened = UnityPy.load(str(target))
    before = {(o.path_id, o.type.name): o for o in env.objects}
    after = {(o.path_id, o.type.name): o for o in reopened.objects}
    if len(before) != len(env.objects) or len(after) != len(reopened.objects) or before.keys() != after.keys():
        raise ValueError('saved object inventory differs')
    for key, old in before.items():
        expected = replacements.get(key, old.get_raw_data())
        if expected != after[key].get_raw_data():
            raise ValueError(f'saved object differs: {key}')
    ui_count = 0
    contrast_assets = speaker_contrast.ASSETS if improve_speaker_contrast else frozenset()
    for name in sorted(ui_files.keys() | contrast_assets):
        target_ui = destination / 'Contents/Resources/Data' / name
        if target_ui.is_symlink() or destination.resolve() not in target_ui.resolve().parents:
            raise ValueError('unsafe UI destination')
        ui_count += ui.patch_into(source / 'Contents/Resources/Data', name, ui_files.get(name), requested,
                                  target_ui, changed if name == 'sharedassets1.assets' else None,
                                  repaired_project=repaired_project if name == 'sharedassets1.assets' else None,
                                  improve_speaker_contrast=name in contrast_assets)
    settings_count = 0
    if prepared_settings is not None:
        target_settings = destination / 'Contents/Resources/Data' / settings.ASSET
        if target_settings.is_symlink() or destination.resolve() not in target_settings.resolve().parents:
            raise ValueError('unsafe settings destination')
        settings_count = settings.patch_into(source / 'Contents/Resources/Data', target_settings,
                                             prepared_settings, ui_files.get(settings.ASSET))
    layout_hash = None
    if test_caption_layout:
        import experimental_settings_layout as layout
        target_layout = destination / 'Contents/Resources/Data' / layout.ASSET
        if target_layout.is_symlink() or destination.resolve() not in target_layout.resolve().parents:
            raise ValueError('unsafe test layout destination')
        layout_hash = layout.patch_into(source / 'Contents/Resources/Data', target_layout, requested,
                                        prior_ui=ui_files.get(layout.ASSET), prepared_settings=prepared_settings)
        experiment_marker = destination / 'Contents/Resources/vn-test-layout.json'
        with experiment_marker.open('x', encoding='utf-8') as f:
            json.dump({'schema': 1, 'testOnly': True, 'assetSha256': layout_hash,
                       'rectTransformPathId': 478, 'oldHeightDelta': -13, 'newHeightDelta': -3}, f)
            f.write('\n')
    slot_font_hash = None
    if test_slot_font:
        import experimental_slot_font as slot_font
        target_slot = destination / 'Contents/Resources/Data' / slot_font.ASSET
        if target_slot.is_symlink() or destination.resolve() not in target_slot.resolve().parents:
            raise ValueError('unsafe test slot font destination')
        slot_font_hash = slot_font.patch_into(source / 'Contents/Resources/Data', target_slot, requested,
                                              prior_ui=ui_files.get(slot_font.ASSET))
        experiment_marker = destination / 'Contents/Resources/vn-test-slot-font.json'
        with experiment_marker.open('x', encoding='utf-8') as f:
            json.dump({'schema': 1, 'testOnly': True, 'assetSha256': slot_font_hash,
                       'textPathIds': list(slot_font.TEXT_IDS), 'oldSize': 20, 'newSize': 18}, f)
            f.write('\n')
    profile = None
    if prepared_profile is not None:
        profile = profile_tool.apply(destination, prepared_profile)
    expected_assemblies = dict(source_assemblies)
    output_dlls = {name: data for name, (data, _) in managed_replacements.items()} | speaker_files
    for assembly, replacement_dll in output_dlls.items():
        copied_dll = destination / MANAGED_RELATIVE / assembly
        if assembly == speakers.COMPANION:
            with copied_dll.open('xb') as companion:
                companion.write(replacement_dll)
        else:
            if copied_dll.is_symlink() or dl.sha(copied_dll.read_bytes()) != source_assemblies[assembly]:
                raise ValueError('unexpected copied managed assembly')
            copied_dll.write_bytes(replacement_dll)
        expected_assemblies[assembly] = dl.sha(replacement_dll)
    # The distribution contains a loose Steam identifier in the bundle root;
    # macOS refuses to seal a bundle with this file there. Preserve it next to
    # the executable, then sign only the copy with an ad-hoc signature.
    steam = destination / 'steam_appid.txt'
    if steam.exists():
        target_steam = destination / 'Contents/MacOS/steam_appid.txt'
        if steam.is_symlink() or target_steam.exists() or destination.resolve() not in target_steam.parent.resolve().parents:
            raise ValueError('ambiguous Steam identifier')
        steam.rename(target_steam)
    else:
        raise ValueError('missing Steam identifier')
    marker = destination / 'Contents/Resources/vn-localization-build.json'
    with marker.open('x', encoding='utf-8') as f:
        json.dump({'schema': 1, 'locale': locale, 'sourceAssetSha256': dl.ASSET_HASH,
                   'steamFileSha256': dl.sha(target_steam.read_bytes())}, f, ensure_ascii=False)
        f.write('\n')
    if package_receipt is not None:
        receipt_path = marker.with_name('vn-localization-package.json')
        with receipt_path.open('x', encoding='utf-8') as f:
            json.dump(package_receipt, f, ensure_ascii=False, sort_keys=True, indent=2)
            f.write('\n')
    subprocess.run(['codesign', '--force', '--deep', '--sign', '-', str(destination)], check=True)
    subprocess.run(['codesign', '--verify', '--deep', '--strict', str(destination)], check=True)
    managed.compare(expected_assemblies, managed.scan(destination / MANAGED_RELATIVE))
    if dl.sha((destination / global_scripts).read_bytes()) != ui.GLOBAL_HASH:
        raise ValueError('candidate global scripts and localization settings changed')
    return {'locale': locale, 'translated': len(translations), 'sourceEntries': len(keys),
                      'dialogueAssetSha256BeforeUi': dl.sha(data), 'uiStrings': ui_count,
                      'settingsStrings': settings_count,
                      'testProfile': profile['code'] if profile else None,
                      'managedManifestSha256': managed_digest, 'preservedGlobalScriptsSha256': ui.GLOBAL_HASH,
                      'managedFallback': managed_replacements.get(managed_fallback.ASSEMBLY, (None, None))[1],
                      'managedSlotNew': managed_replacements.get(managed_fallback.SLOT_ASSEMBLY, (None, None))[1],
                      'managedSpeakers': speaker_report,
                      'speakerContrastAssets': sorted(contrast_assets),
                      'restoredYarnTransitions': len(transitions.CONTINUATIONS) if restore_yarn_transitions else 0,
                      'testSettingsLayoutSha256': layout_hash,
                      'testSlotFontSha256': slot_font_hash}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source-app', type=Path, required=True)
    p.add_argument('--locale-file', type=Path, required=True)
    p.add_argument('--locale', required=True, help='must exactly match the locale file')
    p.add_argument('--output-app', type=Path, required=True)
    p.add_argument('--ui-dir', type=Path, help='optional directory of named UI locale JSON files')
    p.add_argument('--settings-locale', type=Path, help='optional source-pinned settings locale JSON file')
    p.add_argument('--fallback-locale', type=Path, help='optional source-pinned missing-line locale JSON file')
    p.add_argument('--slot-new-locale', type=Path, help='optional source-pinned new-slot locale JSON file')
    p.add_argument('--managed-text-tool', '--fallback-tool', dest='fallback_tool', type=Path,
                   help='compiled managed-fallback.dll')
    p.add_argument('--speaker-locale', type=Path, help='source-pinned display names for Ryan and Conrad')
    p.add_argument('--speaker-tool', type=Path, help='compiled speaker-display-probe.dll')
    p.add_argument('--speaker-runtime', type=Path, help='compiled Dragons.SpeakerPresentation.dll')
    p.add_argument('--speaker-runtime-sha', help='SHA-256 of the compiled speaker runtime')
    p.add_argument('--speaker-contrast', action='store_true', help='use the audited black speaker label style')
    p.add_argument('--test-profile', help='optional fresh four-character isolated test profile; not a player release')
    p.add_argument('--test-settings-caption-layout', action='store_true',
                   help='experimental caption height for isolated test profiles only')
    p.add_argument('--test-slot-font', action='store_true',
                   help='experimental slot font size for isolated test profiles only')
    p.add_argument('--restore-yarn-transitions', action='store_true',
                   help='apply the source-pinned five-node Yarn repair to the output copy')
    a = p.parse_args()
    build(a.source_app, a.locale_file, a.locale, a.output_app, a.ui_dir, a.settings_locale,
          a.test_profile, a.test_settings_caption_layout, a.test_slot_font, a.restore_yarn_transitions,
          fallback_locale=a.fallback_locale, fallback_tool=a.fallback_tool, slot_new_locale=a.slot_new_locale,
          speaker_locale=a.speaker_locale, speaker_tool=a.speaker_tool, speaker_runtime=a.speaker_runtime,
          speaker_runtime_sha=a.speaker_runtime_sha, improve_speaker_contrast=a.speaker_contrast)


if __name__ == '__main__':
    main()
