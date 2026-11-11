#!/usr/bin/env python3
"""Restore the recorded usage counter snapshot from read-only journal prefixes."""

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import zipfile

from restore_probe_assets import read_receipt, relative_path, sha256


def prefix_lines(path, length, expected):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while length:
            line = stream.readline(length)
            if not line:
                raise ValueError('Journal prefix is incomplete')
            length -= len(line)
            digest.update(line)
            yield line
    if digest.hexdigest() != expected:
        raise ValueError('Journal prefix fingerprint mismatch')


def counters(path, row, original_path):
    records = []
    seen = set()
    counts = Counter()
    current = last = None
    lines = prefix_lines(path, row['bytes'], row['sha256'])
    metadata = json.loads(next(lines))['payload']
    for line in lines:
        try:
            record = json.loads(line)
        except ValueError:
            continue
        event = record.get('type')
        payload = record.get('payload', {})
        timestamp = record.get('timestamp')
        if event == 'turn_context':
            turn = payload.get('turn_id')
            if turn in seen:
                counts['replayedTurnContexts'] += 1
                continue
            if current:
                records.append(current)
            current = dict(id=turn, model=payload.get('model'), effort=payload.get('effort'),
                           at=timestamp, baseline=last, requests=[], observedEnd=None)
            seen.add(turn)
        elif event == 'event_msg':
            if payload.get('type') == 'token_count' and payload.get('info'):
                info = payload['info']
                total = info.get('total_token_usage')
                if total and total != last:
                    if current:
                        current['requests'].append(dict(at=timestamp, total=total,
                                                        last=info.get('last_token_usage')))
                    last = total
            elif payload.get('type') == 'task_complete' and current:
                current['observedEnd'] = timestamp
    if current:
        records.append(current)
    return dict(session=metadata.get('id'), path=str(original_path), source=metadata.get('source'),
                startedAt=metadata.get('timestamp'), last=last, turns=records, counts=dict(counts))


def rebuild(receipt, archive_path, journal_root):
    if sha256(archive_path) != receipt['archiveSha256']:
        raise ValueError('Usage evidence archive fingerprint mismatch')
    with zipfile.ZipFile(archive_path) as archive:
        manifest = json.loads(archive.read(receipt['prefixManifest']))
    root = journal_root.resolve(strict=True)
    original_root = Path(manifest['sourceRoot'])
    output = []
    for row in manifest['prefixes']:
        relative = relative_path(row['path'])
        path = root / relative
        if relative.parts[0] not in ('sessions', 'archived_sessions') or path.resolve() != path:
            raise ValueError('Unexpected journal path in the usage evidence')
        output.append(counters(path, row, original_root / relative))
    data = json.dumps(output, separators=(',', ':')).encode()
    if hashlib.sha256(data).hexdigest() != receipt['snapshot']['sha256']:
        raise ValueError('Restored usage snapshot fingerprint mismatch')
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('receipt', 'archive', 'journal_root', 'output'):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    data = rebuild(receipt, args.archive, args.journal_root)
    with args.output.open('xb') as out:
        out.write(data)
    args.output.chmod(int(receipt['snapshot']['mode'], 8))
