#!/usr/bin/env python3
"""Assemble a provisional paired source inventory from pinned discovery exports."""
import argparse
from collections import Counter
import json
from pathlib import Path

import dialogue_locale as dl
import credit_name_preservation as credits
import managed_source_roles as managed

FILES = {
    'yarn-paired-scenes.json': '52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995',
    'ui-windows-all.json': '598c2adb429385d9abc07c68a2ed7465bf2ae510ae70d5f5e5850c3b2c33efca',
    'settings-paired-source.json': 'eda16ce679eedf3e5b76beb76c8e9bc49a62c974639ab6327ea6063c6ad5cf25',
    'legacy-ui-macos.json': '7633ab7cf7622438d7f0ab17c2f58a8ad6190bef255bfb2c177738a2687970c8',
    'legacy-ui-windows.json': 'ff233b106664f8de1fd9f73123dfad1c43babd037ad16f2721d0e915d83b24db',
    'game-components-v2-macos.json': 'bcdca1bc07d540770fe2ca53c40254482353a819acc4d7b026a309ea4987bd96',
    'game-components-v2-windows.json': '25491d730b8b4d81f109ab907248bc8c67c7827c68fe989285dae27921174980',
    'managed-strings-v2-macos.json': '86152819357c568695ba203f2dc434bf7beaccaf1f2534fa95ea4203cdf916ed',
    'managed-strings-v2-windows.json': '3c3a38efa1657c3a02aabc8ecade3db3312ce816cdafea7169ae892414b7c51c',
    'managed-strings-v2-macos-settings.json': '62c9cfebe9c34f01bff27d59aa38b2a0ba690eccdaa1b2c6b521b2c4d1cf8682',
    'managed-strings-v2-windows-settings.json': 'cc975c8a60970047500a07488391ee0323c6fe2e0a5c881d250a7c3c48056337',
    'managed-strings-v2-macos-yarn-unity.json': '3fba6592de02b9c1b6036d39efac47f1c7e3049fca74a0282c06aab73d50ae8e',
    'managed-strings-v2-windows-yarn-unity.json': 'fa21afafe9e5b239a82723a8caacfd3d005cafa38436ad3ada5e6b0ce1f6e1ee',
    'managed-strings-v2-macos-tmp.json': '3f85b9d2458ba010fed921bcfdd46073e65ba1917c7c1b6455b63d4146802388',
    'managed-strings-v2-windows-tmp.json': '1c258b4d54b65a9268560fc77e89a8a8221132be94e7611dad5a7c6ef8da2e19',
    'managed-strings-v2-macos-unity-ui.json': '43506a8ce205f5c19048dcd96fed9d962fbac1b54f455cd33ae5ad2f66d77462',
    'managed-strings-v2-windows-unity-ui.json': '5a690f36f96654e4cced458207c636ed965b1d26443b06a83e20b634e930ae74',
    'managed-context-macos.json': '261278f7b8e69098856623ae108ea7cd6d0d0e8afc128ffb1d82dd041179879f',
    'managed-context-macos-settings.json': '4598c0ce5071b441595886957fa4965dc8da345de644a9c7f16458e5ff36025d',
    'managed-context-macos-yarn-unity.json': 'c5c7d6ef1d22f48aa15165f1508deff84a3c1a1fe3ba223637e0a66d43a106c7',
    'managed-context-macos-tmp.json': '988f663139b9a214db64c5228aefa7dac1ef2e717a08e106a8903d848bd5e8b8',
    'managed-context-macos-unity-ui.json': '56a47beabd0b2fc841d9196dbad59cd29b3e329393a70b77f381980232c0e45e',
    'managed-context-windows.json': 'c535b980972ff114ebc16d62ba7c169da46f35f485c68d5126aa543ac17f6818',
    'managed-context-windows-settings.json': 'd480d63b3dc2497261b51053894d238124c751ddd0ca3bccf967738b1a477e45',
    'managed-context-windows-yarn-unity.json': '70cbfcacc030d63f98d3bb3c6dda3c3fb147c918981cc3ed96e035846c62b5d3',
    'managed-context-windows-tmp.json': '0908f4de904023297d26fb79df3657e13298ee3c0e5d56986c9f195f106bb629',
    'managed-context-windows-unity-ui.json': 'ab87cd0c8164a241862771b6814941e1e3cd4038bb4b82b42333e93e99524f3b',
}
ROLES_SHA = '6219fb3d833a85a61e92392fe7c002738d8b105db61f3f39d82f27153ecfefdc'
INPUT_ACTION_SHA = {
    'macos': '6272020c5766750fe68af6c6601c8c70c6830bc47b9a558af9b20a124d2f6daf',
    'windows': 'dd06623f942b4b5619a278f51ba7dc9c6de5845752d7776e4d06c7b86455a998',
}
YARN_PROTECTED_SHA = 'bff5f4ce3b270dedf77f31518a3bb75efe72d93617796baeff71cbebb5872be3'
OPENING_ROLES_SHA = 'ad01a97ccffb6ea648bd5df90d42416e3c528f649f3fd4a5b5881a3c6a322025'
RYAN23_ROLES_SHA = '82f0dd640b385abeb4a06cec54cc267c61ac60d790035d55a72a3b4a0b7669e1'
RYAN45_ROLES_SHA = '673f13e007da9ae66585d950094a4e660b38c0f13872a7ae013dfe5387d8ec9d'
RYAN_EXTRA_ROLES_SHA = '73f065159d49a1b2cd173cc6d2a333ecb4200c40edd5ab60800640b28b1e5c23'
RYAN_FOOD_ROLES_SHA = '5a0ae69141a87f981bd9249f4ed657387cba73e81073393a6ebfa1f2adef86fa'
CONRAD3_ROLES_SHA = 'cfcfc9ead9be0b1b0d90e5f91862fd09657b9199ce49eba40c3f8a3712df41d3'
CONRAD124_ROLES_SHA = '66a1abafedf495b6e803508500a8cd9ee97bc41565c709296de760b475dc9e17'
ALEXANDER_LEVEL_ROLES_SHA = 'ce9fa72e0a240e38135d17f6e440f17e9c3260086fe27ea43a511a395aa0e3ab'
REMAINING_YARN_ROLES_SHA = 'a563b1027e04af5ed0a6b111cde5eb73a6f11638da6533711fd8389fa526fbb0'
# Pinned ResourceManager and render debugger prefab bindings for the legacy text export.
LEGACY_DEBUG_ROOTS = {
    'DebugUIBitField', 'DebugUIButton', 'DebugUIColor', 'DebugUIEnumField', 'DebugUIEnumHistory',
    'DebugUIFloatField', 'DebugUIFoldout', 'DebugUIGroup', 'DebugUIHandlerRenderingLayerField',
    'DebugUIIntField', 'DebugUIMessageBox', 'DebugUIObject', 'DebugUIObjectList', 'DebugUIObjectPopupField',
    'DebugUIPanel', 'DebugUIProgressBar', 'DebugUIRow', 'DebugUIToggle', 'DebugUIToggleHistory',
    'DebugUIUIntField', 'DebugUIValue', 'DebugUIValuePersistent', 'DebugUIValueTuple', 'DebugUIVector2',
    'DebugUIVector3', 'DebugUIVector4',
}
MANAGED_CONSUMER_SHA = {
    'macos': {
        'setter': 'ea9b68355a532b71831596b4a081dcbebe4de91da3f130a735d51447b83cfa52',
        'reason': '80c3cdd990c097e4c219daa3b852e90ba1bfcbfa00c259ec1ae0c06c1154be44',
        'objective': '72ec67ad4136691a8fe1e60a32fcfaf03d73f97fdd98d476ccb2fe41bd74fce7',
    },
    'windows': {
        'setter': '23f54a5af3602f141a3773946720ff70d33da345919d24ac74cc7ad81ea6f122',
        'reason': 'a4da3783605fc928e282dbeb28e9a4335efee9974c9b64d2a2e8305c79bc391a',
        'objective': 'f5b037d22d5963fc46922b39ba02e0e31c4927642b414d64145f124cdddda0fb',
    },
}


