using Mono.Cecil;
using System.Security.Cryptography;
string Sha(byte[] data) => Convert.ToHexString(SHA256.HashData(data)).ToLowerInvariant();
if(Sha(File.ReadAllBytes(typeof(ModuleDefinition).Assembly.Location))!="831dca77470d85cb6ffbea3072daa7a3df5b7c9fcfd9c3f43674a9be99d4bfcf") throw new Exception("Cecil");
var bytes=File.ReadAllBytes(args[1]);
var expected=args[0]=="macos" ? "f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb" : args[0]=="windows" ? "8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2" : "";
if(Sha(bytes)!=expected) throw new Exception("Wrong input assembly");
using var asm=ModuleDefinition.ReadModule(new MemoryStream(bytes));
foreach(var t in asm.GetTypes())
foreach(var m in t.Methods.Where(x=>x.HasBody)) {
 if (!(t.Name is "SaveManager" or "SaveManagerV1" or "InteractableDismissButton" or "FileManager" or "LevelFlow" or "LevelConfiguration" || t.Name=="WalkNWashSceneState" && m.Name=="NextLevel" || t.Name=="FlagRegistry" && m.Name is "Save" or "Load" or "GetYarnStorage")) continue;
 Console.WriteLine("METHOD "+m.FullName);
 foreach(var i in m.Body.Instructions) Console.WriteLine(i);
}
