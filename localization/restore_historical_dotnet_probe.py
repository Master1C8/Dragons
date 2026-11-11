#!/usr/bin/env python3
"""Rebuild a historical .NET probe output from pinned sources."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile
from xml.sax.saxutils import escape

from restore_probe_assets import read_receipt, relative_path, sha256


CHECKOUT = Path(__file__).resolve().parents[1]


def restore_source(row, build, source_dir=None):
    path = relative_path(row['path'])
    git = ['git', '-C', str(CHECKOUT)]
    if row.get('archived'):
        if source_dir is None:
            raise ValueError('Pass --source-dir with the restored historical sources')
        data = (source_dir / path).read_bytes()
    elif row.get('retained'):
        source = CHECKOUT / path
        if source.resolve() != source:
            raise ValueError(f'Unexpected retained source path: {path}')
        data = source.read_bytes()
    elif 'blob' in row:
        blob = row['blob']
        if not re.fullmatch(r'[0-9a-f]{40}', blob):
            raise ValueError('Expected a full source blob ID')
        data = subprocess.check_output([*git, 'cat-file', 'blob', blob])
    else:
        revision = row['revision']
        if not re.fullmatch(r'[0-9a-f]{40}', revision):
            raise ValueError('Expected a full source revision')
        data = subprocess.check_output([*git, 'show', f'{revision}:{path.as_posix()}'])
    if hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError(f'Probe source fingerprint mismatch: {path}')
    destination = build / path.name
    with destination.open('xb') as out:
        out.write(data)
    return destination


def build_probe(row, build, historical_checkout, *, source_dir=None, game_managed=None, cecil=None):
    project = restore_source(row['project'], build, source_dir)
    for source in row['sources']:
        restore_source(source, build, source_dir)
    command = [
        'dotnet', 'build', str(project), '-c', row['configuration'], '--nologo',
        '--disable-build-servers', '-p:NuGetAudit=false', '--ignore-failed-sources',
        f"-p:SourceRevisionId={row['sourceRevisionId']}",
        f"-p:AssemblyName={row['assemblyName']}",
    ]
    if 'cecilSha256' in row:
        if cecil is None or sha256(cecil) != row['cecilSha256']:
            raise ValueError('Mono.Cecil reference fingerprint mismatch')
        if 'cecilHintPath' in row:
            original = row['cecilHintPath'].encode()
            data = project.read_bytes()
            if data.count(original) != 1:
                raise ValueError('Unexpected Mono.Cecil project hint path')
            project.write_bytes(data.replace(original, escape(str(cecil)).encode()))
        else:
            command.append(f'-p:CecilPath={cecil}')
    if 'gameManaged' in row:
        if game_managed is None:
            raise ValueError('Pass --game-managed for the recorded platform')
        for name, digest in row['gameManaged'].items():
            if sha256(game_managed / relative_path(name)) != digest:
                raise ValueError(f'Stock managed reference fingerprint mismatch: {name}')
        command.append(f'-p:GameManaged={game_managed}')
        command.append(f"-p:WindowsGameplayProbe={str(row['windowsGameplay']).lower()}")
    if row.get('pathMap', True):
        original_object = historical_checkout / relative_path(row['objectPath'])
        original_project = historical_checkout / relative_path(row['project']['path']).parent
        command.append(f'-p:PathMap={build}/obj={original_object}%2C{build}={original_project}')
    if 'embeddedSources' in row:
        command.extend(('-p:EnableSourceLink=false', '-p:EmbedUntrackedSources=false'))
        if row['embeddedSources'] == 'all':
            command.append('-p:EmbedAllSources=true')
        elif row['embeddedSources'] == 'generated':
            targets = build / 'EmbedHistoricalGeneratedSource.targets'
            targets.write_text(
                '<Project><Target Name="EmbedHistoricalGeneratedSource" BeforeTargets="CoreCompile">'
                '<ItemGroup><EmbeddedFiles Include="$(IntermediateOutputPath)*.cs" /></ItemGroup>'
                '</Target></Project>\n',
                encoding='utf-8',
            )
            command.append(f'-p:CustomAfterMicrosoftCommonTargets={targets}')
        else:
            raise ValueError('Unexpected embedded source selection')
    subprocess.run(command, env={**os.environ, 'DOTNET_CLI_UI_LANGUAGE': 'ru'}, check=True)


def verified_output(build, row):
    data = (build / relative_path(row['member'])).read_bytes()
    if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('Rebuilt probe output fingerprint mismatch')
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--source-dir', type=Path)
    parser.add_argument('--game-managed', type=Path)
    parser.add_argument('--cecil', type=Path)
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    if subprocess.check_output(['dotnet', '--version'], text=True).strip() != receipt['sdk']:
        raise ValueError('The recorded .NET SDK is required')
    row = receipt['outputs'][args.recorded_path]
    with tempfile.TemporaryDirectory(prefix='dragons-dotnet-restore-') as scratch:
        build = Path(scratch).resolve()
        build_probe(
            receipt['builds'][row['build']], build, Path(receipt['historicalCheckout']),
            source_dir=args.source_dir, game_managed=args.game_managed,
            cecil=args.cecil.resolve(strict=True) if args.cecil else None,
        )
        data = verified_output(build, row)
    with args.output.open('xb') as out:
        out.write(data)
    args.output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    main()
