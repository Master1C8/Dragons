#!/usr/bin/env python3
"""Rebuild a synthetic missing-line test asset from stock Unity data."""

import argparse
import hashlib
import os
from pathlib import Path
import struct
import tempfile

import UnityPy

import compare_yarn_versions as yarn
from restore_probe_assets import read_receipt, sha256
from yarn_transition_repair import PROGRAM_OFFSET, PROGRAM_SIZE_OFFSET


def raw_objects(asset):
    objects = {(obj.path_id, obj.type.name): obj for obj in asset.objects}
    if len(objects) != len(asset.objects):
        raise ValueError('Duplicate serialized Unity object identity')
    return objects, {key: obj.get_raw_data() for key, obj in objects.items()}


def stock_edit(row, stock, spec, original):
    keys, _, _, program, nodes, _ = yarn.load(stock, spec)
    old = row['sourceLine'].encode('ascii')
    new = b'line:00000000'
    if (len(old) != len(new) or program.count(old) != 1
            or nodes[row['node']].count(old) != 1 or new in program or new.decode() in keys):
        raise ValueError('Unexpected stock Yarn line or node')
    if original.count(old) != 1 or new in original:
        raise ValueError('Unexpected serialized Yarn program')
    return original.replace(old, new, 1)


def packaged_edit(row, original):
    size, = struct.unpack_from('<I', original, PROGRAM_SIZE_OFFSET)
    start = PROGRAM_OFFSET
    program = original[start:start + size]
    nodes, _ = yarn.program_nodes(program)
    node = nodes[row['node']]
    changed = node
    for source, target in row['lineSwaps']:
        old, new = source.encode('ascii'), target.encode('ascii')
        if len(old) != len(new) or changed.count(old) != 1 or new in changed:
            raise ValueError('Unexpected packaged Yarn operand')
        changed = changed.replace(old, new, 1)
    if program.count(node) != 1:
        raise ValueError('Unexpected packaged Yarn node')
    edited = program.replace(node, changed, 1)
    checked, _ = yarn.program_nodes(edited)
    if checked != {**nodes, row['node']: changed} or hashlib.sha256(edited).hexdigest() != row['programSha256']:
        raise ValueError('Rebuilt Yarn program fingerprint mismatch')
    return original[:start] + edited + original[start + size:]


def restore(receipt, recorded_path, stock, base_asset, output):
    rows = read_receipt(receipt)['outputs']
    row = next((item for item in rows if item['path'] == recorded_path), None)
    if row is None:
        raise ValueError(f'Unknown historical test asset: {recorded_path}')
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    spec = yarn.BUILDS[row['platform']]
    if 'baseAssetSha256' in row:
        if base_asset is None or sha256(base_asset) != row['baseAssetSha256']:
            raise ValueError('Packaged base asset fingerprint mismatch')
    else:
        if stock is None:
            raise ValueError('Supply the stock Data directory')
        base_asset = stock / 'sharedassets1.assets'
    asset = UnityPy.load(str(base_asset))
    objects, before = raw_objects(asset)
    identity = spec['project'], 'MonoBehaviour'
    original = before[identity]
    changed = packaged_edit(row, original) if 'baseAssetSha256' in row else stock_edit(row, stock, spec, original)
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
    base = parser.add_mutually_exclusive_group(required=True)
    base.add_argument('--stock', type=Path)
    base.add_argument('--base-asset', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    restore(args.receipt, args.recorded_path, args.stock, args.base_asset, args.output)