def load_pinned(path, expected):
    raw = Path(path).read_bytes()
    if dl.sha(raw) != expected:
        raise ValueError(f'unsupported source export: {Path(path).name}')
    return json.loads(raw, object_pairs_hook=dl.unique_object)


def put(records, record):
    if record['id'] in records:
        raise ValueError(f'duplicate inventory identity: {record["id"]}')
    records[record['id']] = record


def bind_credit_names(roles, manifest, ui):
    if manifest.get('sourceRoleReportSha256') != ROLES_SHA or manifest.get('asset') != 'level2':
        raise ValueError('credit manifest role report mismatch')
    protected = {}
    for item in manifest['entries']:
        key = item['ids']['windows']
        if key in protected or dl.sha(item['source'].encode('utf-8')) != item['sourceSha256']:
            raise ValueError('duplicate or invalid credit-name binding')
        protected[key] = item
    if len(protected) != 34:
        raise ValueError('credit-name count mismatch')
    candidates = [r for r in roles['entries'] if r['provisionalRole'] == 'credit-name-preserve-candidate']
    if len(candidates) != len(protected):
        raise ValueError('credit-name role count mismatch')
    matched = set()
    for row in candidates:
        mac, win = row['macos'], row['windows']
        key = win['id'] if win else None
        if key not in protected or key in matched or not mac:
            raise ValueError('credit-name role identity mismatch')
        entry = protected[key]
        if (row['asset'] != manifest['asset'] or row['hierarchy'] != entry['hierarchy'] or
                mac['id'] != entry['ids']['macos'] or row['sameText'] is not True or
                mac['sourceTextSha256'] != entry['sourceSha256'] or
                win['sourceTextSha256'] != entry['sourceSha256'] or ui.get(key) != entry['source']):
            raise ValueError('credit-name source or hierarchy mismatch')
        matched.add(key)
    if matched != set(protected):
        raise ValueError('credit-name source occurrence missing')
    return matched


