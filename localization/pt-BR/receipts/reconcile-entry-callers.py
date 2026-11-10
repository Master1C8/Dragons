#!/usr/bin/env python3
"""Reconcile direct static Yarn callers and serialized level references."""
import hashlib,json,sys
from pathlib import Path
if len(sys.argv)!=3: raise SystemExit('usage: reconcile-entry-callers.py NEW_EVIDENCE NEW_RECIPE')
inputs={
 'localization/work/cli-terra-high-20261110.J0KLrx/pt-BR/resume-11/affected-node-map.json':'fa05fdf1a278a9bd88e3c37d13fe974dff910e6a07bfdf252b365ed20873de42',
 'localization/work/source-inventory-20261107/yarn-instructions-macos.json':'3e0acd1a2f25811e380de5743e0913535470d931301cc9bc40f5a3c897d73e18',
 'localization/work/source-inventory-20261107/yarn-instructions-windows.json':'13d34e111e48fcd80105f419f1072717ddc11659300474410f52e7839b88522b',
 'localization/evidence/level-dialogues-macos-20261107.json':'4a16420f2b028201e605466c66c103b367c0cc60e8fd04c684df82a0beaaf3bd',
 'localization/evidence/level-dialogues-windows-20261107.json':'cb590fe02f13aa39e04b892d66f873850b6a798870d2dea0fff74c34ce70335b',
 'localization/pt-BR/translation.json':'b1e341f5338fc0c81e4af1e968a5b86acf3447330d726489cbc3ee89032b7311',
 'localization/pt-BR/receipts/author-audit-state-recipe.json':'09f438f75acd9511b78d4136d5400c60f52d0b23c6d13f759190fdcb4a4107e6'}
for p,h in inputs.items():
 if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h: raise SystemExit('hash mismatch '+p)
affected=json.loads(Path(next(iter(inputs))).read_text())['nodes'];target=json.loads(Path('localization/pt-BR/translation.json').read_text())['lines'];recipe=json.loads(Path(list(inputs)[-1]).read_text());result={}
for platform in ('macos','windows'):
 nodes=json.loads(Path('localization/work/source-inventory-20261107/yarn-instructions-'+platform+'.json').read_text())['nodes']; level=json.loads(Path('localization/evidence/level-dialogues-'+platform+'-20261107.json').read_text()); roots={n:{'changedIds':v['changedIds'],'levelReferences':[],'directYarnCallers':[]} for n,v in affected.items()}
 for c in level['configurations']:
  for ref in c['dialogueReferences']:
   if ref['target'] in roots: roots[ref['target']]['levelReferences'].append({'configuration':c['name'],'objectId':c['objectId'],'rawSha256':c['rawSha256'],**ref})
 for name,node in nodes.items():
  for i in node['instructions']:
   if i['opcodeField'] not in (16,18): continue
   for operand in i['operands']:
    dest=operand.get('utf8')
    if dest not in roots: continue
    lines=[{'id':'yarn:'+x['lineId'],'source':x['source'],'target':target.get('yarn:'+x['lineId'])} for x in node['instructions'] if 'lineId' in x]
    roots[dest]['directYarnCallers'].append({'node':name,'nodeSha256':node['nodeSha256'],'index':i['index'],'opcode':i['opcodeField'],'lines':lines})
    ids={x['id'] for x in lines if x['id'] in target}
    for edit in affected[dest]['changedIds']:
     if edit in recipe['edits']:
      e=recipe['edits'][edit];e['runtimeSourceIds']=sorted(set(e['runtimeSourceIds'])|ids)
 result[platform]=roots
for path,data in ((sys.argv[1],{'schema':1,'inputs':inputs,'limitation':'Direct static named Yarn callers and previously extracted serialized level references only. No indirect or code-driven caller, live dispatch, state, gameplay or repaired program execution is proved.','platforms':result}),(sys.argv[2],recipe)):
 with Path(path).open('x') as f: json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
print('roots',len(affected),'paired platforms',len(result))
