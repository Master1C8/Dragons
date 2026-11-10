#!/usr/bin/env python3
"""Decode the remaining pinned camera and render components and classify their strings."""
import argparse
from collections import Counter
import json
from pathlib import Path

import UnityPy
from UnityPy.helpers.TypeTreeNode import TypeTreeNode

import dialogue_locale as dl
import inventory_game_components as components
import inventory_text_assets as text_assets
import inventory_yarn_bindings as bindings
import settings_locale as settings


CAMERA = 'OrbitCameraController'
BAKING = 'ProbeVolumeBakingSet'
PIPELINE = 'UniversalRenderPipelineGlobalSettings'
CORE = 'Unity.RenderPipelines.Core.Runtime'
URP = 'Unity.RenderPipelines.Universal.Runtime'
LOCATIONS = {
    'macos': {'globalgamemanagers.assets': {2290: PIPELINE}, 'sharedassets0.assets': {607: BAKING},
              'sharedassets1.assets': {10686: BAKING, 10692: CAMERA, 10693: CAMERA, 10694: CAMERA}},
    'windows': {'globalgamemanagers.assets': {2289: PIPELINE}, 'sharedassets0.assets': {603: BAKING},
                'sharedassets1.assets': {10674: BAKING, 10680: CAMERA, 10681: CAMERA, 10682: CAMERA}},
}
SHARED_LOCATIONS = {'sharedassets3.assets': {123: BAKING, 125: CAMERA}, 'sharedassets4.assets': {68: BAKING},
                    'sharedassets5.assets': {143: BAKING}, 'sharedassets6.assets': {36: BAKING}}
SCRIPTS = {CAMERA: ('', 'com.naelstrof.orbitcam'), BAKING: ('UnityEngine.Rendering', CORE),
           PIPELINE: ('UnityEngine.Rendering.Universal', URP)}
MANAGED_TYPES = {
    ('GraphProcessor', 'com.alelievr.NodeGraphProcessor.Runtime'): (
        'ExposedParameter/Settings', 'FloatParameter', 'FloatParameter/FloatSettings',
        'ParameterNode', 'QuaternionParameter', 'Vector3Parameter',
    ),
    ('', 'com.naelstrof.orbitcam'): (
        'OrbitCameraDataConstant', 'OrbitCameraLerp', 'OrbitCameraOutput', 'OrbitCameraShake',
    ),
    ('', 'Assembly-CSharp'): (
        'OrbitCameraArbitraryCuts', 'WalkNWashCutsceneNode', 'WalkNWashOrbitCameraCollision',
        'WalkNWashOrbitCameraSettingsFloat',
    ),
    ('UnityEngine.Rendering', CORE): (
        'LightmapSamplingSettings', 'ProbeVolumeGlobalSettings', 'ProbeVolumeRuntimeResources',
        'RenderGraphGlobalSettings', 'ShaderStrippingSetting', 'VrsRenderPipelineRuntimeResources',
    ),
    ('UnityEngine.Rendering.RenderGraphModule.Util', CORE): ('RenderGraphUtilsResources',),
    ('UnityEngine.Rendering', URP): ('URPReflectionProbeSettings',),
    ('UnityEngine.Rendering.Universal', URP): (
        'RenderGraphSettings', 'ScreenSpaceAmbientOcclusionDynamicResources',
        'ScreenSpaceAmbientOcclusionPersistentResources', 'URPDefaultVolumeProfileSettings',
        'UniversalRenderPipelineDebugShaders',
        'UniversalRenderPipelineRuntimeShaders', 'UniversalRenderPipelineRuntimeTextures',
        'UniversalRenderPipelineRuntimeXRResources', 'UniversalRendererResources',
    ),
}
TYPE_ROLES = {('references', 'RefIds', '*', 'type', key): 'managed-type' for key in ('class', 'ns', 'asm')}
CAMERA_ROLES = {
    ('m_Name',): 'object-name',
    ('edges', '*', 'GUID'): 'graph-id',
    ('edges', '*', 'inputNodeGUID'): 'graph-id',
    ('edges', '*', 'outputNodeGUID'): 'graph-id',
    ('edges', '*', 'inputFieldName'): 'graph-port',
    ('edges', '*', 'outputFieldName'): 'graph-port',
    ('edges', '*', 'inputPortIdentifier'): 'graph-port',
    ('edges', '*', 'outputPortIdentifier'): 'graph-port',
    ('pinnedElements', '*', 'editorType', 'serializedType'): 'editor-type',
    ('references', 'RefIds', '*', 'data', 'GUID'): 'graph-id',
    ('references', 'RefIds', '*', 'data', 'guid'): 'graph-id',
    ('references', 'RefIds', '*', 'data', 'parameterGUID'): 'graph-id',
    ('references', 'RefIds', '*', 'data', 'name'): 'camera-parameter',
    **TYPE_ROLES,
}
BAKING_ROLES = {
    ('m_Name',): 'object-name',
    ('m_SceneGUIDs', '*'): 'scene-id',
    ('m_SerializedPerSceneCellList', '*', 'sceneGUID'): 'scene-id',
    ('m_LightingScenarios', '*'): 'lighting-scenario-key',
    ('scenarios', 'm_Keys', '*'): 'lighting-scenario-key',
    ('lightingScenario',): 'lighting-scenario-key',
    **{(*parent, field): role for parent in (
        ('cellSharedDataAsset',), ('cellBricksDataAsset',), ('cellSupportDataAsset',),
        *(('scenarios', 'm_Values', '*', key) for key in (
            'cellDataAsset', 'cellOptionalDataAsset', 'cellProbeOcclusionDataAsset')),
    ) for field, role in (('m_AssetGUID', 'resource-id'), ('m_StreamableAssetPath', 'resource-path'))},
}
PIPELINE_ROLES = {
    ('m_Name',): 'object-name',
    ('m_RenderingLayerNames', '*'): 'rendering-layer-name',
    **{(f'lightLayerName{i}',): 'rendering-layer-name' for i in range(8)},
    **TYPE_ROLES,
}
ROLES = {CAMERA: CAMERA_ROLES, BAKING: BAKING_ROLES, PIPELINE: PIPELINE_ROLES}