def bind_reviewed_roles(scenes, manifest, scoped_nodes, expected_count, *, excluded_ids=()):
    if manifest.get('schema') != 1 or manifest.get('sourceExportSha256') != FILES['yarn-paired-scenes.json']:
        raise ValueError('opening-role source binding mismatch')
    known = {'demo-dialogue-candidate': 'line', 'demo-choice-candidate': 'option',
             'dialogue-candidate': 'line', 'dialogue-punctuation-candidate': 'line',
             'choice-candidate': 'option', 'editor-prompt-candidate': 'line',
             'editor-choice-candidate': 'option', 'recovery-prompt-candidate': 'line',
             'recovery-choice-candidate': 'option', 'diagnostic-dialogue-candidate': 'line'}
    source = {row['id']: (node, row) for node in scoped_nodes for row in scenes['scenes'][node]
              if row['id'] not in excluded_ids}
    if len(source) != expected_count:
        raise ValueError('opening source identity count mismatch')
    matched = {}
    for group in manifest['groups']:
        if (group['node'] not in scoped_nodes or group['role'] not in known or
                group['kind'] != known[group['role']] or
                not group.get('reason') or not isinstance(group['ids'], list)):
            raise ValueError('invalid opening role group')
        for key in group['ids']:
            if key in matched or key not in source or (source[key][0], source[key][1]['kind']) != (group['node'], group['kind']):
                raise ValueError('opening role identity or kind mismatch')
            if group['role'] == 'dialogue-punctuation-candidate':
                a, b = (source[key][1]['source'][p] for p in ('macos', 'windows'))
                if a not in ('..', '...') or b != a:
                    raise ValueError('punctuation role source mismatch')
            matched[key] = group['role']
    if matched.keys() != source.keys():
        raise ValueError('opening source coverage mismatch')
    return matched


