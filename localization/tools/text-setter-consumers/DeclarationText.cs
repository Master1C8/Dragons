using Mono.Cecil;

static class DeclarationText {
    private static readonly HashSet<string> Assemblies = new(StringComparer.Ordinal) {
        "Assembly-CSharp.dll", "YarnSpinner.Unity.dll", "YarnSpinner.dll", "Naelstrof.UnityScriptableSettings.dll",
        "Unity.Localization.dll", "Unity.Addressables.dll", "Unity.TextMeshPro.dll", "UnityEngine.UI.dll",
        "Unity.InputSystem.dll", "com.alelievr.NodeGraphProcessor.Runtime.dll",
    };

    public static object Scan(string platform, string digest, (string name, byte[] bytes)[] files) {
        if (!Assemblies.IsSubsetOf(files.Select(f => f.name)))
            throw new InvalidOperationException("Missing declaration source assembly");
        using var resolver = new PinnedResolver(files);
        var strings = new List<object>();
        var calls = new List<object>();
        foreach (var file in files) {
            var module = resolver.Read(file.name).MainModule;
            bool inspect = Assemblies.Contains(file.name);
            void Add(string owner, string kind, string attribute, string slot, string value) {
                if (!string.IsNullOrWhiteSpace(value))
                    strings.Add(new { assembly = file.name, owner, kind, attribute, slot, value });
            }
            void Argument(string owner, string type, string slot, CustomAttributeArgument argument) {
                switch (argument.Value) {
                    case string value: Add(owner, "attribute", type, slot, value); break;
                    case CustomAttributeArgument boxed: Argument(owner, type, slot + ".object", boxed); break;
                    case CustomAttributeArgument[] array:
                        for (int i = 0; i < array.Length; i++) Argument(owner, type, slot + "[" + i + "]", array[i]);
                        break;
                }
            }
            void Attributes(string owner, ICustomAttributeProvider provider) {
                for (int n = 0; n < provider.CustomAttributes.Count; n++) {
                    var a = provider.CustomAttributes[n];
                    string type = a.AttributeType.FullName;
                    for (int i = 0; i < a.ConstructorArguments.Count; i++) Argument(owner, type, n + ".arg" + i, a.ConstructorArguments[i]);
                    foreach (var f in a.Fields) Argument(owner, type, n + ".field." + f.Name, f.Argument);
                    foreach (var p in a.Properties) Argument(owner, type, n + ".property." + p.Name, p.Argument);
                }
            }
            void Constant(string owner, IConstantProvider provider) {
                if (provider.HasConstant && provider.Constant is string value)
                    Add(owner, "constant", null, null, value);
            }
            void Generics(string owner, IGenericParameterProvider provider) {
                foreach (var g in provider.GenericParameters) {
                    string key = owner + "#generic:" + g.Position;
                    Attributes(key, g);
                    for (int i = 0; i < g.Constraints.Count; i++) Attributes(key + "#constraint:" + i, g.Constraints[i]);
                }
            }
            if (inspect) {
                Attributes("assembly", module.Assembly);
                Attributes("module", module);
            }
            foreach (var type in module.GetTypes()) {
                if (inspect) {
                    Attributes(type.FullName, type);
                    Generics(type.FullName, type);
                    for (int i = 0; i < type.Interfaces.Count; i++) Attributes(type.FullName + "#interface:" + i, type.Interfaces[i]);
                    foreach (var f in type.Fields) { Constant(f.FullName, f); Attributes(f.FullName, f); }
                    foreach (var p in type.Properties) { Constant(p.FullName, p); Attributes(p.FullName, p); }
                    foreach (var e in type.Events) Attributes(e.FullName, e);
                }
                foreach (var method in type.Methods) {
                    if (inspect) {
                        Attributes(method.FullName, method);
                        Generics(method.FullName, method);
                        Constant(method.FullName + "#return", method.MethodReturnType);
                        Attributes(method.FullName + "#return", method.MethodReturnType);
                        foreach (var p in method.Parameters) {
                            string owner = method.FullName + "#param:" + p.Index;
                            Constant(owner, p);
                            Attributes(owner, p);
                        }
                    }
                    if (!method.HasBody) continue;
                    foreach (var instruction in method.Body.Instructions)
                        if (instruction.Operand is MethodReference target && IsMetadataRead(target))
                            calls.Add(new { assembly = file.name, method = method.FullName, offset = instruction.Offset, target = target.FullName });
                }
            }
        }
        return new { schema = 1, platform, managedInventorySha256 = digest, assemblyCount = files.Length,
            declarationAssemblies = Assemblies.OrderBy(n => n, StringComparer.Ordinal), strings, metadataReads = calls,
            dependencyVersionBindings = resolver.VersionBindings };
    }

