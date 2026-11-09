#!/usr/bin/env python3
"""Bind the paired Yarn text scope to the original and repaired programs."""
import argparse
from collections import Counter
import json
from pathlib import Path
import struct

import UnityPy

import audit_yarn_targets as audit
import compare_yarn_versions as versions
import dialogue_locale as dl
import inventory_level_dialogues as levels
import managed_fallback
import map_yarn_context as context
import speaker_locale
import yarn_transition_repair as repair
from assemble_source_inventory import INVENTORY_SHA, YARN_PROTECTED_SHA, load_pinned
from speaker_locale import ALEXANDER, PREFIX_MANIFEST

def game_entries(entries, platform):
    references = [record for record in entries if record['family'] == 'game-component'
                  and record['role'] == 'preserve-exactly-yarn-node-reference'
                  and record['source'].get(platform)]
    counts = Counter(record['class'] for record in references)
    if len(references) != 123 or counts['LevelConfiguration'] != 93:
        raise ValueError(f'{platform}: source entry coverage differs')
    return {record['source'][platform] for record in references} | {'Start'}, dict(sorted(counts.items()))


def read_programs(platform, data, records, roots):
    spec = versions.BUILDS[platform]
    if dl.sha((data / 'Managed/YarnSpinner.dll').read_bytes()) != context.YARN_DLL_SHA:
        raise ValueError(f'{platform}: unsupported Yarn runtime schema')
    keys, values, _, original, nodes, _ = versions.load(data, spec)
    locations, _ = context.map_nodes(nodes, keys)
    if set(keys) != records.keys():
        raise ValueError(f'{platform}: Yarn scope does not match the source table')
    for key, value in zip(keys, values):
        record, location = records[key], locations[key]
        if (record['source'][platform] != value or record['location'][platform] != key or
                record['node'] != location['node'] or record['instructionIndex'] != location['instructionIndex'] or
                record['kind'] != location['kind'] or
                record['instruction'] != {field: location[field] for field in record['instruction']}):
            raise ValueError(f'{platform}: source scope binding differs for {key}')
    env = UnityPy.load(str(data / 'sharedassets1.assets'))
    project, = [obj for obj in env.objects if obj.path_id == spec['project']]
    raw = repair.repair_project(platform, project.get_raw_data())
    size = struct.unpack_from('<I', raw, repair.PROGRAM_SIZE_OFFSET)[0]
    rebuilt = raw[repair.PROGRAM_OFFSET:repair.PROGRAM_OFFSET + size]
    rebuilt_nodes, _ = versions.program_nodes(rebuilt)

    def reach(program, node_bytes):
        code = audit.instruction_records(node_bytes)
        if any(op in (17, 19) for instructions in code.values() for op, _ in instructions):
            raise ValueError(f'{platform}: dynamic transfer requires a different scope audit')
        reachable = levels.named_closure(roots, code)
        full = levels.named_closure(set(code), code)
        if set(full['lineIds']) != records.keys():
            raise ValueError(f'{platform}: full program text IDs differ from the source table')
        return set(reachable['lineIds']), {
            'programSha256': dl.sha(program),
            'allNodes': len(code),
            'reachableNodes': reachable['nodes'],
            'reachableTextCount': len(reachable['lineIds']),
            'reachableUnresolvedTargets': reachable['unresolved'],
            'allUnresolvedTargets': full['unresolved'],
        }

    before, original_report = reach(original, nodes)
    after, repaired_report = reach(rebuilt, rebuilt_nodes)
    return before, after, {'original': original_report, 'repaired': repaired_report}


