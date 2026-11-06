#!/usr/bin/env python3
"""Compare the pinned macOS and Windows Yarn source tables without modifying them."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re
import struct

import UnityPy
import dialogue_locale as dl

BUILDS = {
    'macos': {
        'version': '9/12/2026_a93aa21a', 'localization': 10623, 'project': 10719,
        'globalSha256': '2f3813fddc22b6c6285099f173b922d782e2f06d659482d9373849e3bbb9794b',
        'assetSha256': dl.ASSET_HASH,
        'localizationSha256': dl.OBJECT_HASH,
        'projectSha256': '1487cbd825c98488ce00492dc7c9c5c2c3475657e9a7719e9c1de49b5f2c1189',
    },
    'windows': {
        'version': '9/9/2026_ee944596', 'localization': 10611, 'project': 10707,
        'globalSha256': '2111d3179b716d7cea4d7d7b6695c902c2aae3c834676d6376993494ab5279f6',
        'assetSha256': 'aff0c9a7b017a4b8cd5fa7ee069fa49331703c54bff9e7a2e398fa04b646d231',
        'localizationSha256': '7000b2b93b09f6a7b916e5f57c0dc6cf21ca9e6f9ddbfbc485bce704e8ce28d6',
        'projectSha256': 'f91af8c801958185885c2fc9adf3dfd5188b713c4f1ef264659e44292630b3b5',
    },
}


def varint(data, position):
    value = 0
    for shift in range(0, 70, 7):
        if position >= len(data):
            raise ValueError('truncated protobuf varint')
        byte = data[position]
        position += 1
        value |= (byte & 0x7f) << shift
        if byte < 128:
            return value, position
    raise ValueError('invalid protobuf varint')


def protobuf_fields(data):
    position = 0
    while position < len(data):
        tag, position = varint(data, position)
        number, wire = tag >> 3, tag & 7
        if not number:
            raise ValueError('invalid protobuf field number')
        if wire == 2:
            size, position = varint(data, position)
            if size > len(data) - position:
                raise ValueError('truncated protobuf field')
            value = data[position:position + size]
            position += size
        elif wire == 0:
            value, position = varint(data, position)
        elif wire in (1, 5):
            size = 8 if wire == 1 else 4
            if position + size > len(data):
                raise ValueError('truncated fixed-width field')
            value = data[position:position + size]
            position += size
        else:
            raise ValueError(f'unsupported protobuf wire type: {wire}')
        yield number, wire, value


def program_nodes(program):
    nodes, other = {}, []
    for number, wire, value in protobuf_fields(program):
        if number != 2 or wire != 2:
            other.append((number, wire, value))
            continue
        fields = list(protobuf_fields(value))
        keys = [v for n, w, v in fields if n == 1 and w == 2]
        bodies = [v for n, w, v in fields if n == 2 and w == 2]
        if len(keys) != 1 or len(bodies) != 1:
            raise ValueError('unexpected Yarn node map entry')
        key = keys[0].decode('utf-8', errors='strict')
        if key in nodes:
            raise ValueError(f'duplicate Yarn node: {key}')
        nodes[key] = bodies[0]
    return nodes, other


def load(data, spec):
    data = Path(data)
    if dl.sha((data / 'globalgamemanagers').read_bytes()) != spec['globalSha256']:
        raise ValueError('unsupported global game managers')
    asset = data / 'sharedassets1.assets'
    if dl.sha(asset.read_bytes()) != spec['assetSha256']:
        raise ValueError('unsupported shared asset')
    settings = UnityPy.load(str(data / 'globalgamemanagers'))
    versions = [o.read(check_read=False).bundleVersion for o in settings.objects if o.type.name == 'PlayerSettings']
    if versions != [spec['version']]:
        raise ValueError('unexpected build version')
    env = UnityPy.load(str(asset))
    if str(env.file.unity_version) != '6000.3.14f1':
        raise ValueError('unexpected Unity version')
    objects = {o.path_id: o for o in env.objects}
    if len(objects) != len(env.objects):
        raise ValueError('duplicate Unity object ID')
    raw = objects[spec['localization']].get_raw_data()
    project = objects[spec['project']].get_raw_data()
    if dl.sha(raw) != spec['localizationSha256'] or dl.sha(project) != spec['projectSha256']:
        raise ValueError('Yarn object fingerprint mismatch')
    keys, values, extras = dl.parse(raw)
    if dl.encode(raw, keys, values, extras) != raw:
        raise ValueError('Yarn localization did not round-trip')
    size = struct.unpack_from('<I', project, 40)[0]
    if size > len(project) - 44:
        raise ValueError('truncated Yarn program')
    program = project[44:44 + size]
    nodes, other = program_nodes(program)
    return keys, values, extras, program, nodes, other


def compare(mac, windows):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    a = load(mac, BUILDS['macos'])
    b = load(windows, BUILDS['windows'])
    ak, av, ae, ap, an, ao = a
    bk, bv, be, bp, bn, bo = b
    aa = {k: (v, e) for k, v, e in zip(ak, av, ae)}
    bb = {k: (v, e) for k, v, e in zip(bk, bv, be)}
    common = aa.keys() & bb.keys()
    line_ids = re.compile(rb'line:[0-9a-f]{8}')
    changed = [k for k in ak if k in common and aa[k][0] != bb[k][0]]
    return {
        'schema': 1, 'builds': BUILDS,
        'localization': {
            'macosCount': len(ak), 'windowsCount': len(bk), 'sameOrderedIds': ak == bk,
            'onlyMacos': sorted(aa.keys() - bb.keys()), 'onlyWindows': sorted(bb.keys() - aa.keys()),
            'changedTextIds': changed,
            'changedMetadataIds': [k for k in ak if k in common and aa[k][1] != bb[k][1]],
            'changedMarkupIds': [k for k in changed if dl.TOKENS.findall(aa[k][0]) != dl.TOKENS.findall(bb[k][0])],
        },
        'program': {
            'macosSha256': dl.sha(ap), 'windowsSha256': dl.sha(bp),
            'sameBytes': ap == bp, 'macosNodes': len(an), 'windowsNodes': len(bn),
            'sameNodeNames': an.keys() == bn.keys(),
            'changedCommonNodes': sorted(k for k in an.keys() & bn.keys() if an[k] != bn[k]),
            'sameNonNodeTopLevelFields': ao == bo,
            'sameLineIdMultiset': Counter(line_ids.findall(ap)) == Counter(line_ids.findall(bp)),
        },
        'limitations': 'Static pinned comparison only; changed node behavior, semantic differences, runtime compatibility, and UI/settings sources require separate analysis.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--macos-data', required=True, type=Path)
    parser.add_argument('--windows-data', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(compare(args.macos_data, args.windows_data), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
