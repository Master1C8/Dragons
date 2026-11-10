"""Add a region-specific font to the pinned stock TMP fallback chain."""

from copy import copy
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
import os
import tempfile

from fontTools.ttLib import TTFont
import UnityPy

import dialogue_locale as dl
import inventory_yarn_bindings as bindings
import settings_locale as settings

ASSET = 'sharedassets0.assets'
LICENSE = 'NotoSansCJK-OFL.txt'
LICENSE_SHA = '6a73f9541c2de74158c0e7cf6b0a58ef774f5a780bf191f2d7ec9cc53efe2bf2'
FONTS = {
    'zh': '2c76254f6fc379fddfce0a7e84fb5385bb135d3e399294f6eeb6680d0365b74b',
    'zh-TW': 'dce08bd4fd91aa8aa76ed8fea4b694c2dfb8550f67871e326843212ddbeb88b4',
    'ja': '68a3fc98800b2a27b371f2fb79991daf3633bd89309d4ffaa6946fd587f375b5',
    'ko': '6bcb2a0703aa137e874fc2dffa85f6c21ba9a67fa329e81b8c801663af7e992a',
}
SOURCES = {
    'macos': (627, 626, '40713b00ce12582eebc427c0104e59becf438eb15803725b2248be3471a96aeb'),
    'windows': (622, 621, 'c8ce3f2e8f52bb5d191c773e6f5f2a4e23d6c6c6ee8893aa7ac7a784cb1c7ac3'),
}
ATLAS = 1024


@dataclass(frozen=True)
class Resource:
    font: bytes
    license: bytes
    locale: str


def prepare(locale, font, license):
    if locale not in FONTS:
        if font is not None or license is not None:
            raise ValueError(f'CJK font inputs are unsupported for {locale}')
        return None
    if font is None or license is None:
        raise ValueError(f'{locale} requires the pinned CJK font and OFL license')
    font_bytes, license_bytes = Path(font).read_bytes(), Path(license).read_bytes()
    if dl.sha(font_bytes) != FONTS[locale] or dl.sha(license_bytes) != LICENSE_SHA:
        raise ValueError(f'CJK font or license fingerprint mismatch for {locale}')
    return Resource(font_bytes, license_bytes, locale)


def ptr(path_id):
    return {'m_FileID': 0, 'm_PathID': path_id}


def local_id(ref):
    if ref['m_FileID'] != 0 or ref['m_PathID'] <= 0:
        raise ValueError('expected a local CJK fallback asset reference')
    return ref['m_PathID']


