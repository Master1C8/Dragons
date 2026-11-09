#!/usr/bin/env python3
"""Inventory serialized strings and Yarn references in game-owned components."""
import argparse
import json
from pathlib import Path
from types import SimpleNamespace

import UnityPy
from UnityPy.helpers import TypeTreeHelper
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
from UnityPy.streams import EndianBinaryReader, EndianBinaryWriter

import compare_yarn_versions as yarn
import dialogue_locale as dl
import inventory_level_dialogues as levels
import inventory_text_assets as assets
import inventory_yarn_bindings as bindings
import settings_locale as settings

GAME_ASSEMBLY = 'Assembly-CSharp'
HEADER = ('m_GameObject', 'm_Enabled', 'm_Script', 'm_Name')
MESH_CLASSES = {
    ('', 'DragonBarkFeaturePlapResponse'), ('', 'DragonSkinnedMeshSocketAttachmentPrefab'),
    ('SkinnedMeshAttachmentSystem', 'SkinnedMeshClusterAttachments'),
    ('SkinnedMeshAttachmentSystem', 'SkinnedMeshSocketAttachments'),
}
MANAGED_CLASSES = {
    'DragonBark', 'DragonBarkDialogue', 'DragonBarkAnimationPlayVFX', 'DragonBarkAnimationToggleBool',
    'DragonBarkOviposition', 'DragonBarkSexAct', 'DragonBarkSexActWithCutscene',
    'GameEventResponseAnimatorBoolToggle', 'GameEventResponseAnimatorBoolToggleDuration',
    'GameEventResponseAnimatorTrigger', 'GameEventResponseDisableObjects', 'GameEventResponseEnableObjects',
    'GameEventResponseExplosionForce', 'GameEventResponseLookIKLookAt', 'GameEventResponsePlayEffect',
    'GameEventResponseSpawnObject', 'GameEventResponseSpawnObjectList', 'GameEventResponseSprayJukebox',
    'GameEventResponseUnityEvent',
}


def flat_nodes(schema):
    return [{key: value for key, value in row.items() if key != 'm_Children'} for row in schema.to_dict_list()]


def managed_schemas(generator):
    result = {}
    for name in sorted(MANAGED_CLASSES):
        rows = flat_nodes(generator.get_nodes_up(GAME_ASSEMBLY, name))
        top = [i for i, row in enumerate(rows) if row['m_Level'] == 1]
        if tuple(rows[i]['m_Name'] for i in top[:4]) != HEADER:
            raise ValueError(f'unexpected generated managed reference header: {name}')
        # Inline managed references are serializable classes, so their payload
        # starts after the synthetic MonoBehaviour header from the generator.
        payload = rows[top[4]:] if len(top) > 4 else []
        result[(name, '', GAME_ASSEMBLY)] = TypeTreeNode.from_list([rows[0], *payload])
    return result


def corrected_schema(schema, identity):
    if identity == ('', 'LevelConfiguration'):
        return levels.corrected_schema(schema)
    if identity not in MESH_CLASSES:
        return schema
    rows = flat_nodes(schema)
    indices = [i for i, row in enumerate(rows) if row['m_Name'] == 'bones']
    if len(indices) != 1:
        raise ValueError('expected one generated bone-name array')
    index = indices[0]
    if [(row['m_Type'], row['m_Name']) for row in rows[index:index + 4]] != [
            ('string', 'bones'), ('Array', 'Array'), ('int', 'size'), ('string', 'data')]:
        raise ValueError('unexpected generated bone-name schema')
    rows[index]['m_Type'] = 'vector'
    return TypeTreeNode.from_list(rows)


def read_component(obj, schema, managed):
    raw = obj.get_raw_data()
    if not any(node.m_Type == 'ManagedReferencesRegistry' for node in schema.m_Children):
        tree = obj.read_typetree(nodes=schema, check_read=True)
        return tree, obj.save_typetree(tree, nodes=schema) == raw
    # Supply missing reference type trees to the Python reader for this object
    # only. The original serialized file's reference table remains intact.
    refs = {}
    for item in obj.assets_file.ref_types or []:
        key = (getattr(item, 'm_ClassName', None), getattr(item, 'm_NameSpace', None),
               getattr(item, 'm_AssemblyName', None))
        if item.node is not None:
            refs[key] = item
    for key, node in managed.items():
        refs.setdefault(key, SimpleNamespace(m_ClassName=key[0], m_NameSpace=key[1], m_AssemblyName=key[2], node=node))
    context = SimpleNamespace(ref_types=list(refs.values()))
    reader = EndianBinaryReader(raw, endian=obj.reader.endian)
    tree = TypeTreeHelper.read_value(schema, reader, TypeTreeHelper.TypeTreeConfig(True, context))
    writer = EndianBinaryWriter(endian=obj.reader.endian)
    TypeTreeHelper.write_typetree(tree, schema, writer, assetsfile=context)
    return tree, reader.Position == len(raw) and writer.bytes == raw


