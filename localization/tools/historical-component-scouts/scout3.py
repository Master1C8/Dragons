from pathlib import Path
from collections import Counter,defaultdict
import json,sys
import UnityPy
from UnityPy.helpers import TypeTreeHelper
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
import inventory_text_assets as inventory
import inventory_yarn_bindings as bindings
import inventory_level_dialogues as levels
import settings_locale as settings

p=sys.argv[1]; root=Path(sys.argv[2]); all_rows=[]
pinned=inventory.inspect(root,p); gen=bindings.generator(root,p); cache={}; corrected={}
dec=Counter(); failed=Counter(); errors={}
def strings(tree, path=()):
    if isinstance(tree,str): yield path,tree
    elif isinstance(tree,(list,tuple)):
        for i,v in enumerate(tree): yield from strings(v,path+(i,))
    elif isinstance(tree,dict):
        for k,v in tree.items(): yield from strings(v,path+(k,))
for name in sorted(pinned['assets']):
    env=UnityPy.load(str(root/name)); env.path=str(root)
    for obj in env.objects:
        if obj.type.name!='MonoBehaviour': continue
        head=obj.parse_monobehaviour_head()
        script=head.m_Script.deref().read()
        if script.m_AssemblyName not in ('Assembly-CSharp','Assembly-CSharp.dll'): continue
        k=(script.m_Namespace,script.m_ClassName)
        try:
            h,s,schema=settings.nodes_for(obj,gen,cache)
            if k not in corrected:
                if k==('','LevelConfiguration'): schema=levels.corrected_schema(schema)
                rows=[{key:value for key,value in r.items() if key!='m_Children'} for r in schema.to_dict_list()]
                for i,r in enumerate(rows):
                    if r['m_Name']=='bones' and r['m_Type']=='string' and rows[i+3]['m_Type']=='string':
                        r['m_Type']='vector'
                corrected[k]=TypeTreeNode.from_list(rows)
            schema=corrected[k]
            if k[1] in ('DragonBarkFeaturePlapResponse','HitboxTrigger','IntermissionFinishedSubscriber'):
                boost=TypeTreeHelper.read_typetree_boost
                TypeTreeHelper.read_typetree_boost=None
                try: tree=obj.read_typetree(nodes=schema,check_read=True)
                finally: TypeTreeHelper.read_typetree_boost=boost
            else: tree=obj.read_typetree(nodes=schema,check_read=True)
            settings.check_header(tree,h,obj.path_id)
            raw=obj.get_raw_data()
            if obj.save_typetree(tree,nodes=schema)!=raw: raise ValueError('roundtrip')
            dec[k]+=1
            for path,text in strings(tree):
                if path==('m_Name',): continue
                all_rows.append((name,obj.path_id,k,path,text))
        except (ValueError,EOFError,AssertionError,KeyError,TypeError,AttributeError,RuntimeError) as e:
            failed[k]+=1
            errors.setdefault(k,(type(e).__name__,str(e)[:220]))
print('read',sum(dec.values()),len(dec),'failed',sum(failed.values()),len(failed),'strings',len(all_rows),'nonempty',sum(bool(r[-1]) for r in all_rows))
print('failures',[(k,n,errors[k]) for k,n in failed.most_common(30)])
print('fields',Counter((r[2],r[3][0]) for r in all_rows if r[-1]).most_common(38))
print('possible prose')
for name,id,k,path,text in all_rows:
    if len(text)>9 and ' ' in text and text.count(' ')>=2 and not ('\n' in text or len(text)>200):
        print(name,id,k,path,repr(text))
Path(sys.argv[3]).write_text(json.dumps(all_rows,ensure_ascii=False,indent=2))
