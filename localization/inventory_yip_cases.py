#!/usr/bin/env python3
"""Find Yip-related source candidates and bind their complete Yarn nodes."""
import argparse
import json
from pathlib import Path
import re

import audit_yarn_targets as audit
import compare_yarn_versions as versions
import dialogue_locale as dl
import map_yarn_context as mapping

# Broad substring matching intentionally admits false positives for human review.
YIP = re.compile('yip', re.IGNORECASE)


def matching_spans(value):
    return [{'start': m.start(), 'end': m.end(), 'source': m.group()} for m in YIP.finditer(value)]


def build(mac, windows):
    context = mapping.build(mac, windows)
    sources, instructions = {}, {}
    for platform, root in [('macos', mac), ('windows', windows)]:
        keys, values, _, _, program_nodes, _ = versions.load(root, versions.BUILDS[platform])
        instructions[platform] = audit.instruction_records(program_nodes)
        if len(keys) != len(values) or len(set(keys)) != len(keys):
            raise ValueError(f'invalid source table: {platform}')
        sources[platform] = dict(zip(keys, values))
        if set(sources[platform]) != set(context['lineIds']):
            raise ValueError(f'source and context inventory differ: {platform}')
    matches, affected = {}, set()
    for key, binding in context['lineIds'].items():
        hit = {}
        for platform in ('macos', 'windows'):
            value = sources[platform][key]
            if dl.sha(value.encode('utf-8')) != binding['sourceSha256'][platform]:
                raise ValueError(f'source fingerprint mismatch: {platform} {key}')
            hit[platform] = matching_spans(value)
        if any(hit.values()):
            matches[key] = {'macos': hit['macos'], 'windows': hit['windows']}
            affected.update(binding[platform]['node'] for platform in hit if hit[platform])
    commands = {}
    for platform, node_map in instructions.items():
        commands[platform] = []
        for node, rows in node_map.items():
            for index, (op, operands) in enumerate(rows):
                if op != 4:
                    continue
                command = audit.one_string(operands, f'{node}#{index}')
                if YIP.search(command):
                    commands[platform].append({'node': node, 'instructionIndex': index, 'command': command})
                    affected.add(node)
    nodes = {}
    for node in sorted(affected):
        per_build = {}
        for platform in ('macos', 'windows'):
            entries = []
            for key, binding in context['lineIds'].items():
                location = binding[platform]
                if location['node'] != node:
                    continue
                entries.append({'id': key, 'instructionIndex': location['instructionIndex'],
                                'kind': location['kind'], 'sourceSha256': binding['sourceSha256'][platform]})
            entries.sort(key=lambda x: x['instructionIndex'])
            if len({x['instructionIndex'] for x in entries}) != len(entries):
                raise ValueError(f'ambiguous instruction location: {platform} {node}')
            per_build[platform] = {'nodeSha256': context['nodeSha256'][platform][node], 'lines': entries}
        nodes[node] = per_build
    return {'schema': 1, 'search': 'case-insensitive yip substring in both original Yarn tables and RunCommand values',
            'programSha256': context['programSha256'], 'matches': matches, 'commands': commands, 'nodes': nodes,
            'limitations': 'A substring search is a candidate finder, not exhaustive semantic discovery. Full nodes include all mapped line IDs but not complete control-flow, other scene dependencies, UI or audio. Actual reachability and locale decisions remain unreviewed.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--macos-data', required=True, type=Path)
    p.add_argument('--windows-data', required=True, type=Path)
    args = p.parse_args()
    print(json.dumps(build(args.macos_data, args.windows_data), ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
