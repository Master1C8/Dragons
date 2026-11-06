"""Read and patch version-pinned serialized TextMeshPro UI strings."""
from pathlib import Path
import json
import os

import dialogue_locale as dl

GLOBAL_HASH = '391640e8e7df097a0d377c7a16552975d4821688841ea3460ec99587f4061d9e'
ASSETS = {
    'level0': '4cabf35993c6726ab29e5cb24a1ce74a0fdf3d8061b0de3437415e56bcfa72f7',
    'level1': '6af2815f16cba00e935fe110023ec91421c7d4107c5d8d31f55b70039b17d618',
    'level2': '8a65d8f397e103abf65a6c9daba7668a4efe8c70fbe36f6b6eed676aaa99d808',
    'level3': '32805c0339b0b67b4cc1dd27f8e150419e3f7374132d630921700281a14b833e',
    'level4': '1aeac3e3368bbf5d3198dd6aee5f0969677a13b162158bb592655fdef03ef030',
    'level5': '3241f65111d9639a3e1434e4d5e7dd9aa946eac554675dc4627093638e0341c8',
    'level6': '975954bc0796ab7b60f06f075b3b0ad8ce367d07cede726d53847b61fbe112f6',
    'sharedassets0.assets': '40713b00ce12582eebc427c0104e59becf438eb15803725b2248be3471a96aeb',
    'sharedassets1.assets': dl.ASSET_HASH,
}


def scan(data_dir, name):
    import UnityPy
    if UnityPy.__version__ != '1.25.4' or name not in ASSETS:
        raise ValueError('unsupported UnityPy version or UI asset')
    data_dir = Path(data_dir)
    g = data_dir / 'globalgamemanagers.assets'
    p = data_dir / name
    if dl.sha(g.read_bytes()) != GLOBAL_HASH or dl.sha(p.read_bytes()) != ASSETS[name]:
        raise ValueError(f'unsupported or modified UI source: {name}')
    global_env = UnityPy.load(str(g))
    scripts = {o.path_id: o.read().m_ClassName for o in global_env.objects if o.type.name == 'MonoScript'}
    env = UnityPy.load(str(p))
    rows = {}
    for obj in env.objects:
        if obj.type.name != 'MonoBehaviour':
            continue
        data = obj.read(check_read=False)
        script = data.m_Script
        if script.m_FileID != 1 or scripts.get(script.m_PathID) != 'TextMeshProUGUI':
            continue
        raw = obj.get_raw_data()
        text, end = dl.read_string(raw, 88)
        if raw[88:end] != dl.write_string(text):
            raise ValueError(f'unexpected text encoding: {name}#{obj.path_id}')
        key = f'{name}#{obj.path_id}'
        if key in rows:
            raise ValueError(f'duplicate object: {key}')
        rows[key] = (obj, raw, text, end)
    return env, rows


def export(data_dir, name, path):
    _, rows = scan(data_dir, name)
    with Path(path).open('x', encoding='utf-8') as f:
        json.dump({'schema': 1, 'sourceObjectSha256': ASSETS[name],
                   'lines': {k: v[2] for k, v in rows.items()}}, f, ensure_ascii=False, indent=2)
        f.write('\n')
    print(f'Exported {len(rows)} TextMeshPro objects from {name}; dynamic placeholders and names require classification.')


def patch_into(source_dir, name, locale_file, requested, target, dialogue_object=None):
    import UnityPy
    original, rows = scan(source_dir, name)
    keys = list(rows)
    values = [rows[k][2] for k in keys]
    locale, translations = dl.read_locale(locale_file, keys, values, ASSETS[name])
    if locale != requested:
        raise ValueError(f'UI locale {locale} does not match {requested}')
    target = Path(target)
    env = UnityPy.load(str(target))
    baseline = {(o.path_id, o.type.name): o for o in original.objects}
    current = {(o.path_id, o.type.name): o for o in env.objects}
    if len(baseline) != len(original.objects) or len(current) != len(env.objects) or baseline.keys() != current.keys():
        raise ValueError(f'{name}: object inventory changed')
    for key, obj in baseline.items():
        expected = dialogue_object if name == 'sharedassets1.assets' and key[0] == dl.PATH_ID and dialogue_object is not None else obj.get_raw_data()
        if current[key].get_raw_data() != expected:
            raise ValueError(f'{name}: unexpected base object {key}')
    expected_objects = {}
    for key, value in translations.items():
        old, raw, _, end = rows[key]
        new = raw[:88] + dl.write_string(value) + raw[end:]
        current[(old.path_id, old.type.name)].set_raw_data(new)
        expected_objects[(old.path_id, old.type.name)] = new
    data = env.file.save()
    tmp = target.with_name(target.name + '.ui-localized.tmp')
    with tmp.open('xb') as f:
        f.write(data)
    check = UnityPy.load(str(tmp))
    after = {(o.path_id, o.type.name): o for o in check.objects}
    if len(after) != len(check.objects) or after.keys() != current.keys():
        raise ValueError(f'{name}: saved object inventory changed; temporary file retained')
    for key, obj in current.items():
        if after[key].get_raw_data() != expected_objects.get(key, obj.get_raw_data()):
            raise ValueError(f'{name}: saved object differs: {key}; temporary file retained')
    os.replace(tmp, target)
    return len(translations)


if __name__ == '__main__':
    import argparse
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('source_data', type=Path)
    p.add_argument('asset', choices=ASSETS)
    p.add_argument('--export', type=Path, required=True)
    args = p.parse_args()
    export(args.source_data, args.asset, args.export)
