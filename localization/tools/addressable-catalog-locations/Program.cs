using System.Collections;
using System.Reflection;
using System.Runtime.Loader;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;
using TypeAttributes = Mono.Cecil.TypeAttributes;
using MethodAttributes = Mono.Cecil.MethodAttributes;

if (args.Length != 2 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: addressable-catalog-locations macos|windows ORIGINAL_DATA");
string Hash(byte[] b) => Convert.ToHexString(SHA256.HashData(b)).ToLowerInvariant();
var manifestHashes = new Dictionary<string,string> {
    ["macos"] = "b3186bc39207255e937f5856be09906dc1a428d83a964d5f368f30861e32603c",
    ["windows"] = "9a14fcb1198ca8308ad90a38a1988367074c1f2ec8b6f0a8d97ef3d3c074fc56"
};
var catalogHashes = new Dictionary<string,string> {
    ["macos"] = "3d7c6f7c9e89b3604293cdead97988638c85edece345682c69b61cf7b283994c",
    ["windows"] = "3c384566fa98c6c20ba6d790424c97734532fb0be4403822f3a0b629d8b839fa"
};
if (Hash(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
string data = Path.GetFullPath(args[1]);
string managed = Path.Combine(data, "Managed");
var dlls = Directory.GetFiles(managed).Where(p => p.EndsWith(".dll", StringComparison.Ordinal))
    .OrderBy(Path.GetFileName, StringComparer.Ordinal).Select(p => (path:p, name:Path.GetFileName(p), bytes:File.ReadAllBytes(p))).ToArray();
if (dlls.Any(f => f.name.Any(c => c > 127))) throw new InvalidOperationException("Non-ASCII managed filename");
string manifest = string.Concat(dlls.Select(f => $"{f.name}|{Hash(f.bytes)}\n"));
if (Hash(Encoding.UTF8.GetBytes(manifest)) != manifestHashes[args[0]]) throw new InvalidOperationException("Unsupported managed inventory");
string catalog = Path.Combine(data, "StreamingAssets", "aa", "catalog.bin");
if (Hash(File.ReadAllBytes(catalog)) != catalogHashes[args[0]]) throw new InvalidOperationException("Unsupported catalog");
var manager = dlls.Single(f => f.name == "Unity.ResourceManager.dll");
using var module = ModuleDefinition.ReadModule(new MemoryStream(manager.bytes));
var owner = module.Types.Single(t => t.FullName == "UnityEngine.ResourceManagement.Util.BinaryStorageBuffer");
if (owner.Methods.Any(m => m.Name == "DiagnosticCopy")) throw new InvalidOperationException("Unexpected diagnostic method");
var pointer = new PointerType(module.TypeSystem.Void);
var helper = new MethodDefinition("DiagnosticCopy", MethodAttributes.Assembly | MethodAttributes.Static, module.TypeSystem.Void);
helper.Parameters.Add(new ParameterDefinition(pointer)); helper.Parameters.Add(new ParameterDefinition(pointer));
helper.Parameters.Add(new ParameterDefinition(module.TypeSystem.Int64)); owner.Methods.Add(helper);
var il = helper.Body.GetILProcessor();
il.Append(il.Create(OpCodes.Ldarg_1)); il.Append(il.Create(OpCodes.Ldarg_0));
il.Append(il.Create(OpCodes.Ldarg_2)); il.Append(il.Create(OpCodes.Ldarg_2));
unsafe {
    var copy = typeof(Buffer).GetMethod("MemoryCopy", new[] {typeof(void*), typeof(void*), typeof(long), typeof(long)});
    il.Append(il.Create(OpCodes.Call, module.ImportReference(copy)));
}
il.Append(il.Create(OpCodes.Ret));
var logger = new MethodDefinition("DiagnosticLog", MethodAttributes.Assembly | MethodAttributes.Static, module.TypeSystem.Void);
logger.Parameters.Add(new ParameterDefinition(module.ImportReference(typeof(Exception)))); owner.Methods.Add(logger);
var logil = logger.Body.GetILProcessor();
logil.Append(logil.Create(OpCodes.Call, module.ImportReference(typeof(Console).GetProperty("Error").GetMethod)));
logil.Append(logil.Create(OpCodes.Ldstr, "VN_DIAGNOSTIC_EXCEPTION"));
logil.Append(logil.Create(OpCodes.Callvirt, module.ImportReference(typeof(TextWriter).GetMethod("WriteLine", new[] { typeof(string) }))));
logil.Append(logil.Create(OpCodes.Call, module.ImportReference(typeof(Console).GetProperty("Error").GetMethod)));
logil.Append(logil.Create(OpCodes.Ldarg_0));
logil.Append(logil.Create(OpCodes.Callvirt, module.ImportReference(typeof(TextWriter).GetMethod("WriteLine", new[] { typeof(object) }))));
logil.Append(logil.Create(OpCodes.Ret));
IEnumerable<TypeDefinition> All(IEnumerable<TypeDefinition> types) {
    foreach (var t in types) { yield return t; foreach (var n in All(t.NestedTypes)) yield return n; }
}
int replacements = 0;
foreach (var t in All(module.Types)) foreach (var method in t.Methods.Where(m => m.HasBody)) foreach (var ins in method.Body.Instructions)
    if (ins.OpCode.Code == Code.Call && ins.Operand is MethodReference called &&
        called.FullName == "System.Void Unity.Collections.LowLevel.Unsafe.UnsafeUtility::MemCpy(System.Void*,System.Void*,System.Int64)") {
        ins.Operand = helper; replacements++;
    }
if (replacements != 13) throw new InvalidOperationException("Unexpected memory-copy call count");
int logs = 0;
foreach (var t in All(module.Types)) foreach (var method in t.Methods.Where(m => m.HasBody)) foreach (var ins in method.Body.Instructions)
    if (ins.OpCode.Code == Code.Call && ins.Operand is MethodReference called &&
        called.FullName == "System.Void UnityEngine.Debug::LogException(System.Exception)") { ins.Operand = logger; logs++; }
if (logs != 10) throw new InvalidOperationException("Unexpected exception logger call count");
using var bytes = new MemoryStream(); module.Write(bytes); bytes.Position = 0;
var patchedManager = AssemblyLoadContext.Default.LoadFromStream(bytes);
AssemblyLoadContext.Default.Resolving += (ctx, name) => {
    if (name.Name == "Unity.ResourceManager") return patchedManager;
    var file = dlls.SingleOrDefault(x => x.name == name.Name + ".dll");
    return file.bytes == null ? null : ctx.LoadFromStream(new MemoryStream(file.bytes));
};
var addressables = dlls.Single(f => f.name == "Unity.Addressables.dll");
var assembly = AssemblyLoadContext.Default.LoadFromStream(new MemoryStream(addressables.bytes));
var type = assembly.GetType("UnityEngine.AddressableAssets.ResourceLocators.ContentCatalogData", true);
const BindingFlags flags = BindingFlags.Static | BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
var content = type.GetMethod("LoadFromFile", flags).Invoke(null, new object[] {catalog, false});
var locator = type.GetMethod("CreateCustomLocator", flags).Invoke(content, new object[] {"diagnostic", ""});
var stderr = Console.Error;
using var logged = new StringWriter();
Console.SetError(logged);
var locations = new List<object>();
try {
    var values = (IEnumerable)locator.GetType().GetProperty("AllLocations", flags).GetValue(locator);
    foreach (var item in values) {
        var locationType = item.GetType();
        object Get(string name) => locationType.GetProperty(name, flags).GetValue(item);
        var dependencies = new List<string>();
        foreach (var dep in (IEnumerable)Get("Dependencies"))
            dependencies.Add((string)dep.GetType().GetProperty("InternalId", flags).GetValue(dep));
        locations.Add(new { internalId = (string)Get("InternalId"), primaryKey = (string)Get("PrimaryKey"),
            providerId = (string)Get("ProviderId"), resourceType = ((Type)Get("ResourceType"))?.FullName,
            dependencies, dataAvailable = Get("Data") != null });
    }
} finally { Console.SetError(stderr); }
var exceptions = logged.ToString().Split("VN_DIAGNOSTIC_EXCEPTION", StringSplitOptions.None);
if (exceptions.Length != 4 || exceptions[0].Length != 0 || exceptions.Skip(1).Any(e =>
        !e.TrimStart().StartsWith("System.Security.SecurityException:", StringComparison.Ordinal) ||
        !e.Contains("UnityEngine.Hash128.Hash128ToStringImpl")))
    throw new InvalidOperationException("Unexpected diagnostic location errors: " + logged.ToString());
if (Hash(File.ReadAllBytes(catalog)) != catalogHashes[args[0]]) throw new InvalidOperationException("Catalog changed during reading");
Console.WriteLine(JsonSerializer.Serialize(new {schema = 1, platform = args[0], catalogSha256 = catalogHashes[args[0]],
    managedInventorySha256 = manifestHashes[args[0]], addressablesSha256 = Hash(addressables.bytes),
    resourceManagerSha256 = Hash(manager.bytes), diagnosticMemoryCopyCalls = replacements, diagnosticLoggerCalls = logs,
    nativeHashExceptions = exceptions.Length - 1, locationCount = locations.Count, locations,
    limitations = "Diagnostic in-memory ResourceManager copy substitutes memory copy and logs exceptions. Native Hash128 conversion failed for three bundle option records; location enumeration is partial, with bundle Data unavailable. Runtime loading, remote catalogs and completeness remain unverified."},
    new JsonSerializerOptions {WriteIndented = true}));
