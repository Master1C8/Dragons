from collections import Counter
from pathlib import Path
import json,sys,UnityPy
from inventory_text_assets import inspect

def walk(value,path=()):
    if isinstance(value,dict):
        if set(value)=={'offset','size','path'} and value['path']:
            yield path,value['path'],value['offset'],value['size']
        elif set(value)=={'m_Source','m_Offset','m_Size'} and value['m_Source']:
            yield path,value['m_Source'],value['m_Offset'],value['m_Size']
        for k,v in value.items():
            if isinstance(v,(dict,list)): yield from walk(v,(*path,k))
    elif isinstance(value,list):
        for i,v in enumerate(value):
            if isinstance(v,(dict,list)): yield from walk(v,(*path,i))

platform,root=sys.argv[1],Path(sys.argv[2]); pinned=inspect(root,platform)
candidates={}; records=[]; errors=[]; classes=Counter(); media=Counter()
for name in sorted(pinned['assets']):
    env=UnityPy.load(str(root/name))
    for o in env.objects:
        key=o.type.name
        classes[key]+=1
        if key=='MonoBehaviour': continue
        if key not in candidates:
            try:
                schema=o._get_typetree_node()
                candidates[key]=sorted(set(n['m_Type'] for n in schema.to_dict_list()).intersection(('StreamingInfo','StreamedResource')))
            except Exception as err:
                candidates[key]=None
                errors.append([key,type(err).__name__,str(err)[:120]])
        if key in ('AudioClip','VideoClip'): media[key]+=1
        if not candidates[key]: continue
        try:
            tree=o.read_typetree(check_read=True)
            paths=list(walk(tree))
            if paths and o.save_typetree(tree)!=o.get_raw_data(): raise ValueError('round-trip')
        except Exception as err:
            errors.append([name,key,o.path_id,type(err).__name__,str(err)[:140]])
            continue
        for field,stream,off,size in paths:
            records.append({'asset':name,'id':o.path_id,'class':key,'field':field,'stream':stream,'offset':off,'size':size})
print(json.dumps({'types':classes,'candidates':candidates,'media':media,'errors':errors,'records':records},indent=2))