def bind_opening_roles(scenes, manifest):
    return bind_reviewed_roles(scenes, manifest,
        {'Start', 'Ryan_1_PhoneTutorial', 'Ryan_1_intro', 'Ryan_1_required', 'Ryan_1_nag', 'Ryan_1_Outro'}, 79)


def bind_ryan23_roles(scenes, manifest):
    return bind_reviewed_roles(scenes, manifest,
        {'Ryan_2_Outro', 'Ryan_2_intro', 'Ryan_2_required', 'Ryan_3_Outro',
         'Ryan_3_intro', 'Ryan_3_required', 'Ryan_3_wont_use_mount'}, 133)


def bind_ryan45_roles(scenes, manifest):
    return bind_reviewed_roles(scenes, manifest,
        {'Ryan_4_Cum', 'Ryan_4_JerkOff_Start', 'Ryan_4_Mount_Finish', 'Ryan_4_Mount_Start', 'Ryan_4_intro',
         'Ryan_5_Cum', 'Ryan_5_JerkOff_Start', 'Ryan_5_Mount_Finish', 'Ryan_5_Mount_Start',
         'Ryan_5_Outro_conrad_romanced', 'Ryan_5_Outro_ryan_conrad_romanced', 'Ryan_5_Outro_ryan_romanced',
         'Ryan_5_Required_conrad_romanced', 'Ryan_5_Required_ryan_conrad_romanced',
         'Ryan_5_Required_ryan_romanced', 'Ryan_5_intro', 'Ryan_5_intro_ryan_romanced'}, 197)


def bind_ryan_extra_roles(scenes, manifest):
    return bind_reviewed_roles(scenes, manifest,
        {'Ryan_Conrad_SexScene', 'Ryan_Conrad_SexScene_Cum', 'Ryan_Conrad_SexScene_Loop',
         'Ryan_SexScene', 'Ryan_SexScene_Cum', 'Ryan_SexScene_Loop', 'Ryan_egg_dialog',
         'Ryan_grab_basket', 'Ryan_grapes_dialog', 'Ryan_ham_dialog', 'Ryan_melon_dialog'}, 122)


def bind_conrad3_roles(scenes, manifest):
    return bind_reviewed_roles(scenes, manifest,
        {'Conrad_Intro_3', 'Conrad_idle_3_1', 'Conrad_idle_3_2', 'Conrad_Outro_3',
         'Conrad_started_jerkoff_3', 'Conrad_finished_jerkoff_3', 'Conrad_placed_mount_3',
         'Conrad_finished_mount_3', 'Conrad_3_PhoneTutorial'}, 112)


def bind_conrad124_roles(scenes, manifest):
    return bind_reviewed_roles(scenes, manifest,
        {'Conrad_Intro_1', 'Conrad_required_1', 'Conrad_Outro_1', 'Conrad_1_JerkOff_Start',
         'Conrad_1_Cum', 'conrad_mount_no', 'Conrad_Intro_2', 'Conrad_required_2',
         'Conrad_Outro_2', 'conrad_jerk_off_no', 'Conrad_Intro_4', 'Conrad_required_4',
         'Conrad_Outro_4', 'Conrad_4_JerkOff_Start', 'Conrad_4_Cum',
         'Conrad_4_Mount_Start', 'Conrad_4_Mount_Finish'}, 170)