def string_fields(value, path=()):
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from string_fields(item, (*path, key))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            yield from string_fields(item, (*path, index))


def is_dialogue_field(identity, path):
    namespace, name = identity
    if namespace:
        return False
    if name == 'LevelConfiguration':
        return path[0] in levels.DIALOG_FIELDS
    if name == 'YarnRunDialogOnEnable':
        return path == ('targetDialog',)
    if name in ('DragonPerformanceTriggerEggAnimation', 'DragonPerformanceTriggerDragonBark'):
        return path == ('dialogName',)
    return (name == 'DragonBarkFeaturePlapResponse' and len(path) == 5
            and path[:2] == ('references', 'RefIds') and path[3:] == ('data', 'dialogueTitle'))


def field_role(identity, path, text):
    if is_dialogue_field(identity, path):
        return 'preserve-exactly-yarn-node-reference'
    if not text:
        return 'preserve-exactly-empty-value'
    if identity in MESH_CLASSES and (path[0] == 'anchors' and
            (path[2:] == ('name',) or path[2:-1] == ('coordinates', 'bones'))):
        return 'preserve-exactly-rig-key'
    if path[:2] == ('references', 'RefIds') and path[-2] == 'type' and path[-1] in ('asm', 'class', 'ns'):
        return 'preserve-exactly-managed-type-reference'
    if 'm_PersistentCalls' in path and path[-1] in (
            'm_MethodName', 'm_TargetAssemblyTypeName', 'm_ObjectArgumentAssemblyTypeName'):
        return 'preserve-exactly-unity-event-binding'
    if identity == ('', 'ButtonDragFixed') and path[0] == 'm_AnimationTriggers':
        return 'preserve-exactly-animation-key'
    if identity == ('', 'LevelConfiguration') and path[0] in ('setFlags', 'endFlags', 'dragonSpawnFlag'):
        return 'preserve-exactly-state-key'
    if identity == ('', 'LevelConfiguration') and path == ('playerSpawnTransformName',):
        return 'preserve-exactly-object-lookup'
    return 'serialized-string-needs-consumer-review'


def inspect(root, platform):
    root = Path(root)
    pinned = assets.inspect(root, platform)
    _, _, _, program, nodes, _ = yarn.load(root, yarn.BUILDS[platform])
    generator = bindings.generator(root, platform)
    managed = managed_schemas(generator)
    cache, corrected, records, missing = {}, {}, [], []
    for name in sorted(pinned['assets']):
        env = UnityPy.load(str(root / name))
        env.path = str(root)
        for obj in env.objects:
            if obj.type.name != 'MonoBehaviour':
                continue
            head = obj.parse_monobehaviour_head()
            script = head.m_Script.deref().read()
            if script.m_AssemblyName.removesuffix('.dll') != GAME_ASSEMBLY:
                continue
            identity = (script.m_Namespace, script.m_ClassName)
            key = f'{name}#{obj.path_id}'
            try:
                header, _, schema = settings.nodes_for(obj, generator, cache)
                if identity not in corrected:
                    corrected[identity] = corrected_schema(schema, identity)
                raw = obj.get_raw_data()
                tree, identical = read_component(obj, corrected[identity], managed)
                settings.check_header(tree, header, obj.path_id)
                if not identical:
                    raise ValueError('component did not round-trip exactly')
            except (ValueError, EOFError, KeyError) as error:
                raise ValueError(f'{key} {identity}: {error}') from error
            fields = []
            for path, text in string_fields(tree):
                if path[0] in HEADER:
                    continue
                role = field_role(identity, path, text)
                if role == 'preserve-exactly-yarn-node-reference' and text and text not in nodes:
                    missing.append({'object': key, 'path': list(path), 'target': text})
                fields.append({'path': list(path), 'value': text, 'role': role})
            records.append({'asset': name, 'objectId': obj.path_id, 'namespace': identity[0], 'class': identity[1],
                            'gameObject': tree['m_GameObject'], 'rawSha256': dl.sha(raw), 'fields': fields})
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'assets': pinned['assets'], 'programSha256': dl.sha(program), 'objects': records,
            'missingDialogueTargets': missing,
            'limitations': 'Game-owned MonoBehaviour fields in seventeen pinned assets. Stored references do not prove runtime reachability. Other assemblies, runtime strings and excluded textures are outside this report.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=tuple(yarn.BUILDS))
    parser.add_argument('data', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.data, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
