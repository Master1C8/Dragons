#!/usr/bin/env python3
"""Inventory source Yarn lines with implicit-speaker delimiters."""
import argparse
import json
from pathlib import Path
import re

import dialogue_locale as dl
import map_yarn_context as mapping

SPEAKER = re.compile(r'^[^:]*:\s*')


def inspect(root, platform):
    keys, values, _, program, locations, _, _ = mapping.load_platform(Path(root), platform)
    records = []
    for key, value in zip(keys, values):
        match = SPEAKER.match(value)
        if match is None:
            continue
        prefix = match.group()
        name = prefix.split(':', 1)[0]
        role = ('known-character-prefix' if name in ('Ryan', 'Conrad') else
                'embedded-title-like-source-marker' if name == 'title' else 'nonstandard-prefix-needs-review')
        records.append({'id': key, 'location': locations[key], 'sourceSha256': dl.sha(value.encode('utf-8')),
                        'prefixSha256': dl.sha(prefix.encode('utf-8')), 'nameSha256': dl.sha(name.encode('utf-8')),
                        'nameCharacters': len(name), 'bodyCharacters': len(value[match.end():]), 'provisionalRole': role})
    return {'schema': 1, 'platform': platform, 'build': mapping.source.BUILDS[platform],
            'programSha256': dl.sha(program), 'implicitSpeakerCandidates': records,
            'limitations': 'Pattern-derived candidates in pinned Yarn table only. The parser and presentation path, dynamic markup, runtime state, events and actual visibility need separate validation; title-like strings remain protected.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data_dir', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
