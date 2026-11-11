using Mono.Cecil;
using Mono.Cecil.Cil;
using var m=ModuleDefinition.ReadModule(args[0]);
foreach(var name in new[]{"TMPro.TextMeshPro", "TMPro.TextMeshProUGUI"})
{
 var body=m.GetType(name).Methods.Single(x=>x.Name=="GenerateTextMesh").Body;
 Console.WriteLine(name);
 foreach(var v in body.Variables) Console.WriteLine($"var {v.Index} {v.VariableType}");
 foreach(var x in body.Instructions) Console.WriteLine(x);
}
