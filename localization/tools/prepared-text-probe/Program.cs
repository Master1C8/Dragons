using System.Security.Cryptography;
using System.Text.Json;
using Mono.Cecil;
using Mono.Cecil.Cil;

const string HookName = "System.Void TMPro.TMP_Text::PopulateTextBackingArray(System.String,System.Int32,System.Int32)";
const string HelperName = "Dragons.PreparedTextProbe";
if (args is ["--yarn", var yarn, var layout, var outputYarn])
{
    YarnRevealPatch.Write(yarn, layout, outputYarn, module => Bodies(module));
    return;
}
if (args.Length is not (3 or 4))
    throw new ArgumentException("Expected STOCK_TMP_DLL DISPLAY_MAP_JSON NEW_TMP_DLL [LAYOUT_DLL] or --yarn STOCK_YARN_DLL LAYOUT_DLL NEW_YARN_DLL");
var source = File.ReadAllBytes(args[0]);
var sourceHash = Hash(source);
if (sourceHash is not ("a25a11167a5a7339d611c364a6525fc172d19fe5caa6aa95d6866fd1d36d0743" or
                      "e22d8f83e97d0a27bed0480cfd52d13a6b26b1e74e3ad67e6a17316090ec3f9f"))
    throw new InvalidOperationException("Expected a pinned stock Dragons TextMesh Pro assembly");

var mapBytes = File.ReadAllBytes(args[1]);
using var json = JsonDocument.Parse(mapBytes);
var mappings = json.RootElement.EnumerateArray()
    .Select(row => (Logical: row.GetProperty("logical").GetString()!,
                    Prepared: row.GetProperty("prepared").GetString()!)).ToArray();
if (mappings.Length is < 1 or > 4096 ||
    mappings.Select(x => x.Logical).Distinct(StringComparer.Ordinal).Count() != mappings.Length ||
    mappings.Any(x => string.IsNullOrEmpty(x.Logical) || string.IsNullOrEmpty(x.Prepared)
        || x.Logical.Any(IsPua) || !x.Prepared.Any(IsPua)
        || x.Logical.Contains('\0') || x.Prepared.Contains('\0')))
    throw new ArgumentException("Expected a bounded exact map from logical text to prepared glyphs");

using var module = ModuleDefinition.ReadModule(new MemoryStream(source));
var original = Bodies(module);
var hook = module.GetType("TMPro.TMP_Text").Methods.Single(m => m.FullName == HookName);
var getLength = (MethodReference)hook.Body.Instructions
    .First(i => i.Operand is MethodReference m && m.FullName == "System.Int32 System.String::get_Length()").Operand;
var equality = new MethodReference("op_Equality", module.TypeSystem.Boolean, module.TypeSystem.String);
equality.Parameters.Add(new ParameterDefinition(module.TypeSystem.String));
equality.Parameters.Add(new ParameterDefinition(module.TypeSystem.String));
var compare = new MethodReference("CompareOrdinal", module.TypeSystem.Int32, module.TypeSystem.String);
compare.Parameters.Add(new ParameterDefinition(module.TypeSystem.String));
compare.Parameters.Add(new ParameterDefinition(module.TypeSystem.String));
var helper = new TypeDefinition("Dragons", "PreparedTextProbe",
    TypeAttributes.NotPublic | TypeAttributes.Abstract | TypeAttributes.Sealed, module.TypeSystem.Object);
module.Types.Add(helper);
var rewrite = new MethodDefinition("Rewrite", MethodAttributes.Public | MethodAttributes.Static,
    module.TypeSystem.Void);
helper.Methods.Add(rewrite);
rewrite.Parameters.Add(new ParameterDefinition(new ByReferenceType(module.TypeSystem.String)));
rewrite.Parameters.Add(new ParameterDefinition(module.TypeSystem.Int32));
rewrite.Parameters.Add(new ParameterDefinition(new ByReferenceType(module.TypeSystem.Int32)));
var ordered = mappings.OrderBy(pair => pair.Logical, StringComparer.Ordinal).ToArray();
var lookup = MakeLookup(0, ordered.Length);
var il = rewrite.Body.GetILProcessor();
var done = Instruction.Create(OpCodes.Ret);
var preparedValue = new VariableDefinition(module.TypeSystem.String);
rewrite.Body.Variables.Add(preparedValue);
rewrite.Body.InitLocals = true;

