#!/usr/bin/env python3
"""Check Dragons corpus glyphs and stage shaped font probes without a Unity player."""

import argparse
from collections import defaultdict
import ctypes
import importlib.util
from io import BytesIO
import json
from pathlib import Path
import re
import shutil
import unicodedata

from fontTools.pens.boundsPen import BoundsPen
from fontTools.ttLib import TTFont
import UnityPy
import uharfbuzz

import cjk_font_fallback as fallback
import dialogue_locale as dialogue
import inventory_yarn_bindings as bindings
import paired_locale
import settings_locale as settings


SAMPLES = {'ar': 'لَا', 'fa': 'می‌روم', 'he': 'שָׁלוֹם', 'th': 'น้ำ', 'hi': 'क्षि'}
SONIC_SHAPER_SHA = '30c13e3ba4a7650528840bbbe09ad3c73ccd4029a0f778b9387ca7cb3485cbb8'
TMP_TAG = re.compile(r'<br>|</?(?:b|i|size|gradient|color|style)(?:=[^<>]*)?>', re.IGNORECASE)


def stock_font(platform, data):
    asset = data / fallback.ASSET
    primary_id, fallback_id, expected = fallback.SOURCES[platform]
    if dialogue.sha(asset.read_bytes()) != expected:
        raise ValueError(f'{platform}: stock font asset differs from the pinned input')
    env = UnityPy.load(str(asset))
    env.path = str(data)
    objects = env.file.objects
    generator, cache = bindings.generator(data, platform), {}

    def tmp_tree(path_id):
        obj = objects[path_id]
        header, _, nodes = settings.nodes_for(obj, generator, cache)
        tree = obj.read_typetree(nodes=nodes, check_read=True)
        settings.check_header(tree, header, path_id)
        return tree

    primary, dynamic = tmp_tree(primary_id), tmp_tree(fallback_id)
    if primary['m_FallbackFontAssetTable'] != [fallback.ptr(fallback_id)]:
        raise ValueError(f'{platform}: unexpected fallback order')
    static = {x['m_Unicode'] for x in primary['m_CharacterTable']}
    font = objects[fallback.local_id(dynamic['m_SourceFontFile'])]
    return static, bytes(font.read_typetree(check_read=True)['m_FontData'])


def valid_glyphs(font, characters):
    cmap, shapes = font.getBestCmap(), font.getGlyphSet()
    valid = set()
    for char in characters:
        name = cmap.get(ord(char))
        if not name or name == '.notdef':
            continue
        pen = BoundsPen(shapes)
        shapes[name].draw(pen)
        advance = font['hmtx'][name][0]
        if (advance > 0 or unicodedata.category(char).startswith('M')) and (
            char.isspace() or pen.bounds is not None
        ):
            valid.add(char)
    return valid


def authored_display_values(values, rows):
    for key, by_platform in values.items():
        prefixes = rows[key].get('preserveExactPrefix') or {}
        for platform, text in by_platform.items():
            yield text
            yield text.strip()
            prefix = prefixes.get(platform)
            if prefix and text.startswith(prefix):
                body = text[len(prefix):]
                yield body
                yield body.strip()


def needs_bidi(text):
    classes = {unicodedata.bidirectional(c) for c in TMP_TAG.sub('', text)}
    return bool(classes & {'R', 'AL'}) and bool(classes & {'L', 'EN', 'AN'})


