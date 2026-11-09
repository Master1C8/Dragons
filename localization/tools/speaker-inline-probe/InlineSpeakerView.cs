using Yarn.Markup;
using Yarn.Unity;

internal static class InlineSpeakerView
{
    internal static MarkupParseResult Create(LocalizedLine line, string displayName)
    {
        MarkupParseResult original = line.Text;
        string? name = line.CharacterName;
        if (name is not ("Ryan" or "Conrad"))
            return original;
        string sourcePrefix = name + ": ";
        if (line.RawText?.StartsWith(sourcePrefix, StringComparison.Ordinal) != true ||
            !original.Text.StartsWith(sourcePrefix, StringComparison.Ordinal))
            return original;
        if (string.IsNullOrEmpty(displayName) || !displayName.All(char.IsLetter))
            throw new ArgumentException("Expected a plain display name", nameof(displayName));

        int prefixLength = sourcePrefix.Length;
        var characters = original.Attributes.Where(attribute => attribute.Name == "character").ToArray();
        if (characters.Length != 1 || characters[0].Position != 0 || characters[0].Length != prefixLength ||
            original.Attributes.Any(attribute => attribute.Name != "character" && attribute.Position < prefixLength))
            return original;

        // Parse only the plain replacement prefix. The body has already gone
        // through the game's substitution and markup processors.
        string prefix = displayName + ": ";
        var parsedPrefix = new LineParser().ParseString(prefix + "X", "en", true);
        if (parsedPrefix.Attributes.Count != 1 || parsedPrefix.Attributes[0].Name != "character" ||
            parsedPrefix.Attributes[0].Position != 0 || parsedPrefix.Attributes[0].Length != prefix.Length ||
            parsedPrefix.Text != prefix + "X")
            throw new InvalidOperationException("Unexpected replacement prefix parse");

        int delta = prefix.Length - prefixLength;
        var attributes = original.Attributes.Select(attribute => attribute.Name == "character"
            ? parsedPrefix.Attributes[0] : attribute.Shift(delta)).ToList();
        return new MarkupParseResult(prefix + original.Text[prefixLength..], attributes);
    }
}
