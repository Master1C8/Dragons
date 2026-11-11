using System.IO.Compression;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using Mono.Cecil;

if (args.Length != 5)
{
    Console.Error.WriteLine("Usage: restore RECEIPT RECORDED_PATH MACOS_MANAGED WINDOWS_MANAGED FRESH_OUTPUT");
    return 2;
}

string Hash(byte[] data) => Convert.ToHexString(SHA256.HashData(data)).ToLowerInvariant();
const string cecilHash = "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf";
if (Hash(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != cecilHash)
    throw new InvalidDataException("Unexpected Mono.Cecil build");

using var compressed = File.OpenRead(args[0]);
using var receiptStream = new GZipStream(compressed, CompressionMode.Decompress);
using var receipt = JsonDocument.Parse(receiptStream);
var sources = receipt.RootElement.GetProperty("sources");
var row = receipt.RootElement.GetProperty("outputs").GetProperty(args[1]);
var methodsByAssembly = new Dictionary<string, ILookup<string, string[]>>();
var lines = new List<string>();

foreach (var section in row.GetProperty("sections").EnumerateArray())
{
    if (section.TryGetProperty("literal", out var literal))
    {
        lines.Add(literal.GetString()!);
        continue;
    }

    string key = section.GetProperty("assembly").GetString()!;
    if (!methodsByAssembly.TryGetValue(key, out var methods))
    {
        var source = sources.GetProperty(key);
        string directory = source.GetProperty("platform").GetString() switch
        {
            "macos" => args[2],
            "windows" => args[3],
            _ => throw new InvalidDataException("Unexpected stock platform"),
        };
        string name = source.GetProperty("name").GetString()!;
        if (name != Path.GetFileName(name))
            throw new InvalidDataException("Unexpected stock assembly name");
        byte[] bytes = File.ReadAllBytes(Path.Combine(directory, name));
        if (Hash(bytes) != source.GetProperty("sha256").GetString())
            throw new InvalidDataException($"Stock assembly fingerprint mismatch: {name}");
        using var module = ModuleDefinition.ReadModule(new MemoryStream(bytes));
        methods = module.GetTypes().SelectMany(type => type.Methods)
            .Where(method => method.HasBody)
            .ToLookup(method => method.FullName,
                method => method.Body.Instructions.Select(instruction => instruction.ToString()).ToArray());
        methodsByAssembly.Add(key, methods);
    }

    string methodName = section.GetProperty("method").GetString()!;
    int ordinal = section.GetProperty("ordinal").GetInt32();
    int start = section.GetProperty("start").GetInt32();
    int count = section.GetProperty("count").GetInt32();
    var instructions = methods[methodName].ElementAt(ordinal)[start..checked(start + count)];
    string header = section.GetProperty("header").GetString()!;
    lines.Add(header switch
    {
        "method" => $"METHOD {methodName}",
        "name" => methodName,
        "context" => $"{methodName} @ {instructions[0]}",
        _ => throw new InvalidDataException("Unexpected method header"),
    });
    lines.AddRange(header == "context" ? instructions.Skip(1) : instructions);
}

string text = string.Join("\n", lines) + (row.GetProperty("finalNewline").GetBoolean() ? "\n" : "");
byte[] output = Encoding.UTF8.GetBytes(text);
if (output.Length != row.GetProperty("bytes").GetInt32() || Hash(output) != row.GetProperty("sha256").GetString())
    throw new InvalidDataException("Restored IL report fingerprint mismatch");
using (var destination = new FileStream(args[4], FileMode.CreateNew))
    destination.Write(output);
if (!OperatingSystem.IsWindows())
    File.SetUnixFileMode(args[4], (UnixFileMode)Convert.ToInt32(row.GetProperty("mode").GetString()![2..], 8));
return 0;
