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


def journal_slices(events):
    for event in events:
        for value in event.get('item', {}).values():
            if isinstance(value, dict) and value.keys() == {'outputParts'}:
                for part in value['outputParts']:
                    if part.keys() == {'journalSlice'}:
                        yield part['journalSlice']



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


def rebuild(row, events, records, *, journal_root=None, slice_records=None, retained_input_root=CHECKOUT):
    git_blobs = {}
    documents = {}
    checkout_files = {}

    def output_prefix(source):
        prefix = source.get('prefix', '')
        if prefix and not re.fullmatch(r'cat: [A-Za-z0-9_.-]+: No such file or directory\n', prefix):
            raise ValueError('Unexpected CLI output prefix')
        return prefix

    def git_text(source):
        blob, digest = source['blob'], source['sha256']
        if not re.fullmatch(r'[0-9a-f]{40}', blob):
            raise ValueError('Unexpected CLI output Git reference')
        prefix = output_prefix(source)
        key = (blob, digest)
        if key not in git_blobs:
            raw = subprocess.check_output(['git', '-C', str(CHECKOUT), 'cat-file', 'blob', blob])
            if hashlib.sha256(raw).hexdigest() != digest:
                raise ValueError('CLI output Git blob fingerprint mismatch')
            git_blobs[key] = raw.decode('utf-8')
        text = git_blobs[key]
        if 'start' in source:
            start = source['start']
            end = start + source['length']
            if not 0 <= start < end <= len(text):
                raise ValueError('Unexpected CLI output Git range')
            text = text[start:end]
        return prefix + text

    def document_text(source):
        if journal_root is None:
            raise ValueError('Supply the Codex root for CLI output documents')
        prefix = output_prefix(source)
        relative = relative_path(source['path'])
        if len(relative.parts) < 2 or relative.parts[0] not in {'instructions', 'skills'} or relative.suffix != '.md':
            raise ValueError('Unexpected CLI output document path')
        path = journal_root / relative
        if path.resolve() != path:
            raise ValueError('Unexpected CLI output document path')
        key = (path, source['sha256'])
        if key not in documents:
            raw = path.read_bytes()
            if hashlib.sha256(raw).hexdigest() != source['sha256']:
                raise ValueError('CLI output document fingerprint mismatch')
            documents[key] = raw.decode('utf-8')
        return prefix + documents[key]

    def output_part(part):
        if part.keys() == {'git'}:
            return git_text(part['git'])
        if part.keys() == {'gitGrep'}:
            source = part['gitGrep']
            text = git_text({'blob': source['blob'], 'sha256': source['sha256']})
            raw = subprocess.check_output([
                'rg', '--no-config', '-n', '-i', '--color', 'never',
                '-e', source['regex'], '-',
            ], input=text.encode())
            rendered = ''.join(raw.decode().splitlines(keepends=True)[:source['lines']])
            if hashlib.sha256(rendered.encode()).hexdigest() != source['renderedSha256']:
                raise ValueError('CLI output Git search fingerprint mismatch')
            start = source['start']
            end = start + source['length']
            if not 0 <= start < end <= len(rendered):
                raise ValueError('Unexpected CLI output Git search range')
            return rendered[start:end]
        if part.keys() == {'gitDiff'}:
            source = part['gitDiff']
            revision = source['revision']
            if not re.fullmatch(r'[0-9a-f]{40}', revision):
                raise ValueError('Unexpected CLI diff Git revision')
            paths = [relative_path(name) for name in source['paths']]
            raw = subprocess.check_output([
                'git', '-C', str(CHECKOUT), '--literal-pathspecs', 'diff',
                '--no-ext-diff', '--no-textconv', '--no-color', '--no-renames',
                '--abbrev=7', '--diff-algorithm=myers', '--indent-heuristic',
                '--unified=3', '--src-prefix=a/', '--dst-prefix=b/',
                revision + '^', revision, '--', *map(str, paths),
            ])
            if hashlib.sha256(raw).hexdigest() != source['sha256']:
                raise ValueError('CLI output Git diff fingerprint mismatch')
            return raw.decode('utf-8')
        if part.keys() == {'document'}:
            return document_text(part['document'])
        if part.keys() == {'checkoutSlice'}:
            source = part['checkoutSlice']
            relative = relative_path(source['path'])
            path = retained_input_root / relative
            if (not path.is_relative_to(retained_input_root / 'localization/work') or
                    path.suffix != '.json' or path.resolve() != path or not path.is_file()):
                raise ValueError('Unexpected CLI output checkout path')
            key = (path, source['sha256'])
            if key not in checkout_files:
                raw = path.read_bytes()
                if hashlib.sha256(raw).hexdigest() != source['sha256']:
                    raise ValueError('CLI output checkout file fingerprint mismatch')
                checkout_files[key] = raw.decode('utf-8')
            text = checkout_files[key]
            start = source['start']
            end = start + source['length']
            if not 0 <= start < end <= len(text):
                raise ValueError('Unexpected CLI output checkout range')
            return text[start:end]
        if part.keys() == {'journalSlice'}:
            source = part['journalSlice']
            if slice_records is None:
                raise ValueError('Supply the records for CLI journal output ranges')
            text = resolve([[source['offset'], *source['fields']]], slice_records[source['journal']])
            start = source['start']
            end = start + source['length']
            if not isinstance(text, str) or not 0 <= start < end <= len(text):
                raise ValueError('Unexpected CLI journal output range')
            return text[start:end]
        raise ValueError('Unexpected CLI output source')

    def field_value(value):
        if not isinstance(value, dict):
            return value
        if value.keys() == {'reference'}:
            return resolve(value['reference'], records)
        if value.keys() == {'git'}:
            source = value['git']
            return ''.join(git_text(part) for part in source) if isinstance(source, list) else git_text(source)
        if value.keys() == {'outputParts'}:
            return ''.join(output_part(part) for part in value['outputParts'])
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
    parser.add_argument('--retained-input-root', type=Path, default=CHECKOUT)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    if sha256(args.archive) != receipt['archiveSha256']:
        raise ValueError('CLI event index fingerprint mismatch')
    index = read_receipt(args.archive)
    stream = index['streams'][args.recorded_path]
    row = receipt['outputs'][args.recorded_path]
    offsets = {ref[0][0] for ref in references(stream['events'])}
    journal = index['journals'][stream['journal']]
    journal_root = args.journal_root.resolve(strict=True)
    records = read_records(journal_root, journal, offsets)
    slice_offsets = {}
    for source in journal_slices(stream['events']):
        slice_offsets.setdefault(source['journal'], set()).add(source['offset'])
    slice_records = {
        key: read_records(journal_root, index['journals'][key], selected_offsets)
        for key, selected_offsets in slice_offsets.items()
    }
    data = rebuild(
        row, stream['events'], records, journal_root=journal_root, slice_records=slice_records,
        retained_input_root=args.retained_input_root.resolve(strict=True),
    )
    with args.output.open('xb') as out:
        out.write(data)
    args.output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    main()
