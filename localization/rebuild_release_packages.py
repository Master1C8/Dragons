#!/usr/bin/env python3
"""Build Dragons platform packages from the 0.2.1 recovery inputs."""

import argparse
import hashlib
import json
from pathlib import Path

import build_macos_package
import build_windows_package
import cjk_font_fallback
import complex_text


ROOT = Path(__file__).resolve().parents[1]
MAC_RESOURCES = Path('macos/Dragons — VN Revival.app/Contents/Resources') / (
    'DragonsInstaller_DragonsInstaller.bundle/Contents/Resources'
)
WINDOWS_RESOURCES = Path('windows/Dragons Windows/Resources')
SHAPED_REPORT = '73d128727531f04feb2990e9b369d7da196ca7746254109f695eaa3a428a5ae4'


def sha256(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def archived_file(payload, row, name):
    record = next(item for item in row['files'] if item['path'] == 'Managed/' + name)
    path = (payload / record['payloadPath']).resolve(strict=True)
    if not path.is_relative_to(payload.resolve()) or path.name != name:
        raise ValueError(f'Invalid archived file path for {name}')
    digest = sha256(path)
    if digest != record['payloadSHA256'] or digest != record['artifactSHA256']:
        raise ValueError(f'Archived file fingerprint mismatch for {name}')
    return path, digest


def build(args):
    resources = args.accepted / (MAC_RESOURCES if args.platform == 'macos' else WINDOWS_RESOURCES)
    payload = resources / 'LocalizationPayload'
    released = {r['siteLocale']: r for r in json.loads((resources / 'PackageConfig.json').read_bytes())['languages']}
    pins = {r['siteLocale']: r for r in json.loads((ROOT / 'installer/App/LocalePackages.json').read_bytes())['locales']}
    row = released[args.locale]
    runtime, runtime_sha = archived_file(payload, row, 'Dragons.SpeakerPresentation.dll')
    inputs = args.inputs or ROOT / 'localization' / args.locale / 'translation.json'
    if args.inputs is None and sha256(inputs) != pins[args.locale]['translationSha256']:
        raise ValueError('Translation differs from the 0.2.1 recovery manifest')
    opts = {
        'managed_tool': args.tools / 'managed-fallback/managed-fallback.dll',
        'speaker_tool': args.tools / 'speaker-display-probe/speaker-display-probe.dll',
        'speaker_runtime': runtime,
        'speaker_runtime_sha': runtime_sha,
    }
    licenses = payload / 'Licenses' / args.locale
    if args.locale in cjk_font_fallback.FONTS:
        opts['cjk_font'] = args.fonts / 'cjk' / f'{args.locale}.otf'
        opts['cjk_license'] = licenses / cjk_font_fallback.LICENSE
    if args.locale in complex_text.FONTS:
        layout, layout_sha = archived_file(payload, row, complex_text.LAYOUT)
        opts['complex_inputs'] = complex_text.Inputs(
            args.fonts / 'shaped', SHAPED_REPORT, licenses / complex_text.LICENSE,
            args.tools / 'prepared-text-probe/prepared-text-probe.dll', layout, layout_sha,
        )
    builder = build_macos_package if args.platform == 'macos' else build_windows_package
    return builder.build(
        args.stock, inputs, args.locale,
        args.v42 / 'combined-provisional-v42-20261110.json', args.v42 / 'yarn-scope-v42.json',
        args.output, **opts,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=('macos', 'windows'))
    parser.add_argument('locale')
    for name in ('stock', 'accepted', 'v42', 'fonts', 'tools', 'output'):
        parser.add_argument('--' + name, required=True, type=Path)
    parser.add_argument('--inputs', type=Path, help='Optional preserved per-platform locale input directory')
    build(parser.parse_args())


if __name__ == '__main__':
    main()