def build(inventory, data_paths):
    shared = load_pinned(inventory, INVENTORY_SHA)
    entries = shared['entries']
    records = {r['id'].removeprefix('yarn:'): r for r in entries if r['family'] == 'yarn'}
    if len(records) != 1839:
        raise ValueError('unexpected Yarn source scope size')
    protected = load_pinned(PREFIX_MANIFEST, YARN_PROTECTED_SHA)
    exact_values = {r['id']: r['expected'] for r in protected['fullValueProtection']}
    prefixes = {r['id']: r['expectedPrefix'] for r in protected['prefixProtection']}
    if set(exact_values) - records.keys() or set(prefixes) - records.keys():
        raise ValueError('unbound exact Yarn sources')
    original, repaired, platforms = {}, {}, {}
    for platform in versions.BUILDS:
        roots, classes = game_entries(entries, platform)
        original[platform], repaired[platform], report = read_programs(platform, data_paths[platform], records, roots)
        platforms[platform] = {'rootClasses': classes, 'roots': sorted(roots), **report}

    rows = []
    for key, record in records.items():
        exact = exact_values.get(key)
        prefix = prefixes.get(key)
        if exact is not None and record['source'] != exact:
            raise ValueError(f'exact source binding differs for {key}')
        if key == ALEXANDER and (record.get('localeInput') != 'speaker-locale' or
                                 record.get('preserveExactValue') != exact):
            raise ValueError('Alexander source and presentation binding differs')
        if prefix is not None and (record['preserveExactPrefix'] != prefix or any(
                not record['source'][platform].startswith(value) for platform, value in prefix.items())):
            raise ValueError(f'exact prefix binding differs for {key}')
        channel = 'speaker-locale' if key == ALEXANDER else 'dialogue-locale' if exact is None else None
        row = {'id': key, 'node': record['node'], 'instructionIndex': record['instructionIndex'],
               'kind': record['kind'], 'sourceRole': record['role'], 'localeInput': channel,
               'originalNamedReachableOn': [p for p in platforms if key in original[p]],
               'repairedNamedReachableOn': [p for p in platforms if key in repaired[p]]}
        if exact is not None:
            row['preserveExactValue'] = exact
        if prefix is not None:
            row['preserveExactPrefix'] = prefix
        if record['source']['macos'] != record['source']['windows']:
            row['platformSourceDiffers'] = True
        rows.append(row)
    counts = Counter(row['localeInput'] or 'exact-only' for row in rows)
    return {'schema': 1, 'status': 'paired-yarn-scope', 'sharedInventorySha256': INVENTORY_SHA,
            'protectedYarnSha256': YARN_PROTECTED_SHA, 'builds': platforms,
            'localeInputCounts': dict(sorted(counts.items())),
            'scopePolicy': 'Keep all nontechnical Yarn IDs in translation scope regardless of named reachability.',
            'rows': rows}


def validate_complete(report, platform, data, requested, dialogue_file, speaker_file):
    """Check the full locale inputs structurally against the paired source scope."""
    inputs = {'dialogue': dialogue_file, 'speakers': speaker_file}
    digests = {label: dl.sha(path.read_bytes()) for label, path in inputs.items()}
    spec = versions.BUILDS[platform]
    keys, values, _, _, _, _ = versions.load(data, spec)
    locale, dialogue = dl.read_locale(dialogue_file, keys, values, spec['localizationSha256'])
    if locale != requested:
        raise ValueError(f'{platform}: dialogue locale does not match {requested}')
    expected = {row['id'] for row in report['rows'] if row['localeInput'] == 'dialogue-locale'}
    missing = expected - dialogue.keys()
    if missing:
        raise ValueError(f'{platform}: missing {len(missing)} dialogue IDs: {", ".join(sorted(missing)[:10])}')
    manifest = load_pinned(PREFIX_MANIFEST, YARN_PROTECTED_SHA)
    managed_sha = managed_fallback.source_digest(platform, data / 'Managed/YarnSpinner.Unity.dll')
    _, names, alexander = speaker_locale.read_locale(platform, speaker_file, requested, managed_sha, manifest)
    if alexander is None:
        raise ValueError(f'{platform}: missing {ALEXANDER} in the speaker locale')
    if {label: dl.sha(path.read_bytes()) for label, path in inputs.items()} != digests:
        raise ValueError(f'{platform}: locale inputs changed during validation')
    return {'dialogueIds': len(expected), 'specialDisplayIds': 1, 'speakerNames': len(names),
            'inputSha256': digests}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--inventory', type=Path, required=True)
    for platform in versions.BUILDS:
        parser.add_argument(f'--{platform}-data', type=Path, required=True)
        parser.add_argument(f'--{platform}-dialogue', type=Path)
        parser.add_argument(f'--{platform}-speakers', type=Path)
    parser.add_argument('--locale', help='validate complete inputs for both builds')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    paths = {platform: getattr(args, f'{platform}_data') for platform in versions.BUILDS}
    report = build(args.inventory, paths)
    files = {platform: (getattr(args, f'{platform}_dialogue'), getattr(args, f'{platform}_speakers'))
             for platform in versions.BUILDS}
    if args.locale is not None or any(file is not None for pair in files.values() for file in pair):
        if args.locale is None or any(file is None for pair in files.values() for file in pair):
            parser.error('complete coverage validation needs --locale and both locale files per build')
        report['localeCoverage'] = {p: validate_complete(report, p, paths[p], args.locale, *files[p])
                                    for p in versions.BUILDS}
    with args.output.open('x', encoding='utf-8') as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
    print(json.dumps({'sha256': dl.sha(args.output.read_bytes()), 'counts': report['localeInputCounts']}))


if __name__ == '__main__':
    main()
