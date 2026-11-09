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
import managed_fallback
import package_inputs
import speaker_contrast
import speaker_locale
import windows_ui_locale as assets

PLATFORM = 'windows'
DATA_FOLDER = 'DragNWash_Data'
ASSET_HASHES = assets.ui_map.WINDOWS_ASSETS


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
    with tempfile.TemporaryDirectory(prefix='.dragons-windows-', dir=target.parent) as temporary:
        stage = Path(temporary)
        local = stage / 'locale'
        package_inputs.snapshot_inputs(inputs, local, ASSET_HASHES)
        dialogue, speakers = local / 'dialogue.json', local / 'speakers.json'
        receipt, ui_assets = package_inputs.validate(PLATFORM, data, requested, local, inventory, scope_path)
        manifest = {
            'schema': 1, 'kind': 'windows-localization-replacements',
            'platform': PLATFORM, 'build': versions.BUILDS[PLATFORM]['version'],
            'locale': requested, **receipt,
            'sourceGlobalManagersSha256': versions.BUILDS[PLATFORM]['globalSha256'],
            'sourceGlobalScriptsSha256': assets.ui_map.WINDOWS_GLOBAL,
            'files': {},
        }
        files = manifest['files']
        payload = stage / 'payload'
        managed = payload / 'Managed'
        managed.mkdir(parents=True)
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
