"""Compare the raw metadata of pinned Unity v22 assets, allowing data relocation."""
from hashlib import sha256
import struct

from map_ui_hierarchy import WINDOWS_ASSETS
from ui_locale import ASSETS as MACOS_ASSETS


HEADER = struct.Struct('>4IB3sI3q')
TYPE_PREFIX = struct.Struct('<iBh')
OBJECT = struct.Struct('<qqIi')
ASSETS = {'macos': MACOS_ASSETS, 'windows': WINDOWS_ASSETS}


def read_metadata(raw):
    if len(raw) < HEADER.size:
        raise ValueError('truncated Unity header')
    _, _, version, _, endian, _, meta_size, size, data_offset, _ = HEADER.unpack_from(raw)
    metadata_end = HEADER.size + meta_size
    if (version != 22 or endian != 0 or size != len(raw)
            or not HEADER.size < metadata_end <= data_offset <= size
            or data_offset != ((metadata_end + 15) & ~15)
            or any(raw[metadata_end:data_offset])):
        raise ValueError('unsupported Unity header or metadata extent')
    metadata = bytearray(raw[:data_offset])
    metadata[24:32] = bytes(8)  # Total file size tracks rewritten payloads.
    version_end = raw.find(b'\0', HEADER.size, metadata_end)
    cursor = version_end + 1
    if version_end < 0 or cursor + 9 > metadata_end:
        raise ValueError('truncated Unity type table header')
    _, type_tree, type_count = struct.unpack_from('<iBi', metadata, cursor)
    cursor += 9
    if type_tree or not 0 < type_count <= (metadata_end - cursor) // 23:
        raise ValueError('unsupported Unity type table')
    for _ in range(type_count):
        if cursor + TYPE_PREFIX.size > metadata_end:
            raise ValueError('truncated Unity type table')
        class_id, _, _ = TYPE_PREFIX.unpack_from(metadata, cursor)
        cursor += TYPE_PREFIX.size + 16 + (16 if class_id == 114 else 0)
    if cursor + 4 > metadata_end:
        raise ValueError('truncated Unity object count')
    count, = struct.unpack_from('<i', metadata, cursor)
    cursor += 4
    if not 0 < count <= (metadata_end - cursor) // OBJECT.size:
        raise ValueError('unsupported Unity object count')

    ranges = []
    ids = set()
    for _ in range(count):
        cursor = (cursor + 3) & ~3
        if cursor + OBJECT.size > metadata_end:
            raise ValueError('truncated Unity object table')
        path_id, offset, length, type_index = OBJECT.unpack_from(metadata, cursor)
        if path_id in ids or not 0 <= type_index < type_count or offset < 0:
            raise ValueError('invalid Unity object descriptor')
        ids.add(path_id)
        start = data_offset + offset
        ranges.append((start, start + length))
        metadata[cursor + 8:cursor + 20] = bytes(12)  # Offset and payload length.
        cursor += OBJECT.size

    previous = data_offset
    for start, end in sorted(ranges):
        if start < previous or end > size or start - previous > 15 or any(raw[previous:start]):
            raise ValueError('invalid Unity object extent or padding')
        previous = end
    if size - previous > 15 or any(raw[previous:]):
        raise ValueError('invalid Unity data trailer')
    return bytes(metadata), count


def compare_metadata(source, candidate):
    expected, count = read_metadata(source)
    actual, _ = read_metadata(candidate)
    if actual != expected:
        raise ValueError('serialized metadata differs outside size and relocation fields')
    return {'objects': count, 'metadataSha256': sha256(expected).hexdigest()}


def verify(platform, source, read_candidate, *, added_object_asset=None):
    result = {}
    for name, digest in ASSETS[platform].items():
        original = (source / name).read_bytes()
        if sha256(original).hexdigest() != digest:
            raise ValueError(f'unsupported serialized metadata source: {name}')
        if name == added_object_asset:
            continue
        try:
            result[name] = compare_metadata(original, read_candidate(name))
        except ValueError as error:
            raise ValueError(f'{name}: {error}') from error
    return result
