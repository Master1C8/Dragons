using System.Security.Cryptography;
using Mono.Cecil;
using Mono.Cecil.Cil;

string Sha(string path) => Convert.ToHexString(SHA256.HashData(File.ReadAllBytes(path))).ToLowerInvariant();
const string cecilSha = "831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf";
if (Sha(typeof(AssemblyDefinition).Assembly.Location) != cecilSha)
    throw new InvalidOperationException("Cecil changed");
var files = Directory.GetFiles(args[0], "*.dll").Order(StringComparer.Ordinal).ToArray();
int read = 0, setterRefs = 0;
foreach (string path in files) {
    using var assembly = AssemblyDefinition.ReadAssembly(path);
    read++;
    foreach (var type in assembly.MainModule.GetTypes())
    foreach (var method in type.Methods.Where(m => m.HasBody)) {
        foreach (var instruction in method.Body.Instructions) {
            if (instruction.Operand is MethodReference reference
                && reference.FullName is "System.Void UnityEngine.Application::set_runInBackground(System.Boolean)"
                    or "System.Void UnityEngine.Device.Application::set_runInBackground(System.Boolean)") {
                setterRefs++;
                Console.WriteLine($"{Path.GetFileName(path)} {method.FullName} {instruction}");
            }
            if (instruction.OpCode.Code != Code.Ldstr
                || (string)instruction.Operand != "Waiting for flag {0}...{1}") continue;
            Console.WriteLine($"{Path.GetFileName(path)} {Sha(path)} {method.FullName}");
            foreach (var step in method.Body.Instructions) Console.WriteLine(step);
        }
    }
}
Console.WriteLine($"managedDLLs={read} runInBackgroundSetterRefs={setterRefs}");
