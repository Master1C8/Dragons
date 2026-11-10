#!/usr/bin/env python3
"""Bind static Conrad scene-loop consumers to the effective review recipe."""
import hashlib,json,sys
from pathlib import Path
if len(sys.argv)!=3:raise SystemExit('usage: reconcile-conrad-loop.py NEW_EVIDENCE NEW_RECIPE')
inputs={
 'localization/work/source-inventory-20261107/yarn-instructions-macos.json':'3e0acd1a2f25811e380de5743e0913535470d931301cc9bc40f5a3c897d73e18',
 'localization/work/source-inventory-20261107/yarn-instructions-windows.json':'13d34e111e48fcd80105f419f1072717ddc11659300474410f52e7839b88522b',
 'localization/pt-BR/translation.json':'b1e341f5338fc0c81e4af1e968a5b86acf3447330d726489cbc3ee89032b7311',
 'localization/pt-BR/receipts/author-audit-referent-recipe.json':'9e1ba9b0b54d73b83be4e36c215283b3679819ad56f10d652ed21cceac5328a9'}
for p,h in inputs.items():
 if hashlib.sha256(Path(p).read_bytes()).hexdigest()!=h:raise SystemExit('input hash mismatch: '+p)
targets=json.loads(Path('localization/pt-BR/translation.json').read_text())['lines'];platforms={}; ids=None
for p in ('macos','windows'):
 nodes=json.loads(Path('localization/work/source-inventory-20261107/yarn-instructions-'+p+'.json').read_text())['nodes'];subset={}
 for node in ('Conrad_SexScene_Cum','Conrad_SexScene_Loop'):
  rows=nodes[node]['instructions']; lines=[{'id':'yarn:'+r['lineId'],'source':r['source'],'target':targets['yarn:'+r['lineId']]} for r in rows if 'lineId' in r]; transfers=[{'index':r['index'],'operands':r['operands']} for r in rows if r['opcodeField'] in (16,18)]
  subset[node]={'nodeSha256':nodes[node]['nodeSha256'],'lines':lines,'transfers':transfers}
 loopids={r['id'] for r in subset['Conrad_SexScene_Loop']['lines']}
 if ids is None:ids=loopids
 if ids!=loopids or len(ids)!=4:raise ValueError('unexpected platform loop IDs')
 if not any(t['index']==50 and any(o.get('utf8')=='Conrad_SexScene_Loop' for o in t['operands']) for t in subset['Conrad_SexScene_Cum']['transfers']):raise ValueError('missing outbound transfer')
 if not any(any(o.get('utf8')=='Conrad_SexScene_Cum' for o in t['operands']) for t in subset['Conrad_SexScene_Loop']['transfers']):raise ValueError('missing return transfer')
 platforms[p]=subset
with Path(sys.argv[1]).open('x') as f:json.dump({'schema':1,'inputs':inputs,'limitation':'Static named transfers only, not actual gameplay or proof of dynamic and code-side consumers.','platforms':platforms},f,ensure_ascii=False,indent=2);f.write('\n')
r=json.loads(Path('localization/pt-BR/receipts/author-audit-referent-recipe.json').read_text());e=r['edits']['yarn:line:9addfb4a'];e['runtimeSourceIds']=sorted(set(e['runtimeSourceIds'])|ids)
with Path(sys.argv[2]).open('x') as f:json.dump(r,f,ensure_ascii=False,indent=2);f.write('\n')
print('bound loop IDs:',', '.join(sorted(ids)))
