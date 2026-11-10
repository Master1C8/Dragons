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

    public static void Apply(TMP_Text text)
    {
        if (!text.isRightToLeftText)
            TryApply(text.textInfo, text.text, text.maxVisibleCharacters);
    }

    internal static bool TryApply(TMP_TextInfo info, string? logical, int visible)
    {
        return logical != null && Plans.Value.TryGetValue(logical, out var plan) &&
            MeshLayout.TryApplyPrepared(info, plan.Prepared, plan.Offsets, plan.Ends,
                plan.Levels, plan.TrailingReset, 1, visible);
    }

    private static Dictionary<string, Plan> ReadPlans()
    {
        using var stream = typeof(TMP_Text).Assembly.GetManifestResourceStream(ResourceName)
            ?? throw new InvalidOperationException("Missing Dragons prepared text plans");
        using var reader = new BinaryReader(stream);
        if (reader.ReadInt32() != 2)
            throw new InvalidDataException("Unsupported Dragons display plan format");
        var count = reader.ReadInt32();
        var plans = new Dictionary<string, Plan>(count, StringComparer.Ordinal);
        for (var i = 0; i < count; i++)
        {
            var logical = reader.ReadString();
            var prepared = reader.ReadString();
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
            plans.Add(logical, new Plan(prepared, offsets, ends, sourceEnds, levels, reset));
        }
        if (stream.Position != stream.Length)
            throw new InvalidDataException("Trailing data in Dragons display plans");
        return plans;
    }

    private sealed class Plan
    {
        public readonly string Prepared;
        public readonly int[] Offsets;
        public readonly int[] Ends;
        public readonly int[] SourceEnds;
        public readonly byte[] Levels;
        public readonly bool[] TrailingReset;

        public Plan(string prepared, int[] offsets, int[] ends, int[] sourceEnds, byte[] levels, bool[] trailingReset)
        {
            Prepared = prepared;
            Offsets = offsets;
            Ends = ends;
            SourceEnds = sourceEnds;
            Levels = levels;
            TrailingReset = trailingReset;
        }
    }
}