// Do not change sliced writes, null, or text outside the exact probe map.
il.Emit(OpCodes.Ldarg_1);
il.Emit(OpCodes.Brtrue, done);
il.Emit(OpCodes.Ldarg_0);
il.Emit(OpCodes.Ldind_Ref);
il.Emit(OpCodes.Brfalse, done);
il.Emit(OpCodes.Ldarg_2);
il.Emit(OpCodes.Ldind_I4);
il.Emit(OpCodes.Ldarg_0);
il.Emit(OpCodes.Ldind_Ref);
il.Emit(OpCodes.Callvirt, getLength);
il.Emit(OpCodes.Bne_Un, done);
il.Emit(OpCodes.Ldarg_0);
il.Emit(OpCodes.Ldind_Ref);
il.Emit(OpCodes.Call, lookup);
il.Emit(OpCodes.Stloc, preparedValue);
il.Emit(OpCodes.Ldloc, preparedValue);
il.Emit(OpCodes.Brfalse, done);
il.Emit(OpCodes.Ldarg_0);
il.Emit(OpCodes.Ldloc, preparedValue);
il.Emit(OpCodes.Stind_Ref);
il.Emit(OpCodes.Ldarg_2);
il.Emit(OpCodes.Ldloc, preparedValue);
il.Emit(OpCodes.Callvirt, getLength);
il.Emit(OpCodes.Stind_I4);
il.Append(done);

var patch = hook.Body.GetILProcessor();
var first = hook.Body.Instructions[0];
patch.InsertBefore(first, Instruction.Create(OpCodes.Ldarga_S, hook.Parameters[0]));
patch.InsertBefore(first, Instruction.Create(OpCodes.Ldarg_2));
patch.InsertBefore(first, Instruction.Create(OpCodes.Ldarga_S, hook.Parameters[2]));
patch.InsertBefore(first, Instruction.Create(OpCodes.Call, rewrite));
var renderPlans = args.Length == 4 ? RenderPlans.Encode(json.RootElement) : null;
if (renderPlans != null)
    RenderPlans.Attach(module, args[3], renderPlans);
using var stream = new MemoryStream();
module.Write(stream);
var output = stream.ToArray();
using var reopened = ModuleDefinition.ReadModule(new MemoryStream(output));
var verifiedHook = reopened.GetType("TMPro.TMP_Text").Methods.Single(m => m.FullName == HookName);
var prefix = verifiedHook.Body.Instructions.Take(4).ToArray();
if (prefix[0].OpCode != OpCodes.Ldarga_S || prefix[0].Operand != verifiedHook.Parameters[0] ||
    prefix[1].OpCode != OpCodes.Ldarg_2 ||
    prefix[2].OpCode != OpCodes.Ldarga_S || prefix[2].Operand != verifiedHook.Parameters[2] ||
    prefix[3].OpCode != OpCodes.Call ||
    (prefix[3].Operand as MethodReference)?.DeclaringType.FullName != HelperName)
    throw new InvalidOperationException("Prepared-text hook did not survive read-back");
if (renderPlans != null)
{
    if (reopened.AssemblyReferences.Any(reference => reference.Name == reopened.Assembly.Name.Name))
        throw new InvalidOperationException("Patched TMP contains an unintended self-reference");
    if (!reopened.Resources.OfType<EmbeddedResource>().Single(r => r.Name == RenderPlans.ResourceName)
            .GetResourceData().SequenceEqual(renderPlans))
        throw new InvalidOperationException("Prepared render plans did not survive read-back");
}
var after = Bodies(reopened, skipHookPrefix: 4, normalizeRenderHooks: renderPlans != null);
if (original.Count != after.Count || original.Any(row => !after.TryGetValue(row.Key, out var body) || body != row.Value))
    throw new InvalidOperationException("Original TMP bodies changed beyond the verified hook");

// Exercise the emitted managed helper without loading a player or Unity objects.
var emitted = System.Reflection.Assembly.Load(output).GetType(HelperName, true)!.GetMethod("Rewrite")!;
foreach (var (logical, prepared) in mappings)
{
    Verify(logical, 0, logical.Length, prepared, prepared.Length);
    Verify(logical, 1, logical.Length - 1, logical, logical.Length - 1);
    Verify(logical, 0, logical.Length - 1, logical, logical.Length - 1);
    Verify(prepared, 0, prepared.Length, prepared, prepared.Length);
}
Verify("TMP-42", 0, 6, "TMP-42", 6);
Verify(null, 0, 0, null, 0);
using (var file = new FileStream(args[2], FileMode.CreateNew))
    file.Write(output);
