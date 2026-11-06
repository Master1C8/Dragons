"""Apply a source-pinned font-size candidate to a test copy only."""
from copy import deepcopy
import os
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import ui_locale as ui

ASSET = 'level0'
TEXT_IDS = (5204, 5205, 5207)


def patch_into(source_data, target, requested, *, prior_ui=None):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    if not isinstance(requested, str) or requested not in dl.site_locales():
        raise ValueError('slot font experiment requires a supported non-English locale')
    source_data, target = Path(source_data), Path(target)
    source_root, target_path = source_data.resolve(strict=True), target.resolve(strict=False)
    if target.is_symlink() or not target.is_file() or target_path == source_root or source_root in target_path.parents:
        raise ValueError('slot font experiment requires a separate regular copied asset')
    original, rows = ui.scan(source_data, ASSET)
    before = {(o.path_id, o.type.name): o.get_raw_data() for o in original.objects}
    if len(before) != len(original.objects) or any((i, 'MonoBehaviour') not in before for i in TEXT_IDS):
        raise ValueError('slot font source inventory changed')
    expected = dict(before)
    if prior_ui is not None:
        keys = list(rows)
        code, translations = dl.read_locale(prior_ui, keys, [rows[k][2] for k in keys],
                                             ui.ASSETS[ASSET], yarn_semantics=False)
        if code != requested:
            raise ValueError('slot font experiment UI locale mismatch')
        for key, text in translations.items():
            obj, raw, _, end = rows[key]
            expected[(obj.path_id, obj.type.name)] = raw[:88] + dl.write_string(text) + raw[end:]
    current = UnityPy.load(str(target))
    current.path = str(source_data)
    objects = {(o.path_id, o.type.name): o for o in current.objects}
    if len(objects) != len(current.objects) or objects.keys() != expected.keys():
        raise ValueError('slot font target inventory changed')
    for key, raw in expected.items():
        if objects[key].get_raw_data() != raw:
            raise ValueError(f'unexpected slot font target object: {key}')
    import settings_locale as settings
    import probe_font_roles as fonts
    generator = settings.make_generator(source_data)
    changed, schemas = {}, {}
    for path_id in TEXT_IDS:
        obj = objects[(path_id, 'MonoBehaviour')]
        tree = fonts.read_tree(obj, generator)
        script = obj.parse_monobehaviour_head().m_Script.deref().read()
        if (script.m_Namespace, script.m_ClassName) != ('TMPro', 'TextMeshProUGUI'):
            raise ValueError(f'unexpected slot text component: {path_id}')
        fullname = script.m_Namespace + '.' + script.m_ClassName
        nodes = generator.cache.get(('aligned', script.m_AssemblyName, fullname))
        if obj.save_typetree(tree, nodes=nodes) != expected[(path_id, 'MonoBehaviour')]:
            raise ValueError(f'slot font schema failed no-op byte comparison: {path_id}')
        if tree['m_fontSize'] != 20.0 or tree['m_fontSizeBase'] != 20.0:
            raise ValueError(f'slot font source size changed: {path_id}')
        updated = deepcopy(tree)
        updated['m_fontSize'] = 18.0
        updated['m_fontSizeBase'] = 18.0
        raw = obj.save_typetree(updated, nodes=nodes)
        obj.set_raw_data(raw)
        expected[(path_id, 'MonoBehaviour')] = raw
        changed[path_id], schemas[path_id] = updated, nodes
    result = current.file.save()
    tmp = target.with_name(target.name + '.test-slot-font.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(result)
        reopened = UnityPy.load(str(tmp))
        reopened.path = str(source_data)
        after = {(o.path_id, o.type.name): o for o in reopened.objects}
        if len(after) != len(reopened.objects) or after.keys() != expected.keys():
            raise ValueError('slot font saved inventory changed')
        for key, raw in expected.items():
            if after[key].get_raw_data() != raw:
                raise ValueError(f'slot font saved object differs: {key}')
        for path_id, updated in changed.items():
            if after[(path_id, 'MonoBehaviour')].read_typetree(nodes=schemas[path_id], check_read=True) != updated:
                raise ValueError(f'slot font saved field differs: {path_id}')
        os.replace(tmp, target)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return dl.sha(result)
