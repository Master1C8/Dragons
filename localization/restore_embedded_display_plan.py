#!/usr/bin/env python3
"""Recover a historical display plan or display map from a verified TMP assembly."""

import argparse
import hashlib
from io import BytesIO
import json
from pathlib import Path
import struct

import dnfile

from restore_probe_assets import read_receipt, sha256


def read_string(stream):
    size = 0
    for shift in range(0, 35, 7):
        byte, = stream.read(1)
        size |= (byte & 0x7f) << shift
        if byte < 0x80:
            data = stream.read(size)
            if len(data) != size:
                raise ValueError('Truncated display-plan string')
            return data.decode('utf-8')
    raise ValueError('Invalid display-plan string length')


def decode(data):
    with BytesIO(data) as stream:
        version, count = struct.unpack('<ii', stream.read(8))
        if version not in (1, 2, 3) or not 1 <= count <= 4096:
            raise ValueError('Unsupported display-plan resource header')
        rows = []
        for _ in range(count):
            row = {'logical': read_string(stream), 'prepared': read_string(stream)}
            paragraph = stream.read(1)[0] if version == 3 else None
            offset_count, = struct.unpack('<i', stream.read(4))
            if not 1 <= offset_count <= len(data) // 4:
                raise ValueError('Invalid display-plan offset count')
            row['offsets'] = list(struct.unpack(f'<{offset_count}i', stream.read(4 * offset_count)))
            if paragraph is not None:
                row['paragraphLevel'] = paragraph
            cluster_count, = struct.unpack('<i', stream.read(4))
            if not 1 <= cluster_count <= offset_count:
                raise ValueError('Invalid display-plan cluster count')
            cluster_format = '<iB?' if version == 1 else '<iiB?'
            clusters = tuple(struct.iter_unpack(
                cluster_format, stream.read(struct.calcsize(cluster_format) * cluster_count),
            ))
            if len(clusters) != cluster_count:
                raise ValueError('Invalid display-plan cluster count')
            row['clusterEnds'] = [cluster[0] for cluster in clusters]
            if version != 1:
                row['sourceClusterEnds'] = [cluster[1] for cluster in clusters]
            row['levels'] = [cluster[-2] for cluster in clusters]
            row['trailingReset'] = [cluster[-1] for cluster in clusters]
            rows.append(row)
        if stream.read(1):
            raise ValueError('Unexpected bytes after display-plan resource')
        return rows


def restore(row, assembly, output):
    if sha256(assembly) != row['assemblySha256']:
        raise ValueError('Display-plan assembly fingerprint mismatch')
    with dnfile.dnPE(str(assembly)) as pe:
        resource, = [resource for resource in pe.net.resources
                     if str(resource.name) == 'Dragons.PreparedText.Plans']
        rows = decode(resource.data)
    if row.get('singleLineOnly'):
        rows = [value for value in rows if '\n' not in value['logical']]
    if code_points := row.get('preparedCodePointMap'):
        mapping = {int(source, 16): int(target, 16) for source, target in code_points.items()}
        for value in rows:
            value['prepared'] = value['prepared'].translate(mapping)
    if row['kind'] == 'map':
        rows = [{key: value[key] for key in ('logical', 'prepared')} for value in rows]
    elif row['kind'] != 'plan':
        raise ValueError('Unknown display-plan output kind')
    data = (json.dumps(rows, ensure_ascii=False) + '\n').encode()
    if len(data) != row['bytes']:
        raise ValueError('Display-plan output size mismatch')
    if hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('Display-plan output fingerprint mismatch')
    with output.open('xb') as stream:
        stream.write(data)
    output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    parser.add_argument('--assembly', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    selected = next(row for row in read_receipt(args.receipt)['outputs']
                    if row['path'] == args.recorded_path)
    restore(selected, args.assembly, args.output)
