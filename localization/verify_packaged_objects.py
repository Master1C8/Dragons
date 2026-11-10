#!/usr/bin/env python3
"""Read the Unity object payloads from a complete text-only locale package."""
import argparse
import json
from pathlib import Path
import shutil
import tempfile
import zipfile

import UnityPy

import build_game
from build_windows_package import DATA_FOLDER
import dialogue_locale as dialogue
import package_inputs
import speaker_contrast
import ui_locale as mac_ui
import ui_preservation
import verify_combined_settings_ui as settings
import verify_combined_yarn_ui as yarn
import verify_serialized_metadata as metadata
import windows_ui_locale as win_ui

def verify_scene(platform, stock, asset, candidate, locale, locale_file):
    adapter = mac_ui if platform == 'macos' else win_ui
    source, rows = adapter.scan(stock, asset)
    source_objects = settings.object_map(source)
    expected = {key: obj.get_raw_data() for key, obj in source_objects.items()}
    changes = {}
    if locale_file is not None:
        source_text = {key: row[2] for key, row in rows.items()}
        code, replacements = ui_preservation.read_locale(
            platform, asset, locale_file, source_text, metadata.ASSETS[platform][asset],
        )
        if code != locale:
            raise ValueError(f'{asset}: unexpected UI locale')
        for key, value in replacements.items():
            obj, raw, _, end = rows[key]
            changes[(obj.path_id, obj.type.name)] = raw[:88] + dialogue.write_string(value) + raw[end:]
    if asset in speaker_contrast.ASSETS:
        speaker_contrast.apply(platform, asset, source_objects, changes)
    actual = settings.object_map(UnityPy.load(str(candidate)))
    if actual.keys() != expected.keys():
        raise ValueError(f'{asset}: packaged object inventory differs')
    for identity, raw in expected.items():
        if actual[identity].get_raw_data() != changes.get(identity, raw):
            raise ValueError(f'{asset}: packaged object bytes differ: {identity}')
    return {'verifiedObjects': len(expected), 'checkedTargetObjects': len(changes)}


def verify_data(platform, source, inputs, requested, candidate, assets):
    def ui_input(asset):
        file = inputs / 'ui' / f'{asset}.json'
        return file if file.is_file() else None

    results = {}
    for name in sorted(assets):
        path = candidate / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'expected a regular packaged asset: {name}')
        if name == 'sharedassets1.assets':
            results[name] = yarn.verify(platform, source, path, requested, inputs / 'dialogue.json',
                                        ui_input(name), restore_yarn_transitions=True)
        elif name == 'sharedassets0.assets':
            results[name] = settings.verify(platform, source, path, requested, inputs / 'settings.json', ui_input(name))
        else:
            results[name] = verify_scene(platform, source, name, path, requested, ui_input(name))
    return results


def verify(platform, source, inputs, requested, inventory, scope, candidate):
    source, candidate = Path(source), Path(candidate)
    if source.is_symlink() or candidate.is_symlink():
        raise ValueError('expected real source and package paths')
    if source.resolve(strict=True) == candidate.resolve(strict=True):
        raise ValueError('source and package must be separate')
    hashes = metadata.ASSETS[platform]
    relative = build_game.ASSET_RELATIVE.parent
    stock = source / relative if platform == 'macos' else source
    scratch = Path(__file__).resolve().parent / 'work'
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='packaged-objects-', dir=scratch) as directory:
        stage = Path(directory)
        local = stage / 'locale'
        package_inputs.prepare_inputs(inputs, local, hashes, platform, requested, inventory, scope)
        receipt, ui_assets = package_inputs.validate(platform, stock, requested, local, inventory, scope)
        assets = ui_assets | speaker_contrast.ASSETS | {'sharedassets0.assets', 'sharedassets1.assets'}
        if platform == 'macos':
            results = verify_data(platform, stock, local, requested, candidate / relative, hashes)
        else:
            extracted = stage / 'payload'
            extracted.mkdir()
            with zipfile.ZipFile(candidate) as archive:
                names = archive.namelist()
                packaged_assets = {f'{DATA_FOLDER}/{name}' for name in hashes}.intersection(names)
                expected = {f'{DATA_FOLDER}/{name}' for name in assets}
                if packaged_assets != expected or any(names.count(name) != 1 for name in expected):
                    raise ValueError('Windows packaged Unity asset inventory differs')
                for name in sorted(assets):
                    with archive.open(f'{DATA_FOLDER}/{name}') as data, (extracted / name).open('xb') as output:
                        shutil.copyfileobj(data, output)
            results = verify_data(platform, stock, local, requested, extracted, assets)
    return {'schema': 1, 'platform': platform, 'locale': requested,
            'localeInputSha256': receipt['localeInputSha256'], 'assets': results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=metadata.ASSETS)
    parser.add_argument('source', type=Path, help='stock app bundle on macOS or stock Data directory on Windows')
    parser.add_argument('locale_inputs', type=Path)
    parser.add_argument('package', type=Path, help='built app on macOS or ZIP on Windows')
    parser.add_argument('--locale', required=True)
    parser.add_argument('--inventory', required=True, type=Path)
    parser.add_argument('--yarn-scope', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.platform, args.source, args.locale_inputs, args.locale,
                            args.inventory, args.yarn_scope, args.package), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
