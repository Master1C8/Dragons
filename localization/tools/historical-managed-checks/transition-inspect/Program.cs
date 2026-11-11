using Mono.Cecil;
using var assembly = AssemblyDefinition.ReadAssembly(args[0]);
foreach(var type in assembly.MainModule.Types.Where(t => t.Name is "Interacter" or "Interactable" or "InteractableCrate" or "PlayerInputs" or "ToolTest")) {
    foreach(var method in type.Methods.Where(m => m.HasBody && !m.IsConstructor))
        Console.WriteLine(method + "\n" + string.Join("\n",method.Body.Instructions));
}
