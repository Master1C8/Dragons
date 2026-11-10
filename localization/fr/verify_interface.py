#!/usr/bin/env python3
"""Rebuild and read back French UI and settings against both pinned stock builds."""
import hashlib, json, shutil, sys, tempfile
from pathlib import Path
sys.path.insert(0, 'localization')
import paired_locale as pl, ui_locale as mac_ui, windows_ui_locale as win_ui
import settings_locale as mac_settings
from verify_batch import ROOT, RUN, WORKLIST, LOCALE, DATA, EXPECTED, sha

def main():
    receipt=Path(sys.argv[1])
    if receipt.exists() or receipt.parent != Path('localization/fr/receipts'):
        raise ValueError('receipt must be new and under French receipts')
    if sha(WORKLIST)!=EXPECTED['worklist']: raise ValueError('worklist changed')
    before=sha(LOCALE); work=json.loads(WORKLIST.read_text()); rows={r['id']:r for r in work['rows']}
    translations=pl.read(LOCALE,'fr',work['yarnScopeSha256'],rows,complete=True)
    temp=tempfile.TemporaryDirectory(prefix='interface-',dir=RUN); root=Path(temp.name).resolve(); results={}
    try:
        for platform,data in DATA.items():
            dest=root/platform; dest.mkdir(); pl.materialize(dest,platform,'fr',work['builds'][platform],rows,translations)
            assets={}
            for name in [f'level{i}' for i in range(7)]:
                loc=dest/'ui'/f'{name}.json'; out=dest/f'output-{name}'
                if platform=='macos':
                    shutil.copyfile(data/name,out)
                    count=mac_ui.patch_into(data,name,loc,'fr',out)
                else:
                    report=win_ui.build(data,name,loc,'fr',out); count=report['changedFields']
                assets[name]={'source_sha256':sha(data/name),'binding_sha256':sha(loc),'output_sha256':sha(out),'fields':count}
                out.unlink()
            loc=dest/'settings.json'; out=dest/'output-settings.assets'
            if platform=='macos':
                shutil.copyfile(data/'sharedassets0.assets',out)
                prepared=mac_settings.make_asset(data,loc,'fr')
                count=mac_settings.patch_into(data,out,prepared)
            else:
                report=win_ui.build(data,'sharedassets0.assets',None,'fr',out,settings_locale_file=loc)
                count=report['settingsFields']
            assets['settings']={'source_sha256':sha(data/'sharedassets0.assets'),'binding_sha256':sha(loc),'output_sha256':sha(out),'fields':count}
            out.unlink(); results[platform]=assets
        if sha(LOCALE)!=before: raise ValueError('draft changed during readback')
        report={'schema':1,'locale':'fr','translation_sha256':before,'worklist_sha256':sha(WORKLIST),'helper_sha256':sha(Path(__file__)),'command':[sys.executable,'-B','localization/fr/verify_interface.py','localization/fr/receipts/NEW-RECEIPT.json'],'method':'source-pinned adapters reopen and compare all serialized objects; settings fields decoded and compared; outputs removed after successful readback','platforms':results,'runtime_visual_independent_audit':'not established'}
        receipt.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    except BaseException:
        temp._finalizer.detach(); print(f'Preserved failed diagnostics: {root}',file=sys.stderr); raise
    temp.cleanup(); print(json.dumps(report,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
