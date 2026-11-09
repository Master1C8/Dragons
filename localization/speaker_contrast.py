"""Apply the audited black text style to white speaker labels."""
import json
from pathlib import Path
import struct

import dialogue_locale as dl

ASSETS = frozenset(('level1', 'level3', 'level5', 'level6'))
INDEX_SHA = {
    'macos': '31c4aceb90095b0ecec2faa12ba97f45d79475b05dda469df515b922d5a46f68',
    'windows': '62074f46121cbd2cba35ad9a231ea1c1c750a62f25955d7d493ede1bc40cbede',
}
COLOR_OFFSET = 156
WHITE = struct.pack('<I4f', 0xffffffff, 1, 1, 1, 1)
BLACK = struct.pack('<I4f', 0xff000000, 0, 0, 0, 1)


def apply(platform, asset, objects, changed):
    """Change only the pinned TMP name component in a source-verified scene."""
    if asset not in ASSETS:
        raise ValueError(f'{asset}: no audited speaker contrast patch')
    path = Path(__file__).parent / 'evidence' / f'speaker-presenters-{platform}-20261107.json'
    index = path.read_bytes()
    if dl.sha(index) != INDEX_SHA[platform]:
        raise ValueError('speaker presenter index fingerprint mismatch')
    presenter, = [row for row in json.loads(index)['presenters']
                  if row['asset'] == asset and row['class'] == 'LinePresenter']
    target = presenter['nonNullTargets']['characterNameText']
    identity = (target['objectId'], 'MonoBehaviour')
    obj = objects[identity]
    raw = obj.get_raw_data()
    end = COLOR_OFFSET + len(WHITE)
    if dl.sha(raw) != target['rawSha256'] or raw[COLOR_OFFSET:end] != WHITE:
        raise ValueError(f'{asset}: unexpected speaker contrast source bytes')
    if changed.get(identity, raw) != raw:
        raise ValueError(f'{asset}: speaker contrast overlaps an edited name template')
    updated = raw[:COLOR_OFFSET] + BLACK + raw[end:]
    obj.set_raw_data(updated)
    changed[identity] = updated
