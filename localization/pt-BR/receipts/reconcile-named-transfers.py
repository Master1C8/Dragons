#!/usr/bin/env python3
"""Add statically named downstream Yarn transfer contexts to changed-node edits."""
import hashlib,json,sys
from pathlib import Path
if len(sys.argv)!=3:raise SystemExit('usage: reconcile-named-transfers.py NEW_EVIDENCE NEW_RECIPE')
inputs={
 'localization/work/cli-terra-high-20261110.J0KLrx/pt-BR/resume-11/affected-node-map.json':'fa05fdf1a278a9bd88e3c37d13fe974dff910e6a07bfdf252b365ed20873de42',
 'localization/work/source-inventory-20261107/yarn-instructions-macos.json':'3e0acd1a2f25811e380de5743e0913535470d931301cc9bc40f5a3c897d73e18',
 'localization/work/source-inventory-20261107/yarn-instructions-windows.json':'13d34e111e48fcd80105f419f1072717ddc11659300474410f52e7839b88522b',
 'localization/pt-BR/translation.json':'b1e341f5338fc0c81e4af1e968a5b86acf3447330d726489cbc3ee89032b7311',
 'localization/pt-BR/receipts/author-audit-loop-recipe.json':'e5364975b33ca75c6f02423c1feff58b46d4d3ca29641929a90af0140df47021'}
for p,h in inputs.items():
 if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h:raise SystemExit('hash mismatch '+p)
affected=json.loads(Path(next(iter(inputs))).read_text())['nodes'];targets=json.loads(Path('localization/pt-BR/translation.json').read_text())['lines'];recipe=json.loads(Path(list(inputs)[-1]).read_text()); results={}; added={}
for platform in ('macos','windows'):
 nodes=json.loads(Path('localization/work/source-inventory-20261107/yarn-instructions-'+platform+'.json').read_text())['nodes'];out={}
 for root,info in sorted(affected.items()):
  seen={root};todo=[root];edges=[];missing=[]
  while todo:
   node=todo.pop()
   for ins in nodes[node]['instructions']:
    if ins['opcodeField'] not in (16,18):continue
    dest=next((o['utf8'] for o in ins['operands'] if o.get('utf8')),None);edges.append({'node':node,'index':ins['index'],'opcode':ins['opcodeField'],'target':dest})
    if dest not in nodes:missing.append(dest);continue
    if dest not in seen:seen.add(dest);todo.append(dest)
  details={}
  for node in sorted(seen-{root}):
   lines=[{'id':'yarn:'+i['lineId'],'source':i['source'],'target':targets.get('yarn:'+i['lineId']),'inTargetScope':('yarn:'+i['lineId']) in targets} for i in nodes[node]['instructions'] if 'lineId' in i]
   details[node]={'nodeSha256':nodes[node]['nodeSha256'],'lines':lines}
   for edit in info['changedIds']:
    if edit in recipe['edits']:added.setdefault(edit,set()).update(x['id'] for x in lines if x['inTargetScope'])
  out[root]={'changedIds':info['changedIds'],'edges':edges,'missingTargets':missing,'downstream':details}
 results[platform]=out
for edit,ids in added.items():
 e=recipe['edits'][edit];e['runtimeSourceIds']=sorted(set(e['runtimeSourceIds'])|ids)
with Path(sys.argv[1]).open('x') as f:json.dump({'schema':1,'inputs':inputs,'limitation':'Static named RunNode/DetourToNode transitive closure only. Conditions, reachability, dynamic dispatch and managed-code consumers are not established.','platforms':results},f,ensure_ascii=False,indent=2);f.write('\n')
with Path(sys.argv[2]).open('x') as f:json.dump(recipe,f,ensure_ascii=False,indent=2);f.write('\n')
print('roots',len(affected),'edited roots',len(added),'missing named targets',sum(len(x['missingTargets']) for v in results.values() for x in v.values()))
