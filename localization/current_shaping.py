"""Regenerate the existing TMP render plans with the 317a98f text delta."""
import importlib.util
import json

import cjk_font_fallback
import complex_text
from current_build import digest
import probe_complex_fonts as historical
from rebuild_release_packages import archived_file
import shaped_display_plan
import speaker_locale


def prepare(args, stage, authored, rows, translations, delta, archived, accepted):
    import uharfbuzz

    if (not all((args.shaper, args.shaping_source, args.icu, args.shaping_tool)) or
            uharfbuzz.__version__ != '0.51.7' or
            digest(args.shaper.read_bytes()) != historical.SONIC_SHAPER_SHA):
        raise ValueError('Pinned HarfBuzz, shaper, ICU and shaping inputs are required')
    spec = importlib.util.spec_from_file_location('dragons_reference_shaper', args.shaper)
    shaper = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(shaper)
    shaper.KNOWN_TMP_TAG = historical.TMP_TAG

    locale = args.locale
    font_dir = args.shaping_source / 'fonts'
    name = 'ar-fa' if locale in ('ar', 'fa') else locale
    source = font_dir / ('NotoSansHebrewLatin-Regular.ttf' if locale == 'he' else f'{name}.ttf')
    license_bytes = (archived / 'Licenses' / locale / complex_text.LICENSE).read_bytes()
    expected_font, expected_license = complex_text.FONTS[locale]
    if digest(source.read_bytes()) != expected_font or digest(license_bytes) != expected_license:
        raise ValueError('Shaping source font or license fingerprint mismatch')
    layout, _ = archived_file(archived, accepted, complex_text.LAYOUT)
    augmenter = shaper.FontAugmenter(source, shaper.LOCALE_SPECS[locale])
    bidi = shaped_display_plan.Bidi(args.icu) if locale in ('ar', 'fa', 'he') else None
    split = historical.thai_breaker(args.icu) if locale == 'th' else None
    platforms = ('macos', 'windows')
    names = {platform: {name: translations[f'display:{key}'][platform]
                        for key, name in speaker_locale.SOURCE_NAMES.items()} for platform in platforms}
    corpus = set()
    for key, values in translations.items():
        corpus.update(historical.authored_display_values(values, rows[key], names))
    corpus.update(delta['ui'].values())
    for key, item in delta['yarn'].items():
        row = rows['yarn:' + key]
        corpus.update(historical.authored_display_values(dict.fromkeys(platforms, item['text']), row, names))
    corpus.update(item['text'] for item in delta['settings'].values())
    corpus |= {text.strip() for text in corpus}
    plans = [shaped_display_plan.prepare(text, historical.TMP_TAG, bidi, augmenter, split)
             for text in sorted(corpus) if augmenter.has_script(text)]
    font = stage / 'current-shaped.ttf'
    augmenter.save(font)
    plans_bytes = (json.dumps(plans, ensure_ascii=False) + '\n').encode()
    font_bytes = font.read_bytes()
    receipt = {'plansSha256': digest(plans_bytes), 'fontSha256': digest(font_bytes),
               'deltaSha256': digest(args.delta.read_bytes()), 'count': len(plans)}
    return complex_text.Prepared(cjk_font_fallback.Resource(font_bytes, license_bytes, locale),
                                 plans_bytes, len(plans), digest(json.dumps(receipt).encode()),
                                 authored.read_bytes(), args.shaping_tool.resolve(strict=True),
                                 layout.read_bytes())
