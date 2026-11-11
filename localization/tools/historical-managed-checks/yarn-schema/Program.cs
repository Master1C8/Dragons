using Mono.Cecil;
var a=AssemblyDefinition.ReadAssembly(args[0]);
var ins=a.MainModule.Types.Single(x=>x.FullName=="Yarn.Instruction");
var types=ins.NestedTypes.Single(x=>x.Name=="Types");
foreach (var t in types.NestedTypes.Where(x => x.Name is "RunLineInstruction" or "AddOptionInstruction" or "RunCommandInstruction" or "JumpToInstruction" or "CallFunctionInstruction" or "PushStringInstruction" or "PushVariableInstruction" or "StoreVariableInstruction" or "RunNodeInstruction")) {
 Console.WriteLine("TYPE "+t.Name);
 foreach(var f in t.Fields.Where(x=>x.HasConstant)) Console.WriteLine(" FIELD "+f.Name+"="+f.Constant);
 foreach(var p in t.Properties.Where(x=>!x.Name.Contains("Descriptor") && x.Name!="Parser")) Console.WriteLine(" PROPERTY "+p.PropertyType.FullName+" "+p.Name);
}
