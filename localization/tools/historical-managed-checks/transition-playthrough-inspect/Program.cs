using Mono.Cecil;
using Mono.Cecil.Cil;
using var assembly = AssemblyDefinition.ReadAssembly(args[0]);
IEnumerable<TypeDefinition> All(IEnumerable<TypeDefinition> types) {
    foreach (var t in types) {
        yield return t;
        foreach (var n in All(t.NestedTypes)) yield return n;
    }
}
foreach (var t in All(assembly.MainModule.Types)) {
    foreach (var m in t.Methods.Where(m=>m.HasBody)) {
        if ((t.Name is "InteractableToolEquip" or "InteractableCrate" or "Interacter")
              && (m.Name is "Interact" or "CanInteract" or "OnAttackStarted" or "Update")) {
            Console.WriteLine(m.FullName);
            foreach(var i in m.Body.Instructions) Console.WriteLine(i);
        }
    }
}
