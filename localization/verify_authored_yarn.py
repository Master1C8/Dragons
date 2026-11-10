#!/usr/bin/env python3
"""Check a paired draft's authored dialogue with the package Yarn reader."""

import argparse
import json
from pathlib import Path
from tempfile import TemporaryDirectory

from assemble_source_inventory import INVENTORY_SHA, load_pinned
import dialogue_locale as dialogue
from package_inputs import YARN_SCOPE_SHA
import paired_locale


def verify(locale_file, locale, inventory, scope, *, complete=False):
    entries = load_pinned(inventory, INVENTORY_SHA)['entries']
    yarn_scope = load_pinned(scope, YARN_SCOPE_SHA)
    builds, rows = paired_locale.catalog(entries, yarn_scope)
    payload = locale_file.read_bytes()
    counts = {}
    with TemporaryDirectory(prefix='dragons-authored-yarn-') as scratch:
        root = Path(scratch)
        snapshot = root / 'translation.json'
        snapshot.write_bytes(payload)
        translations = paired_locale.read(snapshot, locale, YARN_SCOPE_SHA, rows, complete=complete)
        for platform, build in builds.items():
            authored = {}
            for key, texts in translations.items():
                if platform in texts and rows[key]['builds'][platform]['file'] == 'dialogue.json':
                    authored[key] = rows[key]
            counts[platform] = len(authored)
            if not authored:
                continue
            target = root / platform
            paired_locale.materialize(target, platform, locale, build, authored, translations)
            bindings = [row['builds'][platform] for row in authored.values()]
            keys = [binding['key'] for binding in bindings]
            sources = [binding['source'] for binding in bindings]
            try:
                code, values = dialogue.read_locale(
                    target / 'dialogue.json', keys, sources, build['sourceFingerprints']['dialogue.json'],
                )
            except ValueError as error:
                raise ValueError(f'{platform}: {error}') from error
            expected = {binding['key']: translations[key][platform]
                        for key, binding in zip(authored, bindings)}
            if code != locale or values != expected:
                raise ValueError(f'{platform}: authored dialogue changed during read-back')
    return {'locale': locale, 'translationSha256': dialogue.sha(payload),
            'completeInputRequired': complete, 'checkedDialogueBindings': counts}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('locale_file', type=Path)
    parser.add_argument('--locale', required=True)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--yarn-scope', type=Path, required=True)
    parser.add_argument('--complete', action='store_true', help='also require every shared authoring ID')
    args = parser.parse_args()
    try:
        report = verify(args.locale_file, args.locale, args.inventory, args.yarn_scope, complete=args.complete)
    except ValueError as error:
        parser.exit(1, f'{error}\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
