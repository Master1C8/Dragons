#!/usr/bin/env python3
"""Inventory exact Unity AnimationClip event data in the pinned stock builds."""
import argparse
import json
from pathlib import Path

import UnityPy

import dialogue_locale as dialogue
import inventory_addressables as addressables
import inventory_text_assets as text_assets

BUILTINS = {
    'macos': {
        'Resources/unity default resources': '4c1f576076250b2225397e576da5d4f3eb0280fbcea1955c999218ba115f65f3',
        'Resources/unity_builtin_extra': 'da431ac53fd46ae56b285cbd1adfb6e8c25c75580080103fb1bfeaea1b371bc7',
    },
    'windows': {
        'Resources/unity default resources': 'fb2492cd1ad7c38dda8a4ce5f1a1fb57edcff44e3ae250b263e44beae3660ec4',
        'Resources/unity_builtin_extra': 'cc7e584091c6ccfb58a91e31fcb75471e68cd05754c7aeab6e0cf513e7998c2b',
    },
}
EVENT_FUNCTIONS = {'PlayStepSFX', 'PlayStepVFX', 'PlayAudio1', 'PlayAudio2'}


def classify(event):
    if event['functionName'] not in EVENT_FUNCTIONS or event['data'] != '':
        raise ValueError('unclassified animation event function or string argument')
    return 'preserve-exactly-animation-dispatch'


def inspect(root, platform):
    root = Path(root)
    pinned = text_assets.inspect(root, platform)
    extra = BUILTINS[platform] | {
        f'StreamingAssets/aa/{name}': digest
        for name, digest in addressables.FILES[platform].items() if name.endswith('.bundle')
    }
    sources = pinned['assets'] | extra
    clips = []
    for name, digest in sorted(sources.items()):
        path = root / name
        if name in extra and dialogue.sha(path.read_bytes()) != digest:
            raise ValueError(f'unsupported animation source: {name}')
        env = UnityPy.load(str(path))
        ids = set()
        for obj in env.objects:
            if obj.type.name != 'AnimationClip':
                continue
            if obj.path_id in ids:
                raise ValueError(f'duplicate animation clip ID: {name}#{obj.path_id}')
            ids.add(obj.path_id)
            raw = obj.get_raw_data()
            tree = obj.read_typetree(check_read=True)
            if obj.save_typetree(tree) != raw:
                raise ValueError(f'animation clip failed byte round trip: {name}#{obj.path_id}')
            events = [dict(index=i, role=classify(event), **event) for i, event in enumerate(tree['m_Events'])]
            clips.append({'asset': name, 'objectId': obj.path_id, 'name': tree['m_Name'],
                          'rawSha256': dialogue.sha(raw), 'events': events})
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'sources': sources, 'clips': clips, 'eventCount': sum(len(clip['events']) for clip in clips)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=BUILTINS)
    parser.add_argument('game_data', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.game_data, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
