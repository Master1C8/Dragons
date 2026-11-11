#!/usr/bin/env python3
"""Recreate a retired screenshot review stream from its compact evidence."""

import argparse
import base64
from contextlib import ExitStack
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


def rebuild(row, evidence, image_sources):
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
        original, archive = image_sources[frame['sha256']]
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
    parser.add_argument('--referenced-images', type=Path)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    if sha256(args.metadata) != receipt['metadata']['sha256']:
        raise ValueError('metadata archive fingerprint mismatch')
    archives = [(receipt['images'], args.images)]
    if 'referencedImages' in receipt:
        if args.referenced_images is None:
            parser.error('--referenced-images is required for this receipt')
        archives.append((receipt['referencedImages'], args.referenced_images))
    row = receipt['outputs'][args.recorded_path]
    with gzip.open(args.metadata, 'rt', encoding='utf-8') as stream:
        evidence = json.load(stream)[args.recorded_path]
    with ExitStack() as opened:
        image_sources = {}
        for source, path in archives:
            if sha256(path) != source['sha256']:
                raise ValueError(f'{source["name"]} archive fingerprint mismatch')
            archive = opened.enter_context(zipfile.ZipFile(path))
            image_receipt = args.receipt.parent / source['receipt']
            for image in read_receipt(image_receipt)['outputs']:
                image_sources.setdefault(image['sha256'], (image, archive))
        data = rebuild(row, evidence, image_sources)
    with args.output.open('xb') as stream:
        stream.write(data)
    args.output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    main()
