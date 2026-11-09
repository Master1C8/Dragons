using System.Security.Cryptography;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 2)
    throw new ArgumentException("Usage: speaker-inline-unity-probe PATCHED_MAC_YARN_DLL OUTPUT_TEST_DLL");
string work = Path.GetFullPath(Path.Combine("localization", "work"));
string outputPath = Path.GetFullPath(args[1]);
if (Path.GetExtension(outputPath) != ".dll" ||
    !outputPath.StartsWith(work + Path.DirectorySeparatorChar, StringComparison.Ordinal))
    throw new InvalidOperationException("Expected a fresh DLL inside localization/work");
for (var directory = new DirectoryInfo(Path.GetDirectoryName(outputPath)); directory != null; directory = directory.Parent)
    if (!directory.Exists || (directory.Attributes & FileAttributes.ReparsePoint) != 0)
        throw new InvalidOperationException("Unsafe test output directory");

string Hash(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
var bytes = File.ReadAllBytes(args[0]);
if (Hash(bytes) != "73192452a93f2ea49ba866a9933b4ca8e8edf68cf946bd5f522472e3513e8e67" ||
    Hash(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) !=
        "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unexpected input assembly");
using var module = ModuleDefinition.ReadModule(new MemoryStream(bytes));
var presenter = module.GetTypes().Single(t => t.FullName == "Yarn.Unity.LinePresenter");
var awake = presenter.Methods.Single(m => m.Name == "Awake" && m.HasBody);
var field = presenter.Fields.Single(f => f.Name == "characterNameText" && f.FieldType.FullName == "TMPro.TMP_Text");
var inline = presenter.Fields.Single(f => f.Name == "showCharacterNameInLine" && f.FieldType.FullName == "System.Boolean");
var log = module.GetTypes().SelectMany(t => t.Methods).Where(m => m.HasBody)
    .SelectMany(m => m.Body.Instructions).Select(i => i.Operand).OfType<MethodReference>()
    .First(m => m.FullName == "System.Void UnityEngine.Debug::Log(System.Object)");
var il = awake.Body.GetILProcessor();
var entry = awake.Body.Instructions[0];
foreach (var instruction in new[]{ il.Create(OpCodes.Ldarg_0), il.Create(OpCodes.Ldnull),
    il.Create(OpCodes.Stfld, field), il.Create(OpCodes.Ldarg_0), il.Create(OpCodes.Ldc_I4_1),
    il.Create(OpCodes.Stfld, inline) }) il.InsertBefore(entry, instruction);

var helper = module.GetTypes().Single(t => t.FullName == "Yarn.Unity.VnSyntheticSpeakerDisplay")
    .Methods.Single(m => m.Name == "GetInlineText");
var resultGetter = module.GetTypes().SelectMany(t => t.Methods).Where(m => m.HasBody)
    .SelectMany(m => m.Body.Instructions).Select(i => i.Operand).OfType<MethodReference>()
    .First(m => m.FullName == "System.String Yarn.Markup.MarkupParseResult::get_Text()");
var returns = helper.Body.Instructions.Where(i => i.OpCode == OpCodes.Ret).ToArray();
if (returns.Length != 3) throw new InvalidOperationException("Unexpected inline bridge");
var result = new VariableDefinition(helper.ReturnType);
helper.Body.Variables.Add(result);
helper.Body.InitLocals = true;
var logIl = helper.Body.GetILProcessor();
foreach (var ret in returns) foreach (var instruction in new[]{
    logIl.Create(OpCodes.Stloc, result), logIl.Create(OpCodes.Ldstr, "VN-INLINE-UNITY-VIEW"),
    logIl.Create(OpCodes.Call, log), logIl.Create(OpCodes.Ldloca, result),
    logIl.Create(OpCodes.Call, resultGetter), logIl.Create(OpCodes.Call, log),
    logIl.Create(OpCodes.Ldloc, result)
}) logIl.InsertBefore(ret, instruction);
using var buffer = new MemoryStream();
module.Write(buffer);
byte[] outputBytes = buffer.ToArray();
using var rebuilt = ModuleDefinition.ReadModule(new MemoryStream(outputBytes));
var verified = rebuilt.GetTypes().Single(t => t.FullName == presenter.FullName).Methods.Single(m => m.Name == awake.Name);
var verifiedBridge = rebuilt.GetTypes().Single(t => t.FullName == helper.DeclaringType.FullName).Methods.Single(m => m.Name == helper.Name);
if (!verified.Body.Instructions.Take(6).Select(i => i.OpCode.Code).SequenceEqual(new[]{
    Code.Ldarg_0,Code.Ldnull,Code.Stfld,Code.Ldarg_0,Code.Ldc_I4_1,Code.Stfld }) ||
    verifiedBridge.Body.Instructions.Count(i => i.OpCode.Code == Code.Ldstr && Equals(i.Operand, "VN-INLINE-UNITY-VIEW")) != 3)
    throw new InvalidOperationException("Test instrumentation failed read-back");
using (var output = new FileStream(outputPath, FileMode.CreateNew)) output.Write(outputBytes);
Console.WriteLine(Hash(outputBytes));
