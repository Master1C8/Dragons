#!/usr/bin/env python3
"""Enumerate explicit Yarn variable references touched by changed nodes."""
import hashlib,json,sys
from pathlib import Path
if len(sys.argv)!=3: raise SystemExit('usage: reconcile-state-consumers.py NEW_EVIDENCE NEW_RECIPE')
inputs={
 'localization/work/cli-terra-high-20261110.J0KLrx/pt-BR/resume-11/affected-node-map.json':'fa05fdf1a278a9bd88e3c37d13fe974dff910e6a07bfdf252b365ed20873de42',
 'localization/work/source-inventory-20261107/yarn-instructions-macos.json':'3e0acd1a2f25811e380de5743e0913535470d931301cc9bc40f5a3c897d73e18',
 'localization/work/source-inventory-20261107/yarn-instructions-windows.json':'13d34e111e48fcd80105f419f1072717ddc11659300474410f52e7839b88522b',
 'localization/pt-BR/translation.json':'b1e341f5338fc0c81e4af1e968a5b86acf3447330d726489cbc3ee89032b7311',
 'localization/pt-BR/receipts/author-audit-transfer-recipe.json':'baefe3fdaa84cb325cbd4d12ceb143f723372f3b307a0cc8f587961a01a15499'}
for p,h in inputs.items():
 if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h: raise SystemExit('hash mismatch '+p)
affected=json.loads(Path(next(iter(inputs))).read_text())['nodes']; target=json.loads(Path('localization/pt-BR/translation.json').read_text())['lines']; recipe=json.loads(Path(list(inputs)[-1]).read_text()); result={}; generic={'$dragonHead','$dragonModel'}
for platform in ('macos','windows'):
 nodes=json.loads(Path('localization/work/source-inventory-20261107/yarn-instructions-'+platform+'.json').read_text())['nodes']
 refs={}; rootvars={}
 for name,node in nodes.items():
  for i in node['instructions']:
   if i['opcodeField'] not in (13,14): continue
   values=[o['utf8'] for o in i['operands'] if o.get('utf8')]
   if len(values)!=1: raise SystemExit('unexpected variable operand '+name)
   v=values[0]; refs.setdefault(v,[]).append({'node':name,'index':i['index'],'operation':'read' if i['opcodeField']==13 else 'write'})
   if name in affected: rootvars.setdefault(name,set()).add(v)
 evidence={}
 for var in sorted(set().union(*rootvars.values())):
  entries=refs[var]; names=sorted({r['node'] for r in entries}); contexts={}
  for name in names:
   lines=[{'id':'yarn:'+i['lineId'],'source':i['source'],'target':target.get('yarn:'+i['lineId'])} for i in nodes[name]['instructions'] if 'lineId' in i]
   contexts[name]={'nodeSha256':nodes[name]['nodeSha256'],'lines':lines}
  evidence[var]={'genericObjectBinding':var in generic,'references':entries,'contexts':contexts}
  if var not in generic:
   ids={x['id'] for node in contexts.values() for x in node['lines'] if x['id'] in target}
   for root,variables in rootvars.items():
    if var in variables:
     for edit in affected[root]['changedIds']:
      if edit in recipe['edits']:
       e=recipe['edits'][edit];e['runtimeSourceIds']=sorted(set(e['runtimeSourceIds'])|ids)
 result[platform]=evidence
for path,data in ((sys.argv[1],{'schema':1,'inputs':inputs,'limitation':'Explicit opcodes 13 and 14 only; whole referencing nodes are conservative context. Generic object bindings are inventoried, not expanded into editorial closure. Code-side accesses, reachability, actual values and side effects are not established.','platforms':result}),(sys.argv[2],recipe)):
 with Path(path).open('x') as f:json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')
print('variables',len(result['macos']),'generic bindings',sorted(generic))
