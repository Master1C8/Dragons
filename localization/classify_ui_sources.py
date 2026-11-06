#!/usr/bin/env python3
"""Provisional source-bound classification of serialized TMP UI fields."""
import argparse
from collections import Counter
import json
from pathlib import Path

import compare_ui_hierarchy as comparison
import map_ui_hierarchy as mapping


def classify(asset, path):
    """Classify known source hierarchies without inferring runtime visibility."""
    if asset == 'sharedassets0.assets':
        return 'settings-prefab-template-needs-consumer-review'
    if asset == 'sharedassets1.assets' and path == ['Option Item']:
        return 'dialogue-option-template-runtime-replaced'
    if 'GDG Dialogue System' in path:
        return 'dialogue-presenter-template-needs-consumer-review'
    if 'VersionDisplay' in path:
        return 'version-display-needs-consumer-review'
    if asset == 'level0' and 'SlotProgress' in path:
        if 'GreyedSlotSelect' in path or 'LoadSlotSelect' in path:
            return 'slot-progress-runtime-replaced'
        if 'NewSlotSelect' in path:
            return 'slot-new-label-serialized-candidate'
    if asset == 'level2' and 'CreditScroll' in path:
        if path[-1] == 'Name':
            return 'credit-name-preserve-candidate'
        return 'credit-description-translate-candidate'
    if asset == 'level2' and path[-1] == 'GameOver!':
        return 'ending-text-translate-candidate'
    if 'FPSCanvas' in path and 'ProgressBars' in path:
        return 'gameplay-indicator-translate-candidate'
    if any('CHEAT' in segment for segment in path):
        return 'cheat-menu-text-needs-visibility-review'
    if (asset in {f'level{i}' for i in range(1, 7)} and path[:3] in
            (['GameMenu', 'Menu_Main', 'Container'], ['GameMenuSexVariant', 'Menu_Main', 'Container']) and
            (path[3:] == ['Text (TMP)'] or
             (len(path) == 6 and path[3] == 'Panel' and path[4] in ('Options', 'Quit', 'Resume')
              and path[5] == 'Text (TMP)'))):
        return 'pause-menu-translate-candidate'
    if any(segment in ('Menu_Loading', 'Menu_DeleteSave', 'HoldToContinue') for segment in path):
        return 'menu-text-translate-candidate'
    raise ValueError(f'unclassified UI hierarchy: {asset}: {path}')


def build(mac, windows):
    a = mapping.inspect(mac, 'macos')
    b = mapping.inspect(windows, 'windows')
    entries = comparison.compare_records(a['objects'], b['objects'])
    counts = Counter()
    for record in entries:
        role = classify(record['asset'], record['hierarchy'])
        record['provisionalRole'] = role
        counts[role] += 1
    return {'schema': 1, 'builds': {
                'macos': {'globalScriptAssetSha256': a['globalScriptAssetSha256'], 'sourceAssets': a['sourceAssets']},
                'windows': {'globalScriptAssetSha256': b['globalScriptAssetSha256'], 'sourceAssets': b['sourceAssets']}},
            'pairedHierarchyCount': len(entries), 'roleCounts': dict(sorted(counts.items())), 'entries': entries,
            'limitations': 'Provisional classifications from serialized paths and pinned text hashes. They are not runtime visibility, final translation scope, editorial acceptance, exact-preservation contracts or proof of a complete UI inventory.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(build(args.macos_data, args.windows_data), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