def add(platform, source_data, target, resource):
    """Edit only the staged asset and return the verified resource receipt."""
    target = Path(target)
    source_path = Path(source_data) / ASSET
    if target.is_symlink() or target.resolve(strict=True) == source_path.resolve(strict=True):
        raise ValueError('CJK fallback requires a separate staged asset')
    primary_id, fallback_id, expected = SOURCES[platform]
    source_bytes = source_path.read_bytes()
    if dl.sha(source_bytes) != expected:
        raise ValueError('CJK fallback source asset fingerprint mismatch')

    original = UnityPy.load(source_bytes).file.objects
    before_bytes = target.read_bytes()
    env = UnityPy.load(str(target))
    env.path = str(source_data)
    objects = env.file.objects
    before = {pid: dl.sha(obj.get_raw_data()) for pid, obj in objects.items()}
    if before.keys() != original.keys():
        raise ValueError('CJK fallback staged object inventory differs from stock')
    generator, cache = bindings.generator(source_data, platform), {}

    def read(pid, kind):
        obj = objects[pid]
        raw = obj.get_raw_data()
        if obj.type.name != kind or raw != original[pid].get_raw_data():
            raise ValueError(f'CJK fallback template differs from stock: {pid}')
        if kind == 'MonoBehaviour':
            head, _, nodes = settings.nodes_for(obj, generator, cache)
            tree = obj.read_typetree(nodes=nodes, check_read=True)
            settings.check_header(tree, head, pid)
        else:
            nodes = None
            tree = obj.read_typetree(check_read=True)
        if obj.save_typetree(tree, nodes=nodes) != raw:
            raise ValueError(f'CJK fallback template failed read-back: {pid}')
        return tree, nodes

    primary, primary_nodes = read(primary_id, 'MonoBehaviour')
    fallback, fallback_nodes = read(fallback_id, 'MonoBehaviour')
    if (primary['m_FallbackFontAssetTable'] != [ptr(fallback_id)]
            or fallback['m_AtlasPopulationMode'] != 1 or not fallback['m_IsMultiAtlasTexturesEnabled']
            or fallback['m_GlyphTable'] or fallback['m_CharacterTable']):
        raise ValueError('unexpected stock CJK fallback chain')
    font_id = local_id(fallback['m_SourceFontFile'])
    material_id = local_id(fallback['m_Material'])
    atlas, = fallback['m_AtlasTextures']
    texture_id = local_id(atlas)
    font, _ = read(font_id, 'Font')
    material, _ = read(material_id, 'Material')
    texture, _ = read(texture_id, 'Texture2D')
    props = material['m_SavedProperties']
    tex_name, tex_env = props['m_TexEnvs'][0]
    sizes = {'_TextureWidth', '_TextureHeight'}
    if (texture['m_Width'] != 1 or texture['m_Height'] != 1 or texture['m_StreamData']['size']
            or tex_name != '_MainTex' or tex_env['m_Texture'] != atlas
            or {name: value for name, value in props['m_Floats'] if name in sizes} != dict.fromkeys(sizes, 512.0)):
        raise ValueError('unexpected stock CJK atlas seed or material')

    with TTFont(BytesIO(resource.font)) as tt:
        family = tt['name'].getDebugName(1)
        units = tt['head'].unitsPerEm
        ascent, descent, gap = tt['hhea'].ascent, tt['hhea'].descent, tt['hhea'].lineGap

    new_font, new_material, new_texture, new_fallback = range(max(objects) + 1, max(objects) + 5)
    font.update(m_Name=family, m_FontData=resource.font, m_FontNames=[family])
    material['m_Name'] = family + ' SDF Material'
    tex_env['m_Texture'] = ptr(new_texture)
    props['m_Floats'] = [(name, float(ATLAS) if name in sizes else value) for name, value in props['m_Floats']]
    texture['m_Name'] = family + ' Dynamic Atlas'
    fallback.update(m_Name='Dragons Japanese SDF' if resource.locale == 'ja' else f'Dragons {resource.locale} SDF',
                    m_SourceFontFile=ptr(new_font), m_Material=ptr(new_material), m_AtlasTextures=[ptr(new_texture)],
                    m_AtlasWidth=ATLAS, m_AtlasHeight=ATLAS,
                    m_FreeGlyphRects=[{'m_X': 0, 'm_Y': 0, 'm_Width': ATLAS - 1, 'm_Height': ATLAS - 1}])
    size = fallback['m_FaceInfo']['m_PointSize']
    fallback['m_FaceInfo'].update(m_FamilyName=family, m_UnitsPerEM=units,
                                  m_LineHeight=(ascent - descent + gap) * size / units,
                                  m_AscentLine=ascent * size / units, m_DescentLine=descent * size / units)
    primary['m_FallbackFontAssetTable'].append(ptr(new_fallback))
    edits = {primary_id: objects[primary_id].save_typetree(primary, nodes=primary_nodes)}
    for old, new, tree, nodes in ((font_id, new_font, font, None), (material_id, new_material, material, None),
                                  (texture_id, new_texture, texture, None),
                                  (fallback_id, new_fallback, fallback, fallback_nodes)):
        obj = copy(objects[old])
        obj.path_id = new
        edits[new] = obj.save_typetree(tree, nodes=nodes)
        objects[new] = obj

    payload = env.file.save()
    checked = UnityPy.load(payload).file.objects
    if checked.keys() != before.keys() | edits.keys():
        raise ValueError('CJK fallback object inventory failed read-back')
    for pid, obj in checked.items():
        raw = obj.get_raw_data()
        if (pid in edits and raw != edits[pid]) or (pid not in edits and dl.sha(raw) != before[pid]):
            raise ValueError(f'CJK fallback object failed read-back: {pid}')

    with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as staged:
        temporary = Path(staged.name)
        try:
            staged.write(payload)
            staged.close()
            if target.read_bytes() != before_bytes:
                raise ValueError('CJK fallback staged asset changed during patching')
            os.chmod(temporary, target.stat().st_mode & 0o777)
            os.replace(temporary, target)
        finally:
            temporary.unlink(missing_ok=True)
    return {'locale': resource.locale, 'fontSha256': dl.sha(resource.font),
            'licenseSha256': dl.sha(resource.license), 'assetSha256': dl.sha(payload),
            'atlasSize': ATLAS, 'fallbackPathId': new_fallback}
