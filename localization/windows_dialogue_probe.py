#!/usr/bin/env python3
"""Build a source-pinned synthetic Windows Yarn asset for isolated tests only."""
import argparse
import json
import os
from pathlib import Path

import UnityPy
import compare_yarn_versions as versions
import dialogue_locale as dl

TEST_WORK = Path(__file__).resolve().parent / 'work'
SPEC = versions.BUILDS['windows']


def build(source_data, locale_file, output):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    source_data = Path(source_data).resolve(strict=True)
    output = Path(output)
    # This is not a Windows installer or release artifact. Require the owned
    # diagnostic directory and reject existing outputs and symbolic links.
    root = TEST_WORK.resolve(strict=True)
    if (output.is_symlink() or output.exists() or output.resolve(strict=False).parent != root
            or output.suffix != '.assets'):
        raise ValueError('output must be a fresh .assets file directly in the test work directory')
    if root == source_data or source_data in root.parents:
        raise ValueError('test output must not be inside the source game')
    keys, values, extras, _, _, _ = versions.load(source_data, SPEC)
    code, translations = dl.read_locale(locale_file, keys, values, SPEC['localizationSha256'],
                                         yarn_semantics=True)
    asset_bytes = (source_data / 'sharedassets1.assets').read_bytes()
    if dl.sha(asset_bytes) != SPEC['assetSha256']:
        raise ValueError('Windows source asset changed during validation')
    original = UnityPy.load(asset_bytes)
    objects = {(o.path_id, o.type.name): o for o in original.objects}
    if len(objects) != len(original.objects):
        raise ValueError('duplicate source object identity')
    identities = [key for key in objects if key[0] == SPEC['localization']]
    if len(identities) != 1:
        raise ValueError('unexpected Windows Yarn object identity')
    selected = objects[identities[0]]
    raw = selected.get_raw_data()
    if dl.sha(raw) != SPEC['localizationSha256'] or dl.parse(raw) != (keys, values, extras):
        raise ValueError('Windows Yarn source changed during validation')
    replacement = [translations.get(k, v) for k, v in zip(keys, values)]
    changed = dl.encode(raw, keys, replacement, extras)
    if dl.parse(changed) != (keys, replacement, extras):
        raise ValueError('Windows Yarn object failed structural read-back')
    baseline = {key: obj.get_raw_data() for key, obj in objects.items()}
    selected.set_raw_data(changed)
    result = original.file.save()
    tmp = output.with_name(output.name + '.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(result)
        saved = UnityPy.load(str(tmp))
        after = {(o.path_id, o.type.name): o for o in saved.objects}
        if len(after) != len(saved.objects) or after.keys() != objects.keys():
            raise ValueError('saved Windows asset object inventory changed')
        for identity, obj in after.items():
            expected = changed if identity == identities[0] else baseline[identity]
            if obj.get_raw_data() != expected:
                raise ValueError(f'saved Windows asset object differs: {identity}')
        if dl.parse(after[identities[0]].get_raw_data()) != (keys, replacement, extras):
            raise ValueError('saved Windows Yarn values failed read-back')
        # Hard-link publishes only if the output is still absent; it never
        # overwrites another test artifact after a concurrent creation.
        os.link(tmp, output)
    finally:
        tmp.unlink(missing_ok=True)
    return {'testOnly': True, 'build': SPEC['version'], 'locale': code,
            'sourceYarnSha256': SPEC['localizationSha256'], 'translatedSyntheticEntries': len(translations),
            'outputSha256': dl.sha(result), 'output': str(output)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source_data', type=Path)
    p.add_argument('--locale-file', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(build(args.source_data, args.locale_file, args.output), ensure_ascii=False))


if __name__ == '__main__':
    main()