def correct_string_arrays(rows):
    # UnityPy reads a `string` node as a scalar before looking at its children.
    # The generator labels some string-array containers by their element type.
    for parent, array, size, element in zip(rows, rows[1:], rows[2:], rows[3:]):
        level = parent['m_Level']
        shape = [(node['m_Type'], node['m_Level'] - level) for node in (parent, array, size, element)]
        if shape == [('string', 0), ('Array', 1), ('int', 2), ('string', 2)]:
            parent['m_Type'] = 'vector'
    return TypeTreeNode.from_list(rows)


def reference_schemas(generator):
    result = {}
    for (namespace, assembly), classes in MANAGED_TYPES.items():
        for cls in classes:
            name = f'{namespace}.{cls}' if namespace else cls
            rows = components.flat_nodes(generator.get_nodes_up(assembly, name))
            top = [i for i, row in enumerate(rows) if row['m_Level'] == 1]
            if tuple(rows[i]['m_Name'] for i in top[:4]) != components.HEADER:
                raise ValueError(f'unexpected generated rendering reference header: {name}')
            payload = rows[top[4]:] if len(top) > 4 else []
            result[(cls, namespace, assembly)] = correct_string_arrays([rows[0], *payload])
    return result


def classify(tree, script):
    roles = ROLES[script]
    rows = []
    for path, value in components.string_fields(tree):
        if not value:
            continue
        key = tuple('*' if isinstance(part, int) else part for part in path)
        if key not in roles:
            raise ValueError(f'unclassified {script} string field: {path}')
        rows.append({'path': path, 'role': roles[key], 'value': value})
    return rows


def inspect(root, platform):
    root = Path(root)
    pinned = text_assets.inspect(root, platform)
    generator = bindings.generator(root, platform)
    references = reference_schemas(generator)
    records = []
    cache = {}
    locations = LOCATIONS[platform] | SHARED_LOCATIONS
    for asset, ids in locations.items():
        env = UnityPy.load(str(root / asset))
        env.path = str(root)
        for obj in env.objects:
            if obj.path_id not in ids:
                continue
            header, script, schema = settings.nodes_for(obj, generator, cache)
            expected = ids[obj.path_id]
            if script.m_ClassName != expected or (script.m_Namespace, script.m_AssemblyName) != SCRIPTS[expected]:
                raise ValueError(f'wrong render script at {asset}#{obj.path_id}')
            schema = correct_string_arrays(components.flat_nodes(schema))
            tree, identical = components.read_component(obj, schema, references)
            settings.check_header(tree, header, obj.path_id)
            if not identical:
                raise ValueError(f'render component did not round-trip: {asset}#{obj.path_id}')
            records.append({'asset': asset, 'pathId': obj.path_id, 'script': expected,
                            'rawSha256': dl.sha(obj.get_raw_data()), 'strings': classify(tree, expected)})
    if Counter((r['asset'], r['pathId']) for r in records) != Counter(
            (asset, path_id) for asset, ids in locations.items() for path_id in ids):
        raise ValueError('render component inventory differs')
    counts = Counter(row['role'] for record in records for row in record['strings'])
    return {'platform': platform, 'sourceAssets': pinned['assets'], 'objects': records,
            'nonemptyStringRoles': dict(sorted(counts.items()))}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=tuple(LOCATIONS))
    parser.add_argument('source_data', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.source_data, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
