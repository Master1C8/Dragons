#!/usr/bin/env python3
"""Rebuild a historical .NET probe output from pinned Git sources."""

import argparse
import hashlib
import os
from pathlib import Path
import re
import subprocess
import tempfile

from restore_probe_assets import read_receipt, relative_path


CHECKOUT = Path(__file__).resolve().parents[1]


def restore_source(row, build):
    revision = row['revision']
    if not re.fullmatch(r'[0-9a-f]{40}', revision):
        raise ValueError('Expected a full source revision')
    path = relative_path(row['path'])
    data = subprocess.check_output(
        ['git', '-C', str(CHECKOUT), 'show', f'{revision}:{path.as_posix()}'],
    )
    if hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError(f'Probe source fingerprint mismatch: {path}')
    destination = build / path.name
    with destination.open('xb') as out:
        out.write(data)
    return destination


def build_probe(row, build, historical_checkout):
    project = restore_source(row['project'], build)
    for source in row['sources']:
        restore_source(source, build)
    command = [
        'dotnet', 'build', str(project), '-c', row['configuration'], '--nologo',
        '--disable-build-servers', '-p:NuGetAudit=false', '--ignore-failed-sources',
        f"-p:SourceRevisionId={row['sourceRevisionId']}",
        f"-p:AssemblyName={row['assemblyName']}",
    ]
    if row.get('pathMap', True):
        original_object = historical_checkout / relative_path(row['objectPath'])
        original_project = historical_checkout / relative_path(row['project']['path']).parent
        command.append(f'-p:PathMap={build}/obj={original_object}%2C{build}={original_project}')
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
    args = parser.parse_args()
    receipt = read_receipt(args.receipt)
    if subprocess.check_output(['dotnet', '--version'], text=True).strip() != receipt['sdk']:
        raise ValueError('The recorded .NET SDK is required')
    row = receipt['outputs'][args.recorded_path]
    with tempfile.TemporaryDirectory(prefix='dragons-dotnet-restore-') as scratch:
        build = Path(scratch).resolve()
        build_probe(receipt['builds'][row['build']], build, Path(receipt['historicalCheckout']))
        data = verified_output(build, row)
    with args.output.open('xb') as out:
        out.write(data)
    args.output.chmod(int(row['mode'], 8))


if __name__ == '__main__':
    main()
