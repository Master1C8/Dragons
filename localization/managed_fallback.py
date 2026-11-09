"""Build the source-pinned Yarn missing-line DLL for a selected locale."""
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


def prepare(platform, source, locale_file, requested, tool):
    expected = SOURCES[platform]
    source = Path(source)
    if source.name != ASSEMBLY or source.is_symlink() or dl.sha(source.read_bytes()) != expected:
        raise ValueError(f'unsupported {platform} missing-line source assembly')
    locale, values = dl.read_locale(locale_file, list(FALLBACK), list(FALLBACK.values()),
                                    expected, yarn_semantics=False)
    if locale != requested:
        raise ValueError(f'managed locale {locale} does not match {requested}')
    replacement = values['yarn-missing-line']
    if any(c in replacement for c in '<>\r\n'):
        raise ValueError('missing-line replacement must be a single plain-text line')
    tool = Path(tool).resolve(strict=True)
    with tempfile.TemporaryDirectory(prefix='dragons-managed-fallback-') as folder:
        output = Path(folder) / ASSEMBLY
        run = subprocess.run(['dotnet', str(tool), str(source), str(output), replacement],
                             check=True, capture_output=True, text=True)
        data = output.read_bytes()
        report = json.loads(run.stdout, object_pairs_hook=dl.unique_object)
    if (report.get('sourceSha256') != expected or report.get('outputSha256') != dl.sha(data)
            or report.get('changedOffsets') != [0x18, 0x39] or report.get('verifiedMethodBodies', 0) <= 0):
        raise ValueError('unexpected managed fallback verification receipt')
    return data, report


def build(platform, source, locale_file, requested, tool, output):
    output = Path(output)
    original = Path(source).resolve(strict=True)
    if output.resolve() == original or original.parent in output.resolve().parents:
        raise ValueError('managed output must be separate from original assemblies')
    data, report = prepare(platform, source, locale_file, requested, tool)
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
    args = parser.parse_args()
    print(json.dumps(build(args.platform, args.source, args.locale_file, args.locale, args.tool, args.output)))
