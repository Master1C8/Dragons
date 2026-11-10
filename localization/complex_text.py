"""Bind verified shaped fonts and managed rendering patches to a package build."""

from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import tempfile

import cjk_font_fallback as fallback
import dialogue_locale as dl

TMP = 'Unity.TextMeshPro.dll'
YARN = 'YarnSpinner.Unity.dll'
LAYOUT = 'Dragons.PreparedTextLayout.dll'
LICENSE = 'NotoShaped-OFL.txt'
WORKLIST = '496d41967a72994bf63de2acf810bdd1e6995806b4f2219fc9f9e61c4f572a45'
# Original font and redistribution license from the same source distribution.
FONTS = {
    'ar': ('bdff3e5659d67e67def05b33f749683b9376ae819d65d3dd62ac4640b3aaef48',
           'a7a5a25eb188bf1cd96982030d53e23c33485c69b1044a562254226857ee13af'),
    'he': ('5d47c2310ef31393df8029d9a85db065133ab7132505248710482cf2d243e694',
           '0dab92d0544f7b233403f14b84a663bdbfa746982eda629e7f4f9ffe1b036feb'),
    'th': ('61cf814eec46b294d6ea4401ac295d0cecd5207bd2331dcc5a15e7301d30ee44',
           '2e98fd23a52d253db8612cd5942c8f2ff4111b21d2367050fdca91d8ccc374a0'),
    'hi': ('4e3c66638958c3e2ab5d37f47a8deb89fffeb7be9985c665a519bbc7ba762313',
           'a216f6f8d85c7228093e0ee5e258d9d377e6671f68acb4db1930b29583d0f331'),
}
FONTS['fa'] = FONTS['ar']


@dataclass(frozen=True)
class Inputs:
    plans: Path
    report_sha: str
    license: Path
    tool: Path
    layout: Path
    layout_sha: str


@dataclass(frozen=True)
class Prepared:
    font: fallback.Resource
    plans: bytes
    plan_count: int
    report_sha: str
    authored: bytes
    tool: Path
    layout: bytes

    def patch(self, managed, speaker_bytes, speaker_receipt):
        with tempfile.TemporaryDirectory(prefix='dragons-complex-text-') as temporary:
            stage = Path(temporary)
            plans, layout = stage / 'plans.json', stage / LAYOUT
            plans.write_bytes(self.plans)
            layout.write_bytes(self.layout)
            speaker = stage / 'speaker-input.dll'
            speaker.write_bytes(speaker_bytes)
            tmp, yarn = stage / TMP, stage / YARN

            def run(*args):
                command = ['dotnet', str(self.tool), *map(str, args)]
                result = subprocess.run(command, check=True, capture_output=True, text=True)
                return json.loads(result.stdout, object_pairs_hook=dl.unique_object)

            tmp_receipt = run(managed / TMP, plans, tmp, layout)
            yarn_receipt = run('--yarn-compose', managed / YARN, speaker,
                               speaker_receipt['outputSha256'], layout, yarn)
            files = {TMP: tmp.read_bytes(), YARN: yarn.read_bytes(), LAYOUT: self.layout}
        if (tmp_receipt['sourceSha256'] != dl.sha((managed / TMP).read_bytes()) or
                tmp_receipt['outputSha256'] != dl.sha(files[TMP]) or
                tmp_receipt['displayMapSha256'] != dl.sha(self.plans) or
                tmp_receipt['mappings'] != self.plan_count or tmp_receipt['renderHook'] is not True or
                tmp_receipt.get('clusterWrapHooks') != 4 or tmp_receipt['verifiedOriginalMethodBodies'] != 1806 or
                yarn_receipt['sourceSha256'] != speaker_receipt['sourceSha256'] or
                yarn_receipt['inputSha256'] != speaker_receipt['outputSha256'] or
                yarn_receipt['outputSha256'] != dl.sha(files[YARN]) or yarn_receipt['revealSites'] != 3):
            raise ValueError('unexpected shaped text managed verification receipt')
        receipt = {'fontPlanReportSha256': self.report_sha, 'translationSha256': dl.sha(self.authored),
                   'layoutSha256': dl.sha(self.layout), 'tmp': tmp_receipt, 'yarn': yarn_receipt}
        return files, receipt


def prepare(platform, locale, authored, inputs):
    if locale not in FONTS:
        if inputs is not None:
            raise ValueError(f'shaped text inputs are unsupported for {locale}')
        return None
    if inputs is None or not Path(authored).is_file() or Path(authored).is_symlink():
        raise ValueError(f'{locale} requires authored JSON and verified shaped text inputs')
    report = (inputs.plans / 'result.json').read_bytes()
    if dl.sha(report) != inputs.report_sha:
        raise ValueError('shaped text report fingerprint mismatch')
    data = json.loads(report, object_pairs_hook=dl.unique_object)
    item = data['locales'][locale]
    kind = 'ltr' if locale in ('th', 'hi') else 'rtl'
    font = (inputs.plans / locale / 'probe.ttf').read_bytes()
    plans = (inputs.plans / locale / f'{kind}-plans.json').read_bytes()
    license = inputs.license.read_bytes()
    layout = inputs.layout.read_bytes()
    authored_bytes = Path(authored).read_bytes()
    source_font, license_sha = FONTS[locale]
    font_receipt = item['platforms'][platform]
    if (data['worklistSha256'] != WORKLIST or item['translationSha256'] != dl.sha(authored_bytes) or
            item['fontSha256'] != source_font or item['probeFontSha256'] != dl.sha(font) or
            item[f'{kind}PlanSha256'] != dl.sha(plans) or item[f'{kind}PlanBoundaries'] or
            font_receipt['remainingAfterCandidate'] or dl.sha(license) != license_sha or
            inputs.layout.name != LAYOUT or dl.sha(layout) != inputs.layout_sha):
        raise ValueError('shaped text inputs differ from the verified locale, font or layout')
    return Prepared(fallback.Resource(font, license, locale), plans, item[f'{kind}Plans'],
                    inputs.report_sha, authored_bytes, inputs.tool.resolve(strict=True), layout)


def add_arguments(parser):
    for name in ('plans', 'license', 'tool', 'layout'):
        parser.add_argument(f'--complex-{name}', type=Path)
    for name in ('report-sha', 'layout-sha'):
        parser.add_argument(f'--complex-{name}')


def arguments(args):
    values = (args.complex_plans, args.complex_report_sha, args.complex_license,
              args.complex_tool, args.complex_layout, args.complex_layout_sha)
    if all(value is None for value in values):
        return None
    if any(value is None for value in values):
        raise ValueError('all shaped text arguments must be supplied together')
    return Inputs(*values)
