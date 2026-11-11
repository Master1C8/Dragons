#!/usr/bin/env python3
"""Recreate an archived Dragons test artifact from a verified base."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import zipfile

import UnityPy

from build_windows_package import DATA_FOLDER, zip_member
import dialogue_locale as dialogue
from restore_probe_assets import read_receipt, sha256
from restore_yarn_probe_asset import raw_objects


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_member(archive, entry):
    with zipfile.ZipFile(archive) as source:
        data = source.read(entry['archiveMember'])
    if digest(data) != entry['sha256']:
        raise ValueError('Recovery member fingerprint mismatch')
    return data


def restore_object(base, object_entry, archive):
    if digest(base) != object_entry['baseAssetSha256']:
        raise ValueError('Base Unity asset fingerprint mismatch')
    asset = UnityPy.load(base)
    objects, before = raw_objects(asset)
    key = object_entry['pathId'], object_entry['type']
    if digest(before[key]) != object_entry['baseObjectSha256']:
        raise ValueError('Base Unity object fingerprint mismatch')
    changed = read_member(archive, object_entry)
    objects[key].set_raw_data(changed)
    data = asset.file.save()
    _, after = raw_objects(UnityPy.load(data))
    if after != {**before, key: changed} or digest(data) != object_entry['outputAssetSha256']:
        raise ValueError('Restored Unity asset fingerprint mismatch')
    return data


def restore_package(base, row, archive, output):
    if sha256(base) != row['basePackageSha256']:
        raise ValueError('Rebuilt base ZIP fingerprint mismatch')
    manifest = row['manifest']
    info = zip_member('manifest.json')
    if 'manifestZipMetadata' in row:
        metadata = row['manifestZipMetadata']
        info.date_time = tuple(metadata['dateTime'])
        info.external_attr = metadata['externalAttr']
    files = {f'{DATA_FOLDER}/{name}' for name in manifest['files']}
    if 'fontLicenseMember' in row:
        files.add(row['fontLicenseMember'])
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, sort_keys=True, indent=2) + '\n').encode()
    with zipfile.ZipFile(base) as source, zipfile.ZipFile(output, 'x') as target:
        if set(source.namelist()) != {'manifest.json', *files}:
            raise ValueError('Rebuilt base ZIP has unexpected entries')
        target.writestr(info, manifest_bytes)
        for name in sorted(files):
            member = zip_member(name)
            if name == row.get('member'):
                target.writestr(member, restore_object(source.read(name), row['unityObject'], archive))
            else:
                with source.open(name) as old, target.open(member, 'w') as new:
                    shutil.copyfileobj(old, new)


def restore_speaker(base, row, archive, output):
    fixture = json.loads(read_member(archive, row['inputMember']))
    asset, obj, original, keys, values, extras = dialogue.load_asset(base)
    if fixture['sourceObjectSha256'] != digest(original):
        raise ValueError('Legacy speaker fixture source fingerprint mismatch')
    source = dict(zip(keys, values))
    for key, entry in fixture['lines'].items():
        if source[key] != entry['source']:
            raise ValueError('Legacy speaker fixture line mismatch')
        values[keys.index(key)] = entry['text']
    obj.set_raw_data(dialogue.encode(original, keys, values, extras))
    output.write_bytes(asset.file.save())


def restore(row, base, archive, output):
    with tempfile.TemporaryDirectory(dir=output.parent) as temporary:
        restored = Path(temporary) / 'restored'
        if 'manifest' in row:
            restore_package(base, row, archive, restored)
        elif 'unityObject' in row:
            restored.write_bytes(restore_object(base.read_bytes(), row['unityObject'], archive))
        else:
            restore_speaker(base, row, archive, restored)
        if sha256(restored) != row['sha256']:
            raise ValueError('Historical control fingerprint mismatch')
        restored.chmod(int(row['mode'], 8))
        os.link(restored, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('name')
    parser.add_argument('--base', type=Path, required=True)
    parser.add_argument('--archive', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    row = next((item for item in receipt['outputs']
                if item['name'] == args.name and 'restoreMethod' in item), None)
    if row is None:
        parser.error(f'Unknown restorable control: {args.name}')
    if 'archive' in row:
        if args.archive is None or sha256(args.archive) != receipt['archives'][row['archive']]['sha256']:
            parser.error('Supply the verified recovery archive recorded for this control')
    restore(row, args.base, args.archive, args.output)
