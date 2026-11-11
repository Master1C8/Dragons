#!/usr/bin/env python3
"""Restore a historical isolated PlayerSettings asset without opening the game."""

import argparse
import hashlib
from pathlib import Path
import re

import UnityPy

from compare_yarn_versions import BUILDS
import isolated_profile as profiles
from restore_probe_assets import read_receipt, sha256


def rebuild(row, stock):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    if sha256(stock) != row['baseSha256'] or row['baseSha256'] != BUILDS[row['platform']]['globalSha256']:
        raise ValueError('Stock PlayerSettings asset fingerprint mismatch')
    profile = row['profile']
    if profile['company'] != profiles.TEST_COMPANY or not re.fullmatch(r'Probe[A-Z0-9]{4}', profile['product']):
        raise ValueError('Unexpected isolated test identity')
    data, before, player = profiles._prepare_global(str(stock), profile)
    profiles._verify_global(data, profile, before, player)
    if hashlib.sha256(data).hexdigest() != row['sha256']:
        raise ValueError('Rebuilt PlayerSettings asset fingerprint mismatch')
    return data


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('recorded_path')
    parser.add_argument('--stock-global', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    row = next((r for r in read_receipt(args.receipt)['outputs']
                if r['path'] == args.recorded_path), None)
    if row is None:
        parser.error(f'Unknown isolated profile asset: {args.recorded_path}')
    data = rebuild(row, args.stock_global)
    with args.output.open('xb') as out:
        out.write(data)
    args.output.chmod(int(row['mode'], 8))
