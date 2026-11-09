using System.Security.Cryptography;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 4 && !(args.Length == 5 && args[4] == "--windows"))
    throw new ArgumentException("Expected game DLL, companion DLL, companion hash and new output [--windows]");
var expectedGameHash = args.Length == 5
    ? "8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2"
    : "f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb";
string Hash(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
var game = File.ReadAllBytes(args[0]);
var companion = File.ReadAllBytes(args[1]);
if (Hash(game) != expectedGameHash ||
    Hash(companion) != args[2] || Hash(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) !=
        "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unexpected input fingerprint");
var output = Path.GetFullPath(args[3]);
var work = Path.GetFullPath(Path.Combine("localization","work")) + Path.DirectorySeparatorChar;
if (!output.StartsWith(work, StringComparison.Ordinal) || !Path.GetFileName(output).Equals("InstrumentedAssembly-CSharp.dll"))
    throw new InvalidOperationException("Expected a new test output under localization/work");
for (var dir = new DirectoryInfo(Path.GetDirectoryName(output)); dir != null; dir = dir.Parent)
    if (!dir.Exists || (dir.Attributes & FileAttributes.ReparsePoint) != 0)
        throw new InvalidOperationException("Unsafe test output directory");
using var module = ModuleDefinition.ReadModule(new MemoryStream(game, writable: false));
using var helper = ModuleDefinition.ReadModule(new MemoryStream(companion, writable: false));
if (helper.Assembly.Name.Name != "Dragons.BackgroundInputProbe")
    throw new InvalidOperationException("Unexpected companion identity");
var probe = helper.GetType("Dragons.BackgroundInputProbe.Probe");
var menu = module.GetType("MenuMain");
var onShow = menu.Methods.Single(m => m.FullName == "System.Void MenuMain::OnShow(MenuResponseTransition)");
var onEvent = menu.Methods.Single(m => m.FullName == "MenuResponse MenuMain::OnEvent(MenuEvent)");
void InsertHook(MethodDefinition body, string name, bool passEvent) {
    var hook = probe.Methods.Single(m => m.IsStatic && m.Name == name && m.Parameters.Count == (passEvent ? 1 : 0));
    var il = body.Body.GetILProcessor();
    var head = body.Body.Instructions[0];
    if (passEvent) il.InsertBefore(head, il.Create(OpCodes.Ldarg_1));
    il.InsertBefore(head, il.Create(OpCodes.Call, module.ImportReference(hook)));
}
InsertHook(onShow, "Start", false);
InsertHook(onEvent, "ObserveMenu", true);
using var buffer = new MemoryStream();
module.Write(buffer);
var patched = buffer.ToArray();
using var verify = ModuleDefinition.ReadModule(new MemoryStream(patched, writable: false));
using var original = ModuleDefinition.ReadModule(new MemoryStream(game, writable: false));
string Format(Instruction ins, Instruction[] code) {
    var operand = ins.Operand switch {
        Instruction label => Array.IndexOf(code, label).ToString(),
        Instruction[] labels => string.Join(",", labels.Select(label => Array.IndexOf(code, label))),
        _ => ins.Operand?.ToString()
    };
    return ins.OpCode.Name + " " + operand;
}
var old = original.GetTypes().SelectMany(t => t.Methods).Where(m => m.HasBody).ToDictionary(m => m.FullName);
var updated = verify.GetTypes().SelectMany(t => t.Methods).Where(m => m.HasBody).ToDictionary(m => m.FullName);
if (!old.Keys.ToHashSet().SetEquals(updated.Keys)) throw new InvalidOperationException("Method inventory changed");
foreach (var name in old.Keys) {
    var a = old[name].Body.Instructions.ToArray();
    var b = updated[name].Body.Instructions.ToArray();
    var count = name == onShow.FullName ? 1 : name == onEvent.FullName ? 2 : 0;
    if (count != 0) {
        var call = b[count - 1];
        var expected = name == onShow.FullName
            ? "System.Void Dragons.BackgroundInputProbe.Probe::Start()"
            : "System.Void Dragons.BackgroundInputProbe.Probe::ObserveMenu(System.Object)";
        if (call.OpCode != OpCodes.Call || call.Operand?.ToString() != expected ||
            count == 2 && b[0].OpCode != OpCodes.Ldarg_1)
            throw new InvalidOperationException("Unexpected hook");
    }
    b = b.Skip(count).ToArray();
    if (!a.Select(i => Format(i, a)).SequenceEqual(b.Select(i => Format(i, b))))
        throw new InvalidOperationException("Original instruction sequence changed: " + name);
}
using (var dest = new FileStream(output, FileMode.CreateNew)) dest.Write(patched);
Console.WriteLine($"verified method bodies={old.Count} hooks=2 output={Hash(patched)}");
