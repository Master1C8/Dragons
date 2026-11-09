"""Snapshot and validate complete, source-pinned locale inputs."""

from pathlib import Path

from assemble_source_inventory import INVENTORY_SHA, load_pinned
import inventory_non_yarn_scope as non_yarn
import inventory_yarn_scope as yarn

YARN_SCOPE_SHA = '753f54cf058bee240e56ab6ddf67b3c549f6804853e493239de097cebef65b30'
LOCALE_FILES = ('dialogue.json', 'speakers.json', 'settings.json', 'slot-new.json', 'missing-line.json')


def snapshot_inputs(source, target, asset_hashes):
    source, target = Path(source), Path(target)
    ui = source / 'ui'
    if source.is_symlink() or ui.is_symlink() or not ui.is_dir():
        raise ValueError('expected real locale input and UI directories')
    if {path.name for path in source.iterdir()} != {*LOCALE_FILES, 'ui'}:
        raise ValueError('locale directory differs from the package input layout')
    files = [Path(name) for name in LOCALE_FILES]
    for path in sorted(ui.iterdir()):
        if path.suffix != '.json' or path.stem not in asset_hashes:
            raise ValueError(f'unexpected UI locale file: {path.name}')
        files.append(Path('ui') / path.name)
    (target / 'ui').mkdir(parents=True)
    for name in files:
        path = source / name
        if path.is_symlink() or not path.is_file():
            raise ValueError(f'expected a real locale input file: {name}')
        (target / name).write_bytes(path.read_bytes())


def validate(platform, data, locale, inputs, inventory, scope_path):
    scope = load_pinned(scope_path, YARN_SCOPE_SHA)
    entries = load_pinned(inventory, INVENTORY_SHA)['entries']
    yarn_receipt = yarn.validate_complete(
        scope, platform, data, locale, inputs / 'dialogue.json', inputs / 'speakers.json',
    )
    other_receipt = non_yarn.verify_platform(entries, platform, data, locale, inputs)
    receipt = {
        'sharedInventorySha256': INVENTORY_SHA,
        'yarnScopeSha256': YARN_SCOPE_SHA,
        'localeInputSha256': {
            'dialogue.json': yarn_receipt['inputSha256']['dialogue'],
            'speakers.json': yarn_receipt['inputSha256']['speakers'],
            **other_receipt['localeInputSha256'],
        },
        'sourceManagedManifestSha256': other_receipt['sourceManagedManifestSha256'],
    }
    ui_assets = {asset for asset, roles in other_receipt['ui'].items() if roles['translate']}
    return receipt, ui_assets
