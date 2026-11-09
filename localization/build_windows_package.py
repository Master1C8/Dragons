#!/usr/bin/env python3
"""Compose verified Windows localization replacements into one fresh ZIP."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

import compare_yarn_versions as versions
import dialogue_locale as dl
import inventory_non_yarn_scope as non_yarn
import inventory_yarn_scope as yarn
import managed_fallback
import speaker_contrast
import speaker_locale
import windows_ui_locale as assets
from assemble_source_inventory import INVENTORY_SHA, load_pinned

PLATFORM = 'windows'
DATA_FOLDER = 'DragNWash_Data'
YARN_SCOPE_SHA = '753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30'
ASSET_HASHES = assets.ui_map.WINDOWS_ASSETS
LOCALE_FILES = ('dialogue.json', 'speakers.json', 'settings.json', 'slot-new.json', 'missing-line.json')


def snapshot_inputs(source, target):
    source, target = Path(source), Path(target)
    ui = source / 'ui'
    if source.is_symlink() or ui.is_symlink() or not ui.is_dir():
        raise ValueError('expected real locale input and UI directories')
    (target / 'ui').mkdir(parents=True)
    files = [Path(name) for name in LOCALE_FILES]
    for path in sorted(ui.iterdir()):
        if path.suffix != '.json' or path.stem not in ASSET_HASHES:
            raise ValueError(f'unexpected UI locale file: {path.name}')
        files.append(Path('ui') / path.name)
    if {path.name for path in source.iterdir()} != {*LOCALE_FILES, 'ui'}:
        raise ValueError('locale directory differs from the Windows input layout')
    for name in files:
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'expected a real locale input file: {name}')
        (target / name).write_bytes(path.read_bytes())


def file_digest(stream):
    return hashlib.file_digest(stream, 'sha256').hexdigest()


def zip_member(name):
    info = zipfile.ZipInfo(name)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    info.external_attr = 0o100644 << 16
    return info


def archive_payload(archive, payload, manifest):
    members = {f'{DATA_FOLDER}/{name}': payload / name for name in manifest['files']}
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    with zipfile.ZipFile(archive, 'x') as package:
        package.writestr(zip_member('manifest.json'), manifest_bytes)
        for name, path in sorted(members.items()):
            with path.open('rb') as source, package.open(zip_member(name), 'w') as output:
                shutil.copyfileobj(source, output)
    with zipfile.ZipFile(archive) as package:
        if package.namelist() != ['manifest.json', *sorted(members)]:
            raise ValueError('Windows ZIP has missing, duplicate or unexpected entries')
        if package.read('manifest.json') != manifest_bytes:
            raise ValueError('Windows ZIP manifest differs from verified inputs')
        for name in members:
            relative = name.removeprefix(f'{DATA_FOLDER}/')
            with package.open(name) as stream:
                if file_digest(stream) != manifest['files'][relative]['outputSha256']:
                    raise ValueError(f'Windows ZIP member differs from verified output: {name}')


def build(data, inputs, requested, inventory, scope_path, output, *,
          managed_tool, speaker_tool, speaker_runtime, speaker_runtime_sha):
    data = Path(data).resolve(strict=True)
    target = assets.safe_output(data, output)
    if target.suffix.lower() != '.zip':
        raise ValueError('Windows output must be a .zip')
    scope = load_pinned(scope_path, YARN_SCOPE_SHA)
    entries = load_pinned(inventory, INVENTORY_SHA)['entries']
    with tempfile.TemporaryDirectory(prefix='.dragons-windows-', dir=target.parent) as temporary:
        stage = Path(temporary)
        local = stage / 'locale'
        snapshot_inputs(inputs, local)
        dialogue, speakers = (local / name for name in LOCALE_FILES[:2])
        yarn_receipt = yarn.validate_complete(scope, PLATFORM, data, requested, dialogue, speakers)
        non_yarn_receipt = non_yarn.verify_platform(entries, PLATFORM, data, requested, local)
        manifest = {
            'schema': 1, 'kind': 'windows-localization-replacements',
            'platform': PLATFORM, 'build': versions.BUILDS[PLATFORM]['version'],
            'locale': requested, 'sharedInventorySha256': INVENTORY_SHA, 'yarnScopeSha256': YARN_SCOPE_SHA,
            'localeInputSha256': {
                'dialogue.json': yarn_receipt['inputSha256']['dialogue'],
                'speakers.json': yarn_receipt['inputSha256']['speakers'],
                **non_yarn_receipt['localeInputSha256'],
            },
            'sourceGlobalManagersSha256': versions.BUILDS[PLATFORM]['globalSha256'],
            'sourceGlobalScriptsSha256': assets.ui_map.WINDOWS_GLOBAL,
            'sourceManagedManifestSha256': non_yarn_receipt['sourceManagedManifestSha256'],
            'files': {},
        }
        files = manifest['files']
        payload = stage / 'payload'
        managed = payload / 'Managed'
        managed.mkdir(parents=True)
        ui_assets = {asset for asset, roles in non_yarn_receipt['ui'].items() if roles['translate']}
        all_assets = ui_assets | {'sharedassets0.assets', 'sharedassets1.assets'} | speaker_contrast.ASSETS
        for asset in sorted(all_assets):
            report = assets.build(
                data, asset, local / 'ui' / f'{asset}.json' if asset in ui_assets else None,
                requested, payload / asset,
                dialogue_locale_file=dialogue if asset == 'sharedassets1.assets' else None,
                settings_locale_file=local / 'settings.json' if asset == 'sharedassets0.assets' else None,
                restore_yarn_transitions=asset == 'sharedassets1.assets',
                improve_speaker_contrast=asset in speaker_contrast.ASSETS,
            )
            files[asset] = {key: report[key] for key in ('sourceSha256', 'outputSha256')}
        patched, speaker_report = speaker_locale.prepare(
            PLATFORM, data / 'Managed' / managed_fallback.ASSEMBLY, speakers, requested,
            speaker_tool, speaker_runtime, speaker_runtime_sha, fallback_locale=local / 'missing-line.json',
        )
        slot, slot_report = managed_fallback.prepare(
            PLATFORM, data / 'Managed' / managed_fallback.SLOT_ASSEMBLY, local / 'slot-new.json',
            requested, managed_tool, slot_new=True,
        )
        patched[managed_fallback.SLOT_ASSEMBLY] = slot
        managed_digests = {
            managed_fallback.ASSEMBLY: (speaker_report['sourceSha256'], speaker_report['outputSha256']),
            managed_fallback.SLOT_ASSEMBLY: (slot_report['sourceSha256'], slot_report['outputSha256']),
            speaker_locale.COMPANION: (None, speaker_report['inlineRuntimeSha256']),
        }
        if patched.keys() != managed_digests.keys():
            raise ValueError('unexpected Windows managed replacement paths')
        for name, raw in patched.items():
            before, after = managed_digests[name]
            (managed / name).write_bytes(raw)
            files[f'Managed/{name}'] = {'sourceSha256': before, 'outputSha256': after}
        archive = stage / 'payload.zip'
        archive_payload(archive, payload, manifest)
        with archive.open('rb') as stream:
            digest = file_digest(stream)
        # Keep a competing output intact and publish only the complete verified archive.
        os.link(archive, target)
    return {'output': str(target), 'sha256': digest, 'manifest': manifest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_data', type=Path)
    parser.add_argument('locale_inputs', type=Path)
    parser.add_argument('--locale', required=True)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--yarn-scope', type=Path, required=True)
    parser.add_argument('--managed-tool', type=Path, required=True)
    parser.add_argument('--speaker-tool', type=Path, required=True)
    parser.add_argument('--speaker-runtime', type=Path, required=True)
    parser.add_argument('--speaker-runtime-sha', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(
        args.source_data, args.locale_inputs, args.locale, args.inventory, args.yarn_scope, args.output,
        managed_tool=args.managed_tool, speaker_tool=args.speaker_tool, speaker_runtime=args.speaker_runtime,
        speaker_runtime_sha=args.speaker_runtime_sha,
    ), ensure_ascii=False))


if __name__ == '__main__':
    main()
