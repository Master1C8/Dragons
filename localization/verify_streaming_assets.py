#!/usr/bin/env python3
"""Verify exact local StreamingAssets files against supported original builds."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import stat

import compare_yarn_versions as versions
import inventory_addressables as addressables

APV_MANIFEST_SHA256 = '7e82d379c31e6bdfa8d1b276eb2d46be64eb551be7ca4c2a481443c70cdaf56a'


def digest_file(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        while block := f.read(1024 * 1024):
            h.update(block)
    return h.hexdigest()


def scan(base):
    base = Path(base)
    if base.is_symlink() or not base.is_dir():
        raise ValueError('expected a real StreamingAssets directory')
    rows = {}
    for current, dirs, files in os.walk(base, followlinks=False):
        directory = Path(current)
        for name in dirs:
            path = directory / name
            if path.is_symlink() or not path.is_dir():
                raise ValueError(f'unsafe StreamingAssets directory: {path.relative_to(base)}')
        for name in files:
            path = directory / name
            if not stat.S_ISREG(path.lstat().st_mode):
                raise ValueError(f'unsafe StreamingAssets file: {path.relative_to(base)}')
            rel = path.relative_to(base).as_posix()
            if not rel.isascii() or any(c in rel for c in '\n\r|'):
                raise ValueError('unsupported streaming path')
            rows[rel] = {'size': path.stat().st_size, 'sha256': digest_file(path)}
    return dict(sorted(rows.items()))


def validate_source(rows, platform):
    expected_aa = {f'aa/{name}': digest for name, digest in
                   {**addressables.COMMON, **addressables.FILES[platform]}.items()}
    aa = {k: v for k, v in rows.items() if k.startswith('aa/')}
    if set(aa) != set(expected_aa) or any(aa[k]['sha256'] != v for k, v in expected_aa.items()):
        raise ValueError('unsupported Addressables inventory or bytes')
    prefix = 'APVStreamingAssets/'
    apv = {k[len(prefix):]: v for k, v in rows.items() if k.startswith(prefix)}
    if len(rows) != len(aa) + len(apv) or len(apv) != 24 or any(not k.endswith('.bytes') for k in apv):
        raise ValueError('unsupported StreamingAssets inventory')
    encoded = ''.join(f"{key}|{value['size']}|{value['sha256']}\n" for key, value in sorted(apv.items())).encode('ascii')
    if hashlib.sha256(encoded).hexdigest() != APV_MANIFEST_SHA256:
        raise ValueError('unsupported APV inventory or bytes')


def compare(before, after):
    if before.keys() != after.keys():
        raise ValueError('candidate StreamingAssets paths changed')
    for name in before:
        if before[name] != after[name]:
            raise ValueError(f'candidate StreamingAssets file changed: {name}')


def verify(platform, source_data, candidate_data):
    source_data = Path(source_data).resolve(strict=True)
    candidate_data = Path(candidate_data).resolve(strict=True)
    if source_data == candidate_data or source_data in candidate_data.parents or candidate_data in source_data.parents:
        raise ValueError('candidate and original data must be separate')
    versions.load(source_data, versions.BUILDS[platform])
    before = scan(source_data / 'StreamingAssets')
    validate_source(before, platform)
    after = scan(candidate_data / 'StreamingAssets')
    compare(before, after)
    return {'schema': 1, 'platform': platform, 'build': versions.BUILDS[platform]['version'],
            'verifiedFiles': len(before), 'verifiedBytes': sum(x['size'] for x in before.values()),
            'apvManifestSha256': APV_MANIFEST_SHA256,
            'limitations': 'Exact files only. APV and binary catalog semantics, runtime loads, external resources, other game assets, translation, and installation/restoration remain unverified.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=tuple(versions.BUILDS))
    p.add_argument('source_data', type=Path)
    p.add_argument('candidate_data', type=Path)
    args = p.parse_args()
    print(json.dumps(verify(args.platform, args.source_data, args.candidate_data), indent=2))


if __name__ == '__main__':
    main()
