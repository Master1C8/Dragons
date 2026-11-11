using System.Text.Json;
using Mono.Cecil;
var imports=new List<object>();
var gameRefs=new List<object>();
var nativeAttributes=new List<object>();
foreach (string path in Directory.GetFiles(args[0], "*.dll").OrderBy(Path.GetFileName,StringComparer.Ordinal)) {
    using var module=ModuleDefinition.ReadModule(path);
    var assembly=Path.GetFileName(path);
    foreach(var method in module.GetTypes().SelectMany(t=>t.Methods)) {
        if (method.HasPInvokeInfo) {
            var info=method.PInvokeInfo;
            imports.Add(new{assembly,method=method.FullName,library=info.Module.Name,entry=info.EntryPoint});
        }
        if (assembly=="Assembly-CSharp.dll" && method.IsInternalCall)
            nativeAttributes.Add(new{assembly,method=method.FullName,kind="internal-call"});
        if (!method.HasBody || assembly!="Assembly-CSharp.dll") continue;
        foreach(var i in method.Body.Instructions) {
            if (i.Operand is not MethodReference t) continue;
            var ty=t.DeclaringType.FullName;
            if (ty.StartsWith("Steamworks.",StringComparison.Ordinal) ||
                ty.StartsWith("UnityEngine.Windows.",StringComparison.Ordinal) ||
                ty=="UnityEngine.Application" && (t.Name is "OpenURL" or "get_systemLanguage" or "Quit") ||
                ty=="System.Runtime.InteropServices.NativeLibrary")
                gameRefs.Add(new{assembly,method=method.FullName,i.Offset,target=t.FullName});
        }
    }
}
Console.WriteLine(JsonSerializer.Serialize(new{imports,gameRefs,nativeAttributes},new JsonSerializerOptions{WriteIndented=true}));
