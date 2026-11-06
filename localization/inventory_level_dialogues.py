#!/usr/bin/env python3
"""Decode source-pinned level configuration references to Yarn nodes."""
import argparse
import json
from pathlib import Path

import UnityPy
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
import audit_yarn_targets as audit
import compare_yarn_versions as versions
import dialogue_locale as dl
import inventory_text_assets as inventory
import inventory_yarn_bindings as bindings
import settings_locale as settings

ARRAYS = {'setFlags', 'endFlags', 'progressDialogs', 'idleDialogs', 'nagDialogs'}
FIELDS = ['dragonDescriptor', 'weatherState', 'levelEvaluationType', 'setFlags', 'endFlags',
          'dialogIntro', 'progressDialogs', 'idleDialogs', 'nagDialogs', 'dialogOutro',
          'dragonSpawnFlag', 'dragonStartJerkingOffDialog', 'dragonCumDialog',
          'dragonStartMountDialogue', 'dragonFinishMountDialogue', 'phoneDialog',
          'playerSpawnTransformName', 'productivityMusicAllowed', 'introMusic']
DIALOG_FIELDS = ['dialogIntro', 'progressDialogs', 'idleDialogs', 'nagDialogs', 'dialogOutro',
                 'dragonStartJerkingOffDialog', 'dragonCumDialog', 'dragonStartMountDialogue',
                 'dragonFinishMountDialogue', 'phoneDialog']


def corrected_schema(generated):
    rows = [{k: v for k, v in row.items() if k != 'm_Children'} for row in generated.to_dict_list()]
    fields = [row['m_Name'] for row in rows if row['m_Level'] == 1][4:]
    if fields != FIELDS:
        raise ValueError('unexpected LevelConfiguration fields')
    output, seen, i = [], set(), 0
    while i < len(rows):
        row = rows[i]
        if row['m_Level'] == 1 and row['m_Name'] in ARRAYS:
            if row['m_Type'] != 'string':
                raise ValueError('unexpected generated array schema')
            end = i + 1
            while end < len(rows) and rows[end]['m_Level'] > 1:
                end += 1
            output.extend([dict(row, m_Type='vector'),
                           dict(row, m_Level=2, m_Type='Array', m_Name='Array', m_MetaFlag=0x4000),
                           dict(row, m_Level=3, m_Type='int', m_Name='size', m_MetaFlag=0),
                           dict(row, m_Level=3, m_Name='data')])
            output.extend(dict(child, m_Level=child['m_Level'] + 2) for child in rows[i + 1:end])
            seen.add(row['m_Name'])
            i = end
        else:
            output.append(row)
            i += 1
    if seen != ARRAYS:
        raise ValueError('missing LevelConfiguration array fields')
    return TypeTreeNode.from_list(output)


def named_closure(roots, code):
    if not roots <= code.keys():
        raise ValueError('closure roots include absent node')
    closure, pending, unresolved = set(roots), list(roots), []
    while pending:
        node = pending.pop()
        for index, (op, operands) in enumerate(code[node]):
            if op not in (16, 18):
                continue
            target = audit.one_string(operands, f'{node}#{index}')
            if target not in code:
                unresolved.append({'node': node, 'instructionIndex': index, 'target': target})
            elif target not in closure:
                closure.add(target)
                pending.append(target)
    line_ids = sorted({audit.one_string(operands, node) for node in closure
                       for op, operands in code[node] if op in (3, 5)})
    return {'roots': sorted(roots), 'nodes': sorted(closure), 'lineIds': line_ids,
            'unresolved': sorted(unresolved, key=lambda x: (x['node'], x['instructionIndex'], x['target']))}


def inspect(root, platform):
    root = Path(root)
    pinned = inventory.inspect(root, platform)
    _, _, _, program, nodes, _ = versions.load(root, versions.BUILDS[platform])
    env = UnityPy.load(str(root / 'sharedassets1.assets'))
    env.path = str(root)
    generator, cache, corrected, records = bindings.generator(root, platform), {}, None, []
    for obj in env.objects:
        if obj.type.name != 'MonoBehaviour':
            continue
        head = obj.parse_monobehaviour_head()
        script = head.m_Script.deref().read()
        if (script.m_Namespace, script.m_ClassName) != ('', 'LevelConfiguration'):
            continue
        checked_head, checked_script, generated = settings.nodes_for(obj, generator, cache)
        if (checked_script.m_Namespace, checked_script.m_ClassName) != ('', 'LevelConfiguration'):
            raise ValueError('unexpected level script identity')
        if corrected is None:
            corrected = corrected_schema(generated)
        tree = obj.read_typetree(nodes=corrected, check_read=True)
        settings.check_header(tree, checked_head, obj.path_id)
        raw = obj.get_raw_data()
        if obj.save_typetree(tree, nodes=corrected) != raw:
            raise ValueError(f'level schema did not round-trip: {obj.path_id}')
        refs = []
        for field in DIALOG_FIELDS:
            values = tree[field] if field in ARRAYS else [tree[field]]
            if not isinstance(values, list) or any(not isinstance(x, str) for x in values):
                raise ValueError(f'invalid dialogue reference field: {obj.path_id} {field}')
            refs.extend({'field': field, 'index': index if field in ARRAYS else None,
                         'target': value, 'targetPresent': value in nodes}
                        for index, value in enumerate(values) if value)
        records.append({'objectId': obj.path_id, 'name': head.m_Name, 'rawSha256': dl.sha(raw),
                        'dialogueReferences': refs})
    if not records or len({r['name'] for r in records}) != len(records):
        raise ValueError('empty or ambiguous level configuration inventory')
    roots = {ref['target'] for item in records for ref in item['dialogueReferences'] if ref['targetPresent']}
    code = audit.instruction_records(nodes)
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'assetSha256': pinned['assets']['sharedassets1.assets'], 'programSha256': dl.sha(program),
            'configurations': sorted(records, key=lambda x: x['name']),
            'namedTransferClosure': named_closure(roots, code),
            'limitations': 'Serialized LevelConfiguration fields in one pinned asset, statically compared with one Yarn program. No runtime selection, reachability, dynamically constructed nodes, other serialized reference classes, program merging or rendering is established.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data_dir', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
