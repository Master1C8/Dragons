namespace Dragons.PreparedText;

public static class ClusterLayout
{
    // Apply the trailing reset and visual reordering to one already wrapped line.
    // Each item is a shaped cluster, so its glyphs are never individually reversed.
    public static int[] VisualOrder(
        ReadOnlySpan<byte> paragraphLevels, ReadOnlySpan<bool> resetAtLineEnd, byte paragraphLevel)
    {
        if (paragraphLevel > 1 || paragraphLevels.Length != resetAtLineEnd.Length)
            throw new ArgumentException("Expected resolved cluster levels and reset flags for one line");

        var levels = paragraphLevels.ToArray();
        var order = new int[levels.Length];
        for (var i = 0; i < levels.Length; i++)
        {
            if (levels[i] > 126)
                throw new ArgumentException("Invalid resolved bidi level");
            order[i] = i;
        }
        for (var i = levels.Length - 1; i >= 0 && resetAtLineEnd[i]; i--)
            levels[i] = paragraphLevel;

        var highest = 0;
        var lowestOdd = 127;
        foreach (var level in levels)
        {
            highest = Math.Max(highest, level);
            if ((level & 1) != 0)
                lowestOdd = Math.Min(lowestOdd, level);
        }
        for (var level = highest; level >= lowestOdd; level--)
        {
            var start = 0;
            while (start < levels.Length)
            {
                if (levels[start] < level)
                {
                    start++;
                    continue;
                }
                var end = start + 1;
                while (end < levels.Length && levels[end] >= level)
                    end++;
                Array.Reverse(order, start, end - start);
                start = end;
            }
        }
        return order;
    }

    // A cluster's width includes its glyph advances and any space measured by TMP.
    public static float[] VisualOrigins(ReadOnlySpan<int> order, ReadOnlySpan<float> widths, float left)
    {
        if (order.Length != widths.Length || float.IsNaN(left) || float.IsInfinity(left))
            throw new ArgumentException("Expected measured widths and a finite line origin");
        var origins = new float[order.Length];
        var seen = new bool[order.Length];
        foreach (var logical in order)
        {
            if ((uint)logical >= (uint)order.Length || seen[logical])
                throw new ArgumentException("Expected a permutation of logical clusters");
            var width = widths[logical];
            if (width < 0 || float.IsNaN(width) || float.IsInfinity(width))
                throw new ArgumentException("Expected nonnegative finite cluster widths");
            seen[logical] = true;
            origins[logical] = left;
            left += width;
        }
        return origins;
    }

    // TMP's stock counter is in generated character indices. Hold that counter
    // at the previous whole cluster until every glyph in the next one can show.
    public static int RevealLimit(ReadOnlySpan<int> clusterEnds, int requested)
    {
        var previous = 0;
        var visible = 0;
        foreach (var end in clusterEnds)
        {
            if (end <= previous)
                throw new ArgumentException("Expected increasing exclusive cluster ends");
            if (end <= requested)
                visible = end;
            previous = end;
        }
        return visible;
    }
}
