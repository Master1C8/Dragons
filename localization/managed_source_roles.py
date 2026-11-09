"""Classify only managed string uses supported by exact call or report bindings."""

# A literal immediately before one of these calls occupies its last argument.
# The same wording at another instruction remains a separate source occurrence.
DIRECT_ROLES = {
    'System.Int32 UnityEngine.Shader::PropertyToID(System.String)': 'preserve-exactly-renderer-key',
    'UnityEngine.Shader UnityEngine.Shader::Find(System.String)': 'preserve-exactly-renderer-key',
    'System.Boolean UnityEngine.Material::HasProperty(System.String)': 'preserve-exactly-renderer-key',
    'UnityEngine.Texture UnityEngine.MaterialPropertyBlock::GetTexture(System.String)': 'preserve-exactly-renderer-key',
    'System.Void UnityEngine.Material::EnableKeyword(System.String)': 'preserve-exactly-renderer-key',
    'System.Void UnityEngine.Material::DisableKeyword(System.String)': 'preserve-exactly-renderer-key',
    'System.Void UnityEngine.Animator::SetTrigger(System.String)': 'preserve-exactly-animation-key',
    'System.Void UnityEngine.Animator::ResetTrigger(System.String)': 'preserve-exactly-animation-key',
    'System.Single UnityEngine.Animator::GetFloat(System.String)': 'preserve-exactly-animation-key',
    'System.Int32 UnityEngine.Animator::StringToHash(System.String)': 'preserve-exactly-animation-key',
    'System.Void UnityEngine.VFX.VisualEffect::SendEvent(System.String)': 'preserve-exactly-animation-key',
    'System.Boolean WalkNWashSceneState::GetFlag(System.String)': 'preserve-exactly-state-key',
    'System.Void MenuEventUserIntent::.ctor(System.String)': 'preserve-exactly-menu-key',
    'System.Void MenuTransitionDataLevelLoad::.ctor(System.String)': 'preserve-exactly-menu-key',
    'UnityScriptableSettings.Setting UnityScriptableSettings.SettingsManager::GetSetting(System.String)':
        'preserve-exactly-setting-key',
    'System.Boolean UnityEngine.PlayerPrefs::HasKey(System.String)': 'preserve-exactly-preference-key',
    'System.Void UnityEngine.PlayerPrefs::DeleteKey(System.String)': 'preserve-exactly-preference-key',
    'System.Single UnityEngine.PlayerPrefs::GetFloat(System.String)': 'preserve-exactly-preference-key',
    'SimpleJSON.JSONNode SimpleJSON.JSONNode::get_Item(System.String)': 'preserve-exactly-json-key',
    'System.Boolean FileManager::FileExists(System.String)': 'preserve-exactly-path',
    'System.Boolean FileManager::TryDelete(System.String)': 'preserve-exactly-path',
    'System.String System.IO.Path::GetFileNameWithoutExtension(System.String)': 'preserve-exactly-path',
    'System.String System.IO.Path::GetExtension(System.String)': 'preserve-exactly-path',
    'UnityEngine.Transform UnityEngine.Transform::Find(System.String)': 'preserve-exactly-object-lookup',
    'UnityEngine.GameObject UnityEngine.GameObject::FindWithTag(System.String)': 'preserve-exactly-object-lookup',
    'UnityEngine.Transform Com.Gatordragongames.Extensions.TransformExtensions::FindDeepChild(UnityEngine.Transform,System.String)':
        'preserve-exactly-object-lookup',
    '!!0 UnityEngine.Resources::Load<TMPro.TMP_Settings>(System.String)': 'preserve-exactly-resource-path',
    '!!0 UnityEngine.Resources::Load<TMPro.TMP_SpriteAsset>(System.String)': 'preserve-exactly-resource-path',
    '!!0 UnityEngine.Resources::Load<UnityEngine.Material>(System.String)': 'preserve-exactly-resource-path',
    '!!0 UnityEngine.Resources::GetBuiltinResource<UnityEngine.Font>(System.String)': 'preserve-exactly-resource-path',
    '!!0 GraphProcessor.BaseGraph::GetParameterValue<UnityEngine.Vector3>(System.String)':
        'preserve-exactly-state-key',
    '!!0 GraphProcessor.BaseGraph::GetParameterValue<UnityEngine.Quaternion>(System.String)':
        'preserve-exactly-state-key',
    'System.Void CommandListener::RunCommand(System.String)': 'preserve-exactly-command',
    'System.Boolean System.String::op_Equality(System.String,System.String)': 'preserve-exactly-comparison',
    'System.Boolean System.String::op_Inequality(System.String,System.String)': 'preserve-exactly-comparison',
    'System.Boolean System.String::StartsWith(System.String)': 'preserve-exactly-comparison',
    'System.Boolean System.String::Contains(System.String)': 'preserve-exactly-comparison',
    'System.Boolean SimpleJSON.JSONNode::op_Equality(SimpleJSON.JSONNode,System.Object)':
        'preserve-exactly-comparison',
    'System.String System.Single::ToString(System.String)': 'preserve-exactly-format',
    'System.String System.UInt16::ToString(System.String)': 'preserve-exactly-format',
    'System.Void Unity.Profiling.ProfilerMarker::.ctor(System.String)': 'profiler-label',
    'System.Void UnityEngine.Debug::Log(System.Object)': 'diagnostic-text-needs-visibility-review',
    'System.Void UnityEngine.Debug::LogError(System.Object)': 'diagnostic-text-needs-visibility-review',
    'System.Void UnityEngine.Debug::LogWarning(System.Object)': 'diagnostic-text-needs-visibility-review',
    'System.Void UnityEngine.UnityException::.ctor(System.String)': 'diagnostic-text-needs-visibility-review',
    'System.Void System.Exception::.ctor(System.String)': 'diagnostic-text-needs-visibility-review',
    'System.Void System.ArgumentException::.ctor(System.String)': 'diagnostic-text-needs-visibility-review',
    'System.Void System.InvalidOperationException::.ctor(System.String)': 'diagnostic-text-needs-visibility-review',
    'System.Void System.NotSupportedException::.ctor(System.String)': 'diagnostic-text-needs-visibility-review',
    'System.Void System.NullReferenceException::.ctor(System.String)': 'diagnostic-text-needs-visibility-review',
}
TEXT_SETTERS = {
    'System.Void TMPro.TMP_Text::set_text(System.String)',
    'System.Void UnityEngine.UI.Text::set_text(System.String)',
    'System.Void TMPro.TMP_Dropdown/OptionData::set_text(System.String)',
    'System.Void UnityEngine.UI.Dropdown/OptionData::set_text(System.String)',
}
SLOT_METHODS = {
    'System.Void MenuSlotsLoad::OnShow(MenuResponseTransition)',
    'System.Void MenuSlotsNew::OnShow(MenuResponseTransition)',
}
FORMAT_CALL = 'System.String System.String::Format(System.String,System.Object)'

