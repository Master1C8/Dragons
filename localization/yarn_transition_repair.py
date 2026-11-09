"""Restore five missing Yarn destinations in the two pinned game builds."""
import struct

import dialogue_locale as dl

PROGRAM_SIZE_OFFSET = 40
PROGRAM_OFFSET = 44

# Each suffix begins after the three source-bound == / title: / --- lines.
CONTINUATIONS = {
    'Alexander_Done': ('Alexander_Outro', 32),
    'ConradBeatup_OutroDone': ('ConradBeatup_Outro', 36),
    'Conrad_OutroDone': ('Conrad_Outro', 36),
    'RyanDate_OutroDone': ('RyanDate_Outro', 4),
    'RyanExploded_OutroDone': ('RyanExploded_Outro', 36),
}

# These pin the exact candidate programs already exercised in the original VM.
REPAIRED_PROGRAM_HASHES = {
    'macos': '7d4a0f1ecb58565a1fd1dc154d2ba3c4c9e4caf1832589da3a53f0e88b5768cc',
    'windows': '6d2dfffecadd81cdeca8ff5e3781bb5ab7e36b7b603f3d6265a444959f73b3f0',
}


def length_delimited(field, payload):
    size = len(payload)
    length = bytearray()
    while size >= 128:
        length.append((size & 127) | 128)
        size >>= 7
    length.append(size)
    return bytes([field << 3 | 2]) + length + payload


def repair_project(platform, raw):
    import compare_yarn_versions as versions

    spec = versions.BUILDS[platform]
    if dl.sha(raw) != spec['projectSha256']:
        raise ValueError('unsupported YarnProject for transition repair')
    size = struct.unpack_from('<I', raw, PROGRAM_SIZE_OFFSET)[0]
    end = PROGRAM_OFFSET + size
    program = raw[PROGRAM_OFFSET:end]
    nodes, _ = versions.program_nodes(program)
    additions = []
    for destination, (host, start) in CONTINUATIONS.items():
        if destination in nodes:
            raise ValueError(f'Yarn transition destination already exists: {destination}')
        name = destination.encode('ascii')
        header = length_delimited(1, b'title') + length_delimited(2, name)
        instructions = [value for field, wire, value in versions.protobuf_fields(nodes[host])
                        if (field, wire) == (7, 2)]
        body = (length_delimited(1, name) + length_delimited(6, header)
                + b''.join(length_delimited(7, value) for value in instructions[start:]))
        entry = length_delimited(1, name) + length_delimited(2, body)
        additions.append(length_delimited(2, entry))
    repaired = program + b''.join(additions)
    if dl.sha(repaired) != REPAIRED_PROGRAM_HASHES[platform]:
        raise ValueError('Yarn transition repair differs from the verified program')
    tail = raw[end + (-end % 4):]
    return (raw[:PROGRAM_SIZE_OFFSET] + struct.pack('<I', len(repaired))
            + repaired + bytes(-len(repaired) % 4) + tail)
