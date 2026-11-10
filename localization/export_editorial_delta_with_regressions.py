#!/usr/bin/env python3
"""Export an editorial delta including stock dialogue markup and placeholders."""

import argparse
import json
from pathlib import Path

import assemble_source_inventory as inventory
import dialogue_locale as dialogue
import export_editorial_delta as legacy
import package_inputs
import paired_locale


def export(inventory_path, scope_path, scenes_path, before_path, after_path, recipe_path, locale):
    result = legacy.export(inventory_path, scope_path, scenes_path, before_path, after_path, recipe_path, locale)
    entries = inventory.load_pinned(inventory_path, inventory.INVENTORY_SHA)['entries']
    scope = inventory.load_pinned(scope_path, package_inputs.YARN_SCOPE_SHA)
    _, rows = paired_locale.catalog(entries, scope)
    source_tokens = {
        key for key, row in rows.items()
        if any(binding['file'] == 'dialogue.json' and dialogue.TOKENS.search(binding['source'])
               for binding in row['builds'].values())
    }
    regression = source_tokens | set(result['components']['regression'])
    closure = source_tokens | set(result['closureIds'])
    regression_sources = set(result['componentSourceIds']['regression'])
    regression_sources.update(source_id for key in source_tokens for binding in rows[key]['builds'].values()
                              for source_id in binding['sourceIds'])

    before = paired_locale.read(before_path, locale, package_inputs.YARN_SCOPE_SHA, rows)
    after = paired_locale.read(after_path, locale, package_inputs.YARN_SCOPE_SHA, rows)
    if (dialogue.sha(before_path.read_bytes()) != result['beforeSha256']
            or dialogue.sha(after_path.read_bytes()) != result['afterSha256']):
        raise ValueError('locale changed during extended delta export')

    result['components']['regression'] = [key for key in rows if key in regression]
    result['componentSourceIds']['regression'] = [row['id'] for row in entries if row['id'] in regression_sources]
    result['componentSha256']['regression'] = legacy.sha_json(result['components']['regression'])
    result['closureIds'] = [key for key in rows if key in closure]
    result['closureIdsSha256'] = legacy.sha_json(result['closureIds'])
    result['reviewRows'] = [{**rows[key], 'before': before[key], 'after': after[key]} for key in result['closureIds']]
    result['additionalRegressionSelector'] = {
        'id': 'paired-stock-dialogue-tokens-v1',
        'sourcePattern': dialogue.TOKENS.pattern,
        'ids': [key for key in rows if key in source_tokens],
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('inventory', 'yarn-scope', 'paired-scenes', 'before', 'after', 'recipe', 'output'):
        parser.add_argument(f'--{name}', type=Path, required=True)
    parser.add_argument('--locale', required=True)
    args = parser.parse_args()
    result = export(args.inventory, args.yarn_scope, args.paired_scenes, args.before, args.after,
                    args.recipe, args.locale)
    with args.output.open('x', encoding='utf-8') as output:
        json.dump(result, output, ensure_ascii=False, indent=2)
        output.write('\n')
    print(json.dumps({key: result[key] for key in ('locale', 'changedIdsSha256', 'closureIdsSha256')}))


if __name__ == '__main__':
    main()
