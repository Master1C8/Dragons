using System.Security.Cryptography;
using Mono.Cecil;
using Mono.Cecil.Cil;
string root="/Users/antonkrutov/Desktop/Dragons/localization/work";
string source=Path.Combine(root,"YarnSpeakerSyntheticMacV2.dll");
string output=Path.Combine(root,"YarnSpeakerSyntheticMacLogged.dll");
string hash(byte[] b)=>Convert.ToHexString(SHA256.HashData(b)).ToLowerInvariant();
var bytes=File.ReadAllBytes(source);
if(hash(bytes)!="8b3906e2bb290fc0761348042abe1c76fea9e565b82eff5d58255877481d5c7f")throw new Exception("Unexpected source");
using var stream=new MemoryStream(bytes,false);
using var mod=ModuleDefinition.ReadModule(stream,new ReaderParameters{InMemory=true});
IEnumerable<TypeDefinition> All(IEnumerable<TypeDefinition> ts){foreach(var t in ts){yield return t;foreach(var c in All(t.NestedTypes))yield return c;}}
var log=All(mod.Types).SelectMany(t=>t.Methods).Where(m=>m.HasBody).SelectMany(m=>m.Body.Instructions).Select(i=>i.Operand).OfType<MethodReference>().First(m=>m.FullName=="System.Void UnityEngine.Debug::Log(System.Object)");
var helper=mod.Types.Single(t=>t.FullName=="Yarn.Unity.VnSyntheticSpeakerDisplay").Methods.Single(m=>m.Name=="GetDisplayName");
var returns=helper.Body.Instructions.Where(i=>i.OpCode==OpCodes.Ret).ToArray();
if(returns.Length!=3)throw new Exception("Unexpected helper layout");
var il=helper.Body.GetILProcessor();
foreach(var ret in returns){il.InsertBefore(ret,il.Create(OpCodes.Ldstr,"VN-SYNTHETIC-SPEAKER-VALUE"));il.InsertBefore(ret,il.Create(OpCodes.Call,log));il.InsertBefore(ret,il.Create(OpCodes.Dup));il.InsertBefore(ret,il.Create(OpCodes.Call,log));}
using(var f=new FileStream(output,FileMode.CreateNew,FileAccess.Write,FileShare.None))mod.Write(f);
using(var read=ModuleDefinition.ReadModule(output)){
 var checkedHelper=read.Types.Single(t=>t.FullName=="Yarn.Unity.VnSyntheticSpeakerDisplay").Methods.Single(m=>m.Name=="GetDisplayName");
 if(checkedHelper.Body.Instructions.Count(i=>i.OpCode==OpCodes.Ldstr && Equals(i.Operand,"VN-SYNTHETIC-SPEAKER-VALUE"))!=3)throw new Exception("Bad logging readback");
}
Console.WriteLine("Test-only instrumented helper SHA256 "+hash(File.ReadAllBytes(output)));
