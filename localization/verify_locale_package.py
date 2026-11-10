#!/usr/bin/env python3
"""Verify an actual locale package against the pinned source and authored inputs."""
import argparse
from contextlib import redirect_stdout
import json
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import zipfile

import build_macos_package as macos
import build_windows_package as windows
import cjk_font_fallback as cjk
import complex_text
import verify_serialized_metadata as serialized


def bundle_files(bundle):
    files = {}
    for path in sorted(bundle.rglob('*')):
        name = path.relative_to(bundle).as_posix()
        mode = path.lstat().st_mode
        if stat.S_ISLNK(mode):
            files[name] = ('link', str(path.readlink()))
        elif stat.S_ISREG(mode):
            with path.open('rb') as stream:
                files[name] = ('file', stat.S_IMODE(mode), windows.file_digest(stream))
        elif stat.S_ISDIR(mode):
            files[name] = ('directory',)
        else:
            raise ValueError(f'unsupported bundle entry: {name}')
    return files


def compare_bundle(expected, candidate):
    reference, actual = bundle_files(expected), bundle_files(candidate)
    if reference.keys() != actual.keys():
        name = min(reference.keys() ^ actual.keys())
        raise ValueError(f'bundle path inventory differs: {name}')
    for name, value in reference.items():
        if actual[name] != value:
            raise ValueError(f'bundle entry differs from verified rebuild: {name}')
    return {'verifiedBundleFiles': sum(row[0] == 'file' for row in reference.values())}


def compare_archive(expected, candidate):
    with zipfile.ZipFile(expected) as reference, zipfile.ZipFile(candidate) as actual:
        if reference.namelist() != actual.namelist():
            raise ValueError('archive member inventory or order differs')
        for original, received in zip(reference.infolist(), actual.infolist(), strict=True):
            if (received.create_system, received.external_attr) != (original.create_system, original.external_attr):
                raise ValueError(f'archive member type or permissions differ: {original.filename}')
            with reference.open(original) as before, actual.open(received) as after:
                if windows.file_digest(before) != windows.file_digest(after):
                    raise ValueError(f'archive member differs from verified rebuild: {original.filename}')
        return {'verifiedArchiveMembers': len(reference.infolist())}


def verify(platform, source, inputs, requested, inventory, scope, candidate, **tools):
    if platform not in ('macos', 'windows'):
        raise ValueError(f'unsupported package platform: {platform}')
    candidate = Path(candidate)
    if candidate.is_symlink() or (platform == 'macos' and not candidate.is_dir()) or (
            platform == 'windows' and not candidate.is_file()):
        raise ValueError('expected a real candidate package')
    # Both font paths use the same four-object fallback adapter.
    has_font = tools.get('cjk_font') is not None or tools.get('complex_inputs') is not None
    added_object_asset = cjk.ASSET if has_font else None
    scratch = Path(__file__).resolve().parent / 'work'
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='package-verify-', dir=scratch) as directory:
        reference = Path(directory) / ('Reference.app' if platform == 'macos' else 'Reference.zip')
        builder = macos if platform == 'macos' else windows
        with redirect_stdout(sys.stderr):
            report = builder.build(source, inputs, requested, inventory, scope, reference, **tools)
        if platform == 'macos':
            comparison = compare_bundle(reference, candidate)
            subprocess.run(['codesign', '--verify', '--deep', '--strict', str(candidate)], check=True)
            relative_data = macos.build_game.ASSET_RELATIVE.parent
            metadata = serialized.verify(platform, Path(source) / relative_data,
                                         lambda name: (candidate / relative_data / name).read_bytes(),
                                         added_object_asset=added_object_asset)
        else:
            comparison = compare_archive(reference, candidate)
            with zipfile.ZipFile(candidate) as archive:
                metadata = serialized.verify(platform, Path(source),
                                             lambda name: archive.read(f'{windows.DATA_FOLDER}/{name}'),
                                             added_object_asset=added_object_asset)
    return {'platform': platform, 'locale': requested, **comparison,
            'componentPreservation': report['componentPreservation'],
            'serializedMetadataPreservation': metadata}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=('macos', 'windows'))
    parser.add_argument('source', type=Path, help='stock macOS app or Windows Data directory')
    parser.add_argument('locale_inputs', type=Path, help='exact shared file or platform input directory used for the package')
    parser.add_argument('candidate', type=Path, help='built macOS app or Windows ZIP')
    parser.add_argument('--locale', required=True)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--yarn-scope', type=Path, required=True)
    parser.add_argument('--managed-tool', type=Path, required=True)
    parser.add_argument('--speaker-tool', type=Path, required=True)
    parser.add_argument('--speaker-runtime', type=Path, required=True)
    parser.add_argument('--speaker-runtime-sha', required=True)
    parser.add_argument('--cjk-font', type=Path)
    parser.add_argument('--cjk-license', type=Path)
    complex_text.add_arguments(parser)
    args = parser.parse_args()
    print(json.dumps(verify(
        args.platform, args.source, args.locale_inputs, args.locale, args.inventory, args.yarn_scope,
        args.candidate, managed_tool=args.managed_tool, speaker_tool=args.speaker_tool,
        speaker_runtime=args.speaker_runtime, speaker_runtime_sha=args.speaker_runtime_sha,
        cjk_font=args.cjk_font, cjk_license=args.cjk_license, complex_inputs=complex_text.arguments(args),
    ), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
