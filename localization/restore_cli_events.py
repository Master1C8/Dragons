#!/usr/bin/env python3
"""Restore historical CLI event streams from the original Codex journals."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import shlex
import subprocess

from restore_probe_assets import read_receipt, relative_path, sha256
from restore_usage_snapshot import prefix_lines


CHECKOUT = Path(__file__).resolve().parents[1]


def references(events):
    for event in events:
        for value in event.get('item', {}).values():
            if isinstance(value, dict) and value.keys() == {'reference'}:
                yield value['reference']


def read_records(journal_root, journal, offsets):
    path = journal_root / relative_path(journal['path'])
    if path.resolve() != path or not path.is_relative_to(journal_root / 'sessions'):
        raise ValueError('Unexpected Codex journal path')
    records = {}
    offset = 0
    for raw in prefix_lines(path, journal['bytes'], journal['sha256']):
        if offset in offsets:
            records[offset] = json.loads(raw)
        offset += len(raw)
    if records.keys() != offsets:
        raise ValueError('Some recorded journal offsets are absent')
    return records


def resolve(reference, records):
    path, *shell = reference
    offset, *fields = path
    value = records[offset]
    for field in fields:
        value = json.loads(value) if field is None else value[field]
    if not shell:
        return value
    prefix, quoting, *redactions = shell
    if redactions:
        (start, end, marker), = redactions
        if not 0 <= start < end <= len(value) or not re.fullmatch(
            r'[^a-zA-Z0-9]*REDACTED[_ A-Z]*[^a-zA-Z0-9]*', marker, re.IGNORECASE
        ):
            raise ValueError('Unexpected CLI command redaction')
        value = value[:start] + marker + value[end:]
    if quoting == 'quote':
        return prefix + shlex.quote(value)
    parts = [prefix]
    start = 0
    for position, escaped in quoting:
        parts.extend((value[start:position], escaped))
        start = position
    parts.append(value[start:])
    return ''.join(parts)


def rebuild(row, events, records):
    git_blobs = {}

    def git_text(source):
        blob, digest, prefix = source['blob'], source['sha256'], source['prefix']
        if not re.fullmatch(r'[0-9a-f]{40}', blob) or (
            prefix and not re.fullmatch(r'cat: [A-Za-z0-9_.-]+: No such file or directory\n', prefix)
        ):
            raise ValueError('Unexpected CLI output Git reference')
        key = (blob, digest)
        if key not in git_blobs:
            raw = subprocess.check_output(['git', '-C', str(CHECKOUT), 'cat-file', 'blob', blob])
            if hashlib.sha256(raw).hexdigest() != digest:
                raise ValueError('CLI output Git blob fingerprint mismatch')
            git_blobs[key] = raw.decode('utf-8')
        return prefix + git_blobs[key]

    def field_value(value):
        if not isinstance(value, dict):
            return value
        if value.keys() == {'reference'}:
            return resolve(value['reference'], records)
        if value.keys() == {'git'}:
            source = value['git']
            return ''.join(git_text(part) for part in source) if isinstance(source, list) else git_text(source)
        return value

    lines = []
    for event in events:
        if 'item' in event:
            fields = {key: field_value(value) for key, value in event['item'].items()}
            event = {**event, 'item': fields}
        lines.append(json.dumps(event, ensure_ascii=False, separators=(',', ':')))
    raw = ('\n'.join(lines) + '\n').encode('utf-8')
    if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
        raise ValueError('Restored CLI event stream fingerprint mismatch')
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    for option in ('archive', 'journal-root', 'output'):
        parser.add_argument('--' + option, type=Path, required=True)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    if sha256(args.archive) != receipt['archiveSha256']:
        raise ValueError('CLI event index fingerprint mismatch')
    index = read_receipt(args.archive)
    stream = index['streams'][args.recorded_path]
    row = receipt['outputs'][args.recorded_path]
    offsets = {ref[0][0] for ref in references(stream['events'])}
    journal = index['journals'][stream['journal']]
    records = read_records(args.journal_root.resolve(strict=True), journal, offsets)
    data = rebuild(row, stream['events'], records)
    with args.output.open('xb') as out:
        out.write(data)
    args.output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    main()
