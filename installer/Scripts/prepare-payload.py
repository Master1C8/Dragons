#!/usr/bin/env python3
"""Produce exact binary deltas for verified Dragons packages."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
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
    if args.platform == 'macos':
        require(args.steam_path_fix is not None and args.steam_path_fix.is_file(),
                'macOS requires the compiled Steam path patcher')
    entries = json.loads(args.inventory.read_bytes())['locales']
    require(entries and len({row['siteLocale'] for row in entries}) == len(entries) and
            len({row['runtimeCode'] for row in entries}) == len(entries), 'Invalid installer locale inventory')
    for row in entries:
        locale = row['siteLocale']
        require(re.fullmatch(r'[a-zA-Z0-9-]{1,15}', locale), f'Invalid locale: {locale}')
        translation = ROOT.parent / 'localization' / locale / 'translation.json'
        require(sha(translation) == row['translationSha256'], f'{locale} translation changed since package verification')
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
        for entry in entries:
            lang, native_name = entry['siteLocale'], entry['nativeLanguageName']
            package = ROOT.parent / entry[args.platform]['path']
            expected = entry[args.platform]['sha256']
            licenses = {}
            if args.platform == 'macos':
                resources = package / 'Contents/Resources'
                manifest = resources / 'vn-localization-package.json'
                require(sha(manifest) == expected, f'{lang} macOS manifest checksum mismatch')
                seal = package / 'Contents/_CodeSignature/CodeResources'
                require(sha(seal) == entry['macos']['resourceSealSha256'], f'{lang} macOS resource seal mismatch')
                subprocess.run(['/usr/bin/codesign', '--verify', '--deep', '--strict', str(package)], check=True)
                meta = json.loads(manifest.read_bytes())
                current = files(resources / 'Data')
                require(set(originals) <= set(current), f'{lang} macOS package removed an original file')
                hashes = {name: sha(path) for name, path in current.items()}
                replacements = {name: path for name, path in current.items() if hashes[name] != original_hashes.get(name)}
                for name in ('NotoShaped-OFL.txt', 'NotoSansCJK-OFL.txt'):
                    if (resources / name).is_file():
                        licenses[name] = (resources / name).read_bytes()
            else:
                require(sha(package) == expected, f'{lang} Windows ZIP checksum mismatch')
                with ZipFile(package) as archive:
                    meta = json.loads(archive.read('manifest.json'))
                    replacements, hashes = {}, {}
                    for name, row in meta['files'].items():
                        require(not name.startswith('/') and '\\' not in name and ':' not in name and
                                all(part not in ('', '.', '..') for part in name.split('/')),
                                f'Unsafe package path: {name}')
                        require(row['sourceSha256'] == original_hashes.get(name), f'{name} source mismatch')
                        path = staging / name
                        path.parent.mkdir(parents=True, exist_ok=True)
                        path.write_bytes(archive.read('DragNWash_Data/' + name))
                        require(sha(path) == row['outputSha256'], f'{name} ZIP checksum mismatch')
                        replacements[name], hashes[name] = path, row['outputSha256']
                    for name in ('NotoShaped-OFL.txt', 'NotoSansCJK-OFL.txt'):
                        if name in archive.namelist():
                            licenses[name] = archive.read(name)
            require(meta['locale'] == lang and meta['platform'] == args.platform, f'{lang} package identity mismatch')
            require(meta['sourceGlobalManagersSha256'] == anchors['globalgamemanagers'], f'{lang} source manager mismatch')
            require(meta['sourceGlobalScriptsSha256'] == anchors['globalgamemanagers.assets'], f'{lang} source scripts mismatch')
            font = meta.get('cjkFallback') or (meta.get('complexText') or {}).get('fontFallback')
            if font:
                require(len(licenses) == 1 and
                        hashlib.sha256(next(iter(licenses.values()))).hexdigest() == font['licenseSha256'] and
                        hashes['sharedassets0.assets'] == font['assetSha256'], f'{lang} font receipt mismatch')
            if args.platform == 'macos':
                assembly = 'Managed/Assembly-CSharp.dll'
                patched = staging / f'{lang}-steam.dll'
                subprocess.run(['dotnet', str(args.steam_path_fix), str(replacements[assembly]), str(patched)], check=True)
                replacements[assembly] = patched
                hashes[assembly] = sha(patched)
            require(config['gameVersion'] in ('', meta['build']), f'{lang} game build mismatch')
            config['gameVersion'] = meta['build']
            for name, contents in licenses.items():
                license_dir = payload / 'Licenses' / lang
                license_dir.mkdir(parents=True, exist_ok=True)
                (license_dir / name).write_bytes(contents)
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
            config['languages'].append({'siteLocale': lang, 'runtimeCode': entry['runtimeCode'], 'nativeLanguageName': native_name,
                                        'ready': True, 'files': result})
            print(args.platform, lang, len(result), flush=True)
    (target / 'PackageConfig.json').write_text(json.dumps(config, ensure_ascii=False, indent=2) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=('macos', 'windows'))
    for arg in ('inventory', 'stock', 'output', 'encoder', 'helper', 'delta-license'):
        parser.add_argument('--' + arg, type=lambda x: Path(x).resolve(), required=True)
    parser.add_argument('--steam-path-fix', type=lambda x: Path(x).resolve())
    prepare(parser.parse_args())
