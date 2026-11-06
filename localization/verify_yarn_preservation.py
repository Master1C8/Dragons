#!/usr/bin/env python3
"""Verify a Yarn-only asset against pinned source and exact authorized values."""
import argparse
import json
from pathlib import Path

import UnityPy
import compare_yarn_versions as versions
import dialogue_locale as dl


def compare_objects(before, after, localization_id, expected_raw):
    """Compare complete object inventories and bytes, with one exact replacement."""
    if before.keys() != after.keys():
        raise ValueError('candidate Unity object inventory changed')
    selected = [key for key in before if key[0] == localization_id]
    if len(selected) != 1 or selected[0][1] != 'MonoBehaviour':
        raise ValueError('unexpected localization object identity')
    for key in before:
        expected = expected_raw if key == selected[0] else before[key]
        if after[key] != expected:
            raise ValueError(f'candidate object differs from expected: {key}')
    return selected[0]


def objects(asset):
    env = UnityPy.load(str(asset))
    pairs = [((o.path_id, o.type.name), o.get_raw_data()) for o in env.objects]
    if len({key for key, _ in pairs}) != len(pairs):
        raise ValueError('duplicate Unity object identity')
    return dict(pairs)


def verify(platform, source_root, candidate, locale_file):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    spec = versions.BUILDS[platform]
    source_root, candidate = Path(source_root), Path(candidate)
    keys, values, extras, program, _, _ = versions.load(source_root, spec)
    locale, replacements = dl.read_locale(locale_file, keys, values, spec['localizationSha256'],
                                          yarn_semantics=True)
    before = objects(source_root / 'sharedassets1.assets')
    after = objects(candidate)
    identity = (spec['localization'], 'MonoBehaviour')
    original = before[identity]
    expected_values = [replacements.get(key, value) for key, value in zip(keys, values)]
    expected_raw = dl.encode(original, keys, expected_values, extras)
    if dl.parse(expected_raw) != (keys, expected_values, extras):
        raise ValueError('expected localization object failed round-trip')
    compare_objects(before, after, spec['localization'], expected_raw)
    return {'schema': 1, 'platform': platform, 'build': spec['version'], 'locale': locale,
            'sourceAssetSha256': spec['assetSha256'], 'sourceProjectObjectSha256': spec['projectSha256'],
            'sourceProgramSha256': dl.sha(program), 'localeFileSha256': dl.sha(Path(locale_file).read_bytes()),
            'candidateAssetSha256': dl.sha(candidate.read_bytes()), 'expectedEntries': len(replacements),
            'verifiedObjects': len(before),
            'limitations': 'Yarn-only asset comparison. Does not permit separately modified UI objects or prove complete source classification, translation quality, runtime rendering, save behavior, or installed package integrity.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('platform', choices=tuple(versions.BUILDS))
    p.add_argument('source_data', type=Path)
    p.add_argument('candidate_asset', type=Path)
    p.add_argument('locale_file', type=Path)
    args = p.parse_args()
    print(json.dumps(verify(args.platform, args.source_data, args.candidate_asset, args.locale_file), indent=2))


if __name__ == '__main__':
    main()
