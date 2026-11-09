"""Repair Yarn transitions in the two pinned game builds."""
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

# These pin the exact output programs.
REPAIRED_PROGRAM_HASHES = {
    'macos': '7d4a0f1ecb58565a1fd1dc154d2ba3c4c9e4caf1832589da3a53f0e88b5768cc',
    'windows': 'e4e29b20afff9ba3306431ed316cbbb327c06e535ebcc2200b2f20bc06c00d8d',
}
CONRAD_MOUNT_FINISH = 'Conrad_finished_mount_3'
# Compiled instruction 89 in the original Windows and macOS nodes.
WINDOWS_CONRAD_JUMP = bytes.fromhex('82010e0a0c436f6e7261645f4f7574726f')
MACOS_CONRAD_JUMP = bytes.fromhex('8201100a0e436f6e7261645f4f7574726f5f33')
MACOS_CONRAD_NODE_HASH = 'a17eea4e1c49090009817f0d38980bf117402ca1229b88baa19bd360b5eab32e'


def length_delimited(field, payload):
    size = len(payload)
    length = bytearray()
    while size >= 128:
        length.append((size & 127) | 128)
        size >>= 7
    length.append(size)
    return bytes([field << 3 | 2]) + length + payload


def node_entry(name, body):
    return length_delimited(2, length_delimited(1, name) + length_delimited(2, body))


def align_windows_conrad(program, node):
    old_jump = length_delimited(7, WINDOWS_CONRAD_JUMP)
    new_jump = length_delimited(7, MACOS_CONRAD_JUMP)
    name = CONRAD_MOUNT_FINISH.encode('ascii')
    old_entry = node_entry(name, node)
    if node.count(old_jump) != 1 or program.count(old_entry) != 1:
        raise ValueError('unexpected Windows Conrad mount finish binding')
    replacement = node.replace(old_jump, new_jump, 1)
    if dl.sha(replacement) != MACOS_CONRAD_NODE_HASH:
        raise ValueError('Windows Conrad mount finish differs from the original macOS node')
    return program.replace(old_entry, node_entry(name, replacement), 1)


def repair_project(platform, raw):
    import compare_yarn_versions as versions

    spec = versions.BUILDS[platform]
    if dl.sha(raw) != spec['projectSha256']:
        raise ValueError('unsupported YarnProject for transition repair')
    size = struct.unpack_from('<I', raw, PROGRAM_SIZE_OFFSET)[0]
    end = PROGRAM_OFFSET + size
    program = raw[PROGRAM_OFFSET:end]
    nodes, _ = versions.program_nodes(program)
    if platform == 'windows':
        program = align_windows_conrad(program, nodes[CONRAD_MOUNT_FINISH])
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
        additions.append(node_entry(name, body))
    repaired = program + b''.join(additions)
    if dl.sha(repaired) != REPAIRED_PROGRAM_HASHES[platform]:
        raise ValueError('Yarn transition repair differs from the verified program')
    tail = raw[end + (-end % 4):]
    return (raw[:PROGRAM_SIZE_OFFSET] + struct.pack('<I', len(repaired))
            + repaired + bytes(-len(repaired) % 4) + tail)
