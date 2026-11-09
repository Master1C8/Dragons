import json
import copy
from pathlib import Path
import tempfile
import unittest

import assemble_source_inventory as inventory

ROOT = Path(__file__).parent
WORK = ROOT / 'work/source-inventory-20261107'
ROLES = ROOT / 'evidence/ui-source-roles-20261107.json'


class SourceInventoryUnitTests(unittest.TestCase):
    def test_pinned_input_and_duplicate_ids_fail_closed(self):
        with tempfile.TemporaryDirectory() as folder:
            p = Path(folder) / 'sample.json'
            p.write_text('{"ok": true}', encoding='utf-8')
            digest = inventory.dl.sha(p.read_bytes())
            self.assertEqual(inventory.load_pinned(p, digest), {'ok': True})
            p.write_text('{"ok": false}', encoding='utf-8')
            with self.assertRaisesRegex(ValueError, 'unsupported source export'):
                inventory.load_pinned(p, digest)
        rows = {}
        inventory.put(rows, {'id': 'same', 'source': 'first'})
        with self.assertRaisesRegex(ValueError, 'duplicate inventory identity'):
            inventory.put(rows, {'id': 'same', 'source': 'second'})
        self.assertEqual(rows['same']['source'], 'first')

    @unittest.skipUnless(WORK.is_dir() and all((WORK / f).is_file() for f in inventory.FILES),
                         'all pinned source exports required')
    def test_all_selected_source_families_and_platform_bindings(self):
        result = inventory.build(WORK, ROLES)
        self.assertEqual(result['status'], 'provisional-not-translation-ready')
        self.assertEqual(result['familyCounts'], {'legacy-ui': 149, 'managed': 2974,
                                                  'settings': 80, 'ui': 162, 'yarn': 1839})
        entries = {r['id']: r for r in result['entries']}
        sample = entries['yarn:line:4b36ea4e']
        self.assertEqual((sample['node'], sample['instructionIndex']), ('Alexander_2', 14))
        self.assertEqual(sample['source']['macos'], sample['source']['windows'])
        self.assertEqual(sample['role'], 'preserve-exactly-pending-source-role')
        self.assertEqual(sum(r['role'] == 'preserve-exactly-pending-source-role' for r in result['entries']), 16)
        self.assertEqual(sum(r.get('preserveExactPrefix') is not None for r in result['entries']), 18)
        self.assertEqual(entries['yarn:line:a99c515c']['role'], 'dialogue-candidate')
        self.assertEqual(entries['yarn:line:ce77a00e']['role'], 'choice-candidate')
        self.assertEqual(entries['yarn:line:7426a997']['role'], 'dialogue-punctuation-candidate')
        self.assertEqual(entries['yarn:line:2b84f2eb']['role'], 'demo-dialogue-candidate')
        self.assertEqual(entries['yarn:line:745c3c12']['role'], 'demo-choice-candidate')
        opening_roles = {'demo-dialogue-candidate', 'demo-choice-candidate', 'dialogue-candidate',
                         'dialogue-punctuation-candidate', 'choice-candidate', 'editor-prompt-candidate',
                         'editor-choice-candidate', 'recovery-prompt-candidate', 'recovery-choice-candidate'}
        self.assertEqual(entries['yarn:line:14d2c62f']['role'], 'choice-candidate')
        self.assertEqual(entries['yarn:line:decf872a']['role'], 'dialogue-punctuation-candidate')
        self.assertEqual(entries['yarn:line:695ef750']['role'], 'dialogue-punctuation-candidate')
        self.assertEqual(entries['yarn:line:7cd85c8e']['role'], 'choice-candidate')
        self.assertEqual(entries['yarn:line:dbab7a39']['role'], 'editor-prompt-candidate')
        self.assertEqual(entries['yarn:line:4ab6c5a9']['role'], 'editor-choice-candidate')
        self.assertEqual(entries['yarn:line:61c7f2d6']['role'], 'recovery-prompt-candidate')
        self.assertEqual(entries['yarn:line:5462913f']['role'], 'recovery-choice-candidate')
        self.assertEqual(entries['yarn:line:3d2df033']['role'], 'dialogue-punctuation-candidate')
        self.assertEqual(entries['yarn:line:f5f5b815']['role'], 'dialogue-candidate')
        self.assertEqual(entries['yarn:line:f5f5b815']['preserveExactPrefix']['macos'], 'Ryan: ')
        self.assertEqual(entries['yarn:line:29237bc3']['role'], 'dialogue-candidate')
        self.assertEqual(entries['yarn:line:36ff6bd9']['role'], 'choice-candidate')
        self.assertEqual(entries['yarn:line:045f5836']['role'], 'dialogue-punctuation-candidate')
        self.assertNotEqual(entries['yarn:line:19cedc30']['source']['macos'],
                            entries['yarn:line:19cedc30']['source']['windows'])
        self.assertEqual(sum(r['role'] in opening_roles for r in result['entries'] if r['family'] == 'yarn'), 643)
        self.assertEqual(result['openingRoleManifestSha256'], inventory.OPENING_ROLES_SHA)
        self.assertEqual(result['ryan23RoleManifestSha256'], inventory.RYAN23_ROLES_SHA)
        self.assertEqual(result['ryan45RoleManifestSha256'], inventory.RYAN45_ROLES_SHA)
        self.assertEqual(result['ryanExtraRoleManifestSha256'], inventory.RYAN_EXTRA_ROLES_SHA)
        self.assertEqual(result['conrad3RoleManifestSha256'], inventory.CONRAD3_ROLES_SHA)
        mac_only = entries['settings:LookInvertY:label']
        self.assertEqual(mac_only['source']['macos'], 'Invert Look Y')
        self.assertIsNone(mac_only['source']['windows'])
        self.assertTrue(all(len(r['source']) == 1 for r in result['entries'] if r['family'] == 'managed'))
        controls = [r for r in result['entries'] if r['role'] == 'preserve-exactly-input-control']
        self.assertEqual(len(controls), 56)
        self.assertEqual(sum('macos' in r['source'] for r in controls), 28)
        self.assertEqual(sum('windows' in r['source'] for r in controls), 28)
        self.assertTrue(all('InputSystem_Actions::.ctor()' in r['method'] for r in controls))
        engine_rows = [r for r in result['entries'] if r['family'] == 'managed' and
                       any(':' + assembly + ':' in r['id'] for assembly in ('Unity.TextMeshPro', 'UnityEngine.UI'))]
        self.assertEqual(len(engine_rows), 1156)
        self.assertTrue(all(r['role'] == 'needs-classification' for r in engine_rows))
        for platform in ('macos', 'windows'):
            self.assertTrue(any(r['source'].get(platform) == 'Mixed...' and
                                'TMPro.TMP_Dropdown::.cctor()' in r['method'] for r in engine_rows))
            self.assertTrue(any(r['source'].get(platform) == 'Enter text...' and
                                'UnityEngine.UI.DefaultControls::CreateInputField' in r['method'] for r in engine_rows))
        names = [r for r in result['entries'] if r['role'] == 'preserve-exactly-credit-name']
        self.assertEqual(len(names), 34)
        self.assertTrue(all(r['source']['macos'] == r['source']['windows'] for r in names))
        self.assertTrue(any(r['source']['macos'] == 'hannagreen' for r in names))
        self.assertFalse(any(r['source']['macos'] == 'GDC Bundle Part 4' for r in names))
        self.assertEqual(result['creditNameManifestSha256'], inventory.credits.MANIFEST_SHA256)
        self.assertEqual(len(entries), sum(result['familyCounts'].values()))

    @unittest.skipUnless((WORK / 'ui-windows-all.json').is_file(), 'pinned UI export required')
    def test_credit_bindings_reject_changed_source_and_wrong_hierarchy(self):
        roles = inventory.load_pinned(ROLES, inventory.ROLES_SHA)
        manifest = inventory.load_pinned(inventory.credits.MANIFEST, inventory.credits.MANIFEST_SHA256)
        ui = inventory.load_pinned(WORK / 'ui-windows-all.json', inventory.FILES['ui-windows-all.json'])
        self.assertEqual(len(inventory.bind_credit_names(roles, manifest, ui)), 34)
        first = manifest['entries'][0]
        changed_ui = dict(ui)
        changed_ui[first['ids']['windows']] += 'x'
        with self.assertRaisesRegex(ValueError, 'credit-name source or hierarchy mismatch'):
            inventory.bind_credit_names(roles, manifest, changed_ui)
        changed_roles = copy.deepcopy(roles)
        row = next(r for r in changed_roles['entries'] if r['windows']['id'] == first['ids']['windows'])
        row['hierarchy'][-1] = 'Description'
        with self.assertRaisesRegex(ValueError, 'credit-name source or hierarchy mismatch'):
            inventory.bind_credit_names(changed_roles, manifest, ui)

    @unittest.skipUnless((WORK / 'yarn-paired-scenes.json').is_file(), 'pinned Yarn export required')
    def test_opening_roles_require_exact_scope_and_instruction_kind(self):
        scenes = inventory.load_pinned(WORK / 'yarn-paired-scenes.json', inventory.FILES['yarn-paired-scenes.json'])
        manifest = inventory.load_pinned(ROOT / 'yarn_roles_opening.json', inventory.OPENING_ROLES_SHA)
        self.assertEqual(len(inventory.bind_opening_roles(scenes, manifest)), 79)
        wrong_kind = copy.deepcopy(manifest)
        wrong_kind['groups'][0]['kind'] = 'option'
        with self.assertRaisesRegex(ValueError, 'invalid opening role group'):
            inventory.bind_opening_roles(scenes, wrong_kind)
        missing = copy.deepcopy(manifest)
        missing['groups'][0]['ids'].pop()
        with self.assertRaisesRegex(ValueError, 'opening source coverage mismatch'):
            inventory.bind_opening_roles(scenes, missing)

    @unittest.skipUnless((WORK / 'yarn-paired-scenes.json').is_file(), 'pinned Yarn export required')
    def test_ryan_roles_require_exact_scope_and_punctuation(self):
        scenes = inventory.load_pinned(WORK / 'yarn-paired-scenes.json', inventory.FILES['yarn-paired-scenes.json'])
        manifest = inventory.load_pinned(ROOT / 'yarn_roles_ryan23.json', inventory.RYAN23_ROLES_SHA)
        self.assertEqual(len(inventory.bind_ryan23_roles(scenes, manifest)), 133)
        wrong_punctuation = copy.deepcopy(manifest)
        group = next(g for g in wrong_punctuation['groups'] if g['role'] == 'dialogue-punctuation-candidate')
        other = next(g for g in wrong_punctuation['groups'] if g['node'] == group['node'] and g['role'] == 'dialogue-candidate')
        group['ids'][0], other['ids'][0] = other['ids'][0], group['ids'][0]
        with self.assertRaisesRegex(ValueError, 'punctuation role source mismatch'):
            inventory.bind_ryan23_roles(scenes, wrong_punctuation)

    @unittest.skipUnless((WORK / 'yarn-paired-scenes.json').is_file(), 'pinned Yarn export required')
    def test_ryan45_roles_require_complete_source_and_correct_instruction_kind(self):
        scenes = inventory.load_pinned(WORK / 'yarn-paired-scenes.json', inventory.FILES['yarn-paired-scenes.json'])
        manifest = inventory.load_pinned(ROOT / 'yarn_roles_ryan45.json', inventory.RYAN45_ROLES_SHA)
        self.assertEqual(len(inventory.bind_ryan45_roles(scenes, manifest)), 197)
        missing = copy.deepcopy(manifest)
        missing['groups'][0]['ids'].pop()
        with self.assertRaisesRegex(ValueError, 'opening source coverage mismatch'):
            inventory.bind_ryan45_roles(scenes, missing)
        wrong = copy.deepcopy(manifest)
        group = next(g for g in wrong['groups'] if g['role'] == 'editor-choice-candidate')
        group['kind'] = 'line'
        with self.assertRaisesRegex(ValueError, 'invalid opening role group'):
            inventory.bind_ryan45_roles(scenes, wrong)

    @unittest.skipUnless((WORK / 'yarn-paired-scenes.json').is_file(), 'pinned Yarn export required')
    def test_ryan_extra_roles_and_prefix_protection(self):
        scenes = inventory.load_pinned(WORK / 'yarn-paired-scenes.json', inventory.FILES['yarn-paired-scenes.json'])
        manifest = inventory.load_pinned(ROOT / 'yarn_roles_ryan_extra.json', inventory.RYAN_EXTRA_ROLES_SHA)
        roles = inventory.bind_ryan_extra_roles(scenes, manifest)
        self.assertEqual(len(roles), 122)
        self.assertEqual(inventory.merge_reviewed_roles((roles,), {}, {'line:f5f5b815': {}}), roles)
        wrong = dict(roles)
        wrong['line:f5f5b815'] = 'choice-candidate'
        with self.assertRaisesRegex(ValueError, 'conflict with protected Yarn bindings'):
            inventory.merge_reviewed_roles((wrong,), {}, {'line:f5f5b815': {}})
        with self.assertRaisesRegex(ValueError, 'conflict with protected Yarn bindings'):
            inventory.merge_reviewed_roles((roles,), {'line:f5f5b815': {}}, {})


if __name__ == '__main__':
    unittest.main()
