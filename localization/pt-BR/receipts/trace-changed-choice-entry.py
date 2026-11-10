#!/usr/bin/env python3
"""Trace the initial static destination path, stopping at unproved control flow."""
import hashlib,json,sys
from pathlib import Path
if len(sys.argv)!=2: raise SystemExit('usage: trace-changed-choice-entry.py NEW_OUTPUT')
inputs={
 'localization/work/cli-terra-high-20261110.J0KLrx/pt-BR/resume-11/affected-node-map.json':'fa05fdf1a278a9bd88e3c37d13fe974dff910e6a07bfdf252b365ed20873de42',
 'localization/work/source-inventory-20261107/yarn-instructions-macos.json':'3e0acd1a2f25811e380de5743e0913535470d931301cc9bc40f5a3c897d73e18',
 'localization/work/source-inventory-20261107/yarn-instructions-windows.json':'13d34e111e48fcd80105f419f1072717ddc11659300474410f52e7839b88522b',
 'localization/pt-BR/translation.json':'b1e341f5338fc0c81e4af1e968a5b86acf3447330d726489cbc3ee89032b7311',
 'localization/pt-BR/receipts/author-audit-referent-delta.json':'e6a02080b993b8f69c03c6098fe26f8bc332451b90619367b535f4cec876ce28'}
for p,h in inputs.items():
 if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h: raise SystemExit('input hash mismatch: '+p)
mapfile=json.loads(Path(next(iter(inputs))).read_text());delta=json.loads(Path(list(inputs)[-1]).read_text());changed=set(delta['changedIds']);targets=json.loads(Path('localization/pt-BR/translation.json').read_text())['lines']
programs={k:json.loads(Path('localization/work/source-inventory-20261107/yarn-instructions-'+k+'.json').read_text())['nodes'] for k in ('macos','windows')}
result=[]
for node,record in sorted(mapfile['nodes'].items()):
 for group in record['platforms']['macos']['optionGroups']:
  for opt in group['options']:
   if opt['id'] not in changed: continue
   row={'id':opt['id'],'node':node,'platforms':{}}
   for platform in programs:
    match=[o for g in record['platforms'][platform]['optionGroups'] for o in g['options'] if o['id']==opt['id']]
    if len(match)!=1: raise ValueError('ambiguous option')
    dest=match[0]['destination'];code=programs[platform][node]['instructions'];i=dest;seen=set();steps=[]
    while 0<=i<len(code) and i not in seen:
     seen.add(i); ins=code[i];op=ins['opcodeField'];steps.append({'index':i,'opcode':op})
     if op==3:
      key='yarn:'+ins['lineId'];end={'kind':'line','id':key,'source':ins['source'],'target':targets.get(key)};break
     if op==1:
      a=[o['unsigned'] for o in ins['operands'] if o['field']==1 and 'unsigned' in o];i=a[0] if a else 0;continue
     if op in (2,5,6,10,15,16,18,20):
      end={'kind':'control-boundary','opcode':op,'index':i,'operands':ins['operands']};break
     i+=1
    else: end={'kind':'loop-or-out-of-range','index':i}
    row['platforms'][platform]={'destination':dest,'steps':steps,'firstBoundary':end}
   result.append(row)
if len(result)!=27:raise ValueError('unexpected changed option count')
with Path(sys.argv[1]).open('x') as f:json.dump({'schema':1,'inputs':inputs,'limitations':'Static initial path only; conditions, selected-state feasibility, later consumers and actual gameplay are not proven. Stops at branch, dispatch, transfer or termination.','rows':result},f,ensure_ascii=False,indent=2);f.write('\n')
print('Traced',len(result),'changed choice entry paths on each platform')
