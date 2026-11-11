using System.Text.Json;
using Mono.Cecil;
var folder = args[0];
var watched = new HashSet<string>(StringComparer.Ordinal) {
    "Assembly-CSharp.dll", "YarnSpinner.Unity.dll", "YarnSpinner.dll", "Naelstrof.UnityScriptableSettings.dll",
    "Unity.Localization.dll", "Unity.Addressables.dll", "Unity.TextMeshPro.dll", "UnityEngine.UI.dll"
};
using var resolver = new DefaultAssemblyResolver();
resolver.AddSearchDirectory(folder);
var rows = new List<object>();
var errors = new List<object>();
var calls = new List<object>();
foreach (string file in Directory.GetFiles(folder, "*.dll").OrderBy(Path.GetFileName, StringComparer.Ordinal)) {
    using var module = ModuleDefinition.ReadModule(file, new ReaderParameters { AssemblyResolver = resolver });
    var assembly = Path.GetFileName(file);
    bool inspect = watched.Contains(assembly);
    void Add(string owner, string kind, string attribute, string slot, string value) {
        if (!string.IsNullOrWhiteSpace(value))
            rows.Add(new { assembly, owner, kind, attribute, slot, value });
    }
    void AttributeText(string owner, string attribute, string slot, CustomAttributeArgument arg) {
        if (arg.Value is string value) Add(owner, "attribute", attribute, slot, value);
        if (arg.Value is CustomAttributeArgument nested) AttributeText(owner, attribute, slot + ".object", nested);
        if (arg.Value is CustomAttributeArgument[] array)
            for (int i = 0; i < array.Length; i++) AttributeText(owner, attribute, slot + "[" + i + "]", array[i]);
    }
    void Attributes(string owner, ICustomAttributeProvider provider) {
        int n = 0;
        foreach (var a in provider.CustomAttributes) {
            string type = a.AttributeType.FullName;
            string root = n++.ToString();
            try {
                for (int i = 0; i < a.ConstructorArguments.Count; i++) AttributeText(owner, type, root + ".arg" + i, a.ConstructorArguments[i]);
                foreach (var f in a.Fields) AttributeText(owner, type, root + ".field." + f.Name, f.Argument);
                foreach (var p in a.Properties) AttributeText(owner, type, root + ".property." + p.Name, p.Argument);
            } catch (AssemblyResolutionException ex) {
                errors.Add(new { assembly, owner, attribute = type, slot = root, unavailable = ex.AssemblyReference.FullName });
            }
        }
    }
    void Constant(string owner, IConstantProvider provider) {
        if (provider.HasConstant && provider.Constant is string text) Add(owner, "constant", null, null, text);
    }
    if (inspect) {
        Attributes("assembly", module.Assembly);
        Attributes("module", module);
    }
    foreach (var t in module.GetTypes()) {
        if (inspect) {
            Attributes(t.FullName, t);
            foreach (var f in t.Fields) { Constant(f.FullName, f); Attributes(f.FullName, f); }
            foreach (var p in t.Properties) { Constant(p.FullName, p); Attributes(p.FullName, p); }
            foreach (var e in t.Events) Attributes(e.FullName, e);
            foreach (var gp in t.GenericParameters) Attributes(t.FullName + "#generic:" + gp.Position, gp);
        }
        foreach (var m in t.Methods) {
            if (inspect) {
                Attributes(m.FullName, m);
                Attributes(m.FullName + "#return", m.MethodReturnType);
                foreach (var p in m.Parameters) {
                    var owner = m.FullName + "#param:" + p.Index;
                    Constant(owner, p); Attributes(owner, p);
                }
                foreach (var gp in m.GenericParameters) Attributes(m.FullName + "#generic:" + gp.Position, gp);
            }
            if (!m.HasBody) continue;
            foreach (var i in m.Body.Instructions) {
                if (i.Operand is not MethodReference target) continue;
                var dt = target.DeclaringType.FullName;
                if (target.Name is "GetCustomAttributes" or "GetCustomAttribute" or "get_CustomAttributes" or "GetCustomAttributesData" or
                    "GetRawConstantValue" or "GetRawDefaultValue" or "GetConstantValue" or "get_RawDefaultValue" or "get_DefaultValue" ||
                    (dt == "System.Enum" && target.Name is "GetName" or "GetNames"))
                    calls.Add(new { assembly, method = m.FullName, offset = i.Offset, target = target.FullName });
            }
        }
    }
}
Console.WriteLine(JsonSerializer.Serialize(new { rows, errors, calls }, new JsonSerializerOptions { WriteIndented = true }));
