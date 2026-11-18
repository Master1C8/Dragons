"""Install a locale fallback using the 317a98f TMP schema and empty atlas seed."""
from copy import copy
from io import BytesIO

from fontTools.ttLib import TTFont

from cjk_font_fallback import ATLAS, ptr
from current_build import digest


def add(asset, resource):
    seed = asset.build.asset('resources.assets')
    primary, primary_nodes = asset.build.schema(asset.objects[524])
    template, nodes = asset.build.schema(asset.objects[558])
    fallback, _ = asset.build.schema(seed.objects[1394])
    if (primary['m_Name'] != 'DragNWash SDF' or
            primary['m_FallbackFontAssetTable'] != [ptr(559)] or
            template.keys() != fallback.keys() or
            template['m_Name'] != 'NotoSans-Fallback' or
            fallback['m_Name'] != 'LiberationSans SDF - Fallback' or
            fallback['m_GlyphTable'] or fallback['m_CharacterTable'] or
            fallback['m_AtlasPopulationMode'] != 1 or not fallback['m_IsMultiAtlasTexturesEnabled']):
        raise ValueError('Unexpected 317a98f TMP font chain or dynamic seed')

    font_obj, material_obj, atlas_obj = (asset.objects[key] for key in (307, 27, 31))
    font = font_obj.read_typetree(check_read=True)
    material = material_obj.read_typetree(check_read=True)
    texture = seed.objects[20].read_typetree(check_read=True)
    props = material['m_SavedProperties']
    tex_env, = [value for key, value in props['m_TexEnvs'] if key == '_MainTex']
    if (tex_env['m_Texture'] != ptr(31) or
            texture['m_Width'] != 1 or texture['m_Height'] != 1 or
            texture['m_StreamData']['size'] or texture['m_TextureFormat'] != 1):
        raise ValueError('Unexpected 317a98f fallback material or atlas')
    with TTFont(BytesIO(resource.font)) as tt:
        name = tt['name'].getDebugName(1)
        units = tt['head'].unitsPerEm
        ascent, descent, gap = tt['hhea'].ascent, tt['hhea'].descent, tt['hhea'].lineGap

    font_id, material_id, texture_id, fallback_id = range(max(asset.objects) + 1, max(asset.objects) + 5)
    font.update(m_Name=name, m_FontNames=[name], m_FontData=resource.font)
    texture['m_Name'] = name + ' Dynamic Atlas'
    material['m_Name'] = name + ' SDF Material'
    tex_env['m_Texture'] = ptr(texture_id)
    sizes = {'_TextureWidth', '_TextureHeight'}
    props['m_Floats'] = [(key, float(ATLAS) if key in sizes else
                         float(fallback['m_AtlasPadding'] + 1) if key == '_GradientScale' else val)
                        for key, val in props['m_Floats']]
    fallback.update(m_GameObject=template['m_GameObject'], m_Script=template['m_Script'],
                    m_Name=f'Dragons {resource.locale} SDF', m_SourceFontFile=ptr(font_id),
                    m_Material=ptr(material_id), m_AtlasTextures=[ptr(texture_id)],
                    m_AtlasWidth=ATLAS, m_AtlasHeight=ATLAS,
                    m_FreeGlyphRects=[{'m_X': 0, 'm_Y': 0, 'm_Width': ATLAS - 1, 'm_Height': ATLAS - 1}])
    size = fallback['m_FaceInfo']['m_PointSize']
    fallback['m_FaceInfo'].update(m_FamilyName=name, m_UnitsPerEM=units,
                                  m_LineHeight=(ascent - descent + gap) * size / units,
                                  m_AscentLine=ascent * size / units, m_DescentLine=descent * size / units)
    # The locale font precedes the generic regional fallbacks.
    primary['m_FallbackFontAssetTable'].insert(0, ptr(fallback_id))
    asset.set(asset.objects[524], asset.objects[524].save_typetree(primary, nodes=primary_nodes))
    for original, ident, tree, schema in (
            (font_obj, font_id, font, None), (material_obj, material_id, material, None),
            (atlas_obj, texture_id, texture, None), (asset.objects[558], fallback_id, fallback, nodes)):
        obj = copy(original)
        obj.path_id = ident
        asset.objects[ident] = obj
        asset.env.file.objects[ident] = obj
        asset.set(obj, obj.save_typetree(tree, nodes=schema))
    return {'locale': resource.locale, 'fontSha256': digest(resource.font),
            'licenseSha256': digest(resource.license), 'atlasSize': ATLAS, 'fallbackPathId': fallback_id}