def thai_breaker(path):
    icu = ctypes.CDLL(str(path))
    open_lines = icu.ubrk_open_78
    open_lines.argtypes = [ctypes.c_int32, ctypes.c_char_p, ctypes.POINTER(ctypes.c_uint16),
                           ctypes.c_int32, ctypes.POINTER(ctypes.c_int32)]
    open_lines.restype = ctypes.c_void_p
    next_line, close = icu.ubrk_next_78, icu.ubrk_close_78
    next_line.argtypes = close.argtypes = [ctypes.c_void_p]
    next_line.restype, close.restype = ctypes.c_int32, None

    def split(text):
        encoded = text.encode('utf-16-le')
        units = (ctypes.c_uint16 * (len(encoded) // 2)).from_buffer_copy(encoded)
        status = ctypes.c_int32()
        iterator = open_lines(2, b'th', units, len(units), ctypes.byref(status))
        if not iterator or status.value > 0:
            if iterator:
                close(iterator)
            raise ValueError(f'ICU Thai line iterator failed: {status.value}')
        try:
            start = 0
            parts = []
            while (end := next_line(iterator)) >= 0:
                if end > start:
                    parts.append(encoded[2 * start:2 * end].decode('utf-16-le'))
                    start = end
            if start != len(units):
                raise ValueError('ICU did not consume the full Thai span')
            return parts
        finally:
            close(iterator)

    return split


def preserve_thai_breaks(augmenter, split):
    shape = augmenter.shape_span

    def with_breaks(text):
        complete = shape(text)
        parts = split(text)
        if len(parts) <= 1:
            return complete
        shaped_parts = [shape(part) for part in parts]
        if ''.join(shaped_parts) != complete:
            raise ValueError('Thai line break would split a shaped cluster')
        return '\u200b'.join(shaped_parts)

    augmenter.shape_span = with_breaks


def probe(args):
    repo = Path(__file__).resolve().parents[1]
    if uharfbuzz.__version__ != '0.51.7':
        raise ValueError('expected uharfbuzz 0.51.7')
    if dialogue.sha(args.shaper.read_bytes()) != SONIC_SHAPER_SHA:
        raise ValueError('unexpected Sonic reference shaper revision')
    spec = importlib.util.spec_from_file_location('sonic_font_probe', args.shaper)
    shaper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(shaper)
    shaper.KNOWN_TMP_TAG = TMP_TAG
    dialogue.SITE_LOCALES = args.site_catalog
    raw = args.worklist.read_bytes()
    worklist = json.loads(raw)
    rows = {row['id']: row for row in worklist['rows']}
    if len(rows) != len(worklist['rows']) or len(rows) != 1947:
        raise ValueError('expected the complete Dragons paired worklist')
    split_thai = thai_breaker(args.icu) if args.icu else None
    if args.ltr_corpus and not split_thai:
        raise ValueError('Thai corpus preparation requires ICU 78 for soft line breaks')
    if split_thai and split_thai('ภาษาไทย') != ['ภาษา', 'ไทย']:
        raise ValueError('ICU Thai dictionary line-break control failed')
    sources = {'macos': args.macos_data, 'windows': args.windows_data}
    stock = {platform: stock_font(platform, data) for platform, data in sources.items()}
    args.output.mkdir()
    report = {'scope': 'offline glyph inventory and synthetic staged-asset probe',
              'worklistSha256': dialogue.sha(raw), 'shaperSha256': SONIC_SHAPER_SHA,
              'harfBuzz': uharfbuzz.version_string(), 'locales': {}}
    for locale, sample in SAMPLES.items():
        if locale == 'he':
            font = args.hebrew_font
        else:
            font = args.fonts / f"{'ar-fa' if locale in ('ar', 'fa') else locale}.ttf"
        authored = repo / 'localization' / locale / 'translation.json'
        values = paired_locale.read(authored, locale, worklist['yarnScopeSha256'], rows)
        target = args.output / locale
        target.mkdir()
        augmenter = shaper.FontAugmenter(font, shaper.LOCALE_SPECS[locale])
        shaped = augmenter.shape_span(sample)
        if not shaped or not all(0xE000 <= ord(c) <= 0xF8FF for c in shaped):
            raise ValueError(f'{locale}: synthetic shaping did not produce mapped glyphs')
        if augmenter.shape_span(sample) != shaped or augmenter.shape_rich_text('TMP-42') != 'TMP-42':
            raise ValueError(f'{locale}: repeat or LTR control failed')
        # The managed probe uses TMP's stock LTR mode. The synthetic RTL case
        # is one run; mixed paragraphs need line-aware ordering.
        visual = shaped[::-1] if shaper.LOCALE_SPECS[locale]['baseDirection'] == 'R' else shaped
        mappings = {sample: visual, f'<i>{sample}</i>': f'<i>{visual}</i>'}
        corpus_mappings = args.ltr_corpus and locale in ('th', 'hi')
        if corpus_mappings and locale == 'th':
            preserve_thai_breaks(augmenter, split_thai)
        if corpus_mappings:
            for logical in sorted(set(authored_display_values(values, rows))):
                if not augmenter.has_script(logical):
                    continue
                display = augmenter.shape_rich_text(logical)
                shaper.validate_shaped_value(logical, display, augmenter, f'{locale} authored display')
                mappings[logical] = display
        prepared = target / 'probe.ttf'
        augmenter.save(prepared)
        with TTFont(prepared) as face:
            cmap, metrics = face.getBestCmap(), face['hmtx'].metrics
            for row in augmenter.rows:
                if (cmap.get(int(row['codepoint'][2:], 16)) != row['glyph']
                        or metrics[row['glyph']][0] != max(0, row['xAdvance'])):
                    raise ValueError(f'{locale}: shaped glyph or advance failed read-back')
        item = {'translationSha256': dialogue.sha(authored.read_bytes()),
                'fontSha256': dialogue.sha(font.read_bytes()),
                'probeFontSha256': dialogue.sha(prepared.read_bytes()),
                'syntheticSample': sample, 'glyphInstances': augmenter.rows, 'platforms': {}}
        records = [{'logical': logical, 'prepared': prepared_text}
                   for logical, prepared_text in sorted(mappings.items())]
        (target / 'display-map.json').write_text(json.dumps(records, ensure_ascii=False) + '\n')
        item['displayMapSha256'] = dialogue.sha((target / 'display-map.json').read_bytes())
        item['displayMapEntries'] = len(records)
        item['softBreaks'] = sum(text.count('\u200b') - logical.count('\u200b')
                                 for logical, text in mappings.items())
        item['displayMapScope'] = 'authored LTR strings and synthetic control' if corpus_mappings else 'synthetic only'
        for platform, data in sources.items():
            chars = defaultdict(set)
            for key, by_platform in values.items():
                for c in by_platform.get(platform, ''):
                    if unicodedata.category(c) not in {'Cc', 'Cf'}:
                        chars[c].add(key)
            primary, stock_data = stock[platform]
            with TTFont(BytesIO(stock_data)) as stock_face, TTFont(font) as candidate:
                gaps = {c for c in chars if ord(c) not in primary} - valid_glyphs(stock_face, chars)
                missing = gaps - valid_glyphs(candidate, gaps)
            stage = target / platform
            stage.mkdir()
            asset = stage / fallback.ASSET
            shutil.copyfile(data / fallback.ASSET, asset)
            # This asset is a probe, with no redistribution license or package manifest.
            resource = fallback.Resource(prepared.read_bytes(), b'', locale)
            receipt = fallback.add(platform, data, asset, resource)
            item['platforms'][platform] = {
                'authoredBindings': sum(platform in v for v in values.values()),
                'mixedDirectionIds': [key for key, v in values.items()
                                      if platform in v and needs_bidi(v[platform])],
                'distinctVisibleCandidates': len(chars),
                'stockGapCount': len(gaps),
                'remainingAfterCandidate': {f'U+{ord(c):04X}': sorted(chars[c])
                                            for c in sorted(missing)},
                'stagedAsset': {k: v for k, v in receipt.items() if k != 'licenseSha256'},
            }
        report['locales'][locale] = item
    (args.output / 'result.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ltr-corpus', action='store_true',
                        help='also stage all authored Thai and Hindi strings for offline verification')
    parser.add_argument('--icu', type=Path, help='ICU 78 library for Thai dictionary breaks')
    for name in ('macos-data', 'windows-data', 'site-catalog', 'worklist', 'fonts',
                 'hebrew-font', 'shaper', 'output'):
        parser.add_argument('--' + name, required=True, type=Path)
    probe(parser.parse_args())


if __name__ == '__main__':
    main()
