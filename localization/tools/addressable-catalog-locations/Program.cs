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

if (args.Length is not (2 or 3) || (args[0] != "macos" && args[0] != "windows") ||
    (args.Length == 3 && args[2] != "--bundle-options"))
    throw new ArgumentException("Usage: addressable-catalog-locations macos|windows ORIGINAL_DATA [--bundle-options]");
bool includeOptions = args.Length == 3;
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
var addressableBytes = addressables.bytes;
if (includeOptions) {
    using var core = ModuleDefinition.ReadModule(new MemoryStream(dlls.Single(f => f.name == "UnityEngine.CoreModule.dll").bytes));
    var hashType = core.GetType("UnityEngine.Hash128");
    if (!hashType.IsSequentialLayout || !hashType.Fields.Where(f => !f.IsStatic)
        .Select(f => (f.Name, f.FieldType.FullName)).SequenceEqual(new[] { ("u64_0", "System.UInt64"), ("u64_1", "System.UInt64") }))
        throw new InvalidOperationException("Unsupported Hash128 layout");
    using var resolver = new DefaultAssemblyResolver();
    resolver.AddSearchDirectory(managed);
    using var addressable = ModuleDefinition.ReadModule(new MemoryStream(addressableBytes),
        new ReaderParameters { AssemblyResolver = resolver });
    var adapter = addressable.GetTypes().Single(t => t.FullName ==
        "UnityEngine.AddressableAssets.ResourceLocators.ContentCatalogData/AssetBundleRequestOptionsSerializationAdapter");
    var decoder = adapter.Methods.Single(m => m.Name == "Deserialize");
    var convert = decoder.Body.Instructions.Single(i => i.Offset == 0x0049);
    var prefix = convert.Previous;
    if (convert.OpCode != OpCodes.Callvirt || ((MethodReference)convert.Operand).FullName !=
        "System.String System.Object::ToString()" || prefix.OpCode != OpCodes.Constrained ||
        ((TypeReference)prefix.Operand).FullName != hashType.FullName)
        throw new InvalidOperationException("Unexpected native hash conversion site");
    var replacement = new GenericInstanceMethod(addressable.ImportReference(typeof(RawHash128).GetMethod(nameof(RawHash128.Words))));
    replacement.GenericArguments.Add((TypeReference)prefix.Operand);
    prefix.OpCode = OpCodes.Nop; prefix.Operand = null;
    convert.OpCode = OpCodes.Call; convert.Operand = replacement;
    using var prepared = new MemoryStream(); addressable.Write(prepared);
    addressableBytes = prepared.ToArray();
}
var assembly = AssemblyLoadContext.Default.LoadFromStream(new MemoryStream(addressableBytes));
var type = assembly.GetType("UnityEngine.AddressableAssets.ResourceLocators.ContentCatalogData", true);
const BindingFlags flags = BindingFlags.Static | BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic;
var content = type.GetMethod("LoadFromFile", flags).Invoke(null, new object[] {catalog, false});
var locator = type.GetMethod("CreateCustomLocator", flags).Invoke(content, new object[] {"diagnostic", ""});
var stderr = Console.Error;
using var logged = new StringWriter();
Console.SetError(logged);
var locations = new List<object>();
var optionRows = new List<object>();
var locationIds = new HashSet<string>(StringComparer.Ordinal);
var keyLocations = new Dictionary<string, string[]>(StringComparer.Ordinal);
const string BundleOptionsType = "UnityEngine.ResourceManagement.ResourceProviders.AssetBundleRequestOptions";
const string BundleResourceType = "UnityEngine.ResourceManagement.ResourceProviders.IAssetBundleResource";
try {
    var values = (IEnumerable)locator.GetType().GetProperty("AllLocations", flags).GetValue(locator);
    foreach (var item in values) {
        var locationType = item.GetType();
        object Get(string name) => locationType.GetProperty(name, flags).GetValue(item);
        var dependencies = new List<string>();
        foreach (var dep in (IEnumerable)Get("Dependencies"))
            dependencies.Add((string)dep.GetType().GetProperty("InternalId", flags).GetValue(dep));
        var id = (string)Get("InternalId");
        var resourceType = ((Type)Get("ResourceType"))?.FullName;
        var option = Get("Data");
        locations.Add(new { internalId = id, primaryKey = (string)Get("PrimaryKey"),
            providerId = (string)Get("ProviderId"), resourceType, dependencies, dataAvailable = option != null });
        if (!includeOptions) continue;
        if (!locationIds.Add(id)) throw new InvalidOperationException("Duplicate catalog location");
        if (resourceType != BundleResourceType && option == null) continue;
        if (resourceType != BundleResourceType || option?.GetType().FullName != BundleOptionsType)
            throw new InvalidOperationException("Unexpected catalog option type");
        object Value(string name) => option.GetType().GetProperty(name, flags).GetValue(option);
        var hash128Words = ((string)Value("Hash")).Split(':');
        if (hash128Words.Length != 2 || hash128Words.Any(word => word.Length != 16 || !word.All(Uri.IsHexDigit)))
            throw new InvalidOperationException("Unexpected Hash128 word representation");
        optionRows.Add(new { internalId = id, hash128Words, bundleName = (string)Value("BundleName"),
            crc = (uint)Value("Crc"), bundleSize = (long)Value("BundleSize"), timeout = (int)Value("Timeout"),
            retryCount = (int)Value("RetryCount"), redirectLimit = (int)Value("RedirectLimit"),
            assetLoadMode = Value("AssetLoadMode").ToString(), chunkedTransfer = (bool)Value("ChunkedTransfer"),
            useCrcForCachedBundle = (bool)Value("UseCrcForCachedBundle"),
            useWebRequestForLocalBundles = (bool)Value("UseUnityWebRequestForLocalBundles"),
            clearOtherCachedVersions = (bool)Value("ClearOtherCachedVersionsWhenLoaded") });
    }
    if (includeOptions) {
        var locatorType = locator.GetType();
        var locate = locatorType.GetMethod("Locate", flags);
        var locatedIds = new HashSet<string>(StringComparer.Ordinal);
        foreach (var key in (IEnumerable)locatorType.GetProperty("Keys", flags).GetValue(locator)) {
            object[] arguments = { key, null, null };
            if (key is not string name || !(bool)locate.Invoke(locator, arguments) || arguments[2] is not IEnumerable matches)
                throw new InvalidOperationException("Catalog key has no location");
            var ids = matches.Cast<object>().Select(item =>
                (string)item.GetType().GetProperty("InternalId", flags).GetValue(item)).ToArray();
            if (ids.Length == 0 || !keyLocations.TryAdd(name, ids))
                throw new InvalidOperationException("Empty or duplicate catalog key");
            locatedIds.UnionWith(ids);
        }
        if (keyLocations.Count != 24 || !locationIds.SetEquals(locatedIds) || locationIds.Count != 13 || optionRows.Count != 3)
            throw new InvalidOperationException("Catalog key and location coverage differs");
    }
} finally { Console.SetError(stderr); }
var exceptions = logged.ToString().Split("VN_DIAGNOSTIC_EXCEPTION", StringSplitOptions.None);
if (includeOptions ? logged.GetStringBuilder().Length != 0 : exceptions.Length != 4 || exceptions[0].Length != 0 || exceptions.Skip(1).Any(e =>
        !e.TrimStart().StartsWith("System.Security.SecurityException:", StringComparison.Ordinal) ||
        !e.Contains("UnityEngine.Hash128.Hash128ToStringImpl")))
    throw new InvalidOperationException("Unexpected diagnostic location errors: " + logged.ToString());
