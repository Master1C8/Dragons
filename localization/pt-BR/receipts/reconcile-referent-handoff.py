#!/usr/bin/env python3
"""Reproduce the bounded author referent and repetition inventory; no runtime claim."""
import hashlib, json, pathlib, sys
P = pathlib.Path('.')
def read(path, expected):
    b = (P/path).read_bytes()
    assert hashlib.sha256(b).hexdigest() == expected, path
    return json.loads(b)
delta = read('localization/pt-BR/receipts/author-audit-callers-delta.json', '60baffadaf7c620ebdb7c286e81aca1a00d9184bd001c3ccdda11bc18d27d786')
node_map = read('localization/work/cli-terra-high-20261110.J0KLrx/pt-BR/resume-11/affected-node-map.json', 'fa05fdf1a278a9bd88e3c37d13fe974dff910e6a07bfdf252b365ed20873de42')
traces = read('localization/pt-BR/receipts/changed-choice-entry-traces.json', '960e2b95e061d4a03539bf4bd4506bba99af9ab6f1324c3612f36d1d5360da9f')
rows = {r['id']: r for r in delta['reviewRows']}
changed = set(delta['changedIds']); assert len(changed)==51
# These source-based editorial classes are deliberately limited to the 51 edits.
classes = {
 'player-address-or-self-reference': '938be2fb 33440e8c 7d13eca0 61c8781b 37c9d915 44701902 cb847372 e7e57d9c d132db41 1538bc7e d66b9155 34cf0601 a0479425 918d7820 fa293cde cf8c5f37 18e5a573 c4cc497f 0bc044da 9addfb4a 7f543c2a f0a0565a 73ea230a 0de4fe62 a00f681d c6202cf2 7f2e2736 e91e2041 601e1b38 822c0718 7f5113d5 07e5fc05 a6c1f2f4 e6290003 b4990e3d 09e5bf43 cd9b2a8f 0d20d327 f83e4966 77ca2316 13c906c7 b05c6259 079b3782 a40e531c',
 'player-and-romantic-partner': '3d723db0',
 'player-and-ryan': '4789095b 5e4d645c',
 'player-addresses-dragon': '41d5085a 94fbdbf0',
 'conrad-wash-or-social-question': '88d7e1e2 a0cf6cae',
}
lookup={}
for label, suffixes in classes.items():
    for suffix in suffixes.split():
        key='yarn:line:'+suffix
        assert key not in lookup; lookup[key]=label
assert set(lookup)==changed, (sorted(changed-set(lookup)), sorted(set(lookup)-changed))
output={'schema':1,'scope':'Author reconciliation for the 51 edits; not independent review or executed runtime.', 'boundDeltaSha256':'60baffadaf7c620ebdb7c286e81aca1a00d9184bd001c3ccdda11bc18d27d786','boundNodeMapSha256':'fa05fdf1a278a9bd88e3c37d13fe974dff910e6a07bfdf252b365ed20873de42','boundChoiceTraceSha256':'960e2b95e061d4a03539bf4bd4506bba99af9ab6f1324c3612f36d1d5360da9f','glossaryBinding':'6309cf331625336c510e6587ce3b35476301f242bfd63618ad01bfbd8b3966ad','changedRows':[], 'exactSourceRepetitions':[], 'specialSceneIntersections':{}}
for ident in delta['changedIds']:
 r=rows[ident]; n=node_map['nodes'][r['group']]
 opts={}
 for plat,data in n['platforms'].items():
  opts[plat]=[{'showOptionsIndex':g['showOptionsIndex'], **o} for g in data['optionGroups'] for o in g['options'] if o['id']==ident]
 assert (r['kind']!='option') or all(len(v)==1 for v in opts.values()),ident
 output['changedRows'].append({'id':ident,'node':r['group'],'kind':r['kind'],'referentClass':lookup[ident], 'pairedSource':{k:v['source'] for k,v in r['builds'].items()},'before':r['before'],'after':r['after'],'options':opts})
for ident in delta['components']['repetitions']:
 r=rows[ident]; output['exactSourceRepetitions'].append({'id':ident,'node':r['group'],'kind':r['kind'],'pairedSource':{k:v['source'] for k,v in r['builds'].items()},'target':r['after']})
for node,record in node_map['nodes'].items():
 if record['specialSceneIntersections']: output['specialSceneIntersections'][node]=record['specialSceneIntersections']
output['boundaries']=['Scene classification identifies editorial referents, not proof of live execution.','Exact source repetition is not a request to impose identical agreement across distinct speakers.','The referenced trace stops at a first line or control boundary; follow conditional and transfer evidence in handoff.','Protected contexts are in the bound delta; original Windows missing-destination repair is a separate technical boundary.']
p=pathlib.Path(sys.argv[1]); assert not p.exists(); p.write_text(json.dumps(output,ensure_ascii=False,indent=2)+'\n',encoding='utf8'); print(hashlib.sha256(p.read_bytes()).hexdigest(),len(output['changedRows']),len(output['exactSourceRepetitions']))
