using System.Reflection;
using System.Runtime.CompilerServices;
using System.Text.Json;
using Dragons.PreparedText;
using TMPro;
using UnityEngine;

if (args.Length != 1)
    throw new ArgumentException("Expected the source display-plan JSON");

if (typeof(TMP_Text).Assembly.GetReferencedAssemblies().Any(x => x.Name == "Unity.TextMeshPro"))
    throw new Exception("Patched TMP contains an unintended self-reference");

using var file = JsonDocument.Parse(File.ReadAllBytes(args[0]));
var rtl = file.RootElement[0].GetProperty("paragraphLevel").GetInt32() == 1;
var plan = file.RootElement.EnumerateArray().First(row =>
    row.GetProperty("levels").EnumerateArray().All(x => x.GetInt32() == (rtl ? 1 : 0)) &&
    row.GetProperty("clusterEnds").GetArrayLength() >= 3);
var logical = plan.GetProperty("logical").GetString()!;
var prepared = plan.GetProperty("prepared").GetString()!;
var offsets = plan.GetProperty("offsets").EnumerateArray().Select(x => x.GetInt32()).ToArray();
var ends = plan.GetProperty("clusterEnds").EnumerateArray().Select(x => x.GetInt32()).ToArray();
var count = offsets.Length;
var info = (TMP_TextInfo)RuntimeHelpers.GetUninitializedObject(typeof(TMP_TextInfo));
info.characterCount = count;
info.characterInfo = new TMP_CharacterInfo[count];
info.meshInfo = new TMP_MeshInfo[1];
info.meshInfo[0].vertices = new Vector3[count * 4];
for (var i = 0; i < count; i++)
{
    info.characterInfo[i] = new TMP_CharacterInfo
    {
        origin = i, xAdvance = i + 1, index = offsets[i], character = prepared[offsets[i]],
        stringLength = 1, isVisible = true, vertexIndex = i * 4
    };
    for (var vertex = 0; vertex < 4; vertex++)
        info.meshInfo[0].vertices[i * 4 + vertex] = new Vector3(i + 0.25f, 3, 0);
}

var method = typeof(RenderHook).GetMethod("TryApply", BindingFlags.Static | BindingFlags.NonPublic)!;
bool Apply(string text) => (bool)method.Invoke(null, new object[] { info, text, int.MaxValue })!;
if (Apply("unmapped") || info.meshInfo[0].vertices[0].x != 0.25f)
    throw new Exception("Unmapped text modified geometry");
if (Apply(logical) != rtl)
    throw new Exception("Unexpected render hook dispatch");
if (rtl && (info.meshInfo[0].vertices[0].x != count - ends[0] + 0.25f ||
    info.meshInfo[0].vertices[(ends[^2]) * 4].x != 0.25f))
    throw new Exception("Mapped glyphs did not move to the expected reversed cluster positions");
if (!rtl && info.meshInfo[0].vertices[0].x != 0.25f)
    throw new Exception("LTR text geometry was unexpectedly reordered");
Console.WriteLine("Verified embedded plan lookup and direction-specific geometry");
var plans = (System.Collections.IDictionary)typeof(RenderHook)
    .GetMethod("ReadPlans", BindingFlags.Static | BindingFlags.NonPublic)!.Invoke(null, null)!;
foreach (var row in file.RootElement.EnumerateArray())
{
    var key = row.GetProperty("logical").GetString()!;
    var entry = plans[key] ?? throw new Exception("Missing binary plan");
    var glyphBoundaries = row.GetProperty("clusterEnds").EnumerateArray().Select(x => x.GetInt32()).ToArray();
    var sourceBoundaries = row.GetProperty("sourceClusterEnds").EnumerateArray().Select(x => x.GetInt32()).ToArray();
    var storedGlyph = (int[])entry.GetType().GetField("Ends")!.GetValue(entry)!;
    var storedSource = (int[])entry.GetType().GetField("SourceEnds")!.GetValue(entry)!;
    if (!storedGlyph.SequenceEqual(glyphBoundaries) || !storedSource.SequenceEqual(sourceBoundaries))
        throw new Exception("Binary reveal boundary mismatch");
    var index = 0;
    for (var step = 0; step <= sourceBoundaries[^1] + 1; step++)
    {
        if (index < sourceBoundaries.Length && sourceBoundaries[index] == step)
            index++;
        var expected = index == 0 ? 0 : glyphBoundaries[index - 1];
        var actual = ClusterLayout.GlyphRevealLimit(storedSource, storedGlyph, step);
        if (expected != actual)
            throw new Exception("Partial cluster reveal or wrong complete count");
    }
}
Console.WriteLine($"Verified every logical reveal step in {plans.Count} embedded plans");
var checkWrap = typeof(RenderHook).GetMethod("TryWrapCluster", BindingFlags.Static | BindingFlags.NonPublic,
    null, new[] { typeof(string), typeof(int[]), typeof(int[]), typeof(uint), typeof(int),
        typeof(int).MakeByRefType(), typeof(int).MakeByRefType() }, null)!;
int interiorCount = 0, thaiBreaks = 0;
foreach (var row in file.RootElement.EnumerateArray())
{
    var planText = row.GetProperty("prepared").GetString()!;
    var planOffsets = row.GetProperty("offsets").EnumerateArray().Select(x => x.GetInt32()).ToArray();
    var planEnds = row.GetProperty("clusterEnds").EnumerateArray().Select(x => x.GetInt32()).ToArray();
    int start = 0;
    foreach (var end in planEnds)
    {
        var marker = planText[planOffsets[end - 1]] == '\u200b';
        var glyphEnd = end - (marker ? 1 : 0);
        if (marker)
            thaiBreaks++;
        for (var i = start; i < end; i++)
        {
            var inputs = new object[] { planText, planOffsets, planEnds, (uint)planText[planOffsets[i]], i, 0, 0 };
            if ((bool)checkWrap.Invoke(null, inputs)! != (i < glyphEnd) ||
                (int)inputs[5] != start || (int)inputs[6] != glyphEnd)
                throw new Exception("Unexpected wrap boundary");
            if (i + 1 < glyphEnd)
                interiorCount++;
            inputs[3] = (uint)planText[planOffsets[i]] + 1;
            if ((bool)checkWrap.Invoke(null, inputs)!)
                throw new Exception("Mismatched glyph accepted");
        }
        start = end;
    }
}
Console.WriteLine($"Verified {interiorCount} interior glyph positions and {thaiBreaks} dictionary break points");
