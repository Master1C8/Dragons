"""Apply a source-pinned settings caption layout experiment to a test copy only."""
from copy import deepcopy
import os
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import ui_locale as ui

ASSET = 'sharedassets0.assets'
RECT = (478, 'RectTransform')


def patch_into(source_data, target, requested, *, prior_ui=None, prepared_settings=None):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    if not isinstance(requested, str) or requested not in dl.site_locales():
        raise ValueError('layout experiment requires a supported non-English locale')
    source_data, target = Path(source_data), Path(target)
    source_root = source_data.resolve(strict=True)
    target_path = target.resolve(strict=False)
    if target.is_symlink() or not target.is_file() or target_path == source_root or source_root in target_path.parents:
        raise ValueError('layout experiment requires a separate regular copied asset')
    source = source_data / ASSET
    if dl.sha(source.read_bytes()) != ui.ASSETS[ASSET]:
        raise ValueError('unsupported layout experiment source')
    original = UnityPy.load(str(source))
    before = {(o.path_id, o.type.name): o.get_raw_data() for o in original.objects}
    source_objects = {(o.path_id, o.type.name): o for o in original.objects}
    if len(before) != len(original.objects) or RECT not in before:
        raise ValueError('layout experiment source inventory changed')
    expected = dict(before)
    if prior_ui is not None:
        _, rows = ui.scan(source_data, ASSET)
        keys = list(rows)
        code, translations = dl.read_locale(prior_ui, keys, [rows[k][2] for k in keys],
                                             ui.ASSETS[ASSET], yarn_semantics=False)
        if code != requested:
            raise ValueError('layout experiment UI locale mismatch')
        for key, text in translations.items():
            obj, raw, _, end = rows[key]
            identity = (obj.path_id, obj.type.name)
            expected[identity] = raw[:88] + dl.write_string(text) + raw[end:]
    if prepared_settings is not None:
        _, settings_before, settings_changed, _, _, code, _, _ = prepared_settings
        if code != requested or settings_before != before:
            raise ValueError('layout experiment settings baseline mismatch')
        for path_id, raw in settings_changed.items():
            key = (path_id, 'MonoBehaviour')
            if key not in expected or expected[key] != before[key]:
                raise ValueError(f'layout experiment prior edits overlap: {key}')
            expected[key] = raw
    current = UnityPy.load(str(target))
    objects = {(o.path_id, o.type.name): o for o in current.objects}
    if len(objects) != len(current.objects) or objects.keys() != expected.keys():
        raise ValueError('layout experiment target inventory changed')
    for key, raw in expected.items():
        if objects[key].get_raw_data() != raw:
            raise ValueError(f'unexpected layout experiment target object: {key}')
    tree = source_objects[RECT].read_typetree(check_read=True)
    updated = deepcopy(tree)
    if updated['m_SizeDelta']['y'] != -13.0:
        raise ValueError('layout experiment source height changed')
    updated['m_SizeDelta']['y'] = -3.0
    raw = objects[RECT].save_typetree(updated)
    expected[RECT] = raw
    result = current.file.save()
    tmp = target.with_name(target.name + '.test-layout.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as f:
            f.write(result)
        reopened = UnityPy.load(str(tmp))
        after = {(o.path_id, o.type.name): o for o in reopened.objects}
        if len(after) != len(reopened.objects) or after.keys() != expected.keys():
            raise ValueError('layout experiment saved inventory changed')
        for key, expected_raw in expected.items():
            if after[key].get_raw_data() != expected_raw:
                raise ValueError(f'layout experiment saved object differs: {key}')
        if after[RECT].read_typetree(check_read=True) != updated:
            raise ValueError('layout experiment field read-back differs')
        os.replace(tmp, target)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return dl.sha(result)
