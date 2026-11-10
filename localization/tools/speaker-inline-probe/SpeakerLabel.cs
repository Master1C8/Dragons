#nullable enable


using System.Globalization;

internal static class SpeakerLabel
{
    public static bool IsValid(string? value)
    {
        if (string.IsNullOrEmpty(value) || value.Length > 40 || !char.IsLetter(value[0]))
            return false;
        foreach (var character in value)
        {
            if (!char.IsLetter(character) && char.GetUnicodeCategory(character) is not
                (UnicodeCategory.NonSpacingMark or UnicodeCategory.SpacingCombiningMark))
                return false;
        }
        return true;
    }
}
