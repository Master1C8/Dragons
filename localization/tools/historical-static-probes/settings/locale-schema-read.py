from pathlib import Path
import json,sys,UnityPy
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
import inventory_game_components as components
import inventory_yarn_bindings as bindings
import settings_locale as settings
r=Path(sys.argv[1]); p=sys.argv[2]
gen=bindings.generator(r,p)
groups={
'Settings': ('CommandLineLocaleSelector','SystemLocaleSelector','SpecificLocaleSelector','LocalesProvider','LocalizedAssetDatabase','LocalizedStringDatabase'),
'SmartFormat': ('SmartFormatter',),
'SmartFormat.Core.Settings':('SmartSettings',),
'SmartFormat.Core.Parsing':('Parser',),
'SmartFormat.Extensions': ('ListFormatter','PersistentVariablesSource','DictionarySource','ValueTupleSource','XmlSource','ReflectionSource','DefaultSource','PluralLocalizationFormatter','ConditionalFormatter','TimeFormatter','XElementFormatter','ChooseFormatter','SubStringFormatter','IsMatchFormatter','DefaultFormatter'),
}
managed={}
for suffix,names in groups.items():
 for name in names:
  ns='UnityEngine.Localization.'+suffix
  rows=components.flat_nodes(gen.get_nodes_up('Unity.Localization',ns+'.'+name))
  top=[i for i,row in enumerate(rows) if row['m_Level']==1]
  assert tuple(rows[i]['m_Name'] for i in top[:4])==components.HEADER, (name,[(i,rows[i]['m_Name']) for i in top])
  managed[name,ns,'Unity.Localization']=TypeTreeNode.from_list([rows[0],*(rows[top[4]:] if len(top)>4 else [])])
env=UnityPy.load(str(r/'globalgamemanagers.assets')); env.path=str(r)
o=next(x for x in env.objects if x.path_id==2285)
h,script,schema=settings.nodes_for(o,gen,{})
from types import SimpleNamespace
from UnityPy.helpers import TypeTreeHelper
from UnityPy.streams import EndianBinaryReader
ctx=SimpleNamespace(ref_types=[SimpleNamespace(m_ClassName=k[0],m_NameSpace=k[1],m_AssemblyName=k[2],node=n) for k,n in managed.items()])
reader=EndianBinaryReader(o.get_raw_data(),endian=o.reader.endian)
tree=TypeTreeHelper.read_value(schema,reader,TypeTreeHelper.TypeTreeConfig(True,ctx))
print(reader.Position,len(o.get_raw_data()),o.get_raw_data()[reader.Position:].hex(),file=sys.stderr)
print(json.dumps(tree,indent=2))
