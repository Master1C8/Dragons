#!/usr/bin/env python3
"""Recreate a retired screenshot review stream from its compact evidence."""

import argparse
import base64
import gzip
import json
from pathlib import Path
import zipfile

from restore_probe_assets import read_receipt, sha256
from dialogue_locale import sha


FRAME_FIELDS = ('index', 'game', 'locale', 'order', 'direction', 'sha256', 'width', 'height')
CONFIG_NOTICE = (
    'Codex is ignoring 1 unrecognized configuration setting. Check for typos or deprecated settings.\n'
    '  session-flags: `tools.view_image` is ignored.'
)


def rebuild(row, evidence, image_rows, archive):
    events = [{'type': 'thread.started', 'thread_id': evidence['sessionId']}]

    def emit(kind, index, item_type, **fields):
        events.append({'type': kind, 'item': {'id': f'item_{index}', 'type': item_type, **fields}})

    for index in range(2):
        emit('item.completed', index, 'error', message=CONFIG_NOTICE)
    events.append({'type': 'turn.started'})
    call_id = 2
    if 'intro' in evidence:
        emit('item.completed', call_id, 'agent_message', text=evidence['intro'])
        call_id += 1

    call = {'server': 'screenshot_packet', 'tool': 'inspect_packet', 'arguments': {}}
    emit('item.started', call_id, 'mcp_tool_call', **call, result=None, error=None, status='in_progress')
    content = []
    for frame in evidence['frames']:
        original = image_rows[frame['sha256']]
        data = archive.read(original['member'])
        if len(data) != original['bytes'] or sha(data) != frame['sha256']:
            raise ValueError('Screenshot fingerprint mismatch')
        content.append({'type': 'text', 'text': json.dumps({key: frame[key] for key in FRAME_FIELDS})})
        content.append({
            'type': 'image', 'data': base64.b64encode(data).decode('ascii'),
            'mimeType': 'image/webp', '_meta': {'codex/imageDetail': 'original'},
        })
    result = {'content': content, 'structured_content': None}
    emit('item.completed', call_id, 'mcp_tool_call', **call, result=result, error=None, status='completed')
    emit('item.completed', call_id + 1, 'agent_message', text=evidence['answer'])
    events.append({'type': 'turn.completed', 'usage': evidence['usage']})
    data = ''.join(json.dumps(event, ensure_ascii=False, separators=(',', ':')) + '\n' for event in events)
    raw = data.encode('utf-8')
    if len(raw) != row['bytes'] or sha(raw) != row['sha256']:
        raise ValueError('Restored screenshot review stream fingerprint mismatch')
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    for option in ('metadata', 'images', 'output'):
        parser.add_argument('--' + option, type=Path, required=True)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    for key, source in (('metadata', args.metadata), ('images', args.images)):
        if sha256(source) != receipt[key]['sha256']:
            raise ValueError(f'{key} archive fingerprint mismatch')
    image_receipt = args.receipt.parent / receipt['images']['receipt']
    image_rows = {row['sha256']: row for row in read_receipt(image_receipt)['outputs']}
    row = receipt['outputs'][args.recorded_path]
    with gzip.open(args.metadata, 'rt', encoding='utf-8') as stream:
        evidence = json.load(stream)[args.recorded_path]
    with zipfile.ZipFile(args.images) as archive:
        data = rebuild(row, evidence, image_rows, archive)
    with args.output.open('xb') as stream:
        stream.write(data)
    args.output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    main()
