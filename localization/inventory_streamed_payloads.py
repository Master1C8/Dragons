#!/usr/bin/env python3
"""Bind root Unity stream files to serialized audio and graphics payloads."""
import argparse
from collections import Counter, defaultdict
from hashlib import file_digest
import json
from pathlib import Path

import UnityPy

import dialogue_locale as dialogue
import inventory_text_assets as text_assets


ROLES = {'AudioClip': 'encoded-audio', 'Texture2D': 'texture-data',
         'Cubemap': 'cubemap-data', 'Mesh': 'mesh-data'}


def stream_digest(path):
    with path.open('rb') as stream:
        return file_digest(stream, 'sha256').hexdigest()


def find_references(root, assets):
    groups, counts, schemas = defaultdict(list), Counter(), {}
    for asset in sorted(assets):
        env = UnityPy.load(str(root / asset))
        for obj in env.objects:
            kind = obj.type.name
            if kind == 'MonoBehaviour':
                continue
            identity = (str(obj.version), kind, obj.serialized_type.old_type_hash)
            if identity not in schemas:
                fields = {row['m_Type'] for row in obj._get_typetree_node().to_dict_list()}
                schemas[identity] = fields & {'StreamedResource', 'StreamingInfo'}
            if kind == 'VideoClip':
                raise ValueError(f'unclassified video clip: {asset}#{obj.path_id}')
            if not schemas[identity]:
                continue
            if kind not in ROLES:
                raise ValueError(f'unclassified stream carrier: {asset}#{obj.path_id}')
            raw = obj.get_raw_data()
            tree = obj.read_typetree(check_read=True)
            audio = kind == 'AudioClip'
            ref = tree['m_Resource' if audio else 'm_StreamData']
            name, offset, size = ((ref['m_Source'], ref['m_Offset'], ref['m_Size']) if audio else
                                  (ref['path'], ref['offset'], ref['size']))
            if not name:
                if audio or size:
                    raise ValueError(f'unbound stream payload: {asset}#{obj.path_id}')
                continue
            if (Path(name).name != name or '\\' in name or size <= 0 or offset < 0
                    or not name.endswith('.resource' if audio else '.resS')):
                raise ValueError(f'invalid stream reference: {asset}#{obj.path_id}')
            if obj.save_typetree(tree) != raw:
                raise ValueError(f'stream carrier failed byte round trip: {asset}#{obj.path_id}')
            groups[name].append({'asset': asset, 'objectId': obj.path_id, 'type': kind,
                                 'role': f'preserve-exactly-{ROLES[kind]}',
                                 'rawObjectSha256': dialogue.sha(raw), 'offset': offset, 'size': size})
            counts[kind] += 1
    return groups, counts


def verify_extents(path, records):
    if path.is_symlink() or not path.is_file():
        raise ValueError(f'expected a regular stream file: {path.name}')
    size = path.stat().st_size
    audio = path.suffix == '.resource'
    end = padding = 0
    with path.open('rb') as stream:
        for row in sorted(records, key=lambda item: item['offset']):
            start, length = row['offset'], row['size']
            gap = start - end
            if length <= 0 or gap < 0 or start + length > size or gap > (0 if audio else 15):
                raise ValueError(f'invalid or uncovered stream extent: {path.name}@{start}')
            stream.seek(end)
            if any(stream.read(gap)):
                raise ValueError(f'nonzero stream padding: {path.name}@{end}')
            padding += gap
            if audio and (length < 4 or stream.read(4) != b'FSB5'):
                raise ValueError(f'unknown encoded audio format: {path.name}@{start}')
            end = start + length
        stream.seek(end)
        remaining = size - end
        if remaining > (0 if audio else 15) or any(stream.read(remaining)):
            raise ValueError(f'uncovered stream trailer: {path.name}')
        padding += remaining
    return {'bytes': size, 'sha256': stream_digest(path), 'paddingBytes': padding,
            'references': sorted(records, key=lambda item: item['offset'])}


def inspect(root, platform, candidate=None):
    if candidate is not None and (candidate.is_symlink() or candidate.resolve() == root.resolve()):
        raise ValueError('expected a separate candidate Data directory')
    pinned = text_assets.inspect(root, platform)
    groups, counts = find_references(root, pinned['assets'])
    physical = {p.name for p in root.iterdir() if p.suffix in ('.resource', '.resS') and p.is_file()}
    if physical != groups.keys():
        raise ValueError('physical stream files differ from referenced paths')
    files = {name: verify_extents(root / name, groups[name]) for name in sorted(physical)}
    if candidate is not None:
        target = {p.name for p in candidate.iterdir() if p.suffix in ('.resource', '.resS') and p.is_file()}
        if target != physical:
            raise ValueError('candidate stream file inventory changed')
        for name, receipt in files.items():
            path = candidate / name
            if path.is_symlink() or stream_digest(path) != receipt['sha256']:
                raise ValueError(f'candidate stream bytes differ: {name}')
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'sourceAssets': pinned['assets'], 'carrierCounts': dict(counts), 'files': files,
            'candidateVerified': candidate is not None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=('macos', 'windows'))
    parser.add_argument('stock_data', type=Path)
    parser.add_argument('--candidate-data', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.stock_data, args.platform, args.candidate_data), indent=2))


if __name__ == '__main__':
    main()
