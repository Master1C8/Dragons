#!/usr/bin/env python3
"""Rebuild the conservative author-delta dependency recipe from its node map."""
import hashlib
import json
import sys
from pathlib import Path

if len(sys.argv) != 3:
    raise SystemExit('usage: make-reconciled-recipe.py NODE_MAP NEW_OUTPUT')
map_path, output = map(Path, sys.argv[1:])
if hashlib.sha256(map_path.read_bytes()).hexdigest() != 'fa05fdf1a278a9bd88e3c37d13fe974dff910e6a07bfdf252b365ed20873de42':
    raise SystemExit('node-map hash mismatch')
recipe = json.loads(Path('localization/pt-BR/receipts/author-audit-recipe.json').read_text())
mapping = json.loads(map_path.read_text())
for node in mapping['nodes'].values():
    related = set(node['sceneSourceIds'])
    for path in node['specialSceneIntersections']:
        related.update(mapping['specialFiles'][path]['ids'])
    for key in node['changedIds']:
        edit = recipe['edits'][key]
        edit['glossaryReferentSourceIds'] = sorted(node['sceneSourceIds'])
        edit['runtimeSourceIds'] = sorted(related)
        edit['reason'] += (' Conservative whole-node referent and consumer context; related special-scene IDs included for review, without asserting every node row is a direct referent.')
with output.open('x', encoding='utf-8') as out:
    json.dump(recipe, out, ensure_ascii=False, indent=2)
    out.write('\n')
