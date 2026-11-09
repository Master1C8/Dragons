"""Share the audited serialized UI roles between the inventory and builders."""
import json
from pathlib import Path

import credit_name_preservation as credits
import dialogue_locale as dl

ROLES = Path(__file__).parent / 'evidence/ui-source-roles-20261107.json'
ROLES_SHA = '6219fb3d833a85a61e92392fe7c002738d8b105db61f3f39d82f27153ecfefdc'
EXACT_ROLES = {
    'version-display-needs-consumer-review': 'preserve-exactly-version-placeholder',
    'dialogue-presenter-template-needs-consumer-review': 'preserve-exactly-dialogue-presenter-template',
    'settings-prefab-template-needs-consumer-review': 'preserve-exactly-settings-prefab-template',
    'cheat-menu-text-needs-visibility-review': 'preserve-exactly-development-menu-text',
    'slot-progress-runtime-replaced': 'preserve-exactly-slot-progress-template',
    'dialogue-option-template-runtime-replaced': 'preserve-exactly-dialogue-option-template',
}


def validate(platform, asset, source, replacements):
    credits.validate(platform, asset, source, replacements)
    raw = ROLES.read_bytes()
    if dl.sha(raw) != ROLES_SHA:
        raise ValueError('UI preservation report fingerprint mismatch')
    report = json.loads(raw, object_pairs_hook=dl.unique_object)
    for row in report['entries']:
        binding = row[platform]
        if row['asset'] != asset or row['provisionalRole'] not in EXACT_ROLES or binding is None:
            continue
        key = binding['id']
        value = source.get(key)
        if value is None or dl.sha(value.encode('utf-8')) != binding['sourceTextSha256']:
            raise ValueError(f'protected UI source mismatch: {key}')
        if key in replacements and replacements[key] != value:
            raise ValueError(f'protected UI text must remain exact: {key}')


def read_locale(platform, asset, path, source, source_hash):
    locale, replacements = dl.read_locale(
        path, list(source), list(source.values()), source_hash, yarn_semantics=False,
    )
    validate(platform, asset, source, replacements)
    return locale, replacements
