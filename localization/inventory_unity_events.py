#!/usr/bin/env python3
"""Read persistent UnityEvent calls in the pinned serialized stock assets."""
import argparse
from collections import Counter
import json
from pathlib import Path
from types import SimpleNamespace

import UnityPy
from UnityPy.helpers import TypeTreeHelper
from UnityPy.streams import EndianBinaryReader, EndianBinaryWriter

import dialogue_locale as dialogue
import inventory_game_components as components
import inventory_render_components as render
import inventory_text_assets as text_assets
import inventory_yarn_bindings as bindings
import settings_locale as settings


LOCALIZATION = 'Unity.Localization'
SETTINGS = ('UnityEngine.Localization.Settings', 'LocalizationSettings')
LOCALIZATION_TYPES = {
    'Settings': ('CommandLineLocaleSelector', 'SystemLocaleSelector', 'SpecificLocaleSelector',
                 'LocalesProvider', 'LocalizedAssetDatabase', 'LocalizedStringDatabase'),
    'SmartFormat': ('SmartFormatter',),
    'SmartFormat.Core.Settings': ('SmartSettings',),
    'SmartFormat.Core.Parsing': ('Parser',),
    'SmartFormat.Extensions': ('ListFormatter', 'PersistentVariablesSource', 'DictionarySource',
                               'ValueTupleSource', 'XmlSource', 'ReflectionSource', 'DefaultSource',
                               'PluralLocalizationFormatter', 'ConditionalFormatter', 'TimeFormatter',
                               'XElementFormatter', 'ChooseFormatter', 'SubStringFormatter',
                               'IsMatchFormatter', 'DefaultFormatter'),
}
CALL_MODES = {
    'PlayAudio1': 1, 'OnContinueClicked': 1, 'OnAction': 1, 'OnIncrement': 6,
    'OnDecrement': 6, 'SelectPreviousItem': 1, 'SelectNextItem': 1,
    'ResetDebugManager': 1, 'OnScrollbarClicked': 1, 'set_text': 0, 'UpdateText': 0,
}


def localization_schemas(generator):
    result = {}
    for group, names in LOCALIZATION_TYPES.items():
        namespace = f'UnityEngine.Localization.{group}'
        for name in names:
            rows = components.flat_nodes(generator.get_nodes_up(LOCALIZATION, f'{namespace}.{name}'))
            top = [i for i, row in enumerate(rows) if row['m_Level'] == 1]
            if tuple(rows[i]['m_Name'] for i in top[:4]) != components.HEADER:
                raise ValueError(f'unexpected managed localization reference header: {name}')
            payload = rows[top[4]:] if len(top) > 4 else []
            result[name, namespace, LOCALIZATION] = render.correct_string_arrays([rows[0], *payload])
    return result


def read_localization_settings(obj, schema, managed):
    # UnityPy's writer expects data even for a null managed reference. Replay
    # the registry explicitly so that this exact null marker has no payload.
    refs = [SimpleNamespace(m_ClassName=k[0], m_NameSpace=k[1], m_AssemblyName=k[2], node=node)
            for k, node in managed.items()]
    context = SimpleNamespace(ref_types=refs)
    config = TypeTreeHelper.TypeTreeConfig(True, context)
    raw = obj.get_raw_data()
    reader = EndianBinaryReader(raw, endian=obj.reader.endian)
    writer = EndianBinaryWriter(endian=obj.reader.endian)
    tree = TypeTreeHelper.read_value(schema, reader, config)
    outer, registry = schema.m_Children[:-1], schema.m_Children[-1]
    version, vector = registry.m_Children
    array, = vector.m_Children
    count, entry = array.m_Children
    rid, identity, data = entry.m_Children
    if (registry.m_Type != 'ManagedReferencesRegistry'
            or (version.m_Name, vector.m_Name, count.m_Name) != ('version', 'RefIds', 'size')
            or (rid.m_Name, identity.m_Name, data.m_Name) != ('rid', 'type', 'data')
            or array.m_MetaFlag != 0x4000
            or any(node.m_MetaFlag for node in (registry, vector, entry))):
        raise ValueError('unexpected localization reference registry layout')
    for child in outer:
        TypeTreeHelper.write_value(tree[child.m_Name], child, writer, config)
    registry_values = tree[registry.m_Name]
    TypeTreeHelper.write_value(registry_values['version'], version, writer, config)
    entries = registry_values['RefIds']
    TypeTreeHelper.write_value(len(entries), count, writer, config)
    for item in entries:
        if item['type']['class']:
            TypeTreeHelper.write_value(item, entry, writer, config)
        else:
            if item != {'rid': -2, 'type': {'class': '', 'ns': '', 'asm': ''}}:
                raise ValueError('unexpected null localization reference')
            TypeTreeHelper.write_value(item['rid'], rid, writer, config)
            TypeTreeHelper.write_value(item['type'], identity, writer, config)
    writer.align_stream()
    return tree, reader.Position == len(raw) and writer.bytes == raw


