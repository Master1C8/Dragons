using TMPro;

namespace Dragons.PreparedText;

public static class RenderHook
{
    public const string ResourceName = "Dragons.PreparedText.Plans";
    private static readonly Lazy<Dictionary<string, Plan>> Plans = new(ReadPlans);

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
        if (reader.ReadInt32() != 1)
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
            var levels = new byte[ends.Length];
            var reset = new bool[ends.Length];
            for (var j = 0; j < ends.Length; j++)
            {
                ends[j] = reader.ReadInt32();
                levels[j] = reader.ReadByte();
                reset[j] = reader.ReadBoolean();
            }
            plans.Add(logical, new Plan(prepared, offsets, ends, levels, reset));
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
        public readonly byte[] Levels;
        public readonly bool[] TrailingReset;

        public Plan(string prepared, int[] offsets, int[] ends, byte[] levels, bool[] trailingReset)
        {
            Prepared = prepared;
            Offsets = offsets;
            Ends = ends;
            Levels = levels;
            TrailingReset = trailingReset;
        }
    }
}
