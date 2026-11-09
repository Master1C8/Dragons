#!/usr/bin/env python3
"""Audit serialized Unity text routes beside the existing Yarn and TMP paths."""
import argparse
import json
from pathlib import Path
import struct

import UnityPy
from UnityPy.helpers import TypeTreeHelper
from UnityPy.helpers.TypeTreeNode import TypeTreeNode
from UnityPy.streams import EndianBinaryReader, EndianBinaryWriter

import dialogue_locale as dl
import inventory_game_components as components
import inventory_text_assets as text_assets
import inventory_yarn_bindings as bindings
import settings_locale as settings

LOCALIZATION = 'UnityEngine.Localization'
DATABASE = 'LocalizedStringDatabase'
SETTINGS_NS = LOCALIZATION + '.Settings'
EVENT = (LOCALIZATION + '.Components', 'LocalizeStringEvent')
NATIVE_TYPES = {'TextMesh', 'UIDocument', 'VisualTreeAsset', 'StyleSheet', 'PanelSettings'}
DEBUG_TYPES = {'DebugUpdater', 'CameraSwitcher'}


def read_segment(raw, start, endian, schema):
    reader = EndianBinaryReader(raw, endian=endian)
    reader.Position = start
    tree = TypeTreeHelper.read_value(schema, reader, TypeTreeHelper.TypeTreeConfig(True, None))
    writer = EndianBinaryWriter(endian=endian)
    TypeTreeHelper.write_typetree(tree, schema, writer)
    if writer.bytes != raw[start:reader.Position]:
        raise ValueError('serialized localization segment did not round-trip')
    return tree


def string_database(obj, schema, generator):
    """Read the outer settings fields and only the bound database reference."""
    raw = obj.get_raw_data()
    rows = components.flat_nodes(schema)
    registry, = [i for i, r in enumerate(rows)
                 if r['m_Level'] == 1 and r['m_Type'] == 'ManagedReferencesRegistry']
    outer = read_segment(raw, 0, obj.reader.endian, TypeTreeNode.from_list(rows[:registry]))
    rid = outer['m_StringDatabase']['rid']
    if rid < 0:
        raise ValueError('missing serialized string database reference')
    header = struct.pack(f'{obj.reader.endian}q', rid) + b''.join(dl.write_string(value)
                for value in (DATABASE, SETTINGS_NS, 'Unity.Localization'))
    if raw.count(header) != 1:
        raise ValueError('serialized string database reference is missing or ambiguous')
    rows = components.flat_nodes(generator.get_nodes_up('Unity.Localization', SETTINGS_NS + '.' + DATABASE))
    top = [i for i, r in enumerate(rows) if r['m_Level'] == 1]
    if tuple(rows[i]['m_Name'] for i in top[:4]) != components.HEADER:
        raise ValueError('unexpected generated string database header')
    database = read_segment(raw, raw.index(header) + len(header), obj.reader.endian,
                            TypeTreeNode.from_list([rows[0], *rows[top[4]:]]))
    return {'projectLocale': outer['m_ProjectLocaleIdentifier']['m_Code'], 'database': database}


def inspect(root, platform):
    root = Path(root)
    pinned = text_assets.inspect(root, platform)
    generator = bindings.generator(root, platform)
    cache, selected, native, events, databases = {}, [], [], [], []
    resolved = 0
    for asset in sorted(pinned['assets']):
        env = UnityPy.load(str(root / asset))
        env.path = str(root)
        for obj in env.objects:
            if obj.type.name in NATIVE_TYPES:
                native.append({'asset': asset, 'id': obj.path_id, 'type': obj.type.name})
            if obj.type.name != 'MonoBehaviour':
                continue
            head = obj.parse_monobehaviour_head()
            script = head.m_Script.deref().read()
            resolved += 1
            ns, name = script.m_Namespace, script.m_ClassName
            if not (ns.startswith((LOCALIZATION, 'UnityEngine.UIElements')) or name in DEBUG_TYPES):
                continue
            row = {'asset': asset, 'id': obj.path_id, 'script': f'{ns}.{name}',
                   'rawSha256': dl.sha(obj.get_raw_data())}
            selected.append(row)
            if (ns, name) == EVENT:
                header, _, schema = settings.nodes_for(obj, generator, cache)
                tree = obj.read_typetree(nodes=schema, check_read=True)
                settings.check_header(tree, header, obj.path_id)
                if obj.save_typetree(tree, nodes=schema) != obj.get_raw_data():
                    raise ValueError('localized string event did not round-trip')
                ref = tree['m_StringReference']
                entry = ref['m_TableEntryReference']
                events.append({**row, 'enabled': bool(tree['m_Enabled']),
                               'table': ref['m_TableReference']['m_TableCollectionName'],
                               'entryId': entry['m_KeyId'], 'entryKey': entry['m_Key'],
                               'localVariables': len(ref['m_LocalVariables']),
                               'listeners': [{'target': c['m_Target'], 'method': c['m_MethodName']}
                                             for c in tree['m_UpdateString']['m_PersistentCalls']['m_Calls']]})
            elif (ns, name) == (SETTINGS_NS, 'LocalizationSettings'):
                _, _, schema = settings.nodes_for(obj, generator, cache)
                databases.append({**row, **string_database(obj, schema, generator)})
    return {'schema': 1, 'platform': platform, 'sourceAssets': pinned['assets'],
            'resolvedBehaviours': resolved, 'nativeTextOrUiObjects': native, 'selectedScripts': selected,
            'localizedStringEvents': events, 'localizationDatabases': databases,
            'limitations': 'Seventeen pinned top-level assets. Only selected LocalizationSettings segments are decoded.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=('macos', 'windows'))
    parser.add_argument('data_dir', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.data_dir, args.platform), indent=2))


if __name__ == '__main__':
    main()
