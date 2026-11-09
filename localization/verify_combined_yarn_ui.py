#!/usr/bin/env python3
"""Compare a combined Yarn/UI asset to exact authorized source-bound values."""
import argparse
import json
from pathlib import Path

import UnityPy
import compare_yarn_versions as versions
import dialogue_locale as dl
import ui_locale as mac_ui
import ui_preservation
import windows_ui_locale as win_ui
import verify_yarn_preservation as common
import yarn_transition_repair as transitions


def verify(platform, source_data, candidate, requested, yarn_locale, ui_locale, *, restore_yarn_transitions=False):
    if UnityPy.__version__ != '1.25.4' or platform not in versions.BUILDS:
        raise ValueError('unsupported UnityPy version or platform')
    if yarn_locale is None and ui_locale is None:
        raise ValueError('at least one locale input is required')
    source_data, candidate = Path(source_data), Path(candidate)
    spec = versions.BUILDS[platform]
    keys, values, extras, program, _, _ = versions.load(source_data, spec)
    _, rows = (mac_ui if platform == 'macos' else win_ui).scan(source_data, 'sharedassets1.assets')
    before = common.objects(source_data / 'sharedassets1.assets')
    after = common.objects(candidate)
    if before.keys() != after.keys():
        raise ValueError('candidate Unity object inventory changed')
    expected = {}
    counts = {'yarn': 0, 'ui': 0}
    if restore_yarn_transitions:
        project = (spec['project'], 'MonoBehaviour')
        expected[project] = transitions.repair_project(platform, before[project])
    if yarn_locale is not None:
        code, translations = dl.read_locale(yarn_locale, keys, values, spec['localizationSha256'], yarn_semantics=True)
        if code != requested:
            raise ValueError('Yarn locale does not match requested locale')
        identity = (spec['localization'], 'MonoBehaviour')
        if identity not in before:
            raise ValueError('missing source Yarn object')
        ordered = [translations.get(k, v) for k, v in zip(keys, values)]
        raw = dl.encode(before[identity], keys, ordered, extras)
        if dl.parse(raw) != (keys, ordered, extras):
            raise ValueError('expected Yarn object failed round-trip')
        expected[identity] = raw
        counts['yarn'] = len(translations)
    if ui_locale is not None:
        ui_source = {key: row[2] for key, row in rows.items()}
        code, translations = ui_preservation.read_locale(
            platform, 'sharedassets1.assets', ui_locale, ui_source, spec['assetSha256'],
        )
        if code != requested:
            raise ValueError('UI locale does not match requested locale')
        for key, value in translations.items():
            obj, raw, _, end = rows[key]
            identity = (obj.path_id, obj.type.name)
            if identity not in before or before[identity] != raw or identity in expected:
                raise ValueError('UI source object missing, changed or overlaps Yarn')
            expected[identity] = raw[:88] + dl.write_string(value) + raw[end:]
        counts['ui'] = len(translations)
    for identity, raw in before.items():
        if after[identity] != expected.get(identity, raw):
            raise ValueError(f'candidate object differs from expected: {identity}')
    return {'schema': 1, 'platform': platform, 'build': spec['version'], 'locale': requested,
            'sourceAssetSha256': spec['assetSha256'], 'sourceProgramSha256': dl.sha(program),
            'yarnLocaleSha256': dl.sha(Path(yarn_locale).read_bytes()) if yarn_locale else None,
            'uiLocaleSha256': dl.sha(Path(ui_locale).read_bytes()) if ui_locale else None,
            'candidateAssetSha256': dl.sha(candidate.read_bytes()), 'expectedEntries': counts,
            'restoredYarnTransitions': len(transitions.CONTINUATIONS) if restore_yarn_transitions else 0,
            'verifiedObjects': len(before),
            'limitations': 'Exact object comparison for one Yarn/UI shared asset only. Not full source classification, semantic translation, runtime, installed-package, saves or restoration evidence.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=tuple(versions.BUILDS))
    parser.add_argument('source_data', type=Path)
    parser.add_argument('candidate_asset', type=Path)
    parser.add_argument('--locale', required=True)
    parser.add_argument('--yarn-locale', type=Path)
    parser.add_argument('--ui-locale', type=Path)
    parser.add_argument('--restore-yarn-transitions', action='store_true')
    args = parser.parse_args()
    print(json.dumps(verify(args.platform, args.source_data, args.candidate_asset, args.locale,
                            args.yarn_locale, args.ui_locale,
                            restore_yarn_transitions=args.restore_yarn_transitions), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
