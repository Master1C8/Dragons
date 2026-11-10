using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 2)
    throw new ArgumentException("Expected localized Assembly-CSharp.dll and a fresh output path");
using var input = ModuleDefinition.ReadModule(args[0]);
var method = input.GetType("SteamManager").Methods.Single(m =>
    m.FullName == "System.Void SteamManager::EnsureSteamAppIdFile(System.UInt32)");
var body = method.Body.Instructions;
var parent = body[1];
if (body.Count != 23 || parent.OpCode != OpCodes.Ldstr || !Equals(parent.Operand, "..") ||
    !Equals(body[2].Operand, "steam_appid.txt") ||
    body[0].Operand is not MethodReference path || path.FullName != "System.String UnityEngine.Application::get_dataPath()" ||
    !body.Any(i => i.Operand is MethodReference write &&
                  write.FullName == "System.Void System.IO.File::WriteAllText(System.String,System.String)"))
    throw new InvalidDataException("Unexpected Steam App ID writer");
var before = input.GetTypes().SelectMany(t => t.Methods).Where(m => m.HasBody)
    .ToDictionary(m => m.FullName, Fingerprint);
parent.Operand = "MacOS";
using var stream = new MemoryStream();
input.Write(stream);
var data = stream.ToArray();
using var reopened = ModuleDefinition.ReadModule(new MemoryStream(data));
var after = reopened.GetTypes().SelectMany(t => t.Methods).Where(m => m.HasBody).ToArray();
var changed = after.Single(m => m.FullName == method.FullName).Body.Instructions[1];
if (!Equals(changed.Operand, "MacOS"))
    throw new InvalidDataException("Steam App ID destination did not survive read-back");
changed.Operand = "..";
if (after.Length != before.Count || after.Any(m => !before.TryGetValue(m.FullName, out var f) || f != Fingerprint(m)))
    throw new InvalidDataException("Unexpected managed changes");
using var output = new FileStream(args[1], FileMode.CreateNew);
output.Write(data);

static string Fingerprint(MethodDefinition method) =>
    string.Join("\n", method.Body.Instructions.Select(i => i.OpCode + " " + i.Operand));
