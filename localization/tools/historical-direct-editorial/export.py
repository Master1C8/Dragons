import hashlib
import json
from pathlib import Path

root = Path('localization/work')
out = Path(__file__).parent
lane = root/'cli-terra-high-20261110.J0KLrx'
for locale in ('it', 'pt-BR'):
    source = lane/locale/'worklist.json'
    target = Path(f'localization/{locale}/translation.json')
    w = json.loads(source.read_bytes())
    t = json.loads(target.read_bytes())
    assert set(t['lines']) == {r['id'] for r in w['rows']}
    assert len(w['rows']) == 1947
    print(locale, hashlib.sha256(source.read_bytes()).hexdigest(), hashlib.sha256(target.read_bytes()).hexdigest())
    rows = []
    for row in w['rows']:
        key = row['id']
        english = list(dict.fromkeys(b['source'] for b in row['builds'].values()))
        v = t['lines'][key]
        translated = [v] if isinstance(v, str) else [v['text']] if 'text' in v else list(dict.fromkeys(v['platforms'].values()))
        rows.append({'id':key,'group':row['group'],'english':english,'translated':translated})
    (out/f'{locale}-rows.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2)+'\n')
    pending = set()
    if locale == 'pt-BR':
        closure = json.loads(Path('localization/pt-BR/receipts/author-audit-callers-delta.json').read_bytes())
        receipt = root/'pt-BR-independent-alexander-20261110.iTEmV0/review.json'
        assert hashlib.sha256(receipt.read_bytes()).hexdigest()=='0749c09562e2672d9e88ad11c36db5fe2011991d4ca119acfa5ca8e26da83193'
        pending.update(json.loads(receipt.read_bytes())['unreadIds'])
        assert len(pending)==378 and pending<=set(closure['closureIds'])
        touched = json.loads(Path('localization/pt-BR/receipts/direct-file-adjudication.json').read_bytes())['changes']
        # Review corrected lines, all existing closure rows in their groups, and prior unread rows.
        groups = {r['group'] for r in rows if r['id'] in touched}
        pending.update(r['id'] for r in rows if r['group'] in groups)
        pending.update(touched)
        print('pt-BR review rows',len(pending))
    for subset,suffix in ((rows,''),([r for r in rows if r['id'] in pending],'-pending')):
        if not subset: continue
        with (out/f'{locale}{suffix}.txt').open('w') as f:
            group=None
            for i,r in enumerate(subset,1):
                if r['group']!=group:
                    group=r['group']
                    print(f'[{group}]',file=f)
                val=lambda s: ' // '.join(s).replace('\n','↵').replace('\t','⇥')
                print(f"{i} {val(r['english'])} → {val(r['translated'])}",file=f)
        (out/f'{locale}{suffix}-ids.json').write_text(json.dumps([r['id'] for r in subset])+'\n')
