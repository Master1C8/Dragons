#!/usr/bin/env python3
"""Prove the embedded source delimiters cannot run from a Yarn node entry."""
import argparse
import json
from pathlib import Path
import struct

import UnityPy
import audit_yarn_targets as audit
import compare_yarn_versions as versions
import dialogue_locale as dl
import map_yarn_context as context
import yarn_transition_repair as repair

# JumpTo, AddOption and JumpIfFalse carry a local target. PeekAndJump
# uses the selected AddOption target in the pinned option dispatch pattern.
LOCAL_TARGET_FIELD = {1: 1, 5: 2, 10: 1}
RETURN_OR_TRANSFER = {15, 16}
SUPPORTED = set(range(1, 17)) | {20}


def prove_block(host_rows, restored_rows, start, destination, text):
    first_marker = start - 3
    if first_marker < 1 or len(host_rows) <= start or host_rows[first_marker - 1][0] not in RETURN_OR_TRANSFER:
        raise ValueError(f'{destination}: no non-fallthrough instruction before markers')
    if restored_rows != host_rows[start:]:
        raise ValueError(f'{destination}: restored node differs from the suffix after markers')
    option_destinations = []
    for index, (opcode, operands) in enumerate(host_rows[:first_marker]):
        if opcode not in SUPPORTED:
            raise ValueError(f'{destination}: unsupported prefix instruction at {index}')
        if opcode in LOCAL_TARGET_FIELD:
            field = LOCAL_TARGET_FIELD[opcode]
            targets = [value for n, wire, value in operands if (n, wire) == (field, 0)]
            # A zero target is encoded as an absent protobuf scalar.
            target, = targets or [0]
            if not 0 <= target < first_marker:
                raise ValueError(f'{destination}: local target can enter the embedded block at {target}')
            if opcode == 5:
                option_destinations.append(target)
        elif opcode == 2:
            dispatch = host_rows[max(0, index - 3):index]
            if [op for op, _ in dispatch] != [6, 10, 11] or not option_destinations:
                raise ValueError(f'{destination}: unproven stack destination at {index}')
            # The selected destination is left on the stack only on the
            # fall-through side of the availability check. A separate jump
            # into that sequence would bypass the proof.
            for op, args in host_rows[:first_marker]:
                if op in LOCAL_TARGET_FIELD and any(
                    (n, wire) == (LOCAL_TARGET_FIELD[op], 0) and index - 2 <= value <= index
                    for n, wire, value in args
                ):
                    raise ValueError(f'{destination}: local target bypasses ShowOptions at {index}')
    ids = []
    for index, expected in enumerate(('==', f'title: {destination}', '---'), first_marker):
        opcode, operands = host_rows[index]
        if opcode != 3:
            raise ValueError(f'{destination}: expected marker RunLine at {index}')
        key = audit.one_string(operands, f'{destination}#{index}')
        if text[key] != expected:
            raise ValueError(f'{destination}: marker value differs at {index}')
        ids.append(key)
    if len(set(ids)) != len(ids):
        raise ValueError(f'{destination}: duplicate marker IDs')
    return {'ids': ids, 'firstInstruction': first_marker, 'precedingOpcode': host_rows[first_marker - 1][0],
            'suffixStart': start, 'suffixInstructions': len(restored_rows)}


def inspect(data, platform):
    if UnityPy.__version__ != '1.25.4':
        raise ValueError('UnityPy 1.25.4 is required')
    spec = versions.BUILDS[platform]
    if dl.sha((data / 'Managed/YarnSpinner.dll').read_bytes()) != context.YARN_DLL_SHA:
        raise ValueError('unsupported Yarn runtime')
    keys, values, _, original, source_nodes, _ = versions.load(data, spec)
    env = UnityPy.load(str(data / 'sharedassets1.assets'))
    project, = [obj for obj in env.objects if obj.path_id == spec['project']]
    raw = repair.repair_project(platform, project.get_raw_data())
    size = struct.unpack_from('<I', raw, repair.PROGRAM_SIZE_OFFSET)[0]
    rebuilt = raw[repair.PROGRAM_OFFSET:repair.PROGRAM_OFFSET + size]
    nodes, _ = versions.program_nodes(rebuilt)
    source_code = audit.instruction_records(source_nodes)
    repaired_code = audit.instruction_records(nodes)
    text = dict(zip(keys, values))
    blocks = {}
    for destination, (host, start) in sorted(repair.CONTINUATIONS.items()):
        if nodes[host] != source_nodes[host]:
            raise ValueError(f'{destination}: repaired host changed')
        block = prove_block(source_code[host], repaired_code[destination], start, destination, text)
        blocks[destination] = {'host': host, **block}
    marker_ids = {key for block in blocks.values() for key in block['ids']}
    locations = []
    for node, instructions in repaired_code.items():
        for index, (op, args) in enumerate(instructions):
            if op in (3, 5) and audit.one_string(args, f'{node}#{index}') in marker_ids:
                locations.append((node, index, op))
    expected = sorted((block['host'], index, 3) for block in blocks.values()
                      for index in range(block['firstInstruction'], block['suffixStart']))
    if len(marker_ids) != 15 or sorted(locations) != expected:
        raise ValueError('repaired program contains additional or duplicated marker occurrences')
    return blocks, {'originalProgramSha256': dl.sha(original), 'repairedProgramSha256': dl.sha(rebuilt)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for platform in versions.BUILDS:
        parser.add_argument(f'--{platform}-data', type=Path, required=True)
    args = parser.parse_args()
    mac, mac_hashes = inspect(args.macos_data, 'macos')
    win, win_hashes = inspect(args.windows_data, 'windows')
    if mac != win:
        raise ValueError('marker blocks differ across builds')
    print(json.dumps({'schema': 1, 'yarnRuntimeSha256': context.YARN_DLL_SHA,
                      'builds': {'macos': mac_hashes, 'windows': win_hashes},
                      'blocks': mac}, indent=2))


if __name__ == '__main__':
    main()
