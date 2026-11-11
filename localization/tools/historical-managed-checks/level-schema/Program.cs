using System;
using Mono.Cecil;
using System.Linq;
if(args.Length > 1 && args[1] == "speaker-directory") {
 int ok=0;
 System.Collections.Generic.IEnumerable<TypeDefinition> AllTypes(System.Collections.Generic.IEnumerable<TypeDefinition> ts) {
  foreach(var t in ts){yield return t;foreach(var c in AllTypes(t.NestedTypes))yield return c;}
 }
 foreach(var p in System.IO.Directory.GetFiles(args[0],"*.dll").OrderBy(x=>x)) {
  try {
   using var asm=ModuleDefinition.ReadModule(p);ok++;
   foreach(var t in AllTypes(asm.Types))foreach(var m in t.Methods.Where(m=>m.HasBody))foreach(var ins in m.Body.Instructions)
    if(ins.Operand is MethodReference mr && mr.FullName.Contains("Yarn.Unity.LocalizedLine::get_CharacterName()"))
     Console.WriteLine($"{System.IO.Path.GetFileName(p)} | {m.FullName} | {ins.Offset:x4} | {ins.OpCode}");
  } catch(Exception ex){Console.WriteLine($"UNREADABLE {System.IO.Path.GetFileName(p)} {ex.GetType().Name}");}
 }
 Console.WriteLine($"ASSEMBLIES_PARSED {ok}");return;
}
var module = ModuleDefinition.ReadModule(args[0]);
if(args.Length > 1 && args[1] == "string-comparisons") {
 foreach(var type in module.Types.SelectMany(t=>new[]{t}.Concat(t.NestedTypes)))foreach(var method in type.Methods.Where(m=>m.HasBody))foreach(var ins in method.Body.Instructions)
  if(ins.Operand is MethodReference mr && mr.DeclaringType.FullName=="System.String" && (mr.Name=="op_Equality" || mr.Name=="Equals")) Console.WriteLine($"{method.FullName} {mr.FullName} scope={mr.DeclaringType.Scope}");
 return;
}
if(args.Length > 1 && args[1] == "speaker-sinks") {
 foreach(var type in module.Types) foreach(var nested in type.NestedTypes) foreach(var method in nested.Methods.Where(m=>m.HasBody)) {
  var code=method.Body.Instructions;
  for(int i=0;i<code.Count;i++) if(code[i].Operand is MethodReference mr && mr.FullName.Contains("Yarn.Unity.LocalizedLine::get_CharacterName()")) {
   Console.WriteLine($"\n{method.FullName}");
   foreach(var ins in code.Skip(Math.Max(0,i-8)).Take(15))Console.WriteLine($"IL_{ins.Offset:x4} {ins.OpCode} {ins.Operand}");
  }
 }
 return;
}
if(args.Length > 1 && args[1] == "speaker-full") {
 foreach(var type in module.Types)foreach(var nested in type.NestedTypes)if(nested.FullName.Contains("LinePresenter/<RunLineAsync>"))foreach(var method in nested.Methods.Where(m=>m.Name=="MoveNext"))foreach(var ins in method.Body.Instructions)Console.WriteLine($"IL_{ins.Offset:x4} {ins.OpCode} {ins.Operand}");
 return;
}
if(args.Length > 1 && args[1] == "presenter-awake") {
 foreach(var type in module.Types.Where(t=>t.FullName=="Yarn.Unity.LinePresenter"))foreach(var method in type.Methods.Where(m=>m.Name=="Awake"))foreach(var ins in method.Body.Instructions)Console.WriteLine($"IL_{ins.Offset:x4} {ins.OpCode} {ins.Operand}");
 return;
}
if(args.Length > 1 && args[1] == "localized-line") {
 foreach(var type in module.Types.Where(t=>t.FullName=="Yarn.Unity.LocalizedLine")) {
  foreach(var f in type.Fields)Console.WriteLine($"FIELD {f.FieldType.FullName} {f.Name}");
  foreach(var method in type.Methods.Where(m=>m.Name is "get_CharacterName" or "get_Text" or "set_Text" or ".ctor")) {Console.WriteLine(method.FullName);if(method.HasBody)foreach(var ins in method.Body.Instructions)Console.WriteLine($"IL_{ins.Offset:x4} {ins.OpCode} {ins.Operand}");}
 }
 return;
}
if(args.Length > 1 && args[1] == "markup-api") {
 foreach(var type in module.Types.Where(t=>t.FullName.Contains("MarkupParser")||t.FullName.Contains("MarkupParseResult")||t.FullName.Contains("LineParser"))) {
  Console.WriteLine("TYPE "+type.FullName);foreach(var f in type.Fields)Console.WriteLine("FIELD "+f.FieldType.FullName+" "+f.Name);
  foreach(var m in type.Methods.Where(m=>m.IsPublic))Console.WriteLine("METHOD "+m.FullName);
 }
 return;
}
if (args.Length > 1 && args[1] == "speakers") {
 foreach(var type in module.Types.SelectMany(t => new[] { t }.Concat(t.NestedTypes))) foreach(var method in type.Methods.Where(m => m.HasBody)) {
  foreach(var ins in method.Body.Instructions) {
   var op=ins.Operand?.ToString() ?? "";
   if(op.Contains("CharacterName", StringComparison.OrdinalIgnoreCase)) Console.WriteLine($"{method.FullName} IL_{ins.Offset:x4} {ins.OpCode} {op}");
  }
 }
 return;
}
if (args.Length > 1 && args[1] == "settings") {
 foreach(var type in module.Types.Where(t => (t.Namespace == "UnityScriptableSettings" && (t.Name.StartsWith("Setting") || t.Name == "ScriptableSettingSpawner")) || t.Name == "ScriptableSettingString")) {
  Console.WriteLine($"TYPE {type.FullName} : {type.BaseType?.FullName}");
  foreach(var field in type.Fields) Console.WriteLine($"FIELD {field.FieldType.FullName} {field.Name}");
  foreach(var method in type.Methods.Where(m=>m.HasBody && (m.Name.Contains("Option") || m.Name.Contains("Value") || m.Name.Contains("Label") || m.Name.Contains("Localized") || m.Name.Contains("Resolution")))) {
   Console.WriteLine($"METHOD {method.FullName}");foreach(var ins in method.Body.Instructions)Console.WriteLine($"IL_{ins.Offset:x4} {ins.OpCode} {ins.Operand}");
  }
 }
 return;
}
System.Collections.Generic.IEnumerable<TypeDefinition> All(System.Collections.Generic.IEnumerable<TypeDefinition> types) {
    foreach(var t in types) { yield return t; foreach(var child in All(t.NestedTypes)) yield return child; }
}
foreach (var type in All(module.Types)) if (type.Name is "Objective" or "ObjectiveDisplay" or "ObjectiveManager" || type.BaseType?.FullName == "Objective") {
    Console.WriteLine($"\nTYPE {type.FullName} : {type.BaseType?.FullName}");
    foreach (var field in type.Fields) Console.WriteLine($" FIELD {field.FieldType.FullName} {field.Name} public={field.IsPublic} attrs={string.Join(",",field.CustomAttributes.Select(a=>a.AttributeType.Name))}");
    foreach (var method in type.Methods.Where(m=>m.Name is "GetName" or "SetObjective")) {
        Console.WriteLine($" METHOD {method.FullName}");
        if(method.HasBody) foreach(var ins in method.Body.Instructions) Console.WriteLine($" IL_{ins.Offset:x4} {ins.OpCode} {ins.Operand}");
    }
}
foreach (var type in All(module.Types)) if (type.Name is "MenuSlotsNew" or "MenuDeleteSave" or "MenuResponseTransition") {
  Console.WriteLine($"\nMENU TYPE {type.FullName}");
  foreach(var f in type.Fields) Console.WriteLine($"FIELD {f.FieldType.FullName} {f.Name}");
  foreach(var method in type.Methods.Where(m => m.Name is "OnEvent" or "OnShow" or ".ctor")) if(method.HasBody) {
    Console.WriteLine($"METHOD {method.FullName}");
    foreach(var ins in method.Body.Instructions) Console.WriteLine($"IL_{ins.Offset:x4} {ins.OpCode} {ins.Operand}");
  }
}
foreach (var type in All(module.Types)) foreach (var method in type.Methods) {
    if (!method.HasBody) continue;
    var code=method.Body.Instructions;
    for(int i=0;i<code.Count;i++) {
        var op=code[i];
        if(op.Operand is MethodReference gm && gm.Name=="GetReason") Console.WriteLine($"REASON CALL {method.FullName} IL_{op.Offset:x4} {gm.FullName}");
        if(op.Operand is FieldReference f && f.FullName=="System.String MenuResponseTransition::reason") Console.WriteLine($"TRANSITION REASON {method.FullName} IL_{op.Offset:x4} {op.OpCode}");
        if(op.OpCode.Code==Mono.Cecil.Cil.Code.Newobj && op.Operand is MethodReference ctor && ctor.DeclaringType.Name.StartsWith("Objective")) Console.WriteLine($"OBJECTIVE NEW {method.FullName} IL_{op.Offset:x4} {ctor.FullName}");
        if (op.Operand is not MethodReference m || (m.Name!="set_text" && m.Name!="SetText")) continue;
        Console.WriteLine($"\n{method.FullName} IL_{op.Offset:x4} -> {m.FullName}");
        foreach (var x in code.Skip(Math.Max(0,i-8)).Take(Math.Min(i,8))) Console.WriteLine($"  IL_{x.Offset:x4} {x.OpCode} {x.Operand}");
    }
}
