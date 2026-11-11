#!/usr/bin/env python3
"""Restore a released asset in a historical test copy without running the game."""

import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

from restore_probe_assets import read_receipt, sha256


MAC = Path('macos/Dragons — VN Revival.app/Contents/Resources') / (
    'DragonsInstaller_DragonsInstaller.bundle/Contents/Resources'
)
WINDOWS = Path('windows/Dragons Windows/Resources')


def safe_member(root, name):
    if any(part in ('', '.', '..') for part in name.split('/')):
        raise ValueError(f'Invalid member path: {name}')
    path = root / name
    if path.resolve() != path or not path.is_file():
        raise ValueError(f'Missing or redirected archive member: {path}')
    return path


class Archive:
    def __init__(self, accepted):
        self.resources = {'macos': accepted / MAC, 'windows': accepted / WINDOWS}
        self.config = {p: json.loads((r / 'PackageConfig.json').read_bytes())
                       for p, r in self.resources.items()}
        self.decoder = safe_member(self.resources['macos'] / 'LocalizationPayload', 'Tools/xdelta3')
        if sha256(self.decoder) != self.config['macos']['deltaToolSHA256']:
            raise ValueError('Unexpected release decoder fingerprint')

    def restore_asset(self, platform, locale, relative, digest, stock, target):
        language = next(x for x in self.config[platform]['languages'] if x['siteLocale'] == locale)
        record = next(x for x in language['files'] if x['path'] == relative)
        if record['payloadSHA256'] != digest:
            raise ValueError(f'Receipt does not match the release: {relative}')
        payload = self.resources[platform] / 'LocalizationPayload'
        if record.get('artifacts'):
            source = safe_member(stock, relative)
            if sha256(source) != record['originalSHA256']:
                raise ValueError(f'Stock input fingerprint mismatch: {relative}')
            for index, item in enumerate(record['artifacts']):
                patch = safe_member(payload, item['path'])
                if sha256(patch) != item['sha256']:
                    raise ValueError(f'Delta fingerprint mismatch: {relative}')
                output = target if index == len(record['artifacts']) - 1 else target.with_name(f'step-{index}')
                subprocess.run([str(self.decoder), '-d', '-f', '-s', str(source), str(patch), str(output)], check=True)
                source = output
        else:
            source = safe_member(payload, record['payloadPath'])
            if sha256(source) != record['artifactSHA256']:
                raise ValueError(f'Payload fingerprint mismatch: {relative}')
            shutil.copyfile(source, target)
        if sha256(target) != digest:
            raise ValueError(f'Restored asset fingerprint mismatch: {relative}')


def restore(receipt, accepted, mac_stock, windows_stock, prefix):
    root = Path(__file__).resolve().parents[1]
    prefix = (root / prefix).resolve(strict=True)
    if not prefix.is_relative_to(root / 'localization/work'):
        raise ValueError('Select a retained test directory within localization/work')
    archive = Archive(accepted.resolve(strict=True))
    stock = {'macos': mac_stock.resolve(strict=True), 'windows': windows_stock.resolve(strict=True)}
    count = 0
    for item in read_receipt(receipt)['assets']:
        target = root / item['path']
        if not target.is_relative_to(prefix):
            continue
        if target.resolve() != target or target.name != Path(item['relative']).name:
            raise ValueError(f'Unexpected target path: {target}')
        if target.exists():
            if not target.is_file() or sha256(target) != item['sha256']:
                raise FileExistsError(target)
            continue
        with tempfile.TemporaryDirectory(dir=target.parent) as stage:
            restored = Path(stage) / 'asset'
            archive.restore_asset(item['platform'], item['locale'], item['relative'],
                                  item['sha256'], stock[item['platform']], restored)
            restored.chmod(int(item['mode'], 8))
            os.link(restored, target)
        count += 1
    print(f'Restored {count} release assets in {prefix}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('receipt', 'accepted', 'mac_stock', 'windows_stock', 'prefix'):
        parser.add_argument(name, type=Path)
    restore(**vars(parser.parse_args()))


if __name__ == '__main__':
    main()
