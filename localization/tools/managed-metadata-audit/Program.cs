using System.Security.Cryptography;
using System.Text.Json;
using Mono.Cecil;

if (args.Length != 2)
    throw new ArgumentException("Expected STOCK_DLL PACKAGED_DLL");

static string Sha(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
var sourceBytes = File.ReadAllBytes(args[0]);
var candidateBytes = File.ReadAllBytes(args[1]);
var sourceSha = Sha(sourceBytes);
var (platform, speaker) = sourceSha switch {
    "54953f9c071aa3ca5b52eb8b12b8e0bedc73f7665a506c61acbef0c58ac340ef" => ("macos", true),
    "3d5def40f51540e79dbb6a897993fe006022cf1f16933a1b47a69334085ad89d" => ("windows", true),
    "f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb" => ("macos", false),
    "8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2" => ("windows", false),
    _ => throw new InvalidOperationException("Unsupported managed source assembly"),
};
if (Sha(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) !=
    "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");

using var source = AssemblyDefinition.ReadAssembly(new MemoryStream(sourceBytes));
using var candidate = AssemblyDefinition.ReadAssembly(new MemoryStream(candidateBytes));
const string helper = "Yarn.Unity.VnSpeakerDisplay";
const string companion = "Dragons.SpeakerPresentation";
var assemblyRefs = candidate.MainModule.AssemblyReferences.ToList();
var originalTypes = candidate.MainModule.GetTypes().ToList();
if (speaker) {
    var extraRef = assemblyRefs.Single(r => r.Name == companion);
    if (extraRef.FullName != companion + ", Version=1.0.0.0, Culture=neutral, PublicKeyToken=null")
        throw new InvalidOperationException("Unexpected speaker companion identity");
    assemblyRefs.Remove(extraRef);
    var extraType = originalTypes.Single(t => t.FullName == helper);
    var methodNames = extraType.Methods.Select(m => m.Name).ToArray();
    if (extraType.IsNested || extraType.BaseType?.FullName != "System.Object" ||
        extraType.Attributes != (TypeAttributes.NotPublic | TypeAttributes.Abstract |
                                 TypeAttributes.Sealed | TypeAttributes.BeforeFieldInit) ||
        extraType.HasFields || extraType.HasProperties || extraType.HasEvents || extraType.HasNestedTypes ||
        extraType.HasGenericParameters || extraType.HasInterfaces || extraType.HasCustomAttributes || extraType.HasSecurityDeclarations ||
        (!methodNames.SequenceEqual(new[] { "GetDisplayName", "GetInlineText" }) &&
         !methodNames.SequenceEqual(new[] { "GetDisplayName", "GetInlineText", "GetAlexanderText", "GetBodyText" })))
        throw new InvalidOperationException("Unexpected speaker helper declaration");
    foreach (var method in extraType.Methods) {
        string resultType = method.Name == "GetDisplayName" ? "System.String" : "Yarn.Markup.MarkupParseResult";
        if (method.Attributes != (MethodAttributes.Assembly | MethodAttributes.Static | MethodAttributes.HideBySig) ||
            method.ReturnType.FullName != resultType || method.Parameters.Count != 1 ||
            method.Parameters[0].ParameterType.FullName != "Yarn.Unity.LocalizedLine" ||
            method.Parameters[0].Name != "line" || method.HasGenericParameters || method.HasCustomAttributes ||
            !method.HasBody)
            throw new InvalidOperationException("Unexpected speaker helper method declaration: " + method.Name);
    }
    originalTypes.Remove(extraType);
}
Check("assembly", AssemblyMetadata(source), AssemblyMetadata(candidate));
Check("module", ModuleMetadata(source.MainModule), ModuleMetadata(candidate.MainModule));
Check("assembly references", source.MainModule.AssemblyReferences.Select(AssemblyIdentity), assemblyRefs.Select(AssemblyIdentity));
var stockTypes = source.MainModule.GetTypes().ToArray();
Check("type inventory", stockTypes.Select(t => t.FullName), originalTypes.Select(t => t.FullName));
foreach (var (stock, output) in stockTypes.Zip(originalTypes))
    Check(stock.FullName, TypeMetadata(stock), TypeMetadata(output));
Console.WriteLine(JsonSerializer.Serialize(new {
    platform, assembly = source.MainModule.Name, sourceSha256 = sourceSha, packageSha256 = Sha(candidateBytes),
    types = stockTypes.Length, methods = stockTypes.Sum(t => t.Methods.Count),
    fields = stockTypes.Sum(t => t.Fields.Count), resources = source.MainModule.Resources.Count,
    speakerHelper = speaker, speakerCompanionReference = speaker,
}, new JsonSerializerOptions { WriteIndented = true }));

static void Check(string key, object source, object candidate) {
    if (JsonSerializer.Serialize(source) != JsonSerializer.Serialize(candidate))
        throw new InvalidOperationException("Managed declaration metadata differs: " + key);
}

static string TypeIdentity(TypeReference type) {
    if (type == null) return null;
    if (type is GenericInstanceType generic)
        return TypeIdentity(generic.ElementType) + "<" + string.Join(",", generic.GenericArguments.Select(TypeIdentity)) + ">";
    if (type is OptionalModifierType opt)
        return TypeIdentity(opt.ElementType) + " modopt(" + TypeIdentity(opt.ModifierType) + ")";
    if (type is RequiredModifierType req)
        return TypeIdentity(req.ElementType) + " modreq(" + TypeIdentity(req.ModifierType) + ")";
    if (type is FunctionPointerType function)
        return function.FullName + "|" + TypeIdentity(function.ReturnType) + "|" +
            string.Join(",", function.Parameters.Select(p => TypeIdentity(p.ParameterType)));
    if (type is TypeSpecification specification)
        return type.FullName + "|" + TypeIdentity(specification.ElementType);
    return type.FullName + "|" + (type.Scope is AssemblyNameReference assembly ? assembly.FullName : type.Scope?.Name);
}
static object MethodIdentity(MethodReference method) => method == null ? null : new {
    method.FullName, type = TypeIdentity(method.DeclaringType), returns = TypeIdentity(method.ReturnType),
    parameters = method.Parameters.Select(p => TypeIdentity(p.ParameterType)),
};
static object Attributes(ICustomAttributeProvider owner) => owner.CustomAttributes.Select(a => new {
    constructor = MethodIdentity(a.Constructor), bytes = a.GetBlob(),
});
static object Security(ISecurityDeclarationProvider owner) => owner.SecurityDeclarations.Select(s => new { s.Action, bytes = s.GetBlob() });
static object Generic(IGenericParameterProvider owner) => owner.GenericParameters.Select(p => new {
    p.Name, p.Position, p.Attributes, custom = Attributes(p),
    constraints = p.Constraints.Select(c => new { type = TypeIdentity(c.ConstraintType), custom = Attributes(c) }),
});
static object Marshal(IMarshalInfoProvider owner) => owner.MarshalInfo switch {
    null => null,
    ArrayMarshalInfo array => new { array.NativeType, array.ElementType, array.Size, array.SizeParameterIndex, array.SizeParameterMultiplier },
    FixedArrayMarshalInfo array => new { array.NativeType, array.ElementType, array.Size },
    FixedSysStringMarshalInfo str => new { str.NativeType, str.Size },
    SafeArrayMarshalInfo array => new { array.NativeType, array.ElementType },
    CustomMarshalInfo custom => new { custom.NativeType, custom.Guid, custom.UnmanagedType, managed = TypeIdentity(custom.ManagedType), custom.Cookie },
    MarshalInfo plain when plain.GetType() == typeof(MarshalInfo) => new { plain.NativeType },
    _ => throw new InvalidOperationException("Unknown managed marshal descriptor"),
};
static object AssemblyIdentity(AssemblyNameReference a) => new { a.FullName, a.Attributes, a.HashAlgorithm, a.Hash, a.PublicKey };
static object AssemblyMetadata(AssemblyDefinition a) => new {
    identity = AssemblyIdentity(a.Name), custom = Attributes(a), security = Security(a),
    modules = a.Modules.Select(m => m.Name),
};
static object ModuleMetadata(ModuleDefinition m) => new {
    m.Name, m.Mvid, m.Architecture, m.RuntimeVersion, m.Kind, m.Attributes, m.Characteristics,
    entry = MethodIdentity(m.EntryPoint), custom = Attributes(m), refs = m.ModuleReferences.Select(r => r.Name),
    exported = m.ExportedTypes.Select(t => new { t.FullName, t.Attributes, t.Identifier, scope = t.Scope?.ToString() }),
    resources = m.Resources.Select(r => r switch {
        EmbeddedResource data => (object)new { r.Name, r.Attributes, content = Sha(data.GetResourceData()) },
        LinkedResource file => new { r.Name, r.Attributes, file.File, file.Hash },
        AssemblyLinkedResource assembly => new { r.Name, r.Attributes, identity = AssemblyIdentity(assembly.Assembly) },
        _ => throw new InvalidOperationException("Unknown managed resource kind"),
    }),
};
static object TypeMetadata(TypeDefinition t) => new {
    t.FullName, t.Attributes, t.PackingSize, t.ClassSize, parent = TypeIdentity(t.BaseType),
    custom = Attributes(t), security = Security(t), generic = Generic(t),
    interfaces = t.Interfaces.Select(i => new { type = TypeIdentity(i.InterfaceType), custom = Attributes(i) }),
    fields = t.Fields.Select(f => new { f.Name, type = TypeIdentity(f.FieldType), f.Attributes, f.Offset,
        f.HasConstant, f.Constant, f.InitialValue, marshal = Marshal(f), custom = Attributes(f) }),
    methods = t.Methods.Select(m => new {
        signature = MethodIdentity(m), m.Attributes, m.ImplAttributes, m.CallingConvention, m.HasThis, m.ExplicitThis, m.SemanticsAttributes,
        custom = Attributes(m), security = Security(m), generic = Generic(m), overrides = m.Overrides.Select(MethodIdentity),
        parameters = m.Parameters.Select(p => new { p.Name, p.Attributes, p.HasConstant, p.Constant, marshal = Marshal(p), custom = Attributes(p) }),
        returns = new { m.MethodReturnType.Name, m.MethodReturnType.Attributes, m.MethodReturnType.HasConstant, m.MethodReturnType.Constant,
            marshal = Marshal(m.MethodReturnType), custom = Attributes(m.MethodReturnType) },
        pinvoke = m.PInvokeInfo == null ? null : new { m.PInvokeInfo.Attributes, m.PInvokeInfo.EntryPoint, m.PInvokeInfo.Module.Name },
    }),
    properties = t.Properties.Select(p => new { p.Name, p.Attributes, type = TypeIdentity(p.PropertyType), p.HasConstant, p.Constant,
        custom = Attributes(p), indices = p.Parameters.Select(index => TypeIdentity(index.ParameterType)),
        get = MethodIdentity(p.GetMethod), set = MethodIdentity(p.SetMethod), other = p.OtherMethods.Select(MethodIdentity) }),
    events = t.Events.Select(e => new { e.Name, e.Attributes, type = TypeIdentity(e.EventType), custom = Attributes(e),
        add = MethodIdentity(e.AddMethod), remove = MethodIdentity(e.RemoveMethod), raise = MethodIdentity(e.InvokeMethod),
        other = e.OtherMethods.Select(MethodIdentity) }),
};