def bind_alexander_level_roles(scenes, manifest):
    return bind_reviewed_roles(scenes, manifest,
        {'Alexander_1_intro', 'Alexander_1_required', 'Alexander_1_Outro',
         'alexander_jerk_off_no', 'alexander_mount_no',
         'Alexander_2_intro', 'Alexander_2_required', 'Alexander_2_Outro',
         'Alexander_3_intro', 'Alexander_3_required', 'Alexander_3_Outro',
         'Alexander_3_JerkOff_Start', 'Alexander_3_Cum',
         'Alexander_4_intro', 'Alexander_4_required', 'Alexander_4_Outro',
         'Alexander_4_JerkOff_Start', 'Alexander_4_Cum', 'Alexander_4_Mount_Start', 'Alexander_4_Mount_Finish',
         'Alexander_5_intro', 'Alexander_5_required', 'Alexander_5_Outro',
         'Alexander_5_JerkOff_Start', 'Alexander_5_Cum', 'Alexander_5_Mount_Start', 'Alexander_5_Mount_Finish',
         'Alexander_questions'}, 379)


def merge_reviewed_roles(role_sets, full, prefixes):
    if any(role_sets[i].keys() & role_sets[j].keys() for i in range(len(role_sets)) for j in range(i)):
        raise ValueError('reviewed Yarn role scopes overlap')
    merged = {}
    for roles in role_sets:
        merged.update(roles)
    if merged.keys() & full.keys() or any(merged[key] != 'dialogue-candidate'
            for key in merged.keys() & prefixes.keys()):
        raise ValueError('reviewed roles conflict with protected Yarn bindings')
    return merged


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
    opening = load_pinned(Path(__file__).with_name('yarn_roles_opening.json'), OPENING_ROLES_SHA)
    opening_roles = bind_opening_roles(scenes, opening)
    ryan23 = load_pinned(Path(__file__).with_name('yarn_roles_ryan23.json'), RYAN23_ROLES_SHA)
    ryan23_roles = bind_ryan23_roles(scenes, ryan23)
    ryan45 = load_pinned(Path(__file__).with_name('yarn_roles_ryan45.json'), RYAN45_ROLES_SHA)
    ryan45_roles = bind_ryan45_roles(scenes, ryan45)
    ryan_extra = load_pinned(Path(__file__).with_name('yarn_roles_ryan_extra.json'), RYAN_EXTRA_ROLES_SHA)
    extra_roles = bind_ryan_extra_roles(scenes, ryan_extra)
    ryan_food = load_pinned(Path(__file__).with_name('yarn_roles_ryan_food.json'), RYAN_FOOD_ROLES_SHA)
    food_roles = bind_reviewed_roles(scenes, ryan_food, {'ryan_food_dialogue'}, 111)
    conrad3 = load_pinned(Path(__file__).with_name('yarn_roles_conrad3.json'), CONRAD3_ROLES_SHA)
    conrad3_roles = bind_conrad3_roles(scenes, conrad3)
    conrad124 = load_pinned(Path(__file__).with_name('yarn_roles_conrad124.json'), CONRAD124_ROLES_SHA)
    conrad124_roles = bind_conrad124_roles(scenes, conrad124)
    alexander = load_pinned(Path(__file__).with_name('yarn_roles_alexander_levels.json'), ALEXANDER_LEVEL_ROLES_SHA)
    alexander_roles = bind_alexander_level_roles(scenes, alexander)
    role_sets = (opening_roles, ryan23_roles, ryan45_roles, extra_roles, food_roles,
                 conrad3_roles, conrad124_roles, alexander_roles)
    reviewed_roles = merge_reviewed_roles(role_sets, full, prefixes)
    remainder = load_pinned(Path(__file__).with_name('yarn_roles_remaining.json'), REMAINING_YARN_ROLES_SHA)
    remainder_roles = bind_reviewed_roles(scenes, remainder, scenes['scenes'], 520,
                                          excluded_ids=reviewed_roles.keys() | full.keys())
    reviewed_roles = merge_reviewed_roles((reviewed_roles, remainder_roles), full, prefixes)
    credit_manifest = load_pinned(credits.MANIFEST, credits.MANIFEST_SHA256)
    protected_names = bind_credit_names(roles, credit_manifest, ui)
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
                          'role': ('preserve-exactly-pending-source-role' if key in full else
                                   reviewed_roles.get(key, 'needs-classification')),
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
        role = row['provisionalRole']
        if win['id'] in protected_names:
            role = 'preserve-exactly-credit-name'
        elif role == 'version-display-needs-consumer-review':
            role = 'preserve-exactly-version-placeholder'
        put(records, {'id': 'ui:' + dl.sha(path.encode('utf-8')), 'family': 'ui',
                      'role': role,
                      'asset': row['asset'], 'hierarchy': row['hierarchy'],
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
    if (len(mac_legacy) != 149 or {asset for asset, _ in mac_legacy} != {'resources.assets'} or
            {row['hierarchy'][0] for row in mac_legacy.values()} != LEGACY_DEBUG_ROOTS):
        raise ValueError('legacy render debugger prefab binding mismatch')
    for (asset, object_id), a in mac_legacy.items():
        b = win_legacy[(asset, object_id)]
        if any(a[k] != b[k] for k in ('hierarchy', 'text', 'textSha256', 'rawSha256')):
            raise ValueError('legacy source mismatch')
        if dl.sha(a['text'].encode('utf-8')) != a['textSha256']:
            raise ValueError('legacy text hash mismatch')
        put(records, {'id': f'legacy:{asset}#{object_id}', 'family': 'legacy-ui',
                      'role': 'preserve-exactly-render-debug-template', 'hierarchy': a['hierarchy'],
                      'source': {'macos': a['text'], 'windows': b['text']},
                      'location': {'macos': f'{asset}#{object_id}', 'windows': f'{asset}#{object_id}'}})
    for platform in ('macos', 'windows'):
        report = inputs[platform]
        hashes = MANAGED_CONSUMER_SHA[platform]
        evidence = Path(roles_path).parent
        game_consumers = managed.bind_game_consumers(
            platform, docs[f'managed-strings-v2-{platform}.json'],
            load_pinned(work / f'text-setter-{platform}-v4.json', hashes['setter']),
            load_pinned(evidence / f'menu-reasons-{platform}-20261107.json', hashes['reason']),
            load_pinned(evidence / f'objective-code-{platform}-20261107.json', hashes['objective']))
        if report['platform'] != platform:
            raise ValueError('input action platform mismatch')
        input_records = {row['id']: row for row in [report['jsonLiteral'], *report['references']]}
        if len(input_records) != 28:
            raise ValueError('input action identity mismatch')
        matched_inputs = set()
        for suffix, assembly in (('', 'Assembly-CSharp'), ('-settings', 'UnityScriptableSettings'),
                                 ('-yarn-unity', 'YarnSpinner.Unity'), ('-tmp', 'Unity.TextMeshPro'),
                                 ('-unity-ui', 'UnityEngine.UI')):
            data = docs[f'managed-strings-v2-{platform}{suffix}.json']
            if len(data['strings']) != data['sourceInstructionCount']:
                raise ValueError('managed source occurrence count mismatch')
            context = managed.bind_context(data, docs[f'managed-context-{platform}{suffix}.json'])
            for row, detailed in zip(data['strings'], context):
                role = 'needs-classification'
                consumer = None
                if assembly == 'Assembly-CSharp' and row['id'] in input_records:
                    expected = input_records[row['id']]
                    if data['assemblySha256'] != report['assemblySha256'] or row['ilOffset'] != expected['offset']:
                        raise ValueError('input action code binding changed')
                    if ('utf8Sha256' in expected and dl.sha(row['value'].encode('utf-8')) != expected['utf8Sha256']) or (
                            'name' in expected and row['value'] != expected['name']):
                        raise ValueError('input action value changed')
                    role = 'preserve-exactly-input-control'
                    matched_inputs.add(row['id'])
                else:
                    binding = game_consumers.get(row['id']) if assembly == 'Assembly-CSharp' else None
                    binding = binding or managed.direct_role(row, assembly) or managed.context_role(detailed)
                    if binding is None and assembly == 'Assembly-CSharp':
                        binding = managed.game_specific_role(row)
                    if binding is None:
                        binding = managed.dependency_role(row, assembly)
                    if binding is not None:
                        role, consumer = binding
                        if role == 'diagnostic-text-needs-visibility-review' and consumer in managed.PLAYER_LOG_SINKS:
                            role = 'preserve-exactly-player-log-text'
                put(records, {'id': f'managed:{platform}:{assembly}:{row["id"]}', 'family': 'managed',
                              'role': role, 'assemblySha256': data['assemblySha256'],
                              'method': row['method'], 'ilOffset': row['ilOffset'],
                              'source': {platform: row['value']}, 'location': {platform: row['id']},
                              **({'consumer': consumer} if consumer is not None else {})})
        if matched_inputs != set(input_records):
            raise ValueError('input action source occurrences missing')
    for platform in ('macos', 'windows'):
        components = docs[f'game-components-v2-{platform}.json']
        if (components['schema'] != 1 or components['platform'] != platform
                or components['buildVersion'] != scenes['builds'][platform]['version']
                or components['programSha256'] != scenes['programSha256'][platform]
                or components['missingDialogueTargets']):
            raise ValueError('serialized game component source or Yarn binding mismatch')
        for obj in components['objects']:
            location = f'{obj["asset"]}#{obj["objectId"]}'
            for field in obj['fields']:
                path = json.dumps(field['path'], separators=(',', ':'))
                # These roles come from the fingerprinted component exports above.
                # The managed consumer audit treats both as internal metadata.
                role = field['role']
                if role in ('dragon-bark-description-needs-runtime-review',
                            'dragon-descriptor-name-needs-runtime-review'):
                    role = 'preserve-exactly-dragon-metadata'
                put(records, {'id': f'game-component:{platform}:{location}:{path}', 'family': 'game-component',
                              'role': role, 'source': {platform: field['value']},
                              'location': {platform: location}, 'fieldPath': field['path'],
                              'class': obj['class'], 'namespace': obj['namespace'],
                              'rawObjectSha256': obj['rawSha256']})
    counts = dict(sorted(Counter(x['family'] for x in records.values()).items()))
    return {'schema': 1, 'status': 'provisional-not-translation-ready', 'builds': scenes['builds'],
            'sourceExportsSha256': FILES, 'uiRolesSha256': ROLES_SHA, 'inputActionReportsSha256': INPUT_ACTION_SHA,
            'yarnProtectedReportSha256': YARN_PROTECTED_SHA, 'creditNameManifestSha256': credits.MANIFEST_SHA256,
            'openingRoleManifestSha256': OPENING_ROLES_SHA,
            'ryan23RoleManifestSha256': RYAN23_ROLES_SHA,
            'ryan45RoleManifestSha256': RYAN45_ROLES_SHA,
            'ryanExtraRoleManifestSha256': RYAN_EXTRA_ROLES_SHA,
            'ryanFoodRoleManifestSha256': RYAN_FOOD_ROLES_SHA,
            'conrad3RoleManifestSha256': CONRAD3_ROLES_SHA,
            'conrad124RoleManifestSha256': CONRAD124_ROLES_SHA,
            'alexanderLevelRoleManifestSha256': ALEXANDER_LEVEL_ROLES_SHA,
            'remainingYarnRoleManifestSha256': REMAINING_YARN_ROLES_SHA,
            'managedConsumerReportsSha256': MANAGED_CONSUMER_SHA,
            'familyCounts': counts,
            'entries': list(records.values()),
            'limitations': 'Provisional union of pinned discovery exports. Managed and game-component occurrences are build-specific and unpaired; roles, runtime visibility, other assemblies/resources, full exact-preservation contract, special-scene decisions and independent review remain incomplete. Texture text is excluded by owner decision.'}


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
