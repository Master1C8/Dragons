from collections import Counter
from pathlib import Path
import unittest

import inventory_game_components as components

MAC = Path.home() / "Documents/Drag'N Wash.app/Contents/Resources/Data"
WIN = Path('/Volumes/KINGSTONMAC/CrossOver/Bottles/Steam/drive_c/Dragn.Wash/game/DragNWash_Data')


@unittest.skipUnless(MAC.is_dir() and WIN.is_dir(), 'both pinned game builds required')
class GameComponentInventoryTests(unittest.TestCase):
    def test_pinned_components_and_bark_references(self):
        for platform, source, object_count, field_count in (
                ('macos', MAC, 1331, 10973), ('windows', WIN, 1299, 10936)):
            with self.subTest(platform=platform):
                report = components.inspect(source, platform)
                self.assertEqual(len(report['objects']), object_count)
                fields = [f for obj in report['objects'] for f in obj['fields']]
                self.assertEqual(len(fields), field_count)
                references = Counter(f['value'] for f in fields
                                     if f['role'] == 'preserve-exactly-yarn-node-reference' and f['value'])
                self.assertEqual(sum(references.values()), 123)
                self.assertEqual(references['DragonColdBalls'], 7)
                self.assertEqual(report['missingDialogueTargets'], [])
                self.assertTrue(any(f['role'] == 'preserve-exactly-rig-key'
                                    and f['path'][-3:-1] == ['coordinates', 'bones'] for f in fields))
                self.assertEqual(sum(f['role'] == 'dragon-bark-description-needs-runtime-review'
                                     for f in fields), 361)
                self.assertEqual(sum(f['role'] == 'dragon-descriptor-name-needs-runtime-review'
                                     for f in fields), 20)
                self.assertEqual(sum(f['role'] == 'preserve-exactly-animation-key'
                                     and f['path'][-2:] == ['data', 'boolName'] for f in fields), 361)
                self.assertTrue(any(f['role'] == 'preserve-exactly-state-key'
                                    and f['path'] == ['placeFlag'] and f['value'] == 'PlacedMount'
                                    for f in fields))
                self.assertTrue(any(f['role'] == 'preserve-exactly-menu-intent-key'
                                    and f['path'][-1] == 'intentName' and f['value'] == 'Pause'
                                    for f in fields))

    def test_bark_role_checks_the_serialized_type(self):
        identity = ('', 'DragonBarkFeaturePlapResponse')
        path = ('references', 'RefIds', 0, 'data', 'boolName')
        bark_type = {'asm': components.GAME_ASSEMBLY, 'ns': '', 'class': 'DragonBarkAnimationPlayVFX'}
        tree = {'references': {'RefIds': [{'type': bark_type}]}}
        self.assertEqual(components.field_role(identity, path, 'Hearts', tree), 'preserve-exactly-animation-key')
        bark_type['class'] = 'DragonBarkDialogue'
        self.assertEqual(components.field_role(identity, path, 'Hearts', tree),
                         'serialized-string-needs-consumer-review')

    def test_wrong_build_rejected_before_schema_decoding(self):
        with self.assertRaisesRegex(ValueError, 'unsupported source:'):
            components.inspect(WIN, 'macos')
