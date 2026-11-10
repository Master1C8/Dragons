"""Prepare logical-order TMP glyph clusters with ICU paragraph levels."""

from collections import defaultdict
import ctypes
import unicodedata

import uharfbuzz


class PlanBoundaryError(ValueError):
    """An authored control cannot be represented by the current mesh adapter."""


class Bidi:
    def __init__(self, library):
        icu = ctypes.CDLL(str(library))
        self.open = icu.ubidi_open_78
        self.open.restype = ctypes.c_void_p
        self.close = icu.ubidi_close_78
        self.close.argtypes = [ctypes.c_void_p]
        self.close.restype = None
        self.set_para = icu.ubidi_setPara_78
        self.set_para.argtypes = [ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint16),
                                  ctypes.c_int32, ctypes.c_uint8, ctypes.c_void_p,
                                  ctypes.POINTER(ctypes.c_int32)]
        self.set_para.restype = None
        self.level = icu.ubidi_getLevelAt_78
        self.level.argtypes = [ctypes.c_void_p, ctypes.c_int32]
        self.level.restype = ctypes.c_uint8
        self.mirror = icu.u_charMirror_78
        self.mirror.argtypes = [ctypes.c_int32]
        self.mirror.restype = ctypes.c_int32

    def levels(self, text):
        # The mesh adapter currently binds one UTF-16 unit per TMP character.
        if any(ord(char) > 0xffff for char in text):
            raise PlanBoundaryError('supplementary character')
        units = (ctypes.c_uint16 * len(text))(*map(ord, text))
        bidi = self.open()
        if not bidi:
            raise RuntimeError('could not allocate ICU bidi paragraph')
        status = ctypes.c_int32()
        try:
            self.set_para(bidi, units, len(text), 1, None, ctypes.byref(status))
            if status.value > 0:
                raise ValueError(f'ICU bidi paragraph failed: {status.value}')
            return [self.level(bidi, index) for index in range(len(text))]
        finally:
            self.close(bidi)


def shape_run(text, start, level, augmenter):
    buffer = uharfbuzz.Buffer()
    buffer.add_codepoints(list(map(ord, text)))
    buffer.direction = 'rtl' if level % 2 else 'ltr'
    buffer.script = augmenter.spec['script']
    buffer.language = augmenter.spec['language']
    buffer.flags = uharfbuzz.BufferFlags.REMOVE_DEFAULT_IGNORABLES
    uharfbuzz.shape(augmenter.hb_font, buffer)
    glyphs = defaultdict(list)
    for info, position in zip(buffer.glyph_infos, buffer.glyph_positions, strict=True):
        glyphs[info.cluster].append(augmenter.map_glyph(
            info.codepoint, position.x_advance, position.x_offset, position.y_offset))
    starts = sorted(glyphs)
    if not starts or starts[0] != 0:
        raise PlanBoundaryError('shaping removed a leading or standalone cluster')
    return [(start + first, start + end, ''.join(glyphs[first]))
            for first, end in zip(starts, starts[1:] + [len(text)], strict=True)]


def prepare(text, tags_pattern, bidi, augmenter):
    tags = defaultdict(list)
    plain_parts = []
    cursor = plain_length = 0
    for match in tags_pattern.finditer(text):
        part = text[cursor:match.start()]
        plain_parts.append(part)
        plain_length += len(part)
        if match.group().lower() == '<br>':
            raise PlanBoundaryError('TMP-generated line break')
        tags[plain_length].append(match.group())
        cursor = match.end()
    plain_parts.append(text[cursor:])
    plain = ''.join(plain_parts)
    classes = [unicodedata.bidirectional(char) for char in plain]
    if any(char != '\n' and kind in {'B', 'S', 'LRE', 'RLE', 'LRO', 'RLO',
                                      'PDF', 'LRI', 'RLI', 'FSI', 'PDI'}
           for char, kind in zip(plain, classes, strict=True)):
        raise PlanBoundaryError('unsupported bidi control')
    levels = []
    for number, paragraph in enumerate(plain.split('\n')):
        if number:
            levels.append(1)
        if paragraph:
            levels.extend(bidi.levels(paragraph))
    output, offsets, ends, source_ends, cluster_levels, reset = [], [], [], [], [], []
    output_length = 0

    def append(part):
        nonlocal output_length
        output.append(part)
        output_length += len(part.encode('utf-16-le')) // 2

    index = 0
    while index < len(plain):
        level = levels[index]
        char = plain[index]
        if augmenter.is_span_character(char):
            stop = index + 1
            while (stop < len(plain) and levels[stop] == level
                   and augmenter.is_span_character(plain[stop])):
                stop += 1
            clusters = shape_run(plain[index:stop], index, level, augmenter)
        else:
            stop = index + 1
            display = chr(bidi.mirror(ord(char))) if level % 2 else char
            clusters = [(index, stop, display)]
        for first, end, display in clusters:
            if any(inner in tags for inner in range(first + 1, end)):
                raise PlanBoundaryError('TMP tag inside shaped cluster')
            append(''.join(tags.get(first, ())))
            offsets.extend(range(output_length, output_length + len(display)))
            append(display)
            ends.append(len(offsets))
            source_ends.append(end)
            cluster_levels.append(level)
            reset.append(all(kind in {'WS', 'BN', 'B'} for kind in classes[first:end]))
        index = stop
    append(''.join(tags.get(len(plain), ())))
    return {'logical': text, 'prepared': ''.join(output), 'offsets': offsets,
            'clusterEnds': ends, 'sourceClusterEnds': source_ends,
            'levels': cluster_levels, 'trailingReset': reset}
