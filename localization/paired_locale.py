"""Bind a shared translation to the source-pinned inputs of both packages."""

import json

from assemble_source_inventory import INVENTORY_SHA
import compare_yarn_versions as versions
import dialogue_locale as dl
import inventory_non_yarn_scope as non_yarn
import managed_fallback
import map_ui_hierarchy
import settings_locale
import speaker_locale
import ui_locale


def catalog(entries, scope):
    if scope['sharedInventorySha256'] != INVENTORY_SHA:
        raise ValueError('Yarn scope does not match the shared inventory')
    yarn = {row['id']: row['localeInput'] for row in scope['rows']}
    rows, builds = {}, {}

    for platform, spec in versions.BUILDS.items():
        hashes = ui_locale.ASSETS if platform == 'macos' else map_ui_hierarchy.WINDOWS_ASSETS
        managed = managed_fallback.SOURCES[platform]
        files = {
            'dialogue.json': spec['localizationSha256'],
            'speakers.json': managed,
            'settings.json': hashes[settings_locale.ASSET],
            'slot-new.json': managed_fallback.SLOT_SOURCES[platform],
            'missing-line.json': managed,
        }
        destinations = set()

        def add(row_id, group, filename, key, text, source_ids, **context):
            destination = (filename, key)
            if filename not in files or destination in destinations:
                raise ValueError(f'{platform}: invalid or repeated input destination {destination}')
            destinations.add(destination)
            row = rows.setdefault(row_id, {'id': row_id, 'group': group, **context, 'builds': {}})
            row['builds'][platform] = {
                'file': filename, 'key': key, 'source': text, 'sourceIds': source_ids,
            }

        for row in entries:
            row_id = row['id']
            family = row['family']
            if family == 'yarn':
                key = row_id.removeprefix('yarn:')
                kind = yarn[key]
                if kind in ('dialogue-locale', 'speaker-locale'):
                    filename = 'dialogue.json' if kind == 'dialogue-locale' else 'speakers.json'
                    add(row_id, row['node'], filename, key, row['source'][platform], [row_id],
                        kind=row['kind'], instructionIndex=row['instructionIndex'],
                        preserveExactPrefix=row['preserveExactPrefix'])
            elif family in ('ui', 'settings'):
                key = row['location'][platform]
                if key is None:
                    continue
                if family == 'ui' and row['role'].endswith('-candidate'):
                    asset = row['asset']
                    filename = f'ui/{asset}.json'
                    files[filename] = hashes[asset]
                    add(row_id, f'UI/{asset}', filename, key, row['source'][platform], [row_id])
                elif family == 'settings' and row['role'][platform] == 'candidate':
                    add(row_id, 'Settings', 'settings.json', key, row['source'][platform], [row_id])

        for role, (filename, sources, _, _) in non_yarn.MANAGED_INPUTS.items():
            key, value = next(iter(sources.items()))
            source_ids = [row['id'] for row in entries if row['family'] == 'managed'
                          and row['role'] == role and platform in row['source']]
            add(f'display:{key}', 'Managed display', f'{filename}.json', key, value, source_ids)
        for key, value in speaker_locale.SOURCE_NAMES.items():
            source_ids = [row['id'] for row in entries if row['family'] == 'yarn' and
                          (row['preserveExactPrefix'] or {}).get(platform) == value + ': ']
            add(f'display:{key}', 'Speaker labels', 'speakers.json', key, value, source_ids)
        builds[platform] = {'inputCount': len(destinations), 'sourceFingerprints': files}
    return builds, rows


def read(path, locale, scope_sha, rows, *, complete=True):
    doc = json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=dl.unique_object)
    fields = {'schema', 'locale', 'sharedInventorySha256', 'yarnScopeSha256', 'lines'}
    if not isinstance(doc, dict) or doc.keys() != fields or type(doc['schema']) is not int or doc['schema'] != 1:
        raise ValueError('invalid shared locale schema')
    if doc['locale'] != locale or locale not in dl.site_locales():
        raise ValueError('shared locale code differs or is unsupported')
    if doc['sharedInventorySha256'] != INVENTORY_SHA or doc['yarnScopeSha256'] != scope_sha:
        raise ValueError('shared locale source fingerprints differ')
    lines = doc['lines']
    if not isinstance(lines, dict):
        raise ValueError('shared locale lines must be an object')
    if unknown := lines.keys() - rows.keys():
        raise ValueError(f'unknown shared locale ID: {min(unknown)}')
    if complete and (missing := rows.keys() - lines.keys()):
        raise ValueError(f'missing {len(missing)} shared locale IDs: {min(missing)}')
    return {key: resolve(key, rows[key]['builds'], value) for key, value in lines.items()}


def resolve(key, bindings, value):
    sources_differ = len({row['source'] for row in bindings.values()}) > 1
    if isinstance(value, str) and not sources_differ:
        texts = dict.fromkeys(bindings, value)
    elif isinstance(value, dict) and value.keys() == {'text', 'sharedAcrossSourceVariants'}:
        if not sources_differ or value['sharedAcrossSourceVariants'] is not True:
            raise ValueError(f'{key}: invalid confirmation for shared translation')
        texts = dict.fromkeys(bindings, value['text'])
    elif isinstance(value, dict) and value.keys() == {'platforms'}:
        texts = value['platforms']
        if not isinstance(texts, dict) or texts.keys() != bindings.keys():
            raise ValueError(f'{key}: platform translations must match source platforms')
    else:
        raise ValueError(f'{key}: expected text, platform translations, or explicit confirmation for differing sources')
    if any(not isinstance(text, str) or not text.strip() or '\0' in text for text in texts.values()):
        raise ValueError(f'{key}: translation must be nonempty text without NUL')
    return texts


def materialize(target, platform, locale, build, rows, translations):
    files = {name: {'schema': 1, 'locale': locale, 'sourceObjectSha256': digest, 'lines': {}}
             for name, digest in build['sourceFingerprints'].items()}
    for key, row in rows.items():
        if platform in row['builds']:
            binding = row['builds'][platform]
            files[binding['file']]['lines'][binding['key']] = {
                'source': binding['source'], 'text': translations[key][platform],
            }
    (target / 'ui').mkdir(parents=True)
    for name, doc in files.items():
        with (target / name).open('x', encoding='utf-8') as stream:
            json.dump(doc, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
