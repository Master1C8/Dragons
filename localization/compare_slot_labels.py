#!/usr/bin/env python3
"""Compare the six serialized new-slot labels in the two pinned game builds."""
import argparse
import json
from pathlib import Path

import UnityPy
import compare_yarn_versions as versions
import dialogue_locale as dl
import ui_locale as ui

BUILD_INPUTS = {
    'macos': {'globalScripts': ui.GLOBAL_HASH, 'level0': ui.ASSETS['level0']},
    'windows': {'globalScripts': '910358d16b824bfd4b8398fea8c0295b5660471bb13a6708655096097bb0f018',
                'level0': '55a296caa23347190faa063efdaab4cf5a37e00bdbffa455729b4aa346cddae0'},
}


def inspect(data, build):
    data = Path(data)
    spec = BUILD_INPUTS[build]
    if dl.sha((data / 'globalgamemanagers').read_bytes()) != versions.BUILDS[build]['globalSha256']:
        raise ValueError(f'{build}: unsupported build identity')
    if dl.sha((data / 'globalgamemanagers.assets').read_bytes()) != spec['globalScripts']:
        raise ValueError(f'{build}: unsupported script inventory')
    if dl.sha((data / 'level0').read_bytes()) != spec['level0']:
        raise ValueError(f'{build}: unsupported level0')
    # Reuse the existing raw-string reader with explicit build-specific hashes;
    # restore its module constants even if the scan fails.
    old_global, old_level = ui.GLOBAL_HASH, ui.ASSETS['level0']
    try:
        ui.GLOBAL_HASH, ui.ASSETS['level0'] = spec['globalScripts'], spec['level0']
        env, rows = ui.scan(data, 'level0')
    finally:
        ui.GLOBAL_HASH, ui.ASSETS['level0'] = old_global, old_level
    objects = {o.path_id: o for o in env.objects}
    if len(objects) != len(env.objects):
        raise ValueError(f'{build}: duplicate object ID')
    transforms, by_game = {}, {}
    for obj in env.objects:
        if obj.type.name not in ('Transform', 'RectTransform'):
            continue
        t = obj.read(check_read=False)
        if t.m_GameObject.m_FileID != 0 or t.m_Father.m_FileID != 0:
            raise ValueError(f'{build}: external transform')
        if t.m_GameObject.m_PathID in by_game:
            raise ValueError(f'{build}: duplicate GameObject transform')
        transforms[obj.path_id] = (t.m_GameObject.m_PathID, t.m_Father.m_PathID)
        by_game[t.m_GameObject.m_PathID] = obj.path_id
    labels = {}
    for key, (obj, _, text, _) in rows.items():
        if text != 'New':
            continue
        owner = obj.parse_monobehaviour_head().m_GameObject
        if owner.m_FileID != 0 or owner.m_PathID not in by_game:
            raise ValueError(f'{build}: invalid label owner')
        current, seen, names = by_game[owner.m_PathID], set(), []
        while current:
            if current in seen or current not in transforms:
                raise ValueError(f'{build}: unresolved hierarchy')
            seen.add(current)
            game_id, current = transforms[current]
            game = objects[game_id]
            if game.type.name != 'GameObject':
                raise ValueError(f'{build}: invalid transform owner')
            names.append(game.read().m_Name)
        slots = {n for n in names if n in ('NewSlot1', 'NewSlot2', 'NewSlot3')}
        groups = {n for n in names if n in ('GreyedSlotSelect', 'NewSlotSelect')}
        if len(slots) != 1 or len(groups) != 1:
            raise ValueError(f'{build}: ambiguous New label ancestry')
        identity = f'{next(iter(groups))}/{next(iter(slots))}'
        if identity in labels:
            raise ValueError(f'{build}: duplicate slot label')
        labels[identity] = {'key': key, 'source': text}
    expected = {f'{group}/NewSlot{i}' for group in ('GreyedSlotSelect', 'NewSlotSelect') for i in range(1, 4)}
    if set(labels) != expected:
        raise ValueError(f'{build}: unexpected slot label inventory')
    return {'version': versions.BUILDS[build]['version'], **spec, 'labels': dict(sorted(labels.items()))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mac-data', type=Path, required=True)
    parser.add_argument('--windows-data', type=Path, required=True)
    args = parser.parse_args()
    result = {name: inspect(path.resolve(strict=True), name) for name, path in
              (('macos', args.mac_data), ('windows', args.windows_data))}
    result['scope'] = 'Six serialized New labels only. Matching hierarchy and source text do not prove runtime visibility, behavior, renderer equivalence or full game compatibility.'
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