Console.WriteLine(JsonSerializer.Serialize(new
{
    sourceSha256 = sourceHash, outputSha256 = Hash(output), displayMapSha256 = Hash(mapBytes),
    patchedMethod = HookName, renderHook = renderPlans != null, verifiedOriginalMethodBodies = original.Count, mappings = mappings.Length,
}));

void Verify(string? value, int start, int length, string? expected, int expectedLength)
{
    object?[] parameters = { value, start, length };
    emitted.Invoke(null, parameters);
    if (!Equals(parameters[0], expected) || !Equals(parameters[2], expectedLength))
        throw new InvalidOperationException("Emitted helper returned unexpected text or length");
}

MethodDefinition MakeLookup(int start, int end)
{
    // Keep generated methods small while limiting each lookup to one leaf.
    var method = new MethodDefinition($"Lookup_{start}_{end}", MethodAttributes.Private | MethodAttributes.Static,
        module.TypeSystem.String);
    method.Parameters.Add(new ParameterDefinition(module.TypeSystem.String));
    helper.Methods.Add(method);
    var emit = method.Body.GetILProcessor();
    if (end - start > 32)
    {
        var middle = start + (end - start) / 2;
        var left = MakeLookup(start, middle);
        var right = MakeLookup(middle, end);
        var rightInput = Instruction.Create(OpCodes.Ldarg_0);
        emit.Emit(OpCodes.Ldarg_0);
        emit.Emit(OpCodes.Ldstr, ordered[middle].Logical);
        emit.Emit(OpCodes.Call, compare);
        emit.Emit(OpCodes.Ldc_I4_0);
        emit.Emit(OpCodes.Bge, rightInput);
        emit.Emit(OpCodes.Ldarg_0);
        emit.Emit(OpCodes.Call, left);
        emit.Emit(OpCodes.Ret);
        emit.Append(rightInput);
        emit.Emit(OpCodes.Call, right);
        emit.Emit(OpCodes.Ret);
        return method;
    }
    foreach (var (logical, prepared) in ordered[start..end])
    {
        var next = Instruction.Create(OpCodes.Nop);
        emit.Emit(OpCodes.Ldarg_0);
        emit.Emit(OpCodes.Ldstr, logical);
        emit.Emit(OpCodes.Call, equality);
        emit.Emit(OpCodes.Brfalse, next);
        emit.Emit(OpCodes.Ldstr, prepared);
        emit.Emit(OpCodes.Ret);
        emit.Append(next);
    }
    emit.Emit(OpCodes.Ldnull);
    emit.Emit(OpCodes.Ret);
    return method;
}

static bool IsPua(char value) => value is >= '\uE000' and <= '\uF8FF';
static string Hash(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();

static Dictionary<string, string> Bodies(ModuleDefinition module, int skipHookPrefix = 0, bool normalizeRenderHooks = false)
{
    return module.GetTypes().Where(t => t.FullName != HelperName).SelectMany(t => t.Methods)
        .Where(m => m.HasBody).ToDictionary(m => m.FullName, m =>
        {
            var body = m.Body;
            var render = normalizeRenderHooks ? RenderPlans.Inspect(m) : null;
            var instructions = body.Instructions.Skip(m.FullName == HookName ? skipHookPrefix : 0)
                .Where(i => i != render?.Load && i != render?.Call).ToArray();
            var indices = instructions.Select((i, n) => (i, n)).ToDictionary(x => x.i, x => x.n);
            int Index(Instruction? instruction) => instruction == null ? -1 :
                indices[instruction == render?.Load ? render.Value.Join : instruction];
            string? Operand(object? value) => value switch
            {
                Instruction target => Index(target).ToString(),
                Instruction[] targets => string.Join(",", targets.Select(Index)),
                VariableDefinition variable => variable.Index.ToString(),
                ParameterDefinition parameter => parameter.Index.ToString(),
                _ => value?.ToString(),
            };
            return JsonSerializer.Serialize(new
            {
                body.InitLocals,
                Locals = body.Variables.Select(v => v.VariableType.FullName),
                Handlers = body.ExceptionHandlers.Select(h => new
                {
                    h.HandlerType, Catch = h.CatchType?.FullName, Try = Index(h.TryStart),
                    EndTry = Index(h.TryEnd), Start = Index(h.HandlerStart), End = Index(h.HandlerEnd),
                    Filter = Index(h.FilterStart),
                }),
                IL = instructions.Select(i => new[] { i.OpCode.Name, Operand(i.Operand) }),
            });
        });
}