if (Hash(File.ReadAllBytes(catalog)) != catalogHashes[args[0]]) throw new InvalidOperationException("Catalog changed during reading");
if (includeOptions) {
    Console.WriteLine(JsonSerializer.Serialize(new {schema = 1, platform = args[0], catalogSha256 = catalogHashes[args[0]],
        managedInventorySha256 = manifestHashes[args[0]], addressablesSha256 = Hash(addressables.bytes),
        resourceManagerSha256 = Hash(manager.bytes), diagnosticMemoryCopyCalls = replacements, diagnosticLoggerCalls = logs,
        nativeHashExceptions = 0, keyCount = keyLocations.Count, locationCount = locations.Count,
        locations, keyLocations, bundleOptions = optionRows,
        limitations = "In-memory diagnostic. Hash128 words are the raw managed UInt64 fields, not native Unity hash strings. Catalog keys and local options were decoded; Unity runtime loading and external catalogs remain unverified." },
        new JsonSerializerOptions {WriteIndented = true}));
    return;
}
Console.WriteLine(JsonSerializer.Serialize(new {schema = 1, platform = args[0], catalogSha256 = catalogHashes[args[0]],
    managedInventorySha256 = manifestHashes[args[0]], addressablesSha256 = Hash(addressables.bytes),
    resourceManagerSha256 = Hash(manager.bytes), diagnosticMemoryCopyCalls = replacements, diagnosticLoggerCalls = logs,
    nativeHashExceptions = exceptions.Length - 1, locationCount = locations.Count, locations,
    limitations = "Diagnostic in-memory ResourceManager copy substitutes memory copy and logs exceptions. Native Hash128 conversion failed for three bundle option records; location enumeration is partial, with bundle Data unavailable. Runtime loading, remote catalogs and completeness remain unverified."},
    new JsonSerializerOptions {WriteIndented = true}));

public static class RawHash128
{
    public static string Words<T>(ref T value) where T : struct
    {
        var bytes = System.Runtime.InteropServices.MemoryMarshal.AsBytes(
            System.Runtime.InteropServices.MemoryMarshal.CreateReadOnlySpan(ref value, 1));
        if (bytes.Length != 16 || !BitConverter.IsLittleEndian)
            throw new InvalidOperationException("Unsupported managed Hash128 layout");
        ulong first = System.Buffers.Binary.BinaryPrimitives.ReadUInt64LittleEndian(bytes);
        ulong second = System.Buffers.Binary.BinaryPrimitives.ReadUInt64LittleEndian(bytes[8..]);
        return $"{first:x16}:{second:x16}";
    }
}
