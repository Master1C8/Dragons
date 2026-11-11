#!/usr/bin/env python3
"""Restore historical helper files from exact Codex journal records."""

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path

from restore_probe_assets import read_receipt, relative_path


def restore(receipt, sessions, destination):
    pending = defaultdict(lambda: defaultdict(list))
    for name, row in read_receipt(receipt)['outputs'].items():
        path = relative_path(name)
        if not path.is_relative_to('localization/work'):
            raise ValueError(f'Unexpected helper path: {name}')
        pending[relative_path(row['day'])][row['recordSha256']].append((path, row))

    sessions = sessions.resolve(strict=True)
    restored = {}
    for day, records in pending.items():
        directory = sessions / day
        if directory.resolve() != directory:
            raise ValueError(f'Unexpected journal directory: {day}')
        for journal in sorted(directory.glob('rollout-*.jsonl')):
            if not records:
                break
            if journal.is_symlink() or not journal.is_file():
                continue
            with journal.open('rb') as stream:
                for line in stream:
                    matches = records.pop(hashlib.sha256(line).hexdigest(), ())
                    if not matches:
                        continue
                    record = json.loads(line)
                    for path, row in matches:
                        text = record
                        for field in row['fields']:
                            text = json.loads(text) if field is None else text[field]
                        start = row['start']
                        end = start + row['length']
                        if not isinstance(text, str) or not 0 <= start < end <= len(text):
                            raise ValueError(f'Unexpected journal helper range: {path}')
                        data = text[start:end].encode()
                        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
                            raise ValueError(f'Journal helper fingerprint mismatch: {path}')
                        restored[path] = (data, int(row['mode'], 8))
                    if not records:
                        break
        if records:
            raise ValueError(f'Missing {len(records)} exact journal records for {day}')

    destination.mkdir()
    for path, (data, mode) in restored.items():
        output = destination / path
        output.parent.mkdir(parents=True, exist_ok=True)
        with output.open('xb') as stream:
            stream.write(data)
        output.chmod(mode)
    return len(restored)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('sessions', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print(f'Restored {restore(args.receipt, args.sessions, args.destination)} helper files.')
