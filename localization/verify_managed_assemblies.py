#!/usr/bin/env python3
"""Verify that a localization copy preserves the pinned Managed directory."""
import argparse
import hashlib
import json
from pathlib import Path
import stat


SOURCE_MANIFESTS = {
    'macos': 'b3186bc39207255e937f5856be09906dc1a428d83a964d5f368f30861e32603c',
    'windows': '9a14fcb1198ca8308ad90a38a1988367074c1f2ec8b6f0a8d97ef3d3c074fc56',
}


def scan(folder):
    folder = Path(folder)
    if folder.is_symlink() or not folder.is_dir():
        raise ValueError('expected a real Managed directory')
    assemblies = {}
    for path in sorted(folder.iterdir()):
        if (path.suffix != '.dll' or not stat.S_ISREG(path.lstat().st_mode)
                or not path.name.isascii() or any(c in path.name for c in '\n\r|')):
            raise ValueError(f'unexpected Managed entry: {path.name!r}')
        assemblies[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return assemblies


def validate_source(platform, assemblies):
    # Same ordinal filename and digest format as the managed consumer probes.
    manifest = ''.join(f'{name}|{digest}\n' for name, digest in sorted(assemblies.items()))
    digest = hashlib.sha256(manifest.encode('ascii')).hexdigest()
    if digest != SOURCE_MANIFESTS[platform]:
        raise ValueError(f'unsupported {platform} Managed inventory or bytes')
    return digest


def compare(before, after):
    if before.keys() != after.keys():
        raise ValueError('candidate Managed paths changed')
    for name in before:
        if before[name] != after[name]:
            raise ValueError(f'candidate managed assembly changed: {name}')


def verify(platform, source, candidate):
    source, candidate = Path(source), Path(candidate)
    if source.resolve(strict=True) == candidate.resolve(strict=True):
        raise ValueError('candidate and original Managed directories must be separate')
    before = scan(source)
    digest = validate_source(platform, before)
    compare(before, scan(candidate))
    return {'platform': platform, 'verifiedAssemblies': len(before), 'managedManifestSha256': digest}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=tuple(SOURCE_MANIFESTS))
    parser.add_argument('source_managed', type=Path)
    parser.add_argument('candidate_managed', type=Path)
    args = parser.parse_args()
    print(json.dumps(verify(args.platform, args.source_managed, args.candidate_managed), indent=2))


if __name__ == '__main__':
    main()
