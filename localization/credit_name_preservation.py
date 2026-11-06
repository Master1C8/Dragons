"""Protect version-bound contributor names in the credits UI."""
import json
from pathlib import Path

import dialogue_locale as dl

MANIFEST = Path(__file__).with_name('credit_name_preservation.json')
MANIFEST_SHA256 = '08ec3974239d2e32e7289826bc7a5c0764f46ae6d0798a524feeb1607784b675'


def validate(platform, asset, source, replacements):
    if platform not in ('macos', 'windows'):
        raise ValueError('unsupported credit-name platform')
    if asset != 'level2':
        return
    raw = MANIFEST.read_bytes()
    if dl.sha(raw) != MANIFEST_SHA256:
        raise ValueError('credit-name manifest fingerprint mismatch')
    doc = json.loads(raw, object_pairs_hook=dl.unique_object)
    if doc.get('schema') != 1 or doc.get('asset') != asset or len(doc.get('entries', [])) != 34:
        raise ValueError('invalid credit-name manifest')
    seen = set()
    for row in doc['entries']:
        key, expected = row['ids'][platform], row['source']
        if key in seen or dl.sha(expected.encode('utf-8')) != row['sourceSha256']:
            raise ValueError('invalid or duplicate credit-name binding')
        seen.add(key)
        if source.get(key) != expected:
            raise ValueError(f'credit-name source mismatch: {key}')
        if key in replacements and replacements[key] != expected:
            raise ValueError(f'credit name must remain exact: {key}')
