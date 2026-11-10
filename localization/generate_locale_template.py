#!/usr/bin/env python3
"""Generate an empty shared translation for both Drag'N Wash packages."""

import argparse
import json
from pathlib import Path

from assemble_source_inventory import INVENTORY_SHA, load_pinned
from package_inputs import YARN_SCOPE_SHA
import paired_locale


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--locale', required=True)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--yarn-scope', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    entries = load_pinned(args.inventory, INVENTORY_SHA)['entries']
    scope = load_pinned(args.yarn_scope, YARN_SCOPE_SHA)
    _, rows = paired_locale.catalog(entries, scope)
    doc = paired_locale.template(args.locale, YARN_SCOPE_SHA, rows)
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(doc, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(f'{len(rows)} translation IDs: {args.output}')


if __name__ == '__main__':
    main()