def persistent_calls(tree, path=()):
    if isinstance(tree, dict):
        if 'm_PersistentCalls' in tree:
            for i, call in enumerate(tree['m_PersistentCalls']['m_Calls']):
                yield (*path, 'm_PersistentCalls', 'm_Calls', i), call
        for key, child in tree.items():
            yield from persistent_calls(child, (*path, key))
    elif isinstance(tree, list):
        for i, child in enumerate(tree):
            yield from persistent_calls(child, (*path, i))


def classify_call(call):
    name = call['m_MethodName']
    if (name not in CALL_MODES or CALL_MODES[name] != call['m_Mode']
            or call['m_Arguments']['m_StringArgument'] != ''):
        raise ValueError('unclassified persistent call or stored string argument')
    return 'preserve-exactly-unity-event-binding'


def classify_localization_strings(tree):
    roles = {
        'm_Name': 'object-name', 'm_Code': 'locale-identity',
        'm_CommandLineArgument': 'command-line-option', 'm_NoTranslationFoundMessage': 'missing-table-fallback',
        'm_AllowedSelectorChars': 'format-parser-syntax', 'm_Operators': 'format-parser-syntax',
        'm_DefaultTwoLetterISOLanguageName': 'locale-identity', 'm_NullDisplayString': 'substring-formatter-fallback',
        'class': 'managed-type', 'ns': 'managed-type', 'asm': 'managed-type',
    }
    rows = []
    for path, value in components.string_fields(tree):
        if not value:
            continue
        role = 'format-identifier' if path[-2:-1] == ('m_Names',) else roles.get(path[-1])
        if role is None:
            raise ValueError(f'unclassified localization settings string: {path}')
        rows.append({'path': path, 'value': value, 'role': f'preserve-exactly-{role}'})
    return rows


def inspect(root, platform):
    root = Path(root)
    pinned = text_assets.inspect(root, platform)
    generator = bindings.generator(root, platform)
    localized_types = localization_schemas(generator)
    managed = components.managed_schemas(generator) | render.reference_schemas(generator) | localized_types
    cache, schemas = {}, {}
    counts, calls, localization = Counter(), [], []
    for asset in sorted(pinned['assets']):
        env = UnityPy.load(str(root / asset))
        env.path = str(root)
        for obj in env.objects:
            if obj.type.name != 'MonoBehaviour':
                continue
            counts['monoBehaviours'] += 1
            header, script, schema = settings.nodes_for(obj, generator, cache)
            identity = script.m_Namespace, script.m_ClassName
            assembly = script.m_AssemblyName.removesuffix('.dll')
            key = assembly, *identity
            if key not in schemas:
                nodes = components.flat_nodes(schema)
                schemas[key] = None
                if any(node['m_Name'] in ('m_PersistentCalls', 'references') for node in nodes):
                    schemas[key] = (components.corrected_schema(schema, identity) if assembly == components.GAME_ASSEMBLY
                                    else render.correct_string_arrays(nodes))
            schema = schemas[key]
            if schema is None:
                counts['schemasWithoutCallsOrReferences'] += 1
                continue
            if key == (LOCALIZATION, *SETTINGS):
                tree, identical = read_localization_settings(obj, schema, localized_types)
            else:
                tree, identical = components.read_component(obj, schema, managed)
            settings.check_header(tree, header, obj.path_id)
            if not identical:
                raise ValueError(f'{asset}#{obj.path_id}: event schema failed byte round trip')
            counts['decodedComponents'] += 1
            source = {'asset': asset, 'objectId': obj.path_id, 'script': key,
                      'rawSha256': dialogue.sha(obj.get_raw_data())}
            if key == (LOCALIZATION, *SETTINGS):
                localization.append({**source, 'strings': classify_localization_strings(tree)})
            calls.extend({**source, 'path': path, 'role': classify_call(call), 'call': call}
                         for path, call in persistent_calls(tree))
    if len(localization) != 1:
        raise ValueError('unexpected localization settings inventory')
    return {'schema': 1, 'platform': platform, 'buildVersion': pinned['buildVersion'],
            'assets': pinned['assets'], 'coverage': dict(counts), 'calls': calls,
            'localizationSettings': localization[0]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=('macos', 'windows'))
    parser.add_argument('data', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.data, args.platform), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
