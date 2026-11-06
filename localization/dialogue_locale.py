#!/usr/bin/env python3
"""Build a version-pinned Drag'N Wash Yarn dialogue asset from a locale file."""
import argparse
import collections
import hashlib
import json
import os
from pathlib import Path
import re
import struct

ASSET_HASH = 'f8c5c51ac1b0cf151177c05ee1805e032cf62baf384bb664337a71b923bee7b8'
OBJECT_HASH = '9baafe5b3c36e63042cc0d02b2c755580e142447cea13f946d485a342c269853'
PATH_ID = 10623
SITE_LOCALES = Path.home() / 'Desktop/SiteForMods/lib/language-data/site-locales.ts'
TOKENS = re.compile(r'<[^<>\n]*>|\{[^{}\n]*\}|\[[^\[\]\n]*\]')
TAGS = re.compile(r'<[^<>\n]*>|\[[^\[\]\n]*\]')
PREFIX = re.compile(r'^([A-Za-z][A-Za-z0-9_ .-]{0,40}:\s*)')


def sha(data):
    return hashlib.sha256(data).hexdigest()


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def site_locales():
    text = SITE_LOCALES.read_text(encoding='utf-8')
    match = re.search(r'export const SITE_LOCALE_CODES = \[([\s\S]*?)\] as const;', text)
    if not match:
        raise ValueError('canonical site locale catalog has an unsupported format')
    body = match.group(1)
    if re.sub(r'"[A-Za-z0-9-]+"\s*,|\s+', '', body):
        raise ValueError('canonical site locale catalog contains unexpected syntax')
    values = re.findall(r'"([A-Za-z0-9-]+)"', body)
    if len(values) != len(set(values)) or 'en' not in values:
        raise ValueError('canonical site locale catalog is invalid')
    return frozenset(values) - {'en'}


def read_u32(data, pos):
    if pos + 4 > len(data):
        raise ValueError('truncated integer')
    return struct.unpack_from('<I', data, pos)[0], pos + 4


def read_string(data, pos):
    size, pos = read_u32(data, pos)
    end = pos + ((size + 3) & ~3)
    if size > len(data) or end > len(data):
        raise ValueError('invalid string length')
    return data[pos:pos + size].decode('utf-8', errors='strict'), end


def write_string(value):
    data = value.encode('utf-8')
    return struct.pack('<I', len(data)) + data + b'\0' * ((-len(data)) % 4)


def parse(data):
    if len(data) < 40 or data[28:36] != b'\x02\0\0\0en\0\0':
        raise ValueError('unexpected Yarn localization object header')
    pos = 36
    count, pos = read_u32(data, pos)
    if count != 1839:
        raise ValueError(f'unexpected key count: {count}')
    keys = []
    for _ in range(count):
        item, pos = read_string(data, pos)
        keys.append(item)
    if len(set(keys)) != count or any(not re.fullmatch(r'line:[0-9a-f]{8}', k) for k in keys):
        raise ValueError('unexpected or duplicate line identifiers')
    value_count, pos = read_u32(data, pos)
    if value_count != count:
        raise ValueError('key/value count mismatch')
    values, extras = [], []
    for _ in range(count):
        value, pos = read_string(data, pos)
        if pos + 24 > len(data):
            raise ValueError('truncated value metadata')
        values.append(value)
        extras.append(data[pos:pos + 24])
        pos += 24
    if data[pos:] != bytes(8):
        raise ValueError('unexpected localization object trailer')
    return keys, values, extras


def encode(original, keys, values, extras):
    out = bytearray(original[:36])
    out += struct.pack('<I', len(keys))
    for key in keys:
        out += write_string(key)
    out += struct.pack('<I', len(values))
    for value, extra in zip(values, extras):
        out += write_string(value) + extra
    out += bytes(8)
    return bytes(out)


