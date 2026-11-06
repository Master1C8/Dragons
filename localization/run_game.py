#!/usr/bin/env python3
"""Run one built macOS game copy and clean up its generated Steam file."""
import argparse
import fcntl
import hashlib
import json
import os
from pathlib import Path
import subprocess

import dialogue_locale as dl


def run(app, extra_args):
    app = app.resolve(strict=True)
    if app.suffix != '.app' or not app.is_dir():
        raise ValueError('expected a built macOS .app')
    marker = app / 'Contents/Resources/vn-localization-build.json'
    reference = app / 'Contents/MacOS/steam_appid.txt'
    executable = app / 'Contents/MacOS/DragNWash'
    generated = app / 'steam_appid.txt'
    for path in (marker, reference, executable):
        if path.is_symlink() or not path.is_file() or app not in path.resolve().parents:
            raise ValueError('missing or unsafe build marker, executable, or Steam file')
    meta = json.loads(marker.read_text(encoding='utf-8'), object_pairs_hook=dl.unique_object)
    if (not isinstance(meta, dict) or set(meta) != {'schema', 'locale', 'sourceAssetSha256', 'steamFileSha256'}
            or type(meta['schema']) is not int or meta['schema'] != 1
            or meta['locale'] not in dl.site_locales() or meta['sourceAssetSha256'] != dl.ASSET_HASH):
        raise ValueError('invalid localization build marker')
    steam_hash = hashlib.sha256(reference.read_bytes()).hexdigest()
    if steam_hash != meta['steamFileSha256']:
        raise ValueError('Steam identifier does not match the signed build marker')
    lock_path = app.parent / ('.' + app.name + '.vn-localization.lock')
    fd = os.open(lock_path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'r+') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError('this localized app is already being run by the launcher') from exc
        if generated.exists() or generated.is_symlink():
            raise ValueError('unexpected root Steam file exists before launch; preserve it and inspect the copy')
        subprocess.run(['codesign', '--verify', '--deep', '--strict', str(app)], check=True)
        process = subprocess.Popen([str(executable), *extra_args], cwd=executable.parent)
        print(f'Launched localized copy, PID {process.pid}', flush=True)
        try:
            status = process.wait()
        except KeyboardInterrupt:
            process.terminate()
            process.wait()
            status = 130
        finally:
            if generated.exists() or generated.is_symlink():
                if generated.is_symlink() or not generated.is_file() or hashlib.sha256(generated.read_bytes()).hexdigest() != steam_hash:
                    raise RuntimeError('unexpected root Steam file was preserved; inspect copy before relaunch')
                generated.unlink()
            subprocess.run(['codesign', '--verify', '--deep', '--strict', str(app)], check=True)
        print('Localized copy exited; generated Steam file removed and signature verified.', flush=True)
        return status


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('app', type=Path)
    parser.add_argument('game_args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    extra = args.game_args[1:] if args.game_args[:1] == ['--'] else args.game_args
    raise SystemExit(run(args.app, extra))


if __name__ == '__main__':
    main()
