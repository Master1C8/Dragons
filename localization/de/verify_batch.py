#!/usr/bin/env python3
"""Verify a German paired draft and save a reproducible diagnostic receipt."""
import hashlib, json, subprocess, sys, tempfile
from pathlib import Path

sys.path.insert(0, 'localization')
import UnityPy, paired_locale as pl, dialogue_locale as dl, compare_yarn_versions as versions
import speaker_locale, managed_fallback, windows_dialogue_probe as win

ROOT = Path('localization/work/cli-terra-high-20261110.J0KLrx/de')
RUN = ROOT / 'resume-04'
INVENTORY = Path('localization/work/source-inventory-20261107/combined-provisional-v42-20261110.json')
SCOPE = Path('localization/work/yarn-markers-20261110.ridbPA/yarn-scope-v42.json')
WORKLIST = ROOT / 'worklist.json'
LOCALE = Path('localization/de/translation.json')
DATA = {'macos': Path.home()/"Documents/Drag'N Wash.app/Contents/Resources/Data", 'windows': Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')}
EXPECTED = {'inventory':'79a38356e74a513bba512f2a23f462d4a6a25bf069519bab03aef96be24f476d', 'scope':'753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30', 'worklist':'9ee266ffbc4643e5b269b75ca03edfb763f1178d3803aa65b627d487c2b0535a'}
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    receipt = Path(sys.argv[1])
    if receipt.exists() or receipt.parent != Path('localization/de/receipts'):
        raise ValueError('receipt must be new and in localization/de/receipts')
    for name, path in [('inventory', INVENTORY), ('scope', SCOPE), ('worklist', WORKLIST)]:
        if sha(path) != EXPECTED[name]: raise ValueError(f'{name} fingerprint changed')
    before = sha(LOCALE)
    verify_cmd = [sys.executable, '-B', 'localization/verify_authored_yarn.py', str(LOCALE), '--locale', 'de', '--inventory', str(INVENTORY), '--yarn-scope', str(SCOPE)]
    report = json.loads(subprocess.check_output(verify_cmd, text=True))
    if report['translationSha256'] != before: raise ValueError('canonical verifier snapshot differs')
    worklist = json.loads(WORKLIST.read_text()); rows = {r['id']:r for r in worklist['rows']}
    translations = pl.read(LOCALE, 'de', worklist['yarnScopeSha256'], rows, complete=False)
    manifest = json.loads(speaker_locale.PREFIX_MANIFEST.read_text())
    input_dir = RUN / 'inputs' / receipt.stem
    input_dir.mkdir(parents=True, exist_ok=False)
    temporary = tempfile.TemporaryDirectory(prefix='batch-', dir=RUN)
    scratch = Path(temporary.name).resolve()
    out = {}
    try:
        for platform, data in DATA.items():
            spec = versions.BUILDS[platform]
            keys, values, extras, *_ = versions.load(data, spec)
            docs = {}
            for filename in ('dialogue.json', 'speakers.json'):
                doc = {'schema':1, 'locale':'de', 'sourceObjectSha256':worklist['builds'][platform]['sourceFingerprints'][filename], 'lines':{}}
                for key,texts in translations.items():
                    b=rows[key]['builds'].get(platform)
                    if b and b['file']==filename: doc['lines'][b['key']]={'source':b['source'],'text':texts[platform]}
                path=input_dir/f'{platform}-{filename}'; path.write_text(json.dumps(doc,ensure_ascii=False,indent=2)+'\n'); docs[filename]=path
            _, mapping = dl.read_locale(docs['dialogue.json'],keys,values,spec['localizationSha256'])
            _, names, alexander = speaker_locale.read_locale(platform,docs['speakers.json'],'de',managed_fallback.SOURCES[platform],manifest)
            assert names == {'speaker-ryan':'Ryan','speaker-conrad':'Conrad'} and alexander == translations['yarn:line:4b36ea4e'][platform]
            asset=scratch/f'{platform}.assets'
            if platform=='macos':
                subprocess.run([sys.executable,'-B','localization/dialogue_locale.py',str(data/'sharedassets1.assets'),'--locale',str(docs['dialogue.json']),'--output',str(asset)],check=True,capture_output=True,text=True)
            else:
                win.TEST_WORK=scratch; win.build(data,docs['dialogue.json'],asset)
            matches=[o for o in UnityPy.load(str(asset)).objects if o.path_id==spec['localization'] and o.type.name=='MonoBehaviour']
            if len(matches)!=1: raise ValueError('unexpected object identity')
            k,v,e=dl.parse(matches[0].get_raw_data())
            if k!=keys or e!=extras or v!=[mapping.get(key,value) for key,value in zip(keys,values)]: raise ValueError('ordered readback mismatch')
            out[platform]={'stock_asset_sha256':sha(data/'sharedassets1.assets'),'source_yarn_sha256':spec['localizationSha256'],'dialogue_binding_sha256':sha(docs['dialogue.json']),'speaker_binding_sha256':sha(docs['speakers.json']),'partial_asset_sha256':sha(asset),'ordered_values':len(keys),'authored_yarn':len(mapping),'untouched_yarn':len(keys)-len(mapping)}
        if sha(LOCALE)!=before: raise ValueError('locale changed during verification')
        receipt.parent.mkdir(parents=True,exist_ok=True)
        data={'schema':1,'locale':'de','translation_sha256':before,'authored_ids':len(translations),'pinned_inputs':EXPECTED,'canonical_verifier':{'command':verify_cmd,'result':report},'reproduction':{'command':[sys.executable,'-B','localization/de/verify_batch.py','localization/de/receipts/NEW-RECEIPT.json'],'helper_sha256':sha(Path(__file__)),'mac_builder':'localization/dialogue_locale.py','windows_builder':'localization/windows_dialogue_probe.py','readback':'reopen built Unity object and compare ordered keys, values, extras','binding_inputs_directory':str(input_dir),'temporary_asset_policy':'run-owned temporary directory; removed only after both platform readbacks and receipt succeed; failed outputs retained'},'platforms':out,'runtime_visual_independent_audit':'not established'}
        receipt.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    except BaseException:
        temporary._finalizer.detach()  # Preserve failed run evidence for diagnosis.
        print(f'Failure: preserve diagnostic directory {scratch}',file=sys.stderr)
        raise
    temporary.cleanup()
    print(json.dumps(data,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
