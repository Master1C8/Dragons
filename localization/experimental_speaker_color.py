"""Apply a source-pinned speaker-color hypothesis to a separate test asset."""
from copy import deepcopy
import os
from pathlib import Path

import UnityPy
import dialogue_locale as dl
import ui_locale as ui
import settings_locale as settings
import probe_font_roles as fonts

ASSET = 'level1'
NAME_ID = 3900
BODY_ID = 3899
WHITE = {'r': 1.0, 'g': 1.0, 'b': 1.0, 'a': 1.0}
BLACK = {'r': 0.0, 'g': 0.0, 'b': 0.0, 'a': 1.0}


def patch_into(source_data, target, requested):
    if UnityPy.__version__ != '1.25.4' or requested not in dl.site_locales():
        raise ValueError('speaker color experiment requires supported tools and locale')
    source_data, target = Path(source_data), Path(target)
    root, resolved = source_data.resolve(strict=True), target.resolve(strict=False)
    if target.is_symlink() or not target.is_file() or resolved == root or root in resolved.parents:
        raise ValueError('speaker color experiment requires a separate regular copied asset')
    original, _ = ui.scan(source_data, ASSET)
    expected = {(o.path_id, o.type.name): o.get_raw_data() for o in original.objects}
    if len(expected) != len(original.objects):
        raise ValueError('source object inventory changed')
    current = UnityPy.load(str(target))
    current.path = str(root)
    objects = {(o.path_id, o.type.name): o for o in current.objects}
    if len(objects) != len(current.objects) or objects.keys() != expected.keys():
        raise ValueError('speaker color target inventory changed')
    for identity, raw in expected.items():
        if objects[identity].get_raw_data() != raw:
            raise ValueError(f'unexpected speaker color target object: {identity}')
    generator = settings.make_generator(source_data)
    trees, nodes = {}, {}
    for path_id in (NAME_ID, BODY_ID):
        obj = objects[(path_id, 'MonoBehaviour')]
        tree = fonts.read_tree(obj, generator)
        script = obj.parse_monobehaviour_head().m_Script.deref().read()
        if (script.m_Namespace, script.m_ClassName) != ('TMPro', 'TextMeshProUGUI'):
            raise ValueError(f'unexpected speaker text component: {path_id}')
        schema = generator.cache.get(('aligned', script.m_AssemblyName, script.m_Namespace + '.' + script.m_ClassName))
        if obj.save_typetree(tree, nodes=schema) != expected[(path_id, 'MonoBehaviour')]:
            raise ValueError(f'speaker color source schema failed no-op: {path_id}')
        trees[path_id], nodes[path_id] = tree, schema
    if (trees[NAME_ID]['m_fontColor'] != WHITE or trees[NAME_ID]['m_fontColor32'] != {'rgba': 4294967295}
            or trees[BODY_ID]['m_fontColor'] != BLACK or trees[BODY_ID]['m_fontColor32'] != {'rgba': 4278190080}):
        raise ValueError('unexpected original dialogue colors')
    updated = deepcopy(trees[NAME_ID])
    updated['m_fontColor'] = deepcopy(BLACK)
    updated['m_fontColor32'] = {'rgba': 4278190080}
    obj = objects[(NAME_ID, 'MonoBehaviour')]
    raw = obj.save_typetree(updated, nodes=nodes[NAME_ID])
    obj.set_raw_data(raw)
    expected[(NAME_ID, 'MonoBehaviour')] = raw
    result = current.file.save()
    tmp = target.with_name(target.name + '.test-speaker-color.tmp')
    fd = os.open(tmp, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(result)
        reopened = UnityPy.load(str(tmp))
        reopened.path = str(root)
        after = {(o.path_id, o.type.name): o for o in reopened.objects}
        if len(after) != len(reopened.objects) or after.keys() != expected.keys():
            raise ValueError('speaker color saved inventory changed')
        for identity, raw in expected.items():
            if after[identity].get_raw_data() != raw:
                raise ValueError(f'speaker color saved object differs: {identity}')
        if after[(NAME_ID, 'MonoBehaviour')].read_typetree(nodes=nodes[NAME_ID], check_read=True) != updated:
            raise ValueError('speaker color saved fields differ')
        os.replace(tmp, target)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    return dl.sha(result)
