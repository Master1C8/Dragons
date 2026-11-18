"""Build source-pinned managed text replacements for a selected locale."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile

import dialogue_locale as dl

ASSEMBLY = 'YarnSpinner.Unity.dll'
SOURCES = {
    'macos': '54953f9c071aa3ca5b52eb8b12b8e0bedc73f7665a506c61acbef0c58ac340ef',
    'windows': '3d5def40f51540e79dbb6a897993fe006022cf1f16933a1b47a69334085ad89d',
}
FALLBACK = {'yarn-missing-line': '!! ERROR: Missing line!'}
SLOT_ASSEMBLY = 'Assembly-CSharp.dll'
SLOT_SOURCES = {
    'macos': 'f9c4ccc1b10f95270d6d0d63a5e150865a070eca353a6c16fa74930f993f7bcb',
    'windows': '8b1b439e62bff222fbce00869a3343422c77d08e384db7ed323b5e66f44195e2',
}
SLOT = {'slot-new': 'NEW'}
CURRENT_SLOT_SOURCES = {
    'macos': '8d626ba9a9c7829dd84a652a233fdfd22edbdc9ca824673193d9a15e82815377',
    'windows': '8610c137ec3d8d5993129a91c0c25a480d2c478b8fe5f3a2c7d1bd20686bb10e',
}
CURRENT_SLOT = {'slot-new': 'New'}


def source_digest(platform, source, *, slot_new=False, current_build=False):
    if current_build and not slot_new:
        raise ValueError('current-build mode applies only to the moved save-slot caption')
    assembly, sources = (SLOT_ASSEMBLY, SLOT_SOURCES) if slot_new else (ASSEMBLY, SOURCES)
    if current_build:
        sources = CURRENT_SLOT_SOURCES
    expected = sources[platform]
    source = Path(source)
    if source.name != assembly or source.is_symlink() or dl.sha(source.read_bytes()) != expected:
        label = 'new-slot' if slot_new else 'missing-line'
        raise ValueError(f'unsupported {platform} {label} source assembly')
    return expected


def read_replacement(locale_file, requested, expected, *, slot_new=False, current_build=False):
    lines = SLOT if slot_new else FALLBACK
    if current_build:
        if not slot_new:
            raise ValueError('current-build mode requires the save-slot caption')
        lines = CURRENT_SLOT
    locale, values = dl.read_locale(locale_file, list(lines), list(lines.values()),
                                    expected, yarn_semantics=False)
    if locale != requested:
        raise ValueError(f'managed locale {locale} does not match {requested}')
    replacement = values[next(iter(lines))]
    if any(c in replacement for c in '<>\r\n'):
        raise ValueError('managed replacement must be a single plain-text line')
    return replacement


def prepare(platform, source, locale_file, requested, tool, *, slot_new=False, current_build=False):
    expected = source_digest(platform, source, slot_new=slot_new, current_build=current_build)
    replacement = read_replacement(locale_file, requested, expected, slot_new=slot_new, current_build=current_build)
    assembly, offsets = (SLOT_ASSEMBLY, [0x85, 0x101, 0x17c]) if slot_new else (ASSEMBLY, [0x18, 0x39])
    if current_build:
        offsets = [0x52, 0xac, 0x105]
    tool = Path(tool).resolve(strict=True)
    with tempfile.TemporaryDirectory(prefix='dragons-managed-fallback-') as folder:
        output = Path(folder) / assembly
        run = subprocess.run(['dotnet', str(tool), str(source), str(output), replacement],
                             check=True, capture_output=True, text=True)
        data = output.read_bytes()
        report = json.loads(run.stdout, object_pairs_hook=dl.unique_object)
    if (report.get('sourceSha256') != expected or report.get('outputSha256') != dl.sha(data)
            or report.get('changedOffsets') != offsets or report.get('verifiedMethodBodies', 0) <= 0):
        raise ValueError('unexpected managed text verification receipt')
    return data, report


def build(platform, source, locale_file, requested, tool, output, *, slot_new=False):
    output = Path(output)
    original = Path(source).resolve(strict=True)
    if output.resolve() == original or original.parent in output.resolve().parents:
        raise ValueError('managed output must be separate from original assemblies')
    data, report = prepare(platform, source, locale_file, requested, tool, slot_new=slot_new)
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix='.managed-fallback-') as staging:
        staging.write(data)
        staging.flush()
        if dl.sha(Path(staging.name).read_bytes()) != report['outputSha256']:
            raise ValueError('staged managed fallback differs from verified output')
        os.link(staging.name, output)
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('platform', choices=tuple(SOURCES))
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--locale-file', type=Path, required=True)
    parser.add_argument('--locale', required=True)
    parser.add_argument('--tool', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--slot-new', action='store_true', help='patch NEW in Assembly-CSharp.dll')
    args = parser.parse_args()
    print(json.dumps(build(args.platform, args.source, args.locale_file, args.locale, args.tool, args.output,
                           slot_new=args.slot_new)))
