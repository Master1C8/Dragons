using System.Runtime.CompilerServices;
using TMPro;

namespace Dragons.PreparedText;

public static class RenderHook
{
    public const string ResourceName = "Dragons.PreparedText.Plans";
    private static readonly Lazy<Dictionary<string, Plan>> Plans = new(ReadPlans);

    private static readonly ConditionalWeakTable<TMP_Text, Reveal> ActiveReveals = new();

    public static int GetLogicalCount(TMP_Text text, string logical)
    {
        var info = text.GetTextInfo(logical);
        ActiveReveals.Remove(text);
        if (text.isRightToLeftText || !Plans.Value.TryGetValue(logical, out var plan) ||
            !MeshLayout.MatchesPrepared(info, plan.Prepared, plan.Offsets))
            return info.characterCount;
        ActiveReveals.Add(text, new Reveal(logical, plan));
        return plan.SourceEnds[plan.SourceEnds.Length - 1];
    }

    public static void Advance(TMP_Text text, int logicalIndex)
    {
        text.maxVisibleCharacters = ActiveReveals.TryGetValue(text, out var reveal) && reveal.Logical == text.text
            ? GlyphLimit(reveal.Plan, logicalIndex + 1)
            : text.maxVisibleCharacters + 1;
    }

    public static void Finish(TMP_Text text, int logicalCount)
    {
        text.maxVisibleCharacters = ActiveReveals.TryGetValue(text, out var reveal) && reveal.Logical == text.text
            ? GlyphLimit(reveal.Plan, logicalCount)
            : logicalCount;
        ActiveReveals.Remove(text);
    }

    private static int GlyphLimit(Plan plan, int logicalVisible) =>
        ClusterLayout.GlyphRevealLimit(plan.SourceEnds, plan.Ends, logicalVisible);

    private sealed class Reveal
    {
        public readonly string Logical;
        public readonly Plan Plan;

        public Reveal(string logical, Plan plan)
        {
            Logical = logical;
            Plan = plan;
        }
    }

    public static bool SkipWrapState(TMP_Text text, uint glyph, int index) =>
        TryWrapCluster(text, glyph, index, out _, out var end) && index + 1 < end;

    public static bool DeferWidthOverflow(TMP_Text text, uint glyph, int index, int lineStart) =>
        TryWrapCluster(text, glyph, index, out var start, out var end) &&
        (index + 1 < end || (index > start && start == lineStart));

    private static bool TryWrapCluster(TMP_Text text, uint glyph, int index, out int start, out int end)
    {
        start = end = index;
        if (glyph is < 0xe000 or > 0xf8ff || text.isRightToLeftText ||
            text.text is not string logical || !Plans.Value.TryGetValue(logical, out var plan))
            return false;
        return TryWrapCluster(plan.Prepared, plan.Offsets, plan.Ends, glyph, index, out start, out end);
    }

    internal static bool TryWrapCluster(string prepared, int[] offsets, int[] ends, uint glyph, int index,
        out int start, out int end)
    {
        start = end = index;
        if ((uint)index >= (uint)offsets.Length || prepared[offsets[index]] != glyph)
            return false;
        var cluster = Array.BinarySearch(ends, index + 1);
        if (cluster < 0)
            cluster = ~cluster;
        start = cluster == 0 ? 0 : ends[cluster - 1];
        end = ends[cluster];
        // The dictionary marker is invisible and remains a legal wrap point.
        if (prepared[offsets[end - 1]] == '\u200b')
            end--;
        return end > start && index < end;
    }

    public static void Apply(TMP_Text text)
    {
        if (!text.isRightToLeftText)
            TryApply(text.textInfo, text.text, text.maxVisibleCharacters);
    }

    internal static bool TryApply(TMP_TextInfo info, string? logical, int visible)
    {
        return logical != null && Plans.Value.TryGetValue(logical, out var plan) && plan.ParagraphLevel == 1 &&
            MeshLayout.TryApplyPrepared(info, plan.Prepared, plan.Offsets, plan.Ends,
                plan.Levels, plan.TrailingReset, 1, visible);
    }

    private static Dictionary<string, Plan> ReadPlans()
    {
        using var stream = typeof(TMP_Text).Assembly.GetManifestResourceStream(ResourceName)
            ?? throw new InvalidOperationException("Missing Dragons prepared text plans");
        using var reader = new BinaryReader(stream);
        if (reader.ReadInt32() != 3)
            throw new InvalidDataException("Unsupported Dragons display plan format");
        var count = reader.ReadInt32();
        var plans = new Dictionary<string, Plan>(count, StringComparer.Ordinal);
        for (var i = 0; i < count; i++)
        {
            var logical = reader.ReadString();
            var prepared = reader.ReadString();
            var paragraphLevel = reader.ReadByte();
            var offsets = new int[reader.ReadInt32()];
            for (var j = 0; j < offsets.Length; j++)
                offsets[j] = reader.ReadInt32();
            var ends = new int[reader.ReadInt32()];
            var sourceEnds = new int[ends.Length];
            var levels = new byte[ends.Length];
            var reset = new bool[ends.Length];
            for (var j = 0; j < ends.Length; j++)
            {
                ends[j] = reader.ReadInt32();
                sourceEnds[j] = reader.ReadInt32();
                levels[j] = reader.ReadByte();
                reset[j] = reader.ReadBoolean();
            }
            plans.Add(logical, new Plan(prepared, paragraphLevel, offsets, ends, sourceEnds, levels, reset));
        }
        if (stream.Position != stream.Length)
            throw new InvalidDataException("Trailing data in Dragons display plans");
        return plans;
    }

    private sealed class Plan
    {
        public readonly string Prepared;
        public readonly byte ParagraphLevel;
        public readonly int[] Offsets;
        public readonly int[] Ends;
        public readonly int[] SourceEnds;
        public readonly byte[] Levels;
        public readonly bool[] TrailingReset;

        public Plan(string prepared, byte paragraphLevel, int[] offsets, int[] ends, int[] sourceEnds, byte[] levels, bool[] trailingReset)
        {
            Prepared = prepared;
            ParagraphLevel = paragraphLevel;
            Offsets = offsets;
            Ends = ends;
            SourceEnds = sourceEnds;
            Levels = levels;
            TrailingReset = trailingReset;
        }
    }
}
