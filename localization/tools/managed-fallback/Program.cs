using System.Globalization;
using System.Security.Cryptography;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

if (args.Length != 3)
    throw new ArgumentException("Expected SOURCE_DLL OUTPUT_DLL REPLACEMENT");
var bytes = File.ReadAllBytes(args[0]);
var sourceHash = Hash(bytes);
if (sourceHash is not ("54953f9c071aa3ca5b52eb8b12b8e0bedc73f7665a506c61acbef0c58ac340ef" or
    "3d5def40f51540e79dbb6a897993fe006022cf1f16933a1b47a69334085ad89d"))
    throw new InvalidOperationException("Unsupported Yarn Spinner Unity assembly");
if (Hash(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) !=
    "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unsupported Cecil assembly");

const string originalText = "!! ERROR: Missing line!";
const string initializer = "System.Void Yarn.Unity.LocalizedLine::.cctor()";
var replacement = args[2];
if (string.IsNullOrWhiteSpace(replacement) || replacement.IndexOfAny(new[] { '<', '>', '\r', '\n', '\0' }) >= 0)
    throw new ArgumentException("Expected a single plain-text replacement");
using var original = ModuleDefinition.ReadModule(new MemoryStream(bytes));
using var edited = ModuleDefinition.ReadModule(new MemoryStream(bytes));
var method = edited.GetType("Yarn.Unity.LocalizedLine").Methods.Single(m => m.FullName == initializer);
var raw = method.Body.Instructions.Single(i => i.Offset == 0x18);
var parsed = method.Body.Instructions.Single(i => i.Offset == 0x39);
if (raw.OpCode.Code != Code.Ldstr || !Equals(raw.Operand, originalText) ||
    raw.Next.OpCode.Code != Code.Stfld ||
    raw.Next.Operand?.ToString() != "System.String Yarn.Unity.LocalizedLine::RawText" ||
    parsed.OpCode.Code != Code.Ldstr || !Equals(parsed.Operand, originalText) ||
    parsed.Next.OpCode.Code != Code.Newobj ||
    parsed.Next.Next.Operand?.ToString() != "System.Void Yarn.Markup.MarkupParseResult::.ctor(System.String,System.Collections.Generic.List`1<Yarn.Markup.MarkupAttribute>)" ||
    parsed.Next.Next.Next.Operand?.ToString() != "System.Void Yarn.Unity.LocalizedLine::set_Text(Yarn.Markup.MarkupParseResult)")
    throw new InvalidOperationException("Unexpected fallback text binding");

var sites = new HashSet<int> { method.Body.Instructions.IndexOf(raw), method.Body.Instructions.IndexOf(parsed) };
raw.Operand = replacement;
parsed.Operand = replacement;
using var memory = new MemoryStream();
if (replacement != originalText)
    edited.Write(memory);
var output = replacement == originalText ? bytes : memory.ToArray();
using var rebuilt = ModuleDefinition.ReadModule(new MemoryStream(output));
var before = Snapshot(original, originalText);
var after = Snapshot(rebuilt, replacement);
if (before.Count != after.Count || before.Any(entry => !after.TryGetValue(entry.Key, out var body) || body != entry.Value))
    throw new InvalidOperationException("Unintended change in managed method bodies");

using (var file = new FileStream(args[1], FileMode.CreateNew, FileAccess.Write, FileShare.None))
    file.Write(output);
Console.WriteLine(JsonSerializer.Serialize(new { sourceSha256 = sourceHash, outputSha256 = Hash(output),
    changedOffsets = new[] { 0x18, 0x39 }, verifiedMethodBodies = before.Count }));

static string Hash(byte[] value) => Convert.ToHexString(SHA256.HashData(value)).ToLowerInvariant();

Dictionary<string, string> Snapshot(ModuleDefinition assembly, string expected)
{
    var result = new Dictionary<string, string>(StringComparer.Ordinal);
    foreach (var method in assembly.GetTypes().SelectMany(t => t.Methods).Where(m => m.HasBody))
    {
        var body = method.Body;
        var indices = body.Instructions.Select((i, n) => (i, n)).ToDictionary(x => x.i, x => x.n);
        int Index(Instruction? i) => i == null ? -1 : indices[i];
        string? Operand(object? value) => value switch
        {
            Instruction target => Index(target).ToString(CultureInfo.InvariantCulture),
            Instruction[] targets => string.Join(",", targets.Select(Index)),
            VariableDefinition variable => variable.Index.ToString(CultureInfo.InvariantCulture),
            ParameterDefinition parameter => parameter.Index.ToString(CultureInfo.InvariantCulture),
            IFormattable formatted => formatted.ToString(null, CultureInfo.InvariantCulture),
            _ => value?.ToString(),
        };
        var instructions = body.Instructions.Select((instruction, index) =>
        {
            if (method.FullName != initializer || !sites.Contains(index))
                return new[] { instruction.OpCode.Name, Operand(instruction.Operand) };
            if (instruction.OpCode.Code != Code.Ldstr || !Equals(instruction.Operand, expected))
                throw new InvalidOperationException("Fallback replacement failed read-back");
            return new[] { instruction.OpCode.Name, "<checked fallback>" };
        });
        result.Add(method.FullName, JsonSerializer.Serialize(new
        {
            body.InitLocals, body.MaxStackSize,
            locals = body.Variables.Select(v => v.VariableType.FullName),
            handlers = body.ExceptionHandlers.Select(h => new { h.HandlerType, catchType = h.CatchType?.FullName,
                tryStart = Index(h.TryStart), tryEnd = Index(h.TryEnd), start = Index(h.HandlerStart),
                end = Index(h.HandlerEnd), filter = Index(h.FilterStart) }),
            instructions,
        }));
    }
    return result;
}
