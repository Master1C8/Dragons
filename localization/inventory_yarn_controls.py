#!/usr/bin/env python3
"""Inventory pinned Yarn substitution operands and visible numeric literals."""
import argparse
from collections import Counter
import json
from pathlib import Path

import dialogue_locale as dl
import map_yarn_context as mapping


def inspect(root, platform):
    keys, values, _, program, locations, hashes, _ = mapping.load_platform(root, platform)
    substitutions, numeric = Counter(), []
    for key, value in zip(keys, values):
        loc = locations[key]
        substitutions[loc['substitutionCount']] += 1
        digits = dl.visible_digit_runs(value)
        if digits:
            numeric.append({'lineId': key, 'node': loc['node'],
                            'instructionIndex': loc['instructionIndex'],
                            'sourceSha256': dl.sha(value.encode('utf-8')),
                            'digitRuns': dict(sorted(digits.items()))})
    return {'schema': 1, 'platform': platform, 'build': mapping.source.BUILDS[platform],
            'programSha256': dl.sha(program), 'nodeCount': len(hashes),
            'lineCount': len(keys), 'substitutionCounts': dict(sorted(substitutions.items())),
            'numericLiteralLines': numeric,
            'limitations': 'Static line/option substitution counts and ASCII digit runs outside recognized markup only. Does not interpret spelled-out numbers, runtime markup, commands, formatted values, dynamic source changes or other resource types.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=('macos', 'windows'))
    p.add_argument('data_dir', type=Path)
    args = p.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
