#!/usr/bin/env python3
"""Build a separate signed macOS app from complete pinned locale inputs."""
import argparse
from pathlib import Path
import tempfile

import build_game
import compare_yarn_versions as versions
import package_inputs
import ui_locale

PLATFORM = 'macos'


def build(source, inputs, requested, inventory, scope_path, output, *,
          managed_tool, speaker_tool, speaker_runtime, speaker_runtime_sha):
    source, output = build_game.bundle_paths(Path(source), Path(output))
    data = source / build_game.ASSET_RELATIVE.parent
    with tempfile.TemporaryDirectory(prefix='dragons-macos-locale-') as temporary:
        local = Path(temporary) / 'locale'
        package_inputs.snapshot_inputs(inputs, local, ui_locale.ASSETS)
        receipt, _ = package_inputs.validate(PLATFORM, data, requested, local, inventory, scope_path)
        manifest = {
            'schema': 1, 'kind': 'macos-localization-app', 'platform': PLATFORM,
            'build': versions.BUILDS[PLATFORM]['version'], 'locale': requested, **receipt,
            'sourceGlobalManagersSha256': versions.BUILDS[PLATFORM]['globalSha256'],
            'sourceGlobalScriptsSha256': ui_locale.GLOBAL_HASH,
        }
        return build_game.build(
            source, local / 'dialogue.json', requested, output, local / 'ui', local / 'settings.json',
            restore_yarn_transitions=True, improve_speaker_contrast=True,
            fallback_locale=local / 'missing-line.json', slot_new_locale=local / 'slot-new.json',
            fallback_tool=managed_tool, speaker_locale=local / 'speakers.json',
            speaker_tool=speaker_tool, speaker_runtime=speaker_runtime, speaker_runtime_sha=speaker_runtime_sha,
            package_receipt=manifest, preservation_inventory=inventory,
        )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_app', type=Path)
    parser.add_argument('locale_inputs', type=Path)
    parser.add_argument('--locale', required=True)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--yarn-scope', type=Path, required=True)
    parser.add_argument('--managed-tool', type=Path, required=True)
    parser.add_argument('--speaker-tool', type=Path, required=True)
    parser.add_argument('--speaker-runtime', type=Path, required=True)
    parser.add_argument('--speaker-runtime-sha', required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    build(args.source_app, args.locale_inputs, args.locale, args.inventory, args.yarn_scope, args.output,
          managed_tool=args.managed_tool, speaker_tool=args.speaker_tool,
          speaker_runtime=args.speaker_runtime, speaker_runtime_sha=args.speaker_runtime_sha)


if __name__ == '__main__':
    main()
