using System.Security.Cryptography;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 3 || args[0] is not ("macos" or "windows"))
    throw new ArgumentException("Usage: patcher macos|windows ORIGINAL_GAME_DLL NEW_PROBE_DLL");
string Sha(byte[] input) => Convert.ToHexString(SHA256.HashData(input)).ToLowerInvariant();
const string cecilHash = "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf";
if (Sha(File.ReadAllBytes(typeof(AssemblyDefinition).Assembly.Location)) != cecilHash)
    throw new InvalidOperationException("Unsupported Mono.Cecil binary");
var expectedGame = args[0] == "macos"
    ? "f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb"
    : "8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2";
var bytes = File.ReadAllBytes(args[1]);
if (Sha(bytes) != expectedGame) throw new InvalidOperationException("Game assembly fingerprint mismatch");
using var asm = AssemblyDefinition.ReadAssembly(new MemoryStream(bytes));
var scene = asm.MainModule.Types.Single(t => t.Name == "WalkNWashSceneState");
var setFlag = scene.Methods.Single(m => m.Name == "_SetFlag" && m.Parameters.Count == 2 &&
    m.Parameters[1].ParameterType.FullName == "System.Boolean");
var find = setFlag.Body.Instructions.Single(i => i.OpCode.Code == Code.Call &&
    i.Operand is GenericInstanceMethod g && g.FullName ==
        "!!0 UnityEngine.Object::FindFirstObjectByType<Yarn.Unity.VariableStorageBehaviour>()");
var log = setFlag.Body.Instructions.Single(i => i.OpCode.Code == Code.Call &&
    i.Operand is MethodReference r && r.FullName == "System.Void UnityEngine.Debug::Log(System.Object)");
var storeType = ((GenericInstanceMethod)find.Operand).GenericArguments.Single();
var store = new FieldDefinition("VnProbeStorage", FieldAttributes.Public | FieldAttributes.Static, storeType);
scene.Fields.Add(store);
find.OpCode = OpCodes.Ldsfld;
find.Operand = store;
log.OpCode = OpCodes.Pop;
log.Operand = null;
var registry = asm.MainModule.Types.Single(t => t.FullName == "WalkNWash.Flags.FlagRegistry");
var findForLoad = registry.Methods.Single(m => m.Name == "GetYarnStorage").Body.Instructions.Single(i =>
    i.OpCode.Code == Code.Call && i.Operand is GenericInstanceMethod g &&
    g.FullName == "!!0 UnityEngine.Object::FindFirstObjectByType<Yarn.Unity.VariableStorageBehaviour>()");
findForLoad.OpCode = OpCodes.Ldsfld;
findForLoad.Operand = store;
var fileManager = asm.MainModule.Types.Single(t => t.Name == "FileManager");
var fullPath = fileManager.Methods.Single(m => m.Name == "GetFullSandboxDirectory");
var persistentPath = fullPath.Body.Instructions.Single(i => i.OpCode.Code == Code.Call &&
    i.Operand is MethodReference r && r.FullName == "System.String UnityEngine.Application::get_persistentDataPath()");
var scratchRoot = new FieldDefinition("VnProbeRoot", FieldAttributes.Public | FieldAttributes.Static,
    asm.MainModule.TypeSystem.String);
fileManager.Fields.Add(scratchRoot);
persistentPath.OpCode = OpCodes.Ldsfld;
persistentPath.Operand = scratchRoot;
var managers = asm.MainModule.Types.Where(t => t.Name is "SaveManager" or "SaveManagerV1").ToArray();
foreach (var manager in managers) {
    var withIndex = manager.Methods.Single(m => m.Name == "GetSteamAndSlotPath" && m.Parameters.Count == 1);
    var steam = withIndex.Body.Instructions.Single(i => i.OpCode.Code == Code.Call &&
        i.Operand is MethodReference r && r.FullName == "System.Boolean SteamManager::get_Initialized()");
    steam.OpCode = OpCodes.Ldc_I4_0;
    steam.Operand = null;
}
foreach (var method in managers.Append(fileManager).SelectMany(t => t.Methods).Where(m => m.HasBody))
foreach (var i in method.Body.Instructions) {
    if (i.OpCode.Code == Code.Call && i.Operand is MethodReference r &&
        r.FullName is "System.Void UnityEngine.Debug::Log(System.Object)" or
        "System.Void UnityEngine.Debug::LogError(System.Object)" or
        "System.Void UnityEngine.Debug::LogWarning(System.Object)") {
        i.OpCode = OpCodes.Pop;
        i.Operand = null;
    }
}
using var output = File.Open(args[2], FileMode.CreateNew);
asm.Write(output);
