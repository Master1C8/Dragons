#!/usr/bin/env python3
"""Conservative, source-bound dependency enumeration for the author audit.

Run from the Dragons root. No game, package, or source files are modified.
The output is evidence for review, not a semantic or runtime pass.
"""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path('.')
P = ROOT / 'localization/pt-BR'
WORK = ROOT / 'localization/work'
INV = WORK / 'source-inventory-20261107/combined-provisional-v42-20261110.json'
SCOPE = WORK / 'yarn-markers-20261110.ridbPA/yarn-scope-v42.json'
SCENES = WORK / 'source-inventory-20261107/yarn-paired-scenes.json'
EXPECTED = {
    INV: '79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d',
    SCOPE: '753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30',
    SCENES: '52ccfea874938c04691ce607b143ab30dad29c06aa49c8ae30517104c7958995',
    WORK / 'source-inventory-20261107/yarn-instructions-macos.json': '3e0acd1a2f25811e380de5743e0913535470d931301cc9bc40f5a3c897d73e18',
    WORK / 'source-inventory-20261107/yarn-instructions-windows.json': '13d34e111e48fcd80105f419f1072717ddc11659300474410f52e7839b88522b',
    P / 'translation.json': 'b1e341f5338fc0c81e4af1e968a5b86acf3447330d726489cbc3ee89032b7311',
    P / 'receipts/author-audit-recipe.json': '84e2e698f372ff0102fbe59b76694b4d7a5a503e149be27da972b2734006e936',
}
def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
    return json.loads(p.read_text(encoding='utf-8'))
for p, expected in EXPECTED.items():
    if digest(p) != expected:
        raise ValueError(f'changed input: {p}')
source = read(INV)['entries']
valid = {entry['id'] for entry in source}
recipe = read(P / 'receipts/author-audit-recipe.json')
scenes = read(SCENES)['scenes']
ins_paths = {x: WORK / f'source-inventory-20261107/yarn-instructions-{x}.json' for x in ('macos', 'windows')}
platforms = {x: read(p) for x, p in ins_paths.items()}
changed = set(recipe['edits'])
assert len(changed) == 51
by_node = {}
for node, rows in scenes.items():
    matches = sorted(changed & {'yarn:' + row['id'] for row in rows})
    if matches:
        by_node[node] = matches
assert set(sum(by_node.values(), [])) == changed
special = {}
for path in sorted((P / 'special-scenes').glob('*.md')):
    ids = sorted(set(re.findall(r'yarn:line:[0-9a-f]{8}', path.read_text(encoding='utf-8'))) & valid)
    special[str(path)] = {'sha256': digest(path), 'ids': ids}
results = {}
for node, edits in sorted(by_node.items()):
    ids = {'yarn:' + row['id'] for row in scenes[node]} & valid
    platform_details = {}
    for platform, data in platforms.items():
        ins = data['nodes'][node]['instructions']
        visible = {('yarn:' + i['lineId']): i for i in ins if 'lineId' in i}
        for row in scenes[node]:
            actual = visible['yarn:' + row['id']]
            assert actual['index'] == row['instructionIndex'] and actual['kind'] == row['kind']
            assert actual.get('source') == row['source'][platform]
        groups, pending = [], []
        for inst in ins:
            if inst['opcodeField'] == 5:
                dest = next(o['unsigned'] for o in inst['operands'] if o['field'] == 2)
                if not 0 <= dest < len(ins):
                    raise ValueError(f'{platform} {node}: invalid destination {dest}')
                pending.append({'id': 'yarn:' + inst['lineId'], 'index': inst['index'],
                                'destination': dest, 'destinationInstruction': ins[dest],
                                'source': inst.get('source'), 'operands': inst['operands']})
            elif inst['opcodeField'] == 6:
                if not pending:
                    raise ValueError(f'{platform} {node}: empty option group')
                groups.append({'showOptionsIndex': inst['index'], 'options': pending})
                pending = []
        if pending:
            raise ValueError(f'{platform} {node}: unclosed options')
        jumps = [{'index': i['index'], 'opcodeField': i['opcodeField'], 'operands': i['operands']} for i in ins if i['opcodeField'] in (1, 2, 10, 16)]
        platform_details[platform] = {'nodeSha256': data['nodes'][node]['nodeSha256'], 'optionGroups': groups, 'jumps': jumps}
    related = {path: sorted(ids & set(v['ids'])) for path, v in special.items() if ids & set(v['ids'])}
    results[node] = {'changedIds': edits, 'sceneSourceIds': sorted(ids), 'specialSceneIntersections': related, 'platforms': platform_details}
out = {'schema': 1, 'meaning': 'Conservative affected-node source inventory and stock instruction topology; no gameplay or independent review implied.',
       'inputSha256': {str(p): digest(p) for p in list(EXPECTED)},
       'specialFiles': special, 'nodes': results}
output = WORK / 'cli-terra-high-20261110.J0KLrx/pt-BR/resume-11/affected-node-map.json'
with output.open('x', encoding='utf-8') as f:
    json.dump(out, f, ensure_ascii=False, indent=2); f.write('\n')
print('nodes',len(results),'changed',len(changed),'scene IDs',len(set().union(*(set(x['sceneSourceIds']) for x in results.values()))))
print('special intersections',sum(len(x['specialSceneIntersections']) for x in results.values()))
print('output',output,'sha256',digest(output))
