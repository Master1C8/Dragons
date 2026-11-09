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
        self.assertEqual(result['familyCounts'], {'game-component': 21909, 'legacy-ui': 149, 'managed': 2974,
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
                         'editor-choice-candidate', 'recovery-prompt-candidate', 'recovery-choice-candidate',
                         'diagnostic-dialogue-candidate'}
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
        self.assertEqual(entries['yarn:line:8f64adc0']['role'], 'recovery-prompt-candidate')
        self.assertEqual(entries['yarn:line:bac1ce29']['role'], 'recovery-choice-candidate')
        self.assertEqual(entries['yarn:line:0090c7b0']['role'], 'choice-candidate')
        self.assertEqual(entries['yarn:line:4810891f']['role'], 'dialogue-punctuation-candidate')
        self.assertNotEqual(entries['yarn:line:fa1a1e76']['source']['macos'],
                            entries['yarn:line:fa1a1e76']['source']['windows'])
        self.assertEqual(entries['yarn:line:7c56b2d8']['role'], 'dialogue-candidate')
        for line in ('bedc761d', 'e104b8e4', 'f5a81524'):
            self.assertEqual(entries[f'yarn:line:{line}']['role'], 'choice-candidate')
        self.assertNotEqual(entries['yarn:line:d38c63ea']['source']['macos'],
                            entries['yarn:line:d38c63ea']['source']['windows'])
        self.assertEqual(entries['yarn:line:6d5ba814']['role'], 'recovery-prompt-candidate')
        self.assertEqual(entries['yarn:line:6a7610f3']['role'], 'recovery-choice-candidate')
        self.assertEqual(entries['yarn:line:7e189c92']['role'], 'dialogue-punctuation-candidate')
        self.assertEqual(entries['yarn:line:c2bdc402']['role'], 'choice-candidate')
        self.assertEqual(entries['yarn:line:66fb84fe']['role'], 'choice-candidate')
        self.assertEqual(entries['yarn:line:8ee41fdc']['role'], 'dialogue-candidate')
        self.assertNotEqual(entries['yarn:line:a1f9de62']['source']['macos'],
                            entries['yarn:line:a1f9de62']['source']['windows'])
        self.assertEqual(entries['yarn:line:3fdb9d01']['role'], 'diagnostic-dialogue-candidate')
        self.assertEqual(entries['yarn:line:61cd33c5']['role'], 'recovery-choice-candidate')
        self.assertEqual(entries['yarn:line:ddab3d34']['role'], 'dialogue-candidate')
        self.assertEqual(sum(r['role'] in opening_roles for r in result['entries'] if r['family'] == 'yarn'), 1823)
        self.assertFalse(any(r['family'] == 'yarn' and r['role'] == 'needs-classification'
                             for r in result['entries']))
        self.assertEqual(result['openingRoleManifestSha256'], inventory.OPENING_ROLES_SHA)
        self.assertEqual(result['ryan23RoleManifestSha256'], inventory.RYAN23_ROLES_SHA)
        self.assertEqual(result['ryan45RoleManifestSha256'], inventory.RYAN45_ROLES_SHA)
        self.assertEqual(result['ryanExtraRoleManifestSha256'], inventory.RYAN_EXTRA_ROLES_SHA)
        self.assertEqual(result['ryanFoodRoleManifestSha256'], inventory.RYAN_FOOD_ROLES_SHA)
        self.assertEqual(result['conrad3RoleManifestSha256'], inventory.CONRAD3_ROLES_SHA)
        self.assertEqual(result['conrad124RoleManifestSha256'], inventory.CONRAD124_ROLES_SHA)
        self.assertEqual(result['alexanderLevelRoleManifestSha256'], inventory.ALEXANDER_LEVEL_ROLES_SHA)
        self.assertEqual(result['remainingYarnRoleManifestSha256'], inventory.REMAINING_YARN_ROLES_SHA)
        mac_only = entries['settings:LookInvertY:label']
        self.assertEqual(mac_only['source']['macos'], 'Invert Look Y')
        self.assertIsNone(mac_only['source']['windows'])
        self.assertTrue(all(len(r['source']) == 1 for r in result['entries'] if r['family'] == 'managed'))
        controls = [r for r in result['entries'] if r['role'] == 'preserve-exactly-input-control'
                    and 'InputSystem_Actions::.ctor()' in r['method']]
        self.assertEqual(len(controls), 56)
        self.assertEqual(sum('macos' in r['source'] for r in controls), 28)
        self.assertEqual(sum('windows' in r['source'] for r in controls), 28)
        engine_rows = [r for r in result['entries'] if r['family'] == 'managed' and
                       any(':' + assembly + ':' in r['id'] for assembly in ('Unity.TextMeshPro', 'UnityEngine.UI'))]
        self.assertEqual(len(engine_rows), 1156)
        self.assertEqual(sum(r['role'] == 'engine-default-text-needs-visibility-review' for r in engine_rows), 34)
        for platform in ('macos', 'windows'):
            for value, method in (('Mixed...', 'TMPro.TMP_Dropdown::.cctor()'),
                                  ('Enter text...', 'UnityEngine.UI.DefaultControls::CreateInputField')):
                self.assertTrue(any(r['source'].get(platform) == value and method in r['method'] and
                                    r['role'] == 'engine-default-text-needs-visibility-review'
                                    for r in engine_rows))
            game_rows = [r for r in result['entries'] if r['id'].startswith(f'managed:{platform}:Assembly-CSharp:')]
            for role, count, value in (
                    ('slot-new-runtime-text-candidate', 3, 'NEW'),
                    ('preserve-exactly-slot-progress-format', 6, '{0} / 14')):
                self.assertEqual([r['source'][platform] for r in game_rows if r['role'] == role], [value] * count)
            self.assertEqual([r['source'][platform] for r in game_rows
                              if r.get('consumer') == 'MenuResponseTransition.reason'], ['Delete Save?'] * 3)
            self.assertEqual(sum(r['role'] == 'objective-text-needs-visibility-review' for r in game_rows), 4)
            for role, value, consumer in (
                    ('preserve-exactly-animation-key', 'Speed', 'LocomotionAnimationBridge::speedParam'),
                    ('preserve-exactly-command', 'BlackoutFadeIn', '::AddCommandHandler('),
                    ('preserve-exactly-preference-key', 'saveSlot', 'UnityEngine.PlayerPrefs::GetInt(')):
                self.assertTrue(any(r['role'] == role and r['source'][platform] == value and
                                    consumer in r.get('consumer', '') for r in game_rows), (platform, role, value))
            self.assertTrue(any(r['role'] == 'preserve-exactly-input-control' and
                                r['source'].get(platform) == 'Horizontal' and
                                'StandaloneInputModule::m_HorizontalAxis' in r.get('consumer', '')
                                for r in engine_rows), platform)
            for value, role, target in (
                    ('Menu_Loading', 'preserve-exactly-menu-key', inventory.managed.MENU_TRANSITION),
                    ('Going back to new game menu!', 'preserve-exactly-menu-transition-reason',
                     inventory.managed.MENU_TRANSITION),
                    ('_FluidHeight', 'preserve-exactly-renderer-key', inventory.managed.DECAL_SETTINGS)):
                self.assertTrue(any(r['source'][platform] == value and r['role'] == role and
                                    r.get('consumer') == target for r in game_rows), (platform, value))
            missing = [r for r in result['entries'] if r['source'].get(platform) == '!! ERROR: Missing line!']
            self.assertEqual([r['role'] for r in missing], ['error-fallback-text-needs-runtime-review'] * 2)
            self.assertEqual({r['consumer'] for r in missing}, {
                inventory.managed.MISSING_BODY_FIELD, inventory.managed.SET_PARSED_TEXT,
            })
            flag_writer = [r for r in game_rows
                           if r['method'] == 'SimpleJSON.JSONNode WalkNWash.Flags.FlagRegistry::ToJson(System.Int32)']
            expected_keys = {'levelIndex', 'id', 'type', 'boolValue', 'stringValue'}
            if platform == 'macos':
                expected_keys.add('version')
            self.assertEqual({r['source'][platform] for r in flag_writer}, expected_keys)
            self.assertTrue(all(r['role'] == 'preserve-exactly-json-key' for r in flag_writer))
            make_face = [r for r in game_rows if r['method'] == inventory.managed.REGISTER_ACTIONS
                         and r['source'][platform] == 'MakeFace']
            self.assertEqual([r['role'] for r in make_face],
                             ['preserve-exactly-command', 'preserve-exactly-reflection-member'])
            egg = [r for r in game_rows if r['source'][platform] == 'Player put egg']
            self.assertEqual({r['role'] for r in egg}, {'dragon-bark-description-needs-runtime-review',
                                                        'dragon-bark-transition-reason-needs-runtime-review'})
            for value, method, role in (
                ('hand.l', 'System.Void WalkNWashStepHandler::Start()', 'preserve-exactly-rig-key'),
                ('_BaseColorMap_ST', 'System.Void WalkNWashParticleSpline::LateUpdate()',
                 'preserve-exactly-renderer-key'),
                ('', 'System.Boolean LevelFlow::GetRandomNagDialog(System.Int32,System.String&)',
                 'preserve-exactly-empty-value'),
                ('Idle', 'System.String DragonBark::GetDescription()', 'dragon-bark-description-needs-runtime-review'),
            ):
                rows = [r for r in game_rows if r['source'][platform] == value and r['method'] == method]
                self.assertEqual([r['role'] for r in rows], [role], (platform, method, value))
            self.assertFalse(any(r['role'] == 'needs-classification' for r in game_rows))
            flags = [r for r in game_rows if r['method'] == 'System.String WalkNWash.Flags.FlagEntry::ToString()']
            self.assertEqual([r['role'] for r in flags], ['string-representation-needs-visibility-review'] * 6)
            ui_code = [r for r in result['entries'] if r['id'].startswith(f'managed:{platform}:UnityEngine.UI:')]
            self.assertFalse(any(r['role'] == 'needs-classification' for r in ui_code))
            toggle = [r for r in ui_code if 'DefaultControls::CreateToggle(' in r['method']
                      and r['source'][platform] == 'Toggle']
            self.assertEqual([(r['ilOffset'], r['role']) for r in toggle], [
                (0, 'preserve-exactly-object-name'), (210, 'engine-default-text-needs-visibility-review'),
            ])
            stencil = [r for r in ui_code if r['method'] == inventory.managed.UI_STENCIL_ADD
                       and r['source'][platform] == '_Stencil']
            self.assertEqual([r['consumer'] for r in stencil], [
                'System.Boolean UnityEngine.Material::HasProperty(System.String)',
                'System.Void UnityEngine.Material::SetFloat(System.String,System.Single)',
            ])
            resolution = [r for r in result['entries']
                          if r['id'].startswith(f'managed:{platform}:UnityScriptableSettings:')
                          and r['source'][platform] == '{0} x {1}']
            self.assertEqual([r['role'] for r in resolution], ['preserve-exactly-resolution-format'])
            for method, value, role, consumer in (
                ('TMP_InputField::UpdateLabel()', '\u200b', 'preserve-exactly-input-control',
                 'System.Void TMPro.TMP_Text::set_text(System.String)'),
                ('TMP_ResourceManager::.cctor()', 'Regular', 'preserve-exactly-font-style-key',
                 'System.Int32 TMPro.TMP_TextUtilities::GetHashCode(System.String)'),
                ('LocalizedLine::get_CharacterName()', 'name', 'preserve-exactly-markup-key',
                 inventory.managed.YARN_MARKUP_LOOKUP),
                ('DialogueRunner::.ctor()', 'Start', 'preserve-exactly-yarn-node-reference',
                 'System.String Yarn.Unity.DialogueRunner::startNode'),
            ):
                rows = [r for r in result['entries'] if r['family'] == 'managed' and r['method'].endswith(method)
                        and r['source'].get(platform) == value]
                self.assertTrue(rows, (platform, method))
                self.assertEqual({(r['role'], r['consumer']) for r in rows}, {(role, consumer)})
            fallback = [r for r in result['entries'] if r['family'] == 'managed'
                        and r['source'].get(platform, '').startswith('!! Error: Missing localisation')]
            self.assertEqual([r['role'] for r in fallback], ['error-fallback-text-needs-runtime-review'])
        wait = next(r for r in result['entries'] if r['source'].get('windows') == 'Waiting for flag {0}...{1}')
        self.assertEqual(wait['role'], 'diagnostic-text-needs-visibility-review')
        self.assertEqual(wait['consumer'], 'System.Void UnityEngine.Debug::Log(System.Object)')
        self.assertFalse(any(r['role'] == 'needs-classification' for r in result['entries']
                             if r['family'] == 'managed'))
        component_rows = [r for r in result['entries'] if r['family'] == 'game-component']
        for platform in ('macos', 'windows'):
            cold = [r for r in component_rows if r['source'].get(platform) == 'DragonColdBalls']
            self.assertEqual(len(cold), 7)
            self.assertTrue(all(r['role'] == 'preserve-exactly-yarn-node-reference' and
                                r['fieldPath'][-2:] == ['data', 'dialogueTitle'] for r in cold))
        self.assertEqual(sum(r['role'].startswith('preserve-exactly-') for r in component_rows), 21147)
        self.assertEqual(sum(r['role'] == 'dragon-bark-description-needs-runtime-review'
                             for r in component_rows), 722)
        self.assertEqual(sum(r['role'] == 'dragon-descriptor-name-needs-runtime-review'
                             for r in component_rows), 40)
        self.assertFalse(any(r['role'] == 'serialized-string-needs-consumer-review' for r in component_rows))
        names = [r for r in result['entries'] if r['role'] == 'preserve-exactly-credit-name']
        self.assertEqual(len(names), 34)
        self.assertTrue(all(r['source']['macos'] == r['source']['windows'] for r in names))
        self.assertTrue(any(r['source']['macos'] == 'hannagreen' for r in names))
        self.assertFalse(any(r['source']['macos'] == 'GDC Bundle Part 4' for r in names))
        self.assertEqual(result['creditNameManifestSha256'], inventory.credits.MANIFEST_SHA256)
        self.assertEqual(len(entries), sum(result['familyCounts'].values()))

    def test_managed_direct_role_requires_immediate_consumer(self):
        target = 'System.Int32 UnityEngine.Shader::PropertyToID(System.String)'
        row = {'ilOffset': 100, 'value': '_Stencil',
               'followingCalls': [{'offset': 105, 'target': target, 'opcode': 'call'}]}
        self.assertEqual(inventory.managed.direct_role(row, 'Assembly-CSharp'),
                         ('preserve-exactly-renderer-key', target))
        row['followingCalls'][0]['offset'] = 106
        self.assertIsNone(inventory.managed.direct_role(row, 'Assembly-CSharp'))

    def test_managed_context_binds_exact_literals_and_rejects_unknown_stack_steps(self):
        target = 'System.Void UnityEngine.Animator::SetBool(System.String,System.Boolean)'
        row = {'id': 'literal', 'method': 'method', 'methodToken': 1, 'ilOffset': 100, 'value': 'Spraying'}
        detailed = {**row, 'following': [
            {'offset': 105, 'opcode': 'ldc.i4.1', 'operand': None},
            {'offset': 106, 'opcode': 'callvirt', 'operand': target},
        ]}
        header = {'schema': 1, 'platform': 'macos', 'assemblySha256': 'source',
                  'cecilSha256': 'cecil', 'sourceInstructionCount': 1}
        source = {**header, 'strings': [row]}
        context = {**header, 'strings': [detailed]}
        self.assertEqual(inventory.managed.bind_context(source, context), [detailed])
        self.assertEqual(inventory.managed.context_role(detailed), ('preserve-exactly-animation-key', target))
        with self.assertRaisesRegex(ValueError, 'managed context literal mismatch'):
            inventory.managed.bind_context(source, {**context, 'strings': [{**detailed, 'value': 'changed'}]})
        detailed['following'][0]['opcode'] = 'dup'
        self.assertIsNone(inventory.managed.context_role(detailed))

    def test_diagnostic_binding_requires_the_literal_to_reach_the_message_argument(self):
        sink = 'System.Void UnityEngine.Debug::LogWarning(System.Object,UnityEngine.Object)'
        steps = [
            {'opcode': 'ldarg.1', 'operand': None},
            {'opcode': 'call', 'operand': 'System.String System.String::Format(System.String,System.Object)'},
            {'opcode': 'ldarg.0', 'operand': None},
            {'opcode': 'call', 'operand': sink},
        ]
        role = inventory.managed.stacked_argument_role
        self.assertEqual(role(steps), ('diagnostic-text-needs-visibility-review', sink))
        self.assertIsNone(role(steps[:2] + steps[3:]))
        self.assertIsNone(role(steps[:2] + [{'opcode': 'pop', 'operand': None}] + steps[2:]))
        self.assertIsNone(role(steps[:2] + [{'opcode': 'br.s', 'operand': 'IL_001a'}] + steps[2:]))

    def test_menu_role_distinguishes_slots_and_unverified_payloads(self):
        target = inventory.managed.MENU_TRANSITION
        payload = [
            {'opcode': 'ldstr', 'operand': 'PlayGame'},
            {'opcode': 'newobj', 'operand': inventory.managed.LEVEL_LOAD},
            {'opcode': 'newobj', 'operand': target},
        ]
        role = inventory.managed.stacked_argument_role
        self.assertEqual(role(payload), ('preserve-exactly-menu-transition-reason', target))
        self.assertEqual(role([{'opcode': 'ldstr', 'operand': 'Time to play!'}, *payload]),
                         ('preserve-exactly-menu-key', target))
        self.assertIsNone(role(payload[1:]))
        self.assertIsNone(role([payload[0], {'opcode': 'call', 'operand': 'unverified'}, payload[2]]))

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
