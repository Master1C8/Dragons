#!/usr/bin/env python3
"""Restore a historical CJK font-only control from a verified stock asset."""

import argparse
import os
from pathlib import Path
import tempfile

import UnityPy

import inventory_yarn_bindings as bindings
import settings_locale as settings
from restore_probe_assets import read_receipt, sha256


def objects(asset):
    return {(obj.path_id, obj.type.name): obj for obj in asset.objects}


def expand_atlas(payload, stock, platform, object_id):
    asset = UnityPy.load(payload)
    asset.path = str(stock)
    obj = objects(asset)[object_id, 'MonoBehaviour']
    generator = bindings.generator(stock, platform)
    head, _, nodes = settings.nodes_for(obj, generator, {})
    tree = obj.read_typetree(nodes=nodes, check_read=True)
    settings.check_header(tree, head, object_id)
    if (tree['m_AtlasWidth'], tree['m_AtlasHeight']) != (512, 512):
        raise ValueError('Expected the original 512-pixel atlas')
    tree.update(
        m_AtlasWidth=1024, m_AtlasHeight=1024,
        m_FreeGlyphRects=[{'m_X': 0, 'm_Y': 0, 'm_Width': 1023, 'm_Height': 1023}],
    )
    obj.save_typetree(tree, nodes=nodes)
    return asset.file.save()


def restore(receipt, recorded_path, stock, base_asset, font, output):
    rows = read_receipt(receipt)['outputs']
    row = next((entry for entry in rows if entry['path'] == recorded_path), None)
    if row is None:
        raise ValueError(f'Unknown CJK test asset: {recorded_path}')
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    source = base_asset or stock / 'sharedassets0.assets'
    if sha256(source) != row['baseAssetSha256'] or sha256(font) != row['fontSha256']:
        raise ValueError('CJK probe input fingerprint mismatch')
    asset = UnityPy.load(str(source))
    key = row['fontObject'], 'Font'
    obj = objects(asset)[key]
    tree = obj.read_typetree(check_read=True)
    tree['m_FontData'] = font.read_bytes()
    obj.save_typetree(tree)
    payload = asset.file.save()
    if 'atlasObject' in row:
        payload = expand_atlas(payload, stock, row['platform'], row['atlasObject'])
    with tempfile.TemporaryDirectory(dir=output.parent) as staging:
        restored = Path(staging) / source.name
        restored.write_bytes(payload)
        if sha256(restored) != row['sha256']:
            raise ValueError('Restored CJK probe fingerprint mismatch')
        restored.chmod(int(row['mode'], 8))
        os.link(restored, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    parser.add_argument('--stock', type=Path, required=True)
    parser.add_argument('--base-asset', type=Path)
    parser.add_argument('--font', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    restore(args.receipt, args.recorded_path, args.stock, args.base_asset, args.font, args.output)
