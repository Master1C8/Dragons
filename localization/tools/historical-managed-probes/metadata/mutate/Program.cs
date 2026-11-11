using Mono.Cecil;
using var module = ModuleDefinition.ReadModule(args[0]);
if (args[2] == "parameter") {
    var method = module.GetType("MenuSlotsNew").Methods.Single(m => m.Name == "OnShow");
    method.Parameters.Single().Name = "metadataControl";
}
module.Write(args[1]);
