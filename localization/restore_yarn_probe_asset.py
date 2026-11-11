#!/usr/bin/env python3
"""Rebuild a synthetic missing-line test asset from stock Unity data."""

import argparse
import os
from pathlib import Path
import tempfile

import UnityPy

import compare_yarn_versions as yarn
from restore_probe_assets import read_receipt, sha256


def raw_objects(asset):
    objects = {(obj.path_id, obj.type.name): obj for obj in asset.objects}
    if len(objects) != len(asset.objects):
        raise ValueError('Duplicate serialized Unity object identity')
    return objects, {key: obj.get_raw_data() for key, obj in objects.items()}


def restore(receipt, recorded_path, stock, output):
    rows = read_receipt(receipt)['outputs']
    row = next((item for item in rows if item['path'] == recorded_path), None)
    if row is None:
        raise ValueError(f'Unknown historical test asset: {recorded_path}')
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    spec = yarn.BUILDS[row['platform']]
    keys, _, _, program, nodes, _ = yarn.load(stock, spec)
    old = row['sourceLine'].encode('ascii')
    new = b'line:00000000'
    if (len(old) != len(new) or program.count(old) != 1
            or nodes[row['node']].count(old) != 1 or new in program or new.decode() in keys):
        raise ValueError('Unexpected stock Yarn line or node')
    asset = UnityPy.load(str(stock / 'sharedassets1.assets'))
    objects, before = raw_objects(asset)
    identity = spec['project'], 'MonoBehaviour'
    original = before[identity]
    if original.count(old) != 1 or new in original:
        raise ValueError('Unexpected serialized Yarn program')
    changed = original.replace(old, new, 1)
    objects[identity].set_raw_data(changed)
    with tempfile.TemporaryDirectory(dir=output.parent) as staging:
        restored = Path(staging) / 'sharedassets1.assets'
        restored.write_bytes(asset.file.save())
        _, after = raw_objects(UnityPy.load(str(restored)))
        if after != {**before, identity: changed} or sha256(restored) != row['sha256']:
            raise ValueError('Restored test asset fingerprint mismatch')
        restored.chmod(int(row['mode'], 8))
        os.link(restored, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    parser.add_argument('--stock', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    restore(args.receipt, args.recorded_path, args.stock, args.output)