# These fields store identifiers used by animation, input, and rendering code.
FIELD_ROLES = {
    **{f'System.String TMPro.ShaderUtilities::{field}': 'preserve-exactly-renderer-key'
       for field in ('Keyword_Bevel', 'Keyword_Glow', 'Keyword_Underlay', 'Keyword_Ratios',
                     'Keyword_MASK_SOFT', 'Keyword_MASK_HARD', 'Keyword_MASK_TEX', 'Keyword_Outline',
                     'ShaderTag_ZTestMode', 'ShaderTag_CullMode')},
    **{f'System.String {field}': 'preserve-exactly-animation-key'
       for field in ('CreditsIconAnimator::_iconIndexParameterName',
                     'LocomotionAnimationBridge::speedParam', 'LocomotionAnimationBridge::postureParam',
                     'LocomotionAnimationBridge::onGroundParam', 'LocomotionAnimationBridge::isSlidingParam',
                     'LocomotionAnimationBridge::turnParam', 'IntermissionFade::_idleState',
                     'IntermissionFade::_intermissionState', 'IntermissionFade::_blackscreenState',
                     'IntermissionFade::_unstickPlayerState', 'IntermissionFade::_nightTimeParameter')},
    **{f'System.String UnityEngine.UI.AnimationTriggers::m_{name}Trigger': 'preserve-exactly-animation-key'
       for name in ('Normal', 'Highlighted', 'Pressed', 'Selected', 'Disabled')},
    **{f'System.String UnityEngine.EventSystems.StandaloneInputModule::m_{field}': 'preserve-exactly-input-control'
       for field in ('HorizontalAxis', 'VerticalAxis', 'SubmitButton', 'CancelButton')},
    **{f'System.String Yarn.Unity.LineAdvancer::{field}': 'preserve-exactly-input-control'
       for field in ('hurryUpLineAxis', 'nextLineAxis', 'hurryUpOptionsAxis', 'cancelDialogueAxis')},
}
FIRST_ARGUMENT_ROLES = {
    'System.Void UnityEngine.Material::SetFloat(System.String,System.Single)': 'preserve-exactly-renderer-key',
    'System.Void UnityEngine.Material::SetColor(System.String,UnityEngine.Color)': 'preserve-exactly-renderer-key',
    'System.Void UnityEngine.Animator::SetBool(System.String,System.Boolean)': 'preserve-exactly-animation-key',
    'System.Void UnityEngine.Animator::SetFloat(System.String,System.Single)': 'preserve-exactly-animation-key',
    'System.Void WalkNWashSceneState::SetFlag(System.String,System.Boolean)': 'preserve-exactly-state-key',
    'System.Void Yarn.Unity.VariableStorageBehaviour::SetValue(System.String,System.Boolean)':
        'preserve-exactly-state-key',
    'System.Int32 UnityEngine.PlayerPrefs::GetInt(System.String,System.Int32)': 'preserve-exactly-preference-key',
    'System.Void UnityEngine.PlayerPrefs::SetInt(System.String,System.Int32)': 'preserve-exactly-preference-key',
    'System.Int32 SaveManager::GetDataByKey(System.String,SimpleJSON.JSONNode)': 'preserve-exactly-json-key',
    'System.Int32 SaveManagerV1::GetDataByKey(System.String,SimpleJSON.JSONNode)': 'preserve-exactly-json-key',
    'System.Boolean FileManager::TryLoadJSON(System.String,SimpleJSON.JSONNode&)': 'preserve-exactly-path',
    'System.Boolean Yarn.Markup.MarkupParseResult::TryGetAttributeWithName(System.String,Yarn.Markup.MarkupAttribute&)':
        'preserve-exactly-markup-key',
    'System.Boolean Yarn.Markup.MarkupAttribute::TryGetProperty(System.String,System.String&)':
        'preserve-exactly-markup-key',
    'System.Void Yarn.Unity.LineProviderBehaviour::RegisterMarkerProcessor(System.String,Yarn.Markup.IAttributeMarkerProcessor)':
        'preserve-exactly-markup-key',
    'System.Boolean CsvHelper.CsvReader::TryGetField<System.String>(System.String,!!0&)':
        'preserve-exactly-csv-key',
    'UnityEngine.GameObject TMPro.TMP_DefaultControls::CreateUIElementRoot(System.String,UnityEngine.Vector2)':
        'preserve-exactly-object-name',
    'UnityEngine.GameObject TMPro.TMP_DefaultControls::CreateUIObject(System.String,UnityEngine.GameObject)':
        'preserve-exactly-object-name',
    'System.Void UnityEngine.UISystemProfilerApi::AddMarker(System.String,UnityEngine.Object)': 'profiler-label',
}
SINGLE_VALUE_LOADS = {
    'ldnull', 'ldstr', 'ldsfld', 'ldarg', 'ldarg.s', 'ldarga', 'ldarga.s',
    'ldarg.0', 'ldarg.1', 'ldarg.2', 'ldarg.3', 'ldloc', 'ldloc.s', 'ldloca', 'ldloca.s',
    'ldloc.0', 'ldloc.1', 'ldloc.2', 'ldloc.3', 'ldc.i4', 'ldc.i4.s', 'ldc.i4.m1',
    'ldc.i4.0', 'ldc.i4.1', 'ldc.i4.2', 'ldc.i4.3', 'ldc.i4.4', 'ldc.i4.5', 'ldc.i4.6',
    'ldc.i4.7', 'ldc.i4.8', 'ldc.i8', 'ldc.r4', 'ldc.r8',
}
ZERO_ARGUMENT_CALLS = {
    'UnityEngine.FullScreenMode UnityEngine.Screen::get_fullScreenMode()',
    'System.Int32 UnityEngine.QualitySettings::GetQualityLevel()',
    'UnityEngine.Color UnityEngine.Color::get_white()',
    'System.Boolean UnityEngine.Application::get_isEditor()',
}
COMMAND_REGISTRATIONS = {
    f'System.Void Yarn.Unity.ActionRegistrationExtension::AddCommandHandler{generic}'
    f'(Yarn.Unity.IActionRegistration,System.String,System.{handler})'
    for generic, handler in (
        ('', 'Action'),
        ('<System.Int32>', 'Action`1<!!0>'),
        ('<System.String>', 'Action`1<!!0>'),
        ('<UnityEngine.GameObject>', 'Action`1<!!0>'),
        ('<UnityEngine.GameObject,UnityEngine.GameObject>', 'Action`2<!!0,!!1>'),
        ('<System.Single>', 'Func`2<T1,System.Collections.IEnumerator>'),
    )
}


