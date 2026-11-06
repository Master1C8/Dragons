#!/usr/bin/env python3
"""Assemble a provisional paired source inventory from pinned discovery exports."""
import argparse
from collections import Counter
import json
from pathlib import Path

import dialogue_locale as dl

FILES = {
    'yarn-paired-scenes.json': '52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995',
    'ui-windows-all.json': '598c2adb429385d9abc07c68a2ed7465bf2ae510ae70d5f5e5850c3b2c33efca',
    'settings-paired-source.json': 'eda16ce679eedf3e5b76beb76c8e9bc49a62c974639ab6327ea6063c6ad5cf25',
    'legacy-ui-macos.json': '7633ab7cf7622438d7f0ab17c2f58a8ad6190bef255bfb2c177738a2687970c8',
    'legacy-ui-windows.json': 'ff233b106664f8de1fd9f73123dfad1c43babd037ad16f2721d0e915d83b24db',
    'managed-strings-v2-macos.json': '86152819357c568695ba203f2dc434bf7beaccaf1f2534fa95ea4203cdf916ed',
    'managed-strings-v2-windows.json': '3c3a38efa1657c3a02aabc8ecade3db3312ce816cdafea7169ae892414b7c51c',
    'managed-strings-v2-macos-settings.json': '62c9cfebe9c34f01bff27d59aa38b2a0ba690eccdaa1b2c6b521b2c4d1cf8682',
    'managed-strings-v2-windows-settings.json': 'cc975c8a60970047500a07488391ee0323c6fe2e0a5c881d250a7c3c48056337',
    'managed-strings-v2-macos-yarn-unity.json': '3fba6592de02b9c1b6036d39efac47f1c7e3049fca74a0282c06aab73d50ae8e',
    'managed-strings-v2-windows-yarn-unity.json': 'fa21afafe9e5b239a82723a8caacfd3d005cafa38436ad3ada5e6b0ce1f6e1ee',
}
ROLES_SHA = '6219fb3d833a85a61e92392fe7c002738d8b105db61f3f39d82f27153ecfefdc'
INPUT_ACTION_SHA = {
    'macos': '6272020c5766750fe68af6c6601c8c70c6830bc47b9a558af9b20a124d2f6daf',
    'windows': 'dd06623f942b4b5619a278f51ba7dc9c6de5845752d7776e4d06c7b86455a998',
}
YARN_PROTECTED_SHA = 'bff5f4ce3b270dedf77f31518a3bb75efe72d93617796baeff71cbebb5872be3'


def load_pinned(path, expected):
    raw = Path(path).read_bytes()
    if dl.sha(raw) != expected:
        raise ValueError(f'unsupported source export: {Path(path).name}')
    return json.loads(raw, object_pairs_hook=dl.unique_object)


def put(records, record):
    if record['id'] in records:
        raise ValueError(f'duplicate inventory identity: {record["id"]}')
    records[record['id']] = record


