#!/usr/bin/env python3
"""Record source-bound provisional Yarn full-value and prefix protections."""
import argparse
import json
from pathlib import Path

import dialogue_locale as dl

PAIRED_SHA = '52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995'
TARGETS_SHA = '9cd529422340084c5dda98865ad485930d8a92fb6790c77c9a7c2e66a70068e4'
LONG_COLON_ID = 'line:4b36ea4e'


def load(path, expected):
    raw = Path(path).read_bytes()
    if dl.sha(raw) != expected:
        raise ValueError(f'unsupported source input: {Path(path).name}')
    return json.loads(raw, object_pairs_hook=dl.unique_object)


def build(paired, audit):
    rows = {}
    for node, lines in paired['scenes'].items():
        for row in lines:
            if row['id'] in rows:
                raise ValueError('duplicate Yarn source ID')
            rows[row['id']] = {'node': node, **row}
    if len(rows) != paired['sourceLineCount']:
        raise ValueError('Yarn source count mismatch')
    title_ids = {}
    for platform in ('macos', 'windows'):
        title_ids[platform] = {v['lineId'] for v in audit['builds'][platform]['embeddedTitleMarkers'].values()}
    if title_ids['macos'] != title_ids['windows'] or len(title_ids['macos']) != 5:
        raise ValueError('title marker inventory differs')
    full, prefixes = [], []
    for key in sorted(rows):
        row = rows[key]
        sources = row['source']
        if key in dl.YARN_UNRESOLVED_SOURCE_MARKERS:
            if any(sources[p] != dl.YARN_UNRESOLVED_SOURCE_MARKERS[key] for p in ('macos', 'windows')):
                raise ValueError(f'unexpected marker source: {key}')
            reason = 'adjacent-marker-needs-review'
        elif key in title_ids['macos']:
            if any(not sources[p].startswith('title: ') for p in ('macos', 'windows')):
                raise ValueError(f'unexpected title source: {key}')
            reason = 'embedded-title-needs-review'
        elif key == LONG_COLON_ID:
            if any(sources[p] != 'The most prestigious college hosting prestigious professors like me:'
                   for p in ('macos', 'windows')):
                raise ValueError('unexpected long-colon source')
            reason = 'long-implicit-speaker-needs-adapter'
        else:
            reason = None
        if reason:
            full.append({'id': key, 'node': row['node'], 'reason': reason, 'expected': sources,
                         'sourceSha256': {p: dl.sha(sources[p].encode('utf-8')) for p in ('macos', 'windows')}})
        matches = {p: dl.PREFIX.match(sources[p]) for p in ('macos', 'windows')}
        if key not in title_ids['macos'] and any(matches.values()):
            if not all(matches.values()) or any(matches[p].group(1) not in ('Ryan: ', 'Conrad: ') for p in matches):
                raise ValueError(f'unexpected prefix classification: {key}')
            prefixes.append({'id': key, 'node': row['node'],
                             'expectedPrefix': {p: matches[p].group(1) for p in ('macos', 'windows')},
                             'sourceSha256': {p: dl.sha(sources[p].encode('utf-8')) for p in ('macos', 'windows')}})
    if len(full) != 16 or len(prefixes) != 18:
        raise ValueError('unexpected protected Yarn record counts')
    return {'schema': 1, 'status': 'partial-preservation-not-source-complete',
            'pairedScenesSha256': PAIRED_SHA, 'targetAuditSha256': TARGETS_SHA,
            'programSha256': paired['programSha256'], 'fullValueProtection': full, 'prefixProtection': prefixes,
            'limitations': 'Known source cases only. Exact protection is provisional, not a full preserve-exactly set, final translation classification, runtime test, or license to translate remaining strings.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('paired', type=Path)
    p.add_argument('target_audit', type=Path)
    args = p.parse_args()
    print(json.dumps(build(load(args.paired, PAIRED_SHA), load(args.target_audit, TARGETS_SHA)),
                     ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