def bind_context(data, context):
    """Require the same pinned build and literal sequence in both exports."""
    header = ('schema', 'platform', 'assemblySha256', 'cecilSha256', 'sourceInstructionCount')
    if any(data[key] != context[key] for key in header):
        raise ValueError('managed context header mismatch')
    if len(context['strings']) != data['sourceInstructionCount']:
        raise ValueError('managed context occurrence count mismatch')
    identities = ('id', 'method', 'methodToken', 'ilOffset', 'value')
    for source, detailed in zip(data['strings'], context['strings']):
        if any(source[key] != detailed[key] for key in identities):
            raise ValueError('managed context literal mismatch')
    return context['strings']


def context_role(row):
    steps = row['following']
    if not steps or steps[0]['offset'] != row['ilOffset'] + 5:
        return None
    first = steps[0]
    if first['opcode'] in ('stfld', 'stsfld') and first['operand'] in FIELD_ROLES:
        return FIELD_ROLES[first['operand']], first['operand']
    if len(steps) >= 2 and steps[1]['opcode'] in ('call', 'callvirt'):
        target = steps[1]['operand']
        if first['opcode'] in SINGLE_VALUE_LOADS or (
                first['opcode'] == 'call' and first['operand'] in ZERO_ARGUMENT_CALLS):
            if target in FIRST_ARGUMENT_ROLES:
                return FIRST_ARGUMENT_ROLES[target], target
    if len(steps) >= 4 and [step['opcode'] for step in steps[:4]] in (
            ['ldnull', 'ldftn', 'newobj', 'call'], ['ldarg.0', 'ldftn', 'newobj', 'call']):
        constructor, target = steps[2]['operand'], steps[3]['operand']
        if (constructor.startswith(('System.Void System.Action', 'System.Void System.Func'))
                and constructor.endswith('::.ctor(System.Object,System.IntPtr)')
                and target in COMMAND_REGISTRATIONS):
            return 'preserve-exactly-command', target
    return None


