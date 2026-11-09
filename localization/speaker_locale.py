"""Prepare an ID-bound Yarn display locale and its companion as one unit."""
import json
from pathlib import Path
import subprocess
import tempfile

import dialogue_locale as dl
import managed_fallback

COMPANION = 'Dragons.SpeakerPresentation.dll'
SOURCE_NAMES = {'speaker-ryan': 'Ryan', 'speaker-conrad': 'Conrad'}
ROOT = Path(__file__).resolve().parent.parent
PREFIX_MANIFEST = ROOT / 'localization/evidence/yarn-protected-partial-20261107.json'


def prepare(platform, source, locale_file, requested, tool, runtime, runtime_sha, *, fallback_locale=None):
    expected = managed_fallback.source_digest(platform, source)
    locale, names = dl.read_locale(locale_file, list(SOURCE_NAMES), list(SOURCE_NAMES.values()),
                                   expected, yarn_semantics=False)
    if locale != requested or names.keys() != SOURCE_NAMES.keys():
        raise ValueError('speaker locale must match the request and contain both source names')
    # Match the game-side label guard. The current two speakers are single words.
    if any(len(name) > 40 or not all(c.isalpha() and ord(c) <= 0xffff for c in name)
           for name in names.values()):
        raise ValueError('speaker labels must be single words of at most 40 BMP letters')
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
        run = subprocess.run(['dotnet', str(Path(tool).resolve(strict=True)), platform, str(Path(source).resolve()),
                              str(mapping), str(output), str(staged_runtime), runtime_sha, '--locale', locale, fallback],
                             cwd=ROOT, check=True, capture_output=True, text=True)
        report = json.loads(run.stdout, object_pairs_hook=dl.unique_object)
        data = output.read_bytes()
    ids = sorted(row['id'] for row in json.loads(PREFIX_MANIFEST.read_text())['prefixProtection'])
    if (report.get('testOnly') is not False or report.get('platform') != platform or report.get('locale') != locale
            or report.get('sourceSha256') != expected or report.get('outputSha256') != dl.sha(data)
            or report.get('inlineRuntimeSha256') != runtime_sha or report.get('inlineIds') != ids
            or report.get('mappedSpeakers') != sorted(SOURCE_NAMES.values())
            or len(report.get('changedDisplayCallSites', ())) != 3 or report.get('verifiedExistingMethodBodies') != 717
            or report.get('fallbackChanged') is not (fallback != original_fallback)):
        raise ValueError('unexpected speaker presentation verification receipt')
    return {managed_fallback.ASSEMBLY: data, COMPANION: runtime_bytes}, report
