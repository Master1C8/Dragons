#!/usr/bin/env python3
"""Build a source-pinned synthetic Windows new-slot UI asset for isolated tests."""
import argparse
import json
import os
from pathlib import Path

import UnityPy
import compare_slot_labels as slots
import dialogue_locale as dl

TEST_WORK = Path(__file__).resolve().parent / 'work'


def build(source_data, locale_file, output):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    source_data = Path(source_data).resolve(strict=True)
    output = Path(output)
    root = TEST_WORK.resolve(strict=True)
    if (output.is_symlink() or output.exists() or output.resolve(strict=False).parent != root
            or output.suffix != '.assets'):
        raise ValueError('output must be a fresh .assets file directly in the test work directory')
    if root == source_data or source_data in root.parents:
        raise ValueError('test output must not be inside the source game')
    info = slots.inspect(source_data, 'windows')
    keys = [info['labels'][f'NewSlotSelect/NewSlot{i}']['key'] for i in (1, 2, 3)]
    code, translations = dl.read_locale(locale_file, keys, ['New'] * 3, info['level0'], yarn_semantics=False)
    raw_asset = (source_data / 'level0').read_bytes()
    if dl.sha(raw_asset) != info['level0']:
        raise ValueError('Windows UI source changed during validation')
    env = UnityPy.load(raw_asset)
    objects = {(o.path_id, o.type.name): o for o in env.objects}
    if len(objects) != len(env.objects):
        raise ValueError('duplicate source object identity')
    baseline = {identity: obj.get_raw_data() for identity, obj in objects.items()}
    changed = {}
    for key, value in translations.items():
        path_id = int(key.split('#')[1])
        identity = (path_id, 'MonoBehaviour')
        if identity not in objects:
            raise ValueError('selected slot component is missing')
        raw = baseline[identity]
        source, end = dl.read_string(raw, 88)
        if source != 'New' or raw[88:end] != dl.write_string(source):
            raise ValueError('unexpected selected slot text encoding')
        changed[identity] = raw[:88] + dl.write_string(value) + raw[end:]
        objects[identity].set_raw_data(changed[identity])
    result = env.file.save()
    tmp = output.with_name(output.name + '.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(result)
        saved = UnityPy.load(str(tmp))
        after = {(o.path_id, o.type.name): o for o in saved.objects}
        if len(after) != len(saved.objects) or after.keys() != objects.keys():
            raise ValueError('saved Windows UI object inventory changed')
        for identity, obj in after.items():
            if obj.get_raw_data() != changed.get(identity, baseline[identity]):
                raise ValueError(f'saved Windows UI object differs: {identity}')
        os.link(tmp, output)
    finally:
        tmp.unlink(missing_ok=True)
    return {'testOnly': True, 'build': info['version'], 'locale': code,
            'sourceLevel0Sha256': info['level0'], 'changedSyntheticEntries': len(translations),
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
