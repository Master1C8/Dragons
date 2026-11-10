#!/usr/bin/env python3
"""Reconstruct the pinned stock app from an owned installation and its backup."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def restore(installation, output):
    installation = installation.resolve(strict=True)
    if output.exists() or output.is_symlink():
        raise FileExistsError(output)
    output = output.resolve()
    if not installation.is_dir() or installation.suffix != '.app' or output.suffix != '.app':
        raise ValueError('source and destination must be .app directories')
    if installation in output.parents:
        raise FileExistsError('destination must be new and outside the installed game')
    manifest = json.loads(Path(__file__).with_name('macos_stock_files.json').read_text())
    resources = installation / 'Contents/Resources'
    backup = resources / 'VNRevival/dragons-vnrevival/original-backup'
    selected = []
    for relative, expected in manifest.items():
        candidates = [installation / relative]
        if relative.startswith('Contents/Resources/Data/'):
            candidates.append(backup / relative.removeprefix('Contents/Resources/Data/'))
        if relative == 'steam_appid.txt':
            candidates.append(installation / 'Contents/MacOS/steam_appid.txt')
        match = next((path for path in candidates if path.is_file() and sha256(path) == expected), None)
        if match is None:
            raise ValueError(f'No verified stock source for {relative}')
        selected.append((relative, match, expected))

    with tempfile.TemporaryDirectory(prefix='.stock-restore-', dir=output.parent) as scratch:
        restored = Path(scratch) / output.name
        (restored / 'Contents/Resources/VNRevival').mkdir(parents=True)
        for relative, source, expected in selected:
            target = restored / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(['/bin/cp', '-c', '-p', str(source), str(target)], check=True)
            if sha256(target) != expected:
                raise ValueError(f'Copied file failed verification: {relative}')
        shutil.move(restored, output)
    print(f'Verified {len(selected)} stock files in {output}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('installation', type=Path)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    restore(args.installation, args.output)
