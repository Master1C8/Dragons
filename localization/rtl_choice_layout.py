"""Right-align the pinned dialogue choice text prefab for RTL locales."""
import struct

import dialogue_locale as dl

ASSET = 'sharedassets1.assets'
LOCALES = frozenset(('ar', 'fa', 'he'))
TEXT = {
    'macos': (11117, '1c3a0c2e4b49d50f05e2d2e2eee423c299ed7f4dd8749274d0990e5d0fc72513'),
    'windows': (11105, '3ebcb0c4c115da384c40005e759eec78ff525e9dda7f186a9f7e627bc6903183'),
}


def apply(platform, objects, changed):
    path_id, expected = TEXT[platform]
    identity = (path_id, 'MonoBehaviour')
    obj = objects[identity]
    raw = obj.get_raw_data()
    if dl.sha(raw) != expected or identity in changed:
        raise ValueError('unexpected or overlapping RTL choice text prefab')
    # Keep vertical alignment, retain left padding, and add equal right padding.
    updated = bytearray(raw)
    struct.pack_into('<I', updated, 324, 4)
    struct.pack_into('<f', updated, 480, 30.0)
    changed[identity] = bytes(updated)
    obj.set_raw_data(changed[identity])