def read_locale(path, keys, values, source_hash=OBJECT_HASH, *, yarn_semantics=True):
    doc = json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=unique_object)
    if not isinstance(doc, dict) or set(doc) != {'schema', 'locale', 'sourceObjectSha256', 'lines'}:
        raise ValueError('locale file must contain exactly schema, locale, sourceObjectSha256, lines')
    if type(doc['schema']) is not int or doc['schema'] != 1 or doc['sourceObjectSha256'] != source_hash:
        raise ValueError('unsupported schema or source fingerprint')
    if not isinstance(doc['locale'], str) or doc['locale'] not in site_locales():
        raise ValueError('locale must be a supported non-English site language code')
    lines = doc['lines']
    if not isinstance(lines, dict) or not lines:
        raise ValueError('lines must be a non-empty object')
    source = dict(zip(keys, values))
    if set(lines) - source.keys():
        raise ValueError('unknown line IDs: ' + ', '.join(sorted(set(lines) - source.keys())[:10]))
    for key, value in lines.items():
        if not isinstance(value, dict) or set(value) != {'source', 'text'}:
            raise ValueError(f'{key}: expected exactly source and text')
        if value['source'] != source[key] or not isinstance(value['text'], str) or not value['text'].strip():
            raise ValueError(f'{key}: source mismatch or empty/non-string translation')
        if source[key].startswith('title:') and value['text'] != source[key]:
            raise ValueError(f'{key}: title directive must remain unchanged')
        # Yarn's line provider enables implicit character names and its parser
        # interprets text before a colon as a speaker. Until every such source
        # case is classified, reject both new and removed delimiters in Yarn
        # values. This rule must not be applied to unrelated UI/settings text.
        if yarn_semantics and (':' in source[key]) != (':' in value['text']):
            raise ValueError(f'{key}: implicit speaker delimiter presence changed')
        if yarn_semantics and ':' in source[key] and not PREFIX.match(source[key]) and value['text'] != source[key]:
            raise ValueError(f'{key}: unclassified colon-bearing source must remain unchanged')
        if collections.Counter(TOKENS.findall(source[key])) != collections.Counter(TOKENS.findall(value['text'])):
            raise ValueError(f'{key}: markup or placeholders differ')
        if TAGS.findall(source[key]) != TAGS.findall(value['text']):
            raise ValueError(f'{key}: markup order differs')
        prefix = PREFIX.match(source[key])
        if prefix and not value['text'].startswith(prefix.group(1)):
            raise ValueError(f'{key}: initial label/command must remain unchanged')
        if '\0' in value['text']:
            raise ValueError(f'{key}: NUL is not allowed')
    return doc['locale'], {k: v['text'] for k, v in lines.items()}


def load_asset(path):
    try:
        import UnityPy
    except ImportError as exc:
        raise RuntimeError('UnityPy 1.25.4 is required; see README.md') from exc
    if UnityPy.__version__ != '1.25.4':
        raise RuntimeError(f'Expected UnityPy 1.25.4, found {UnityPy.__version__}')
    path = Path(path)
    if sha(path.read_bytes()) != ASSET_HASH:
        raise ValueError('unsupported or modified asset: source SHA-256 does not match')
    env = UnityPy.load(str(path))
    matches = [o for o in env.objects if o.path_id == PATH_ID and o.type.name == 'MonoBehaviour']
    if len(matches) != 1:
        raise ValueError('expected one Yarn localization object')
    raw = matches[0].get_raw_data()
    if sha(raw) != OBJECT_HASH:
        raise ValueError('unexpected Yarn localization object fingerprint')
    keys, values, extras = parse(raw)
    if encode(raw, keys, values, extras) != raw:
        raise ValueError('source object does not round-trip exactly')
    return env, matches[0], raw, keys, values, extras


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('asset', type=Path, help='original sharedassets1.assets')
    parser.add_argument('--export', type=Path, help='write source IDs and text as JSON')
    parser.add_argument('--locale', type=Path, help='locale JSON file')
    parser.add_argument('--output', type=Path, help='new output asset; never overwrites')
    args = parser.parse_args()
    if bool(args.export) == bool(args.locale) or bool(args.locale) != bool(args.output):
        parser.error('use --export FILE or --locale FILE --output FILE')
    env, obj, raw, keys, values, extras = load_asset(args.asset)
    if args.export:
        with args.export.open('x', encoding='utf-8') as f:
            json.dump({'schema': 1, 'sourceObjectSha256': OBJECT_HASH, 'lines': dict(zip(keys, values))}, f, ensure_ascii=False, indent=2)
            f.write('\n')
        print(f'Exported {len(keys)} source lines to {args.export}')
        return
    locale, translations = read_locale(args.locale, keys, values, yarn_semantics=True)
    replacement = [translations.get(k, v) for k, v in zip(keys, values)]
    changed = encode(raw, keys, replacement, extras)
    if parse(changed) != (keys, replacement, extras):
        raise ValueError('rebuilt object failed exact structural read-back')
    obj.set_raw_data(changed)
    result = env.file.save()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    # Reserve the target first: neither the original nor an existing output can be overwritten.
    fd = os.open(args.output, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(result)
        import UnityPy
        check = UnityPy.load(str(args.output))
        matches = [o for o in check.objects if o.path_id == PATH_ID and o.type.name == 'MonoBehaviour']
        if len(matches) != 1 or matches[0].get_raw_data() != changed:
            raise ValueError('saved asset failed exact object read-back')
        before = {(o.path_id, o.type.name): o for o in env.objects}
        after = {(o.path_id, o.type.name): o for o in check.objects}
        if len(before) != len(env.objects) or len(after) != len(check.objects) or before.keys() != after.keys():
            raise ValueError('saved asset object inventory changed or contains duplicate identifiers')
        for key, old in before.items():
            if key[0] != PATH_ID and old.get_raw_data() != after[key].get_raw_data():
                raise ValueError(f'unrelated Unity object changed: {key}')
    except BaseException:
        args.output.unlink(missing_ok=True)
        raise
    print(f'Built {locale}: {len(translations)}/{len(keys)} lines; output SHA-256 {sha(result)}')
    print('Remaining lines retain English. Runtime loading, fonts, UI and shaping are not verified.')


if __name__ == '__main__':
    main()
