"""Prepare an ID-bound Yarn display locale and its companion as one unit."""
import json
from pathlib import Path
import subprocess
import tempfile
import unicodedata

import dialogue_locale as dl
import managed_fallback

COMPANION = 'Dragons.SpeakerPresentation.dll'
SOURCE_NAMES = {'speaker-ryan': 'Ryan', 'speaker-conrad': 'Conrad'}
ROOT = Path(__file__).resolve().parent.parent
PREFIX_MANIFEST = ROOT / 'localization/evidence/yarn-protected-partial-20261107.json'
ALEXANDER = 'line:4b36ea4e'


def read_locale(platform, locale_file, requested, expected, manifest):
    alexander_source, = [row['expected'][platform] for row in manifest['fullValueProtection']
                         if row['id'] == ALEXANDER]
    sources = SOURCE_NAMES | {ALEXANDER: alexander_source}
    locale, names = dl.read_locale(locale_file, list(sources), list(sources.values()),
                                   expected, yarn_semantics=False)
    alexander = names.pop(ALEXANDER, None)
    if alexander is not None and (not alexander.endswith(':') or not alexander[:-1].strip() or
                                  any(not c.isprintable() or c in '<>[]{}' for c in alexander)):
        raise ValueError('Alexander presentation requires plain text ending with a colon')
    if locale != requested or names.keys() != SOURCE_NAMES.keys():
        raise ValueError('speaker locale must match the request and contain both source names')
    # Match the game-side BMP letter and combining mark guard.
    if any(not name or len(name) > 40 or not name[0].isalpha() or
           not all(ord(c) <= 0xffff and (c.isalpha() or unicodedata.category(c) in {'Mn', 'Mc'})
                   for c in name) for name in names.values()):
        raise ValueError('speaker labels must start with a letter and contain at most 40 BMP letters or marks')
    return locale, names, alexander


def prepare(platform, source, locale_file, requested, tool, runtime, runtime_sha, *, fallback_locale=None):
    expected = managed_fallback.source_digest(platform, source)
    manifest = json.loads(PREFIX_MANIFEST.read_text(encoding='utf-8'))
    locale, names, alexander = read_locale(platform, locale_file, requested, expected, manifest)
    original_fallback = managed_fallback.FALLBACK['yarn-missing-line']
    fallback = (managed_fallback.read_replacement(fallback_locale, requested, expected)
                if fallback_locale is not None else original_fallback)
    runtime = Path(runtime)
    if runtime.name != COMPANION or runtime.is_symlink():
        raise ValueError('expected the speaker presentation runtime assembly')
    runtime_bytes = runtime.read_bytes()
    if dl.sha(runtime_bytes) != runtime_sha:
        raise ValueError('speaker presentation runtime fingerprint mismatch')
    with tempfile.TemporaryDirectory(prefix='dragons-speaker-locale-') as folder:
        stage = Path(folder)
        staged_runtime = stage / COMPANION
        staged_runtime.write_bytes(runtime_bytes)
        mapping = stage / 'mapping.json'
        mapping.write_text(json.dumps({'schema': 1, 'locale': locale,
                                       'map': {source_name: names[key] for key, source_name in SOURCE_NAMES.items()}}),
                           encoding='utf-8')
        output = stage / managed_fallback.ASSEMBLY
        command = ['dotnet', str(Path(tool).resolve(strict=True)), platform, str(Path(source).resolve()),
                   str(mapping), str(output), str(staged_runtime), runtime_sha, '--locale', locale, fallback]
        if alexander is not None:
            command.append(alexander)
        run = subprocess.run(command,
                             cwd=ROOT, check=True, capture_output=True, text=True)
        report = json.loads(run.stdout, object_pairs_hook=dl.unique_object)
        data = output.read_bytes()
    ids = sorted(row['id'] for row in manifest['prefixProtection'])
    if (report.get('testOnly') is not False or report.get('platform') != platform or report.get('locale') != locale
            or report.get('sourceSha256') != expected or report.get('outputSha256') != dl.sha(data)
            or report.get('inlineRuntimeSha256') != runtime_sha or report.get('inlineIds') != ids
            or report.get('mappedSpeakers') != sorted(SOURCE_NAMES.values())
            or len(report.get('changedDisplayCallSites', ())) != (10 if alexander is not None else 3)
            or report.get('alexanderBodyId') != (ALEXANDER if alexander is not None else None)
            or report.get('verifiedExistingMethodBodies') != 717
            or report.get('fallbackChanged') is not (fallback != original_fallback)):
        raise ValueError('unexpected speaker presentation verification receipt')
    return {managed_fallback.ASSEMBLY: data, COMPANION: runtime_bytes}, report
