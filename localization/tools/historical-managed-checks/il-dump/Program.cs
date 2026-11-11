using Mono.Cecil;
var a=AssemblyDefinition.ReadAssembly(args[0]);
foreach(var t in a.MainModule.Types.Where(x=>x.FullName=="Yarn.Unity.OptionItem"))foreach(var m in t.Methods.Where(x=>x.Name=="set_Option" && x.HasBody)){Console.WriteLine(m.FullName);foreach(var i in m.Body.Instructions)Console.WriteLine(i);}
