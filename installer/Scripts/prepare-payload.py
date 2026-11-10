#!/usr/bin/env python3
"""Produce exact binary deltas for the five verified Dragons packages."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = {'ar': 'العربية', 'fa': 'فارسی', 'he': 'עברית', 'th': 'ไทย', 'hi': 'हिन्दी'}
APP_ID = '4739660'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def files(root):
    return {p.relative_to(root).as_posix(): p for p in root.rglob('*') if p.is_file()}


def prepare(args):
    target = args.output
    target.mkdir(parents=True)
    payload = target / 'LocalizationPayload'
    tools = payload / 'Tools'
    tools.mkdir(parents=True)
    helper = tools / ('xdelta3' if args.platform == 'macos' else 'xdelta3.exe')
    shutil.copy2(args.helper, helper)
    shutil.copy2(args.delta_license, tools / 'XDELTA-LICENSE')
    helper_sha = sha(helper)
    (payload / 'BuildManifest.json').write_text(json.dumps({'deltaTool': {'sha256': helper_sha}}) + '\n')
    originals = files(args.stock)
    original_hashes = {name: sha(p) for name, p in originals.items()}
    anchors = {name: original_hashes[name] for name in ('globalgamemanagers', 'globalgamemanagers.assets')}
    config = {
        'schemaVersion': 2, 'packageID': 'dragons-vnrevival', 'sourceLocale': 'en',
        'steamAppID': APP_ID, 'steamBuildID': 'content-pinned', 'gameVersion': '',
        'unityVersion': '6000.3.14f1', 'payloadReady': True, 'files': [],
        'deltaToolSHA256': helper_sha, 'anchors': anchors, 'languages': [],
        **json.loads((ROOT / 'App/ConfigTemplate.json').read_bytes()),
    }
    cache = {}
    with tempfile.TemporaryDirectory(dir=target) as tmp:
        staging = Path(tmp)
        for lang, native_name in LANGUAGES.items():
            container = args.packages / args.platform
            if args.platform == 'macos':
                app = container / f'DragNWash-{lang}.app'
                resources = app / 'Contents/Resources'
                meta = json.loads((resources / 'vn-localization-package.json').read_bytes())
                current = files(resources / 'Data')
                require(set(originals) <= set(current), f"{lang} macOS package removed an original file")
                hashes = {name: sha(p) for name, p in current.items()}
                replacements = {name: p for name, p in current.items() if hashes[name] != original_hashes.get(name)}
                license_bytes = (resources / 'NotoShaped-OFL.txt').read_bytes()
            else:
                archive = container / f'DragNWash-{lang}.zip'
                receipt = json.loads((container / f'{lang}-receipt.json').read_bytes())
                if sha(archive) != receipt['sha256']:
                    raise ValueError(f'{lang} ZIP differs from the verified package')
                with ZipFile(archive) as z:
                    meta = json.loads(z.read('manifest.json'))
                    require(meta == receipt['manifest'], f'{lang} ZIP manifest mismatch')
                    replacements, hashes = {}, {}
                    for name, row in meta['files'].items():
                        require(not name.startswith('/') and '\\' not in name and ':' not in name and
                                all(part not in ('', '.', '..') for part in name.split('/')),
                                f'Unsafe package path: {name}')
                        require(row['sourceSha256'] == original_hashes.get(name), f'{name} source mismatch')
                        p = staging / name
                        p.parent.mkdir(parents=True, exist_ok=True)
                        p.write_bytes(z.read('DragNWash_Data/' + name))
                        require(sha(p) == row['outputSha256'], f'{name} ZIP checksum mismatch')
                        replacements[name], hashes[name] = p, row['outputSha256']
                    license_bytes = z.read('NotoShaped-OFL.txt')
            require(meta['locale'] == lang and meta['platform'] == args.platform, f"{lang} package receipt mismatch")
            require(meta['sourceGlobalManagersSha256'] == anchors['globalgamemanagers'], f"{lang} package receipt mismatch")
            require(meta['sourceGlobalScriptsSha256'] == anchors['globalgamemanagers.assets'], f"{lang} package receipt mismatch")
            require(hashlib.sha256(license_bytes).hexdigest() == meta['complexText']['fontFallback']['licenseSha256'], f"{lang} package receipt mismatch")
            require(hashes['sharedassets0.assets'] == meta['complexText']['fontFallback']['assetSha256'], f"{lang} package receipt mismatch")
            require(hashes['Managed/Unity.TextMeshPro.dll'] == meta['complexText']['tmp']['outputSha256'], f"{lang} package receipt mismatch")
            require(hashes['Managed/YarnSpinner.Unity.dll'] == meta['complexText']['yarn']['outputSha256'], f"{lang} package receipt mismatch")
            require(hashes['Managed/Dragons.PreparedTextLayout.dll'] == meta['complexText']['layoutSha256'], f"{lang} package receipt mismatch")
            config['gameVersion'] = meta['build']
            licenses = payload / 'Licenses'
            licenses.mkdir(exist_ok=True)
            (licenses / f'NotoShaped-{lang}-OFL.txt').write_bytes(license_bytes)
            result = []
            for name, p in sorted(replacements.items()):
                old, new = original_hashes.get(name), hashes[name]
                item = {'path': name, 'originalSHA256': old, 'payloadSHA256': new}
                if old is None:
                    path = f'Files/{new}/{p.name}'
                    output = payload / path
                    output.parent.mkdir(parents=True, exist_ok=True)
                    if not output.exists():
                        shutil.copy2(p, output)
                    item.update(payloadPath=path, artifactSHA256=new)
                else:
                    key = (old, new)
                    if key not in cache:
                        path = f'Deltas/{old[:12]}-{new}.vcdiff'
                        output = payload / path
                        output.parent.mkdir(parents=True, exist_ok=True)
                        subprocess.run([str(args.encoder), '-e', '-s', str(originals[name]), str(p), str(output)], check=True)
                        decoded = staging / 'decoded'
                        subprocess.run([str(args.encoder), '-d', '-s', str(originals[name]), str(output), str(decoded)], check=True)
                        if sha(decoded) != new:
                            raise ValueError(f'{name} did not reconstruct')
                        decoded.unlink()
                        cache[key] = {'path': path, 'sha256': sha(output)}
                    item['artifacts'] = [cache[key]]
                result.append(item)
            config['languages'].append({'siteLocale': lang, 'runtimeCode': lang, 'nativeLanguageName': native_name,
                                        'ready': True, 'files': result})
            print(args.platform, lang, len(result), flush=True)
    if len({tuple(item['path'] for item in lang['files']) for lang in config['languages']}) != 1:
        raise ValueError('unexpected locale-specific destination inventory')
    (target / 'PackageConfig.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=('macos', 'windows'))
    for arg in ('packages', 'stock', 'output', 'encoder', 'helper', 'delta-license'):
        parser.add_argument('--' + arg, type=lambda x: Path(x).resolve(), required=True)
    prepare(parser.parse_args())
