#!/usr/bin/env python3
"""Check bounded player-choice agreement candidates and extend the delta recipe."""
import hashlib, json, re, sys
from pathlib import Path
if len(sys.argv)!=3: raise SystemExit('usage: check-choice-referents.py NEW_EVIDENCE NEW_RECIPE')
evidence, output = map(Path,sys.argv[1:])
p=Path('localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json')
t=Path('localization/pt-BR/translation.json')
r=Path('localization/pt-BR/receipts/author-audit-reconciled-recipe.json')
for path,sha in [(p,'79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d'),(t,'b1e341f5338fc0c81e4af1e968a5b86acf3447330d726489cbc3ee89032b7311'),(r,'17f709c4b2f2f6312cb630ace3b6bfbd0f0720c60f5fa5c57ffcd870c90ba021')]:
 if hashlib.sha256(path.read_bytes()).hexdigest()!=sha: raise SystemExit(f'input changed: {path}')
pattern=r'\b(obrigado|animado|ansioso|preparado|pronto|pequeno|fofo|gostoso|lindo|certificado)\b'
decisions={
'yarn:line:b2fe309b':'The excited person addressed is Conrad, not the player.',
'yarn:line:f57fc630':'Pronto is an impersonal completion exclamation; source is All done.',
'yarn:line:4766af08':'Pronto is an impersonal completion exclamation; source says the work is complete.',
'yarn:line:c13d4e24':'Ele and gostoso refer to the male character, not the player.',
'yarn:line:9addfb4a':'Tudo pronto is an impersonal readiness statement.',
'yarn:line:31281c6d':'The masculine adjective modifies the red dragon, Conrad.',
'yarn:line:48d4a45a':'The masculine adjectives refer explicitly to Conrad.',
}
lines=json.loads(t.read_text())['lines']; entries=json.loads(p.read_text())['entries']; found=[]
for row in entries:
 key=row['id']
 if key not in lines or row.get('kind')!='option': continue
 value=lines[key]; candidate=value if isinstance(value,str) else json.dumps(value,ensure_ascii=False)
 if re.search(pattern,candidate,re.I):
  found.append({'id':key,'node':row.get('node'),'kind':row['kind'],'instructionIndex':row.get('instructionIndex'),'english':row['source'],'target':value,'adjudication':decisions.get(key)})
if {x['id'] for x in found} != decisions.keys() or len(found)!=len(decisions): raise SystemExit('selector set changed; re-adjudicate')
with evidence.open('x',encoding='utf-8') as f:
 json.dump({'schema':1,'pattern':pattern,'scope':'Visible Yarn option IDs in the pinned inventory; this literal selector does not cover implicit or morphological variants.','inventorySha256':'79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d','translationSha256':'b1e341f5338fc0c81e4af1e968a5b86acf3447330d726489cbc3ee89032b7311','rows':found},f,ensure_ascii=False,indent=2);f.write('\n')
recipe=json.loads(r.read_text())
for edited,extra in {
 'yarn:line:d66b9155':['yarn:line:b2fe309b'],
 'yarn:line:9addfb4a':['yarn:line:f57fc630','yarn:line:4766af08'],
 'yarn:line:c4cc497f':['yarn:line:c13d4e24'],
}.items():
 values=recipe['edits'][edited]['glossaryReferentSourceIds'];recipe['edits'][edited]['glossaryReferentSourceIds']=sorted(set(values)|set(extra))
with output.open('x',encoding='utf-8') as f:json.dump(recipe,f,ensure_ascii=False,indent=2);f.write('\n')
print('reviewed',len(found),'choice IDs; added three previously unselected context IDs')
