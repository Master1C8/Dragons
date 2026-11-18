#!/usr/bin/env python3
"""Bind the complete current Windows and macOS locale outputs to installer preparation."""
import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLATFORMS = ('macos', 'windows')


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packages', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--platform', choices=PLATFORMS)
    args = parser.parse_args()
    platforms = (args.platform,) if args.platform else PLATFORMS
    roster = json.loads((ROOT / 'installer/App/LocalePackages.json').read_bytes())['locales']
    expected = {row['siteLocale'] for row in roster}
    for platform in platforms:
        actual = {path.parent.name for path in (args.packages / platform).glob('*/manifest.json')}
        if actual != expected:
            raise ValueError(f'{platform}: missing {sorted(expected - actual)}, extra {sorted(actual - expected)}')
    entries = []
    for row in roster:
        entry = {key: row[key] for key in ('siteLocale', 'runtimeCode', 'nativeLanguageName', 'translationSha256')}
        lang = entry['siteLocale']
        for platform in platforms:
            package = (args.packages / platform / lang).resolve(strict=True)
            manifest = package / 'manifest.json'
            result = json.loads(manifest.read_bytes())
            if (result['locale'], result['platform'], result['build']) != (lang, platform, '11/4/2026_317a98f0'):
                raise ValueError(f'{platform}/{lang}: unexpected manifest identity')
            entry[platform] = {'format': 'verified-replacements', 'path': str(package), 'sha256': sha(manifest)}
        entries.append(entry)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump({'locales': entries}, stream, ensure_ascii=False, indent=2)
        stream.write('\n')


if __name__ == '__main__':
    main()
