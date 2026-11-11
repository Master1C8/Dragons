using Mono.Cecil;
using System.Security.Cryptography;
string Hash(byte[] bytes) => Convert.ToHexString(SHA256.HashData(bytes)).ToLowerInvariant();
if (Hash(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location)) != "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf")
    throw new InvalidOperationException("Unexpected Mono.Cecil");
var chosen = new HashSet<string> {"Yarn.Unity.BuiltinLocalisedLineProvider","Yarn.Unity.UnityLocalization.UnityLocalisedLineProvider",
 "Yarn.Markup.LineParser/MarkupDiagnostic","Yarn.Markup.ReplacementMarkerResult",
 "Yarn.Unity.Attributes.MessageBoxAttribute","Yarn.Unity.Cultures"};
foreach (var path in Directory.GetFiles(args[0], "*.dll").Order(StringComparer.Ordinal)) {
    var bytes = File.ReadAllBytes(path);
    Console.WriteLine("INPUT " + Path.GetFileName(path) + " " + Hash(bytes));
    using var module = ModuleDefinition.ReadModule(new MemoryStream(bytes, writable: false));
    foreach (var t in module.GetTypes()) {
        foreach (var attr in t.Fields.SelectMany(f=>f.CustomAttributes).Concat(t.Methods.SelectMany(m=>m.CustomAttributes)))
            if (attr.AttributeType.Name == "MessageBoxAttribute")
                Console.WriteLine($"MESSAGE_ATTRIBUTE {t.FullName} {string.Join(" ",attr.ConstructorArguments.Select(x=>x.Value))}");
        foreach (var m in t.Methods.Where(m => m.HasBody)) {
            var code = m.Body.Instructions;
            bool body = chosen.Any(n => t.FullName==n || t.FullName.StartsWith(n + "/", StringComparison.Ordinal))
                || (t.FullName.StartsWith("Yarn.Unity.DialogueRunner") && (m.Name == "get_LineProvider" || t.Name.StartsWith("<RunLocalisedLine")));
            for (int j = 0; j < code.Count; j++) {
                var i = code[j];
                if (body) Console.WriteLine($"BODY {m.FullName} @ {i}");
                bool hit = i.Operand switch {
                    MethodReference f when chosen.Contains(f.DeclaringType.FullName) || f.DeclaringType.FullName == "Yarn.Markup.LineParser" && f.Name.Contains("Parse") => true,
                    FieldReference f when (f.DeclaringType.FullName == "Yarn.Unity.LocalizedLine" && f.Name == "InvalidLine") || chosen.Contains(f.DeclaringType.FullName) || (f.DeclaringType.FullName == "Yarn.Unity.Culture" && f.Name == "DisplayName") => true,
                    _ => false
                };
                if (!hit) continue;
                Console.WriteLine($"REFERENCE {m.FullName} @ {i}");
                foreach (var next in code.Skip(j+1).Take(9)) Console.WriteLine($"NEXT {next}");
            }
        }
    }
}