def direct_role(row, assembly):
    calls = row['followingCalls']
    # ldstr is a one-byte opcode with a four-byte metadata token.
    if not calls or calls[0]['offset'] != row['ilOffset'] + 5:
        return None
    target = calls[0]['target']
    role = DIRECT_ROLES.get(target)
    if target in TEXT_SETTERS:
        role = ('engine-default-text-needs-visibility-review'
                if assembly in ('Unity.TextMeshPro', 'UnityEngine.UI') else 'runtime-text-needs-visibility-review')
        if not row['value']:
            role = 'preserve-exactly-empty-text'
    return (role, target) if role is not None else None


def bind_game_consumers(platform, data, setters, reasons, objectives):
    """Join exact managed occurrences to the independently pinned IL reports."""
    if any(report['platform'] != platform for report in (data, setters, reasons, objectives)):
        raise ValueError('managed consumer report platform mismatch')
    if any(report['assemblySha256'] != data['assemblySha256'] for report in (reasons, objectives)):
        raise ValueError('managed consumer report assembly mismatch')
    by_position = {(r['method'], r['ilOffset']): r for r in data['strings']}
    if len(by_position) != len(data['strings']):
        raise ValueError('duplicate managed literal position')
    roles = {}
    for site in setters['sites']:
        if site['assembly'] != 'Assembly-CSharp.dll' or site['method'] not in SLOT_METHODS:
            continue
        preceding = site['preceding']
        literals = [r for r in preceding if r['opcode'] == 'ldstr']
        if len(literals) != 1 or site['setter'] not in TEXT_SETTERS:
            raise ValueError('unexpected save-slot text consumer')
        literal = literals[0]
        row = by_position.get((site['method'], literal['offset']))
        if row is None or row['value'] != literal['operand'] or row['id'] in roles:
            raise ValueError('save-slot literal source mismatch')
        if row['value'] == '{0} / 14' and preceding[-1]['operand'] == FORMAT_CALL:
            role = 'preserve-exactly-slot-progress-format'
        elif row['value'] == 'NEW' and preceding[-1] == literal:
            role = 'slot-new-runtime-text-candidate'
        else:
            raise ValueError('unrecognized save-slot text consumer')
        roles[row['id']] = (role, site['setter'])
    counts = [role for role, _ in roles.values()]
    if counts.count('slot-new-runtime-text-candidate') != 3 or counts.count('preserve-exactly-slot-progress-format') != 6:
        raise ValueError('incomplete save-slot consumer coverage')
    if len(set(reasons['occurrenceOffsets'])) != 3:
        raise ValueError('incomplete menu reason coverage')
    for offset in reasons['occurrenceOffsets']:
        row = by_position.get(('MenuResponse MenuSlotsNew::OnEvent(MenuEvent)', offset))
        if row is None or row['value'] != reasons['transitionReasonLiteral'] or row['id'] in roles:
            raise ValueError('menu reason literal source mismatch')
        roles[row['id']] = ('preserve-exactly-menu-transition-reason', 'MenuResponseTransition.reason')
    if len(objectives['objectiveNames']) != 4:
        raise ValueError('incomplete objective name coverage')
    for cls, value in objectives['objectiveNames'].items():
        rows = [r for r in data['strings'] if r['method'] == f'System.String {cls}::GetName()']
        if len(rows) != 1 or rows[0]['value'] != value or rows[0]['id'] in roles:
            raise ValueError('objective literal source mismatch')
        roles[rows[0]['id']] = ('objective-text-needs-visibility-review', 'ObjectiveDisplay.SetObjective')
    return roles
