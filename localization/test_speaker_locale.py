import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import dialogue_locale as dl
import managed_fallback as fallback
import speaker_locale as speakers

WORK = Path(__file__).parent / 'work'
TOOLS = os.environ.get('DRAGONS_SPEAKER_LOCALE_TOOLS')
SOURCES = {
    'macos': Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data/Managed",
    'windows': Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data/Managed'),
}


@unittest.skipUnless(TOOLS and all(p.is_dir() for p in SOURCES.values()), 'paired builds and speaker locale tools required')
class SpeakerLocaleTests(unittest.TestCase):
    def test_source_pinned_display_and_missing_line_on_both_builds(self):
        tools = Path(TOOLS)
        for platform, managed in SOURCES.items():
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as folder:
                root = Path(folder)
                source = managed / fallback.ASSEMBLY
                digest = fallback.SOURCES[platform]
                locale = root / 'names.json'
                missing = root / 'missing.json'
                replacement = 'Жж Ъъ 741'
                names = {'speaker-ryan': {'source': 'Ryan', 'text': 'Жж'},
                         'speaker-conrad': {'source': 'Conrad', 'text': 'ЪъЬьЯяЖ'}}

                def write(file, lines):
                    file.write_text(json.dumps({'schema': 1, 'locale': 'ru',
                                                'sourceObjectSha256': digest, 'lines': lines}), encoding='utf-8')

                write(locale, names)
                write(missing, {'yarn-missing-line': {'source': '!! ERROR: Missing line!', 'text': replacement}})
                runtime = tools / platform / 'runtime/bin' / speakers.COMPANION
                runtime_sha = dl.sha(runtime.read_bytes())
                args = (platform, source, locale, 'ru', tools / 'tool/bin/speaker-display-probe.dll', runtime)
                with self.assertRaisesRegex(ValueError, 'runtime fingerprint mismatch'):
                    speakers.prepare(*args, '0' * 64, fallback_locale=missing)
                write(locale, {'speaker-ryan': names['speaker-ryan']})
                with self.assertRaisesRegex(ValueError, 'contain both source names'):
                    speakers.prepare(*args, runtime_sha, fallback_locale=missing)
                write(locale, names)
                files, report = speakers.prepare(*args, runtime_sha, fallback_locale=missing)
                self.assertEqual(files.keys(), {fallback.ASSEMBLY, speakers.COMPANION})
                self.assertTrue(report['fallbackChanged'])
                self.assertEqual(dl.sha(source.read_bytes()), digest)
                harness = root / 'harness'
                shutil.copytree(tools / platform / 'harness/bin', harness)

                def check(files, report, *special):
                    for name, data in files.items():
                        (harness / name).write_bytes(data)
                    run = subprocess.run([
                        'dotnet', str(harness / 'speaker-inline-probe.dll'), platform,
                        str(WORK / 'source-inventory-20261107/yarn-paired-scenes.json'),
                        report['outputSha256'], str(harness / speakers.COMPANION), runtime_sha, replacement, *special,
                    ], capture_output=True, text=True)
                    self.assertEqual(run.returncode, 0, run.stderr)
                    result = json.loads(run.stdout)
                    self.assertEqual(len(result['mappedIds']), 18)
                    self.assertEqual(result['markupControls'], 2)
                    self.assertEqual(result['unchangedControls'], 8)
                    self.assertEqual(result.get('alexanderBodyVerified', False), bool(special))

                check(files, report)
                english = 'The most prestigious college hosting prestigious professors like me:'
                synthetic = 'Жёлтый ёж. Ъъ Ьь Щщ Йй. Жёлтый ёж. Ъъ Ьь Щщ Йй:'
                write(locale, names | {speakers.ALEXANDER: {'source': english, 'text': '<i>Ж</i>:'}})
                with self.assertRaisesRegex(ValueError, 'markup or placeholders differ'):
                    speakers.prepare(*args, runtime_sha, fallback_locale=missing)
                for invalid in (synthetic[:-1], '  :'):
                    write(locale, names | {speakers.ALEXANDER: {'source': english, 'text': invalid}})
                    with self.assertRaisesRegex(ValueError, 'plain text ending with a colon'):
                        speakers.prepare(*args, runtime_sha, fallback_locale=missing)
                write(locale, names | {speakers.ALEXANDER: {'source': english, 'text': synthetic}})
                files, report = speakers.prepare(*args, runtime_sha, fallback_locale=missing)
                self.assertEqual(report['alexanderBodyId'], speakers.ALEXANDER)
                self.assertEqual(len(report['changedDisplayCallSites']), 10)
                check(files, report, synthetic)
