using TMPro;
using UnityEngine;

namespace Dragons.PreparedText;

public static class MeshLayout
{
    public static bool TryApplyPrepared(
        TMP_TextInfo info, string preparedText, ReadOnlySpan<int> visibleOffsets,
        ReadOnlySpan<int> clusterEnds, ReadOnlySpan<byte> levels,
        ReadOnlySpan<bool> trailingReset, byte paragraphLevel, int requestedVisible)
    {
        if (info.characterCount != visibleOffsets.Length || info.characterInfo.Length < visibleOffsets.Length)
            return false;
        var previous = -1;
        for (var i = 0; i < visibleOffsets.Length; i++)
        {
            var offset = visibleOffsets[i];
            ref var ch = ref info.characterInfo[i];
            if (offset <= previous || offset >= preparedText.Length ||
                ch.index != offset || ch.character != preparedText[offset] || ch.stringLength != 1)
                return false;
            previous = offset;
        }
        return TryApply(info, clusterEnds, levels, trailingReset, paragraphLevel, requestedVisible);
    }

    // Input must be resolved against this exact TMP character table. Leave the
    // mesh intact if TMP wrapped inside a cluster or assigned unexpected slots.
    public static bool TryApply(
        TMP_TextInfo info, ReadOnlySpan<int> clusterEnds, ReadOnlySpan<byte> levels,
        ReadOnlySpan<bool> trailingReset, byte paragraphLevel, int requestedVisible)
    {
        var count = info.characterCount;
        if (count == 0 || clusterEnds.Length == 0 || clusterEnds[clusterEnds.Length - 1] != count ||
            clusterEnds.Length != levels.Length || levels.Length != trailingReset.Length ||
            paragraphLevel > 1 || count > info.characterInfo.Length)
            return false;

        var previousEnd = 0;
        for (var cluster = 0; cluster < clusterEnds.Length; cluster++)
        {
            if (clusterEnds[cluster] <= previousEnd || clusterEnds[cluster] > count || levels[cluster] > 126)
                return false;
            previousEnd = clusterEnds[cluster];
        }

        var characters = info.characterInfo;
        var requested = Math.Max(0, Math.Min(count, requestedVisible));
        var reveal = ClusterLayout.RevealLimit(clusterEnds, requested);
        var offsets = new float[count];
        var occupied = new HashSet<(int Material, int Vertex)>();
        const FontStyles Decorations = FontStyles.Underline | FontStyles.Strikethrough | FontStyles.Highlight;
        for (var i = 0; i < count; i++)
        {
            ref var ch = ref characters[i];
            if (ch.pageNumber != 0 || (ch.style & Decorations) != 0)
                return false;
            if (i >= requested || !ch.isVisible)
                continue;
            if ((uint)ch.materialReferenceIndex >= (uint)info.meshInfo.Length)
                return false;
            var vertices = info.meshInfo[ch.materialReferenceIndex].vertices;
            if (vertices == null || ch.vertexIndex < 0 || ch.vertexIndex > vertices.Length - 4 ||
                !occupied.Add((ch.materialReferenceIndex, ch.vertexIndex)))
                return false;
        }

        var ends = clusterEnds.ToArray();
        int ClusterStart(int cluster) => cluster == 0 ? 0 : ends[cluster - 1];
        var start = 0;
        while (start < clusterEnds.Length)
        {
            var line = characters[ClusterStart(start)].lineNumber;
            var end = start;
            while (end < clusterEnds.Length && characters[ClusterStart(end)].lineNumber == line)
            {
                for (var i = ClusterStart(end); i < clusterEnds[end]; i++)
                    if (characters[i].lineNumber != line)
                        return false;
                end++;
            }
            var widths = new float[end - start];
            var left = characters[ClusterStart(start)].origin;
            if (float.IsNaN(left) || float.IsInfinity(left))
                return false;
            for (var cluster = start; cluster < end; cluster++)
            {
                var origin = characters[ClusterStart(cluster)].origin;
                var right = cluster + 1 < end
                    ? characters[ClusterStart(cluster + 1)].origin
                    : characters[clusterEnds[cluster] - 1].xAdvance;
                var width = right - origin;
                if (width < 0 || float.IsNaN(width) || float.IsInfinity(width))
                    return false;
                widths[cluster - start] = width;
            }
            var order = ClusterLayout.VisualOrder(
                levels.Slice(start, end - start), trailingReset.Slice(start, end - start), paragraphLevel);
            var positions = ClusterLayout.VisualOrigins(order, widths, left);
            for (var cluster = start; cluster < end; cluster++)
            {
                var first = ClusterStart(cluster);
                var delta = positions[cluster - start] - characters[first].origin;
                for (var i = first; i < clusterEnds[cluster]; i++)
                    offsets[i] = delta;
            }
            start = end;
        }

        for (var i = 0; i < count; i++)
        {
            ref var ch = ref characters[i];
            var delta = offsets[i];
            ch.origin += delta;
            ch.xAdvance += delta;
            ch.bottomLeft.x += delta;
            ch.topLeft.x += delta;
            ch.topRight.x += delta;
            ch.bottomRight.x += delta;
            ch.vertex_BL.position.x += delta;
            ch.vertex_TL.position.x += delta;
            ch.vertex_TR.position.x += delta;
            ch.vertex_BR.position.x += delta;
            if (i >= requested || !ch.isVisible)
                continue;
            var vertices = info.meshInfo[ch.materialReferenceIndex].vertices;
            for (var v = ch.vertexIndex; v < ch.vertexIndex + 4; v++)
            {
                if (i >= reveal)
                    vertices[v] = default;
                else
                    vertices[v].x += delta;
            }
        }
        return true;
    }
}
