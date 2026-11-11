#!/usr/bin/env python3
"""Restore historical helper files from exact Codex journal records."""

import argparse
import ast
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

from restore_probe_assets import read_receipt, relative_path


def extract_text(record, row):
    text = record
    for field in row['fields']:
        text = json.loads(text) if field is None else text[field]
    if 'literal' not in row:
        return text

    start, length = row['literal']
    if not 0 <= start < start + length <= len(text):
        raise ValueError('Unexpected command literal range')
    command = json.loads(text[start:start + length])
    form = row['form']
    if form == 'command':
        return command
    if form == 'patch':
        return ''.join(line[1:] if line.startswith('+') else '\n'
                       for line in command.splitlines(keepends=True))
    if form == 'constant':
        heredoc, node = row['constant']
        bodies = re.findall(r"<<'PY'\n(.*?)\nPY(?:\n|$)", command, re.S)
        return list(ast.walk(ast.parse(bodies[heredoc])))[node].value
    raise ValueError(f'Unexpected journal source form: {form}')


def restore(receipt, sessions, destination):
    pending = defaultdict(lambda: defaultdict(list))
    outputs = read_receipt(receipt)['outputs']
    parts = {}
    for name, row in outputs.items():
        path = relative_path(name)
        if not path.is_relative_to('localization/work'):
            raise ValueError(f'Unexpected helper path: {name}')
        ranges = row.get('parts', [row])
        parts[path] = [None] * len(ranges)
        for index, part in enumerate(ranges):
            pending[relative_path(part['day'])][part['recordSha256']].append(
                (path, index, part))

    sessions = sessions.resolve(strict=True)
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
                    for path, index, part in matches:
                        text = extract_text(record, part)
                        start = part['start']
                        end = start + part['length']
                        if not isinstance(text, str) or not 0 <= start < end <= len(text):
                            raise ValueError(f'Unexpected journal helper range: {path}')
                        parts[path][index] = text[start:end]
                    if not records:
                        break
        if records:
            raise ValueError(f'Missing {len(records)} exact journal records for {day}')

    restored = {}
    for path, ranges in parts.items():
        row = outputs[path.as_posix()]
        data = ''.join(ranges).encode()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise ValueError(f'Journal helper fingerprint mismatch: {path}')
        restored[path] = (data, int(row['mode'], 8))

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
