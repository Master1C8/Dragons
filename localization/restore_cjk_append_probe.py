#!/usr/bin/env python3
"""Restore either version of the historical Japanese fallback control."""

import argparse
import os
from pathlib import Path
import shutil
import tempfile

import UnityPy

import cjk_font_fallback as cjk
from restore_probe_assets import read_receipt, sha256
from restore_release_probe_assets import Archive


def original_shader_size(staged, material_id):
    asset = UnityPy.load(str(staged))
    material = asset.file.objects[material_id]
    tree = material.read_typetree(check_read=True)
    props = tree['m_SavedProperties']
    sizes = {'_TextureWidth', '_TextureHeight'}
    if {key: value for key, value in props['m_Floats'] if key in sizes} != dict.fromkeys(sizes, 1024.0):
        raise ValueError('Unexpected aligned shader dimensions')
    props['m_Floats'] = [(key, 512.0 if key in sizes else value) for key, value in props['m_Floats']]
    material.save_typetree(tree)
    staged.write_bytes(asset.file.save())


def restore(row, stock, accepted, font, license, output):
    platform = row['platform']
    stock = stock.resolve(strict=True)
    if sha256(font) != row['fontSha256']:
        raise ValueError('Unexpected Japanese font fingerprint')
    resource = cjk.prepare('ja', font, license)
    with tempfile.TemporaryDirectory(dir=output.parent) as temporary:
        staged = Path(temporary) / cjk.ASSET
        if platform == 'macos':
            Archive(accepted.resolve(strict=True)).restore_asset(
                platform, 'ru', cjk.ASSET, row['baseAssetSha256'], stock, staged)
        else:
            shutil.copyfile(stock / cjk.ASSET, staged)
        if sha256(staged) != row['baseAssetSha256']:
            raise ValueError('Unexpected staged source fingerprint')
        receipt = cjk.add(platform, stock, staged, resource)
        if receipt['fallbackPathId'] - 2 != row['materialPathId']:
            raise ValueError('Unexpected Japanese material object')
        if row['variant'] == 'baseline':
            original_shader_size(staged, row['materialPathId'])
        if sha256(staged) != row['sha256']:
            raise ValueError('Restored Japanese control fingerprint mismatch')
        staged.chmod(int(row['mode'], 8))
        os.link(staged, output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('name')
    for arg in ('stock', 'accepted', 'font', 'license', 'output'):
        parser.add_argument('--' + arg, type=Path, required=True)
    args = parser.parse_args()
    row = next((item for item in read_receipt(args.receipt)['appendVariants']
                if item['name'] == args.name), None)
    if row is None:
        parser.error(f'Unknown CJK append variant: {args.name}')
    restore(row, args.stock, args.accepted, args.font, args.license, args.output)
