using System.Security.Cryptography;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 2 || (args[0] != "macos" && args[0] != "windows"))
    throw new ArgumentException("Usage: settings-semantics macos|windows Naelstrof.UnityScriptableSettings.dll");
string Sha(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
var hashes = new Dictionary<string, string> {
    ["macos"] = "a16b7a3a94bd62e059694a311f68dec012aa66696a6eff9880ceb9087e6c915d",
    ["windows"] = "b6f215bc0eef09035d800a2fab01bed0a8ffeba8f85ba00cfb329ebf009c1f90"
};
var bytes = File.ReadAllBytes(args[1]);
if (Sha(bytes) != hashes[args[0]]) throw new InvalidOperationException("Unsupported settings assembly");
if (Sha(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");
using var module = ModuleDefinition.ReadModule(new MemoryStream(bytes));
MethodDefinition Get(string type, string name) => module.Types.Single(t => t.FullName == type).Methods.Single(m => m.Name == name && m.HasBody);
string[] Refs(MethodDefinition m) => m.Body.Instructions.Select(i => i.Operand).OfType<MemberReference>().Select(x => x.FullName).ToArray();
void Require(bool value, string message) { if (!value) throw new InvalidOperationException(message); }
const string ns = "UnityScriptableSettings.";
var dropdown = Get(ns + "SettingDropdown", "GetLocalizedDropdowns");
Require(dropdown.Body.Instructions.Select(x => x.OpCode.Code).SequenceEqual(new[] { Code.Ldarg_0, Code.Ldfld, Code.Ret }) &&
        Refs(dropdown).SequenceEqual(new[] { "ScriptableSettingString[] UnityScriptableSettings.SettingDropdown::dropdownOptions" }), "Unexpected dropdown source");
var setDropdown = Get(ns + "SettingDropdown", "SetValue");
Require(Refs(setDropdown).SequenceEqual(new[] { "ScriptableSettingString[] UnityScriptableSettings.SettingDropdown::dropdownOptions",
        "System.Int32 UnityEngine.Mathf::Clamp(System.Int32,System.Int32,System.Int32)",
        "System.Void UnityScriptableSettings.SettingInt::SetValue(System.Int32)" }) &&
        !setDropdown.Body.Instructions.Any(x => x.OpCode.Code == Code.Ldstr), "Unexpected dropdown value processing");
var resolution = Get(ns + "SettingResolution", "GetLocalizedDropdowns");
var resRefs = Refs(resolution);
Require(resRefs.Contains("UnityEngine.Resolution[] UnityEngine.Screen::get_resolutions()") &&
        resRefs.Contains("System.Int32 UnityEngine.Resolution::get_width()") &&
        resRefs.Contains("System.Int32 UnityEngine.Resolution::get_height()") &&
        resRefs.Contains("System.Void ScriptableSettingString::.ctor(System.String)") &&
        !resRefs.Any(x => x.Contains("::dropdownOptions")), "Unexpected resolution option generation");
var resSet = Get(ns + "SettingResolution", "SetValue");
Require(Refs(resSet).Contains("UnityEngine.Resolution[] UnityEngine.Screen::get_resolutions()"), "Unexpected resolution selection");
var fullscreen = Get(ns + "SettingFullscreenMode", "SetValue");
Require(fullscreen.Body.Instructions.Count(x => x.OpCode.Code == Code.Switch && ((Instruction[])x.Operand).Length == 4) == 1 &&
        Refs(fullscreen).Count(x => x == "System.Void UnityEngine.Screen::set_fullScreenMode(UnityEngine.FullScreenMode)") == 4 &&
        Refs(fullscreen).Contains("System.Void UnityScriptableSettings.SettingDropdown::SetValue(System.Int32)"), "Unexpected fullscreen handling");
var sync = Get(ns + "SettingVSync", "SetValue");
Require(Refs(sync).Contains("System.Void UnityEngine.QualitySettings::set_vSyncCount(System.Int32)") &&
        Refs(sync).Contains("System.Void UnityScriptableSettings.SettingDropdown::SetValue(System.Int32)"), "Unexpected VSync handling");
var fallback = Get("ScriptableSettingString", "GetLocalizedString");
Require(Refs(fallback).Count(x => x == "System.String ScriptableSettingString::backupString") == 2 &&
        Refs(fallback).Contains("System.Boolean UnityEngine.Localization.LocalizedReference::get_IsEmpty()") &&
        Refs(fallback).Contains("System.String UnityEngine.Localization.LocalizedString::GetLocalizedString()"), "Unexpected localized string fallback");
var methods = new[] { dropdown, setDropdown, resolution, resSet, fullscreen, sync, fallback };
var report = new { schema = 1, platform = args[0], assemblySha256 = hashes[args[0]],
    methods = methods.Select(m => new { signature = m.FullName,
        instructions = m.Body.Instructions.Select(i => new { offset = i.Offset, opcode = i.OpCode.Name,
            operand = i.Operand switch { null => null, Instruction target => $"IL_{target.Offset:x4}",
                Instruction[] targets => string.Join(",", targets.Select(t => $"IL_{t.Offset:x4}")), _ => i.Operand.ToString() } }).ToArray() }).ToArray(),
    limitations = "Selected static managed methods only. Runtime visibility, other callers, dynamic changes, external libraries and behavior on actual hardware are not established." };
Console.WriteLine(JsonSerializer.Serialize(report, new JsonSerializerOptions { WriteIndented = true }));