def build(work, roles_path):
    work = Path(work)
    docs = {name: load_pinned(work / name, expected) for name, expected in FILES.items()}
    roles = load_pinned(roles_path, ROLES_SHA)
    inputs = {p: load_pinned(Path(roles_path).parent / f'input-actions-{p}-20261107.json', digest)
              for p, digest in INPUT_ACTION_SHA.items()}
    yarn_protected = load_pinned(Path(roles_path).parent / 'yarn-protected-partial-20261107.json', YARN_PROTECTED_SHA)
    full = {row['id']: row for row in yarn_protected['fullValueProtection']}
    prefixes = {row['id']: row for row in yarn_protected['prefixProtection']}
    if len(full) != 16 or len(prefixes) != 18 or full.keys() & prefixes.keys():
        raise ValueError('protected Yarn identity mismatch')
    scenes, ui, settings = docs['yarn-paired-scenes.json'], docs['ui-windows-all.json'], docs['settings-paired-source.json']
    records = {}
    for node, rows in scenes['scenes'].items():
        for row in rows:
            key = row['id']
            if key in full and (full[key]['node'] != node or full[key]['expected'] != row['source']):
                raise ValueError('protected Yarn value binding changed')
            if key in prefixes and (prefixes[key]['node'] != node or any(
                    not row['source'][p].startswith(prefixes[key]['expectedPrefix'][p]) or
                    dl.sha(row['source'][p].encode('utf-8')) != prefixes[key]['sourceSha256'][p]
                    for p in ('macos', 'windows'))):
                raise ValueError('protected Yarn prefix binding changed')
            put(records, {'id': 'yarn:' + key, 'family': 'yarn',
                          'role': 'preserve-exactly-pending-source-role' if key in full else 'needs-classification',
                          'node': node, 'instructionIndex': row['instructionIndex'], 'kind': row['kind'],
                          'instruction': {k: row[k] for k in ('substitutionCount', 'destination', 'hasCondition') if k in row},
                          'preserveExactPrefix': prefixes[key]['expectedPrefix'] if key in prefixes else None,
                          'source': row['source'], 'location': {p: row['id'] for p in ('macos', 'windows')}})
    if len(records) != scenes['sourceLineCount']:
        raise ValueError('Yarn count mismatch')
    if not (full.keys() | prefixes.keys()) <= {key.removeprefix('yarn:') for key in records}:
        raise ValueError('protected Yarn source occurrence missing')
    used_windows = set()
    for row in roles['entries']:
        win = row['windows']
        if not win or win['id'] in used_windows or win['id'] not in ui:
            raise ValueError('missing or duplicate UI source binding')
        used_windows.add(win['id'])
        value = ui[win['id']]
        if dl.sha(value.encode('utf-8')) != win['sourceTextSha256']:
            raise ValueError('Windows UI source mismatch')
        mac = row['macos']
        if mac and (row['sameText'] is not True or mac['sourceTextSha256'] != win['sourceTextSha256']):
            raise ValueError('macOS UI source mismatch')
        path = json.dumps([row['asset'], row['hierarchy']], ensure_ascii=False, separators=(',', ':'))
        put(records, {'id': 'ui:' + dl.sha(path.encode('utf-8')), 'family': 'ui',
                      'role': row['provisionalRole'], 'asset': row['asset'], 'hierarchy': row['hierarchy'],
                      'source': {'macos': value if mac else None, 'windows': value},
                      'location': {'macos': mac['id'] if mac else None, 'windows': win['id']}})
    if used_windows != set(ui):
        raise ValueError('unmapped Windows UI values')
    for name, pair in settings['settings'].items():
        all_fields = set().union(*(set(pair[p]['fields']) for p in ('macos', 'windows') if pair[p]))
        for field in sorted(all_fields):
            by_platform = {p: pair[p]['fields'].get(field) if pair[p] else None for p in ('macos', 'windows')}
            for value in by_platform.values():
                if value and dl.sha(value['source'].encode('utf-8')) != value['sourceSha256']:
                    raise ValueError('settings source mismatch')
            put(records, {'id': f'settings:{name}:{field}', 'family': 'settings', 'setting': name, 'field': field,
                          'role': {p: v['provisionalRole'] if v else None for p, v in by_platform.items()},
                          'source': {p: v['source'] if v else None for p, v in by_platform.items()},
                          'location': {p: v['id'] if v else None for p, v in by_platform.items()}})
    legacy = {p: docs[f'legacy-ui-{p}.json']['entries'] for p in ('macos', 'windows')}
    def legacy_map(rows):
        result = {}
        for item in rows:
            key = (item['asset'], item['objectId'])
            if key in result: raise ValueError('duplicate legacy object')
            result[key] = item
        return result
    mac_legacy, win_legacy = legacy_map(legacy['macos']), legacy_map(legacy['windows'])
    if mac_legacy.keys() != win_legacy.keys(): raise ValueError('legacy identity mismatch')
    for (asset, object_id), a in mac_legacy.items():
        b = win_legacy[(asset, object_id)]
        if any(a[k] != b[k] for k in ('hierarchy', 'text', 'textSha256', 'rawSha256')):
            raise ValueError('legacy source mismatch')
        if dl.sha(a['text'].encode('utf-8')) != a['textSha256']:
            raise ValueError('legacy text hash mismatch')
        put(records, {'id': f'legacy:{asset}#{object_id}', 'family': 'legacy-ui',
                      'role': 'debug-template-needs-review', 'hierarchy': a['hierarchy'],
                      'source': {'macos': a['text'], 'windows': b['text']},
                      'location': {'macos': f'{asset}#{object_id}', 'windows': f'{asset}#{object_id}'}})
    for platform in ('macos', 'windows'):
        report = inputs[platform]
        if report['platform'] != platform:
            raise ValueError('input action platform mismatch')
        input_records = {row['id']: row for row in [report['jsonLiteral'], *report['references']]}
        if len(input_records) != 28:
            raise ValueError('input action identity mismatch')
        matched_inputs = set()
        for suffix, assembly in (('', 'Assembly-CSharp'), ('-settings', 'UnityScriptableSettings'), ('-yarn-unity', 'YarnSpinner.Unity')):
            data = docs[f'managed-strings-v2-{platform}{suffix}.json']
            if len(data['strings']) != data['sourceInstructionCount']:
                raise ValueError('managed source occurrence count mismatch')
            for row in data['strings']:
                role = 'needs-classification'
                if assembly == 'Assembly-CSharp' and row['id'] in input_records:
                    expected = input_records[row['id']]
                    if data['assemblySha256'] != report['assemblySha256'] or row['ilOffset'] != expected['offset']:
                        raise ValueError('input action code binding changed')
                    if ('utf8Sha256' in expected and dl.sha(row['value'].encode('utf-8')) != expected['utf8Sha256']) or (
                            'name' in expected and row['value'] != expected['name']):
                        raise ValueError('input action value changed')
                    role = 'preserve-exactly-input-control'
                    matched_inputs.add(row['id'])
                put(records, {'id': f'managed:{platform}:{assembly}:{row["id"]}', 'family': 'managed',
                              'role': role, 'assemblySha256': data['assemblySha256'],
                              'method': row['method'], 'ilOffset': row['ilOffset'],
                              'source': {platform: row['value']}, 'location': {platform: row['id']}})
        if matched_inputs != set(input_records):
            raise ValueError('input action source occurrences missing')
    counts = dict(sorted(Counter(x['family'] for x in records.values()).items()))
    return {'schema': 1, 'status': 'provisional-not-translation-ready', 'builds': scenes['builds'],
            'sourceExportsSha256': FILES, 'uiRolesSha256': ROLES_SHA, 'inputActionReportsSha256': INPUT_ACTION_SHA,
            'yarnProtectedReportSha256': YARN_PROTECTED_SHA, 'familyCounts': counts,
            'entries': list(records.values()),
            'limitations': 'Provisional union of pinned discovery exports. Managed occurrences are build-specific and unpaired; roles, runtime visibility, other assemblies/resources, full exact-preservation contract, special-scene decisions and independent review remain incomplete. Texture text is excluded by owner decision.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--work', required=True, type=Path)
    p.add_argument('--ui-roles', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    args = p.parse_args()
    data = build(args.work, args.ui_roles)
    with args.output.open('x', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(json.dumps({'output': str(args.output), 'sha256': dl.sha(args.output.read_bytes()),
                      'familyCounts': data['familyCounts'], 'status': data['status']}))


if __name__ == '__main__':
    main()