    private static bool IsMetadataRead(MethodReference method) {
        string type = method.DeclaringType.FullName;
        string name = method.Name;
        return ((type.StartsWith("System.Reflection.", StringComparison.Ordinal) || type is "System.Type" or "System.Attribute") &&
                name is "GetCustomAttributes" or "GetCustomAttribute" or "get_CustomAttributes" or "GetCustomAttributesData" or
                    "GetRawConstantValue" or "GetRawDefaultValue" or "GetConstantValue" or "get_RawDefaultValue" or "get_DefaultValue") ||
               (type == "System.Enum" && name is "GetName" or "GetNames") ||
               ((type is "UnityEngine.Localization.DisplayNameAttribute" or "Yarn.Unity.Attributes.LabelAttribute" or
                   "UnityEngine.TooltipAttribute" or "UnityEngine.HeaderAttribute") && name != ".ctor") ||
               (type, name) is ("UnityEngine.InputSystem.InputInteraction", "GetDisplayName") or
                   ("UnityEngine.InputSystem.InputActionRebindingExtensions", "GetBindingDisplayString") or
                   ("UnityEngine.InputSystem.InputBinding", "ToDisplayString") or
                   ("UnityEngine.InputSystem.InputControlPath", "ToHumanReadableString") or
                   ("UnityEngine.InputSystem.InputControl", "get_displayName" or "get_shortDisplayName") or
                   ("Yarn.Unity.Actions/CommandRegistration", "get_UsageString");
    }

    private sealed class PinnedResolver((string name, byte[] bytes)[] files) : IAssemblyResolver {
        private readonly Dictionary<string, byte[]> inputs = files.ToDictionary(f => f.name, f => f.bytes, StringComparer.Ordinal);
        private readonly Dictionary<string, AssemblyDefinition> resolved = new(StringComparer.Ordinal);
        private readonly SortedDictionary<string, string> versionBindings = new(StringComparer.Ordinal);
        public IReadOnlyDictionary<string, string> VersionBindings => versionBindings;

        public AssemblyDefinition Read(string name) {
            if (!resolved.TryGetValue(name, out var assembly)) {
                if (!inputs.TryGetValue(name, out var bytes)) throw new InvalidOperationException("Unpinned assembly dependency: " + name);
                assembly = AssemblyDefinition.ReadAssembly(new MemoryStream(bytes), new ReaderParameters { AssemblyResolver = this });
                resolved.Add(name, assembly);
            }
            return assembly;
        }
        public AssemblyDefinition Resolve(AssemblyNameReference reference) => Resolve(reference, null);
        public AssemblyDefinition Resolve(AssemblyNameReference reference, ReaderParameters parameters) {
            var assembly = Read(reference.Name + ".dll");
            if (assembly.Name.Name != reference.Name || assembly.Name.Culture != reference.Culture ||
                !assembly.Name.PublicKeyToken.SequenceEqual(reference.PublicKeyToken))
                throw new InvalidOperationException("Mismatched declaration dependency: " + reference.FullName);
            // Decode attributes using the shipped facade, even when its reference version differs.
            if (assembly.Name.Version != reference.Version)
                versionBindings[reference.FullName] = assembly.Name.FullName;
            return assembly;
        }
        public void Dispose() {
            foreach (var assembly in resolved.Values) assembly.Dispose();
        }
    }
}
