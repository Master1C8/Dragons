#!/usr/bin/env python3
"""Restore a recorded review diff from the Git blobs it compared."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile

from restore_probe_assets import read_receipt, relative_path


CHECKOUT = Path(__file__).resolve().parents[1]
RENDER_OPTIONS = {'--binary', '--minimal', '--full-index'}


def git(*args, data=None, env=None):
    return subprocess.check_output(['git', '-C', str(CHECKOUT), *args], input=data, env=env)


def comparison_tree(files, side, env):
    git('read-tree', '--empty', env=env)
    entries = []
    for row in files:
        oid = row[side]
        if oid is None:
            continue
        mode = row[side + 'Mode']
        if mode not in ('100644', '100755', '120000') or not re.fullmatch(r'[0-9a-f]{40}', oid):
            raise ValueError('Unexpected Git blob or file mode in review receipt')
        path = relative_path(row['path']).as_posix()
        entries.append(f'{mode} {oid}\t{path}\0'.encode())
    if entries:
        git('update-index', '-z', '--index-info', data=b''.join(entries), env=env)
    return git('write-tree', env=env).decode().strip()


def rebuild(row):
    if set(row['options']) - RENDER_OPTIONS or not 4 <= row['abbrev'] <= 40:
        raise ValueError('Unexpected historical Git diff options')
    main_objects = git('rev-parse', '--path-format=absolute', '--git-path', 'objects').decode().strip()
    with tempfile.TemporaryDirectory() as staging:
        scratch = Path(staging)
        objects = scratch / 'objects'
        objects.mkdir()
        env = {**os.environ, 'GIT_INDEX_FILE': str(scratch / 'index'),
               'GIT_OBJECT_DIRECTORY': str(objects), 'GIT_ALTERNATE_OBJECT_DIRECTORIES': main_objects}
        before, after = (comparison_tree(row['files'], side, env) for side in ('before', 'after'))
        data = git('diff-tree', '-p', '-r', '--no-commit-id', '--no-renames', '--no-color',
                   '--no-ext-diff', '--no-textconv', '--src-prefix=a/', '--dst-prefix=b/',
                   f"--abbrev={row['abbrev']}", *row['options'], before, after, env=env)
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('Restored Git diff fingerprint mismatch')
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    row = next((r for r in read_receipt(args.receipt)['outputs']
                if r['path'] == args.recorded_path), None)
    if row is None:
        parser.error(f'Unknown review diff: {args.recorded_path}')
    data = rebuild(row)
    with args.output.open('xb') as out:
        out.write(data)
    args.output.chmod(int(row['mode'], 8))
