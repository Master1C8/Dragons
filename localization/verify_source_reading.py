#!/usr/bin/env python3
"""Verify a recorded partial scene-reading scope against its paired export."""
import argparse
import hashlib
import json
from pathlib import Path

import dialogue_locale as dl


def digest_rows(rows, platform):
    encoded = json.dumps([(r['id'], r['source'][platform]) for r in rows],
                         ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(encoded).hexdigest()


def verify(corpus_bytes, receipt):
    if receipt.get('schema') != 1 or receipt.get('status') != 'partial-source-read':
        raise ValueError('unsupported reading receipt')
    if dl.sha(corpus_bytes) != receipt['pairedScenesSha256']:
        raise ValueError('paired scene fingerprint changed')
    corpus = json.loads(corpus_bytes, object_pairs_hook=dl.unique_object)
    if receipt['programSha256'] != corpus['programSha256'] or receipt['builds'] != corpus['builds']:
        raise ValueError('build or program binding changed')
    nodes, ids = set(), []
    for entry in receipt['nodes']:
        name = entry['node']
        if name in nodes or name not in corpus['scenes']:
            raise ValueError('duplicate or unknown reviewed node')
        nodes.add(name)
        source = corpus['scenes'][name]
        current = [row['id'] for row in source]
        if entry['lineIds'] != current:
            raise ValueError(f'reviewed node IDs changed: {name}')
        if entry['sourceHashes'] != {platform: digest_rows(source, platform) for platform in ('macos', 'windows')}:
            raise ValueError(f'reviewed source text changed: {name}')
        ids.extend(current)
    if (len(ids) != len(set(ids)) or len(nodes) != receipt['nodesRead'] or
            len(ids) != receipt['lineOccurrences'] or len(set(ids)) != receipt['uniqueLineIds']):
        raise ValueError('reviewed reading count or identity mismatch')
    return {'nodes': len(nodes), 'uniqueIds': len(set(ids)), 'status': 'binding-valid-not-editorial-acceptance'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('paired_scenes', type=Path)
    parser.add_argument('receipt', type=Path)
    args = parser.parse_args()
    receipt = json.loads(args.receipt.read_text(encoding='utf-8'), object_pairs_hook=dl.unique_object)
    print(json.dumps(verify(args.paired_scenes.read_bytes(), receipt), indent=2))


if __name__ == '__main__':
    main()
