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
    'System.Void UnityEngine.Object::set_name(System.String)': 'preserve-exactly-object-name',
    'System.Void UnityEngine.GameObject::.ctor(System.String)': 'preserve-exactly-object-name',
    'System.Collections.IEnumerator PlapperHand::SetBoolForOneFrame(UnityEngine.Animator,System.String)':
        'preserve-exactly-animation-key',
    'System.Int32 UnityEngine.InputSystem.InputActionAsset::FindControlSchemeIndex(System.String)':
        'preserve-exactly-input-control',
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
    'System.String Yarn.Unity.LocalizedLine::TextID': 'preserve-exactly-yarn-line-id',
    'System.String Yarn.Unity.DialogueOption::TextID': 'preserve-exactly-yarn-line-id',
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
    'System.Void UnityEngine.Material::SetTexture(System.String,UnityEngine.Texture)': 'preserve-exactly-renderer-key',
    'System.Void UnityEngine.VFX.VisualEffect::SetTexture(System.String,UnityEngine.Texture)':
        'preserve-exactly-renderer-key',
    'System.Void UnityEngine.VFX.VisualEffect::SetSkinnedMeshRenderer(System.String,UnityEngine.SkinnedMeshRenderer)':
        'preserve-exactly-renderer-key',
    'System.Void UnityEngine.Animator::SetBool(System.String,System.Boolean)': 'preserve-exactly-animation-key',
    'System.Void UnityEngine.Animator::SetFloat(System.String,System.Single)': 'preserve-exactly-animation-key',
    'System.Void WalkNWashSceneState::SetFlag(System.String,System.Boolean)': 'preserve-exactly-state-key',
    'System.Void Yarn.Unity.VariableStorageBehaviour::SetValue(System.String,System.Boolean)':
        'preserve-exactly-state-key',
    'System.Void Yarn.Unity.VariableStorageBehaviour::SetValue(System.String,System.String)':
        'preserve-exactly-state-key',
    'System.Boolean GraphProcessor.BaseGraph::SetParameterValue(System.String,System.Object)':
        'preserve-exactly-state-key',
    'System.Int32 UnityEngine.PlayerPrefs::GetInt(System.String,System.Int32)': 'preserve-exactly-preference-key',
    'System.Void UnityEngine.PlayerPrefs::SetInt(System.String,System.Int32)': 'preserve-exactly-preference-key',
    'System.Int32 SaveManager::GetDataByKey(System.String,SimpleJSON.JSONNode)': 'preserve-exactly-json-key',
    'System.Int32 SaveManagerV1::GetDataByKey(System.String,SimpleJSON.JSONNode)': 'preserve-exactly-json-key',
    'System.Void SimpleJSON.JSONNode::set_Item(System.String,SimpleJSON.JSONNode)': 'preserve-exactly-json-key',
    'System.Void DialogCommands::SetValue(System.String,System.String)': 'preserve-exactly-state-key',
    'System.Boolean FileManager::TryLoadJSON(System.String,SimpleJSON.JSONNode&)': 'preserve-exactly-path',
    'System.Boolean Yarn.Markup.MarkupParseResult::TryGetAttributeWithName(System.String,Yarn.Markup.MarkupAttribute&)':
        'preserve-exactly-markup-key',
    'System.Boolean Yarn.Markup.MarkupAttribute::TryGetProperty(System.String,System.String&)':
        'preserve-exactly-markup-key',
    'System.Void Yarn.Unity.LineProviderBehaviour::RegisterMarkerProcessor(System.String,Yarn.Markup.IAttributeMarkerProcessor)':
        'preserve-exactly-markup-key',
    'System.Void Yarn.Markup.LineParser::RegisterMarkerProcessor(System.String,Yarn.Markup.IAttributeMarkerProcessor)':
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
DEBUG_SINK_ARITY = {
    f'System.Void UnityEngine.Debug::{name}(System.Object{context})': arity
    for name in ('Log', 'LogWarning', 'LogError')
    for context, arity in (('', 1), (',UnityEngine.Object', 2))
}
MENU_TRANSITION = 'System.Void MenuResponseTransition::.ctor(System.String,System.String,MenuTransitionData)'
LEVEL_LOAD = 'System.Void MenuTransitionDataLevelLoad::.ctor(System.String)'
MENU_UNPAUSE = 'System.Void MenuTransitionDataUnpause::.ctor(MenuTransitionDataUnpause/UnpauseOption)'
BARK_NOTIFY = 'System.Void DragonBarkNotifyTransition::.ctor(DragonBark,System.String)'
BARK_TRANSITION = 'System.Void DragonBarkResponseTransition::.ctor(DragonBark,System.String)'
BARK_SEX_ACT = ('System.Void DragonBarkSexAct::.ctor(UnityEngine.AnimationCurve,DPG.Penetrable,'
                'System.String,System.Single,System.String)')
BARK_OVIPOSITION = ('System.Void DragonBarkOviposition::.ctor(SphereCaster,UnityEngine.GameObject,'
                    'UnityEngine.Transform,System.String,System.Single,System.String,System.String)')
DECAL_SETTINGS = ('System.Void SkinnedMeshDecals.DecalSettings::.ctor('
                  'System.Nullable`1<SkinnedMeshDecals.DecalResolution>,'
                  'System.Nullable`1<SkinnedMeshDecals.DilationType>,System.String,'
                  'UnityEngine.RenderTextureFormat,UnityEngine.RenderTextureReadWrite)')
TYPED_ARGUMENT_ROLES = {
    ('newobj', MENU_TRANSITION, 2): 'preserve-exactly-menu-key',
    ('newobj', MENU_TRANSITION, 1): 'preserve-exactly-menu-transition-reason',
    ('newobj', DECAL_SETTINGS, 2): 'preserve-exactly-renderer-key',
    ('newobj', BARK_NOTIFY, 0): 'dragon-bark-transition-reason-needs-runtime-review',
    ('newobj', BARK_TRANSITION, 0): 'dragon-bark-transition-reason-needs-runtime-review',
    ('newobj', BARK_SEX_ACT, 0): 'dragon-bark-description-needs-runtime-review',
    ('newobj', BARK_SEX_ACT, 2): 'preserve-exactly-animation-key',
    ('newobj', BARK_OVIPOSITION, 1): 'dragon-bark-description-needs-runtime-review',
    **{(opcode, signature, 1): role for signature, role in FIRST_ARGUMENT_ROLES.items()
       for opcode in ('call', 'callvirt')},
}
ABOVE_VALUE_CALL_ARITY = {
    ('newobj', LEVEL_LOAD): 1,
    ('newobj', MENU_UNPAUSE): 1,
    ('call', 'UnityEngine.Vector3 UnityEngine.Vector3::Lerp(UnityEngine.Vector3,UnityEngine.Vector3,System.Single)'): 3,
    ('call', 'UnityEngine.Quaternion UnityEngine.Quaternion::Lerp(UnityEngine.Quaternion,UnityEngine.Quaternion,System.Single)'): 3,
    ('call', 'UnityEngine.Vector3 UnityEngine.Vector3::op_Subtraction(UnityEngine.Vector3,UnityEngine.Vector3)'): 2,
    ('call', 'System.Single UnityEngine.Vector3::Distance(UnityEngine.Vector3,UnityEngine.Vector3)'): 2,
    ('call', 'System.Single UnityEngine.Mathf::Lerp(System.Single,System.Single,System.Single)'): 3,
    ('call', 'UnityEngine.Texture UnityEngine.MaterialPropertyBlock::GetTexture(System.String)'): 2,
    ('callvirt', 'UnityEngine.Texture UnityEngine.MaterialPropertyBlock::GetTexture(System.String)'): 2,
    ('call', 'System.String System.String::Join(System.String,System.String[])'): 2,
}
MISSING_LINE = 'System.Void Yarn.Unity.LocalizedLine::.cctor()'
MISSING_BODY_FIELD = 'System.String Yarn.Unity.LocalizedLine::RawText'
EMPTY_MARKUP_LIST = 'System.Void System.Collections.Generic.List`1<Yarn.Markup.MarkupAttribute>::.ctor()'
MARKUP_RESULT = ('System.Void Yarn.Markup.MarkupParseResult::.ctor('
                 'System.String,System.Collections.Generic.List`1<Yarn.Markup.MarkupAttribute>)')
SET_PARSED_TEXT = 'System.Void Yarn.Unity.LocalizedLine::set_Text(Yarn.Markup.MarkupParseResult)'
INVALID_LINE_FIELD = 'Yarn.Unity.LocalizedLine Yarn.Unity.LocalizedLine::InvalidLine'
STRING_COMPOSITION_ARITY = {
    f'System.String System.String::{name}({",".join(parameters)})': len(parameters)
    for count in (2, 3, 4)
    for name, parameters in (('Concat', ['System.String'] * count),
                             ('Format', ['System.String', *(['System.Object'] * (count - 1))]))
}
# Known calls consuming one stack value and returning one, including receivers.
SINGLE_VALUE_CALLS = {
    'System.Boolean WalkNWashSceneState::GetFlag(System.String)',
    'System.String UnityEngine.Object::get_name()',
    'System.Int32 UnityEngine.Object::GetInstanceID()',
    'UnityEngine.GameObject UnityEngine.Component::get_gameObject()',
    'UnityEngine.RectTransform UnityEngine.UI.Dropdown::get_template()',
    'UnityEngine.RectTransform TMPro.TMP_Dropdown::get_template()',
    'System.String System.Exception::get_Message()',
    'System.String Yarn.Line::get_ID()',
    'System.String Yarn.Command::get_Text()',
    'UnityEngine.Transform UnityEngine.Component::get_transform()',
    'UnityEngine.Vector3 UnityEngine.Transform::get_position()',
    'UnityEngine.Quaternion UnityEngine.Quaternion::LookRotation(UnityEngine.Vector3)',
    'UnityEngine.Quaternion LookController::get_LookRotation()',
    'UnityEngine.Vector3 LookController::get_LookPosition()',
    'System.Single UnityScriptableSettings.SettingFloat::GetValue()',
    'System.Int32 UnityScriptableSettings.SettingInt::GetValue()',
    'System.String MenuResponseTransition::GetDestination()',
    'System.Single UnityEngine.UIElements.Experimental.Easing::OutCubic(System.Single)',
    'System.String System.IO.Path::GetFullPath(System.String)',
    'System.String System.IO.Path::GetExtension(System.String)',
    'System.String System.Object::ToString()',
    *(f'SimpleJSON.JSONNode SimpleJSON.JSONNode::op_Implicit(System.{kind})'
      for kind in ('Int32', 'String', 'Boolean')),
    *(f'System.String System.{kind}::ToString()' for kind in ('Int32', 'UInt32', 'Boolean', 'Single', 'Object')),
}
JSON_PROTOCOL_VALUES = {
    'System.String SimpleJSON.JSONNode::get_Value()': {''},
    'System.Void SimpleJSON.JSONNode::Add(SimpleJSON.JSONNode)': {''},
    'System.Void SimpleJSON.JSONNode::set_AsBool(System.Boolean)': {'false', 'true'},
    'System.String SimpleJSON.JSONNode::Escape(System.String)': {
        r'\\', r'\"', r'\n', r'\r', r'\t', r'\b', r'\f', r'\u',
    },
    'SimpleJSON.JSONNode SimpleJSON.JSONNode::Parse(System.String)': {''},
    **{f'System.Void SimpleJSON.{node}::WriteToStringBuilder('
       'System.Text.StringBuilder,System.Int32,System.Int32,SimpleJSON.JSONTextMode)': values
       for node, values in (
           ('JSONObject', {' : '}), ('JSONBool', {'false', 'true'}),
           ('JSONNull', {'null'}), ('JSONLazyCreator', {'null'}),
       )},
    'System.String SimpleJSON.JSONNull::get_Value()': {'null'},
    'System.Int64 SimpleJSON.JSONLazyCreator::get_AsLong()': {'0'},
}
SAVE_PATH_PARTS = {
    'System.String SaveManager::GetSteamAndSlotPath(System.Int32)': {'_slot', 'defaultUser_slot'},
    'System.String SaveManagerV1::GetSteamAndSlotPath(System.Int32)': {'slot', 'defaultUser'},
    **{f'System.Void {manager}::Save(SimpleJSON.JSONNode,System.Int32)': {'savegame.dgn', '_backup'}
       for manager in ('SaveManager', 'SaveManagerV1')},
    'System.Void SteamManager::EnsureSteamAppIdFile(System.UInt32)': {'..', 'steam_appid.txt'},
}
REGISTER_ACTIONS = ('System.Void Yarn.Unity.Generated.ActionRegistration::RegisterActions('
                    'Yarn.Unity.IActionRegistration,Yarn.Unity.RegistrationType)')
REFLECTION_GET_METHOD = 'System.Reflection.MethodInfo System.Type::GetMethod(System.String,System.Type[])'
REGISTER_REFLECTED_COMMAND = (
    'System.Void Yarn.Unity.IActionRegistration::AddCommandHandler(System.String,System.Reflection.MethodInfo)')

# These values reach their consumers through locals, branches or arrays in
# the pinned game methods. A matching literal in any other method is separate.
GAME_METHOD_LITERALS = {
    'System.Void WalkNWashStepHandler::Start()':
        ({'hand.l', 'foot_dupli_001.l', 'hand.r', 'foot_dupli_001.r', 'foot.l', 'foot.r'},
         'preserve-exactly-rig-key', 'System.Void WalkNWashStepHandler::AddFoot(System.String[])'),
    'System.Void LocomotionAnimationBridge::PlayStepSFX(UnityEngine.AnimationEvent)':
        ({'Foot1.R', 'Foot1.L'}, 'preserve-exactly-rig-key',
         'System.Boolean LocomotionAnimationBridge::TryFindTransform(System.String,UnityEngine.Transform,UnityEngine.Transform&)'),
    'System.Void WalkNWashParticleSpline::LateUpdate()':
        ({'_BaseColorMap_ST', '_EmissiveMap_ST'}, 'preserve-exactly-renderer-key',
         'System.Void UnityEngine.Material::SetVector(System.String,UnityEngine.Vector4)'),
    'System.Void WalkNWashSceneState::OnYarnFlagSet(System.String,System.Object)':
        ({'$', ''}, 'preserve-exactly-state-key', 'System.Void WalkNWash.Flags.Flags::Set(System.String,System.Boolean)'),
    'T Raliv.AutoLibrary.AutoLibrary`1::FindByName(System.String)':
        ({'Body_Canine', 'Body_Canine_Clothes'}, 'preserve-exactly-object-lookup',
         'Raliv.AutoLibrary.AutoLibrary`1::elementDictionary'),
    'System.Void Raliv.AnimationSystem.Animation::RunQueuedCommands(AnimationStationBase/AnimatedBody[])':
        ({'Wait', ''}, 'preserve-exactly-command', 'System.String Raliv.AnimationSystem.Animation::waitString'),
    'System.Void Raliv.AnimationSystem.CameraDirectionSet::PositionCamera(OrbitCamera)':
        ({'TargetScreenPosition'}, 'preserve-exactly-state-key',
         'System.Boolean GraphProcessor.BaseGraph::SetParameterValue(System.String,System.Object)'),
    'System.Void Raliv.AnimationSystem.PosePreview::TPose()':
        ({'TPose'}, 'preserve-exactly-animation-key',
         'System.Void UnityEngine.Animator::Play(System.String,System.Int32,System.Single)'),
    'System.Void InteractableDismissButton::OnDragonStateChanged(WalkNWashSceneState/DragonState)':
        ({'Flashing'}, 'preserve-exactly-animation-key',
         'System.Void UnityEngine.Animator::SetBool(System.String,System.Boolean)'),
    **{method: ({value}, 'preserve-exactly-animation-key',
                 'System.Void UnityEngine.Animator::SetFloat(System.String,System.Single)')
       for method, value in (
           ('System.Void InteractableJukebox::Start()', 'MusicSpeed'),
           ('System.Void AnimationBlender::Update()', 'Speed'),
           ('DragonBarkResponse DragonBarkSexAct::Update(DragonBarker)', 'SexSpeed'),
       )},
    **{method: ({'TempVFX'}, 'preserve-exactly-object-name', 'System.Void UnityEngine.GameObject::.ctor(System.String,System.Type[])')
       for method in ('System.Void InteractableWetSponge::SpawnVFX(UnityEngine.Vector3,UnityEngine.Vector3,System.Single)',
                      'System.Void VisualEffectHelper::SpawnVFX(UnityEngine.VFX.VisualEffectAsset,UnityEngine.Vector3,UnityEngine.Vector3,System.Single)')},
    **{f'System.Boolean {owner}::{method}({params})':
        ({''}, 'preserve-exactly-empty-value', 'System.String& failure result')
       for owner, methods, params in (
           ('LevelConfiguration', ('GetRandomIdleDialog', 'GetRandomNagDialog'), 'System.String&'),
           ('LevelFlow', ('GetRandomIdleDialog', 'GetRandomNagDialog'), 'System.Int32,System.String&'),
           ('WalkNWashSceneState', ('TryGetRandomIdleDialog', 'TryGetRandomNagDialog'), 'System.String&'),
       ) for method in methods},
    'System.Void WalkNWash.Flags.FlagEntry::.ctor(System.String,System.Boolean)':
        ({''}, 'preserve-exactly-empty-value', 'System.String WalkNWash.Flags.FlagEntry::stringValue'),
    'System.String DragonBark::GetDescription()':
        ({'Idle'}, 'dragon-bark-description-needs-runtime-review', 'System.String DragonBark::GetDescription()'),
    'System.Void InteractableToolEquip::OnFlagChanged(System.String,System.Boolean)':
        ({'>', ' '}, 'diagnostic-text-needs-visibility-review',
         'System.Void UnityEngine.Debug::Log(System.Object,UnityEngine.Object)'),
    'System.Void WalkNWashStepHandler::AddFoot(System.String[])':
        ({', '}, 'diagnostic-text-needs-visibility-review',
         'System.Void UnityEngine.Debug::LogWarning(System.Object,UnityEngine.Object)'),
    'HitboxTrigger DragonBarkFeaturePlapResponse::CreateTrigger(UnityEngine.Transform,System.Single)':
        ({'paw lift trigger'}, 'preserve-exactly-object-name',
         'System.Void UnityEngine.GameObject::.ctor(System.String,System.Type[])'),
    'HitboxTrigger WalkNWashDragonBoner::CreateTrigger(UnityEngine.Transform,System.Single)':
        ({'boner trigger'}, 'preserve-exactly-object-name',
         'System.Void UnityEngine.GameObject::.ctor(System.String,System.Type[])'),
    'System.Void WalkNWashMaskGenerator::Start()':
        ({'Assets/WalkNWash/CleaningMask.png'}, 'preserve-exactly-path',
         'System.Void WalkNWashMaskGenerator::SaveToTextureAsset(UnityEngine.RenderTexture,System.String)'),
    'T GatorDragonGames.StateMachine`2::ProcessResponse(GatorDragonGames.Response)':
        ({'response'}, 'preserve-exactly-parameter-name',
         'System.Void System.ArgumentOutOfRangeException::.ctor(System.String)'),
    'System.Boolean SkinnedMeshAttachmentSystem.SkinnedMeshBoneTools::BakeMeshCoordinate('
    'SkinnedMeshAttachmentSystem.EvaluationBoneCache&,SkinnedMeshAttachmentSystem.MeshHit&,'
    'SkinnedMeshAttachmentSystem.MeshCoordinates&)':
        ({'Bone_{0}'}, 'preserve-exactly-rig-key', 'System.String[] SkinnedMeshAttachmentSystem.MeshCoordinates::bones'),
    'System.Boolean FileManager::TryLoadJSON(System.String,SimpleJSON.JSONNode&)':
        ({''}, 'preserve-exactly-empty-value', 'System.String local for JSON payload'),
    **{f'System.Void {owner}::Save(SimpleJSON.JSONNode,System.Int32)':
        ({''}, 'preserve-exactly-empty-value', 'System.Boolean FileManager::TrySaveString(System.String,System.String)')
       for owner in ('SaveManager', 'SaveManagerV1')},
    'System.Void Raliv.AnimationSystem.Animation/CommandAction::.ctor()':
        ({''}, 'preserve-exactly-empty-value', 'System.String Raliv.AnimationSystem.Animation/CommandAction::command'),
    **{f'System.Void Raliv.AnimationSystem.{owner}::.ctor()':
        ({'None'}, 'preserve-exactly-state-key',
         f'Raliv.AnimationSystem.{owner}::currentLineKey or previousLineKey')
       for owner in ('AnimationBlockingAgent', 'CameraDirectionSet', 'RalivAnimator')},
    **{f'System.String {owner}::ToString()':
        (values, 'string-representation-needs-visibility-review', f'System.String {owner}::ToString()')
       for owner, values in (
           ('MenuEventUserIntent', {':[', ']'}),
           ('DragonBarkMachine', {'BarkMachine: {0}'}),
           ('TicketLock/Ticket', {'LockReason: {0}, {1}'}),
           ('WalkNWash.Flags.FlagEntry', {'[{0}={1}]', '[', '="', '"]', '=UNKNOWN]'}),
       )},
}


def game_specific_role(row):
    method, value = row['method'], row['value']
    if value in JSON_PROTOCOL_VALUES.get(method, ()):
        return 'preserve-exactly-json-protocol', method
    if value in SAVE_PATH_PARTS.get(method, ()):
        return 'preserve-exactly-path', method
    binding = GAME_METHOD_LITERALS.get(method)
    if binding is not None:
        values, role, consumer = binding
        if value in values:
            return role, consumer
    if method == REGISTER_ACTIONS and '#ldstr:' in row['id']:
        suffix = row['id'].rsplit('#ldstr:', 1)[1]
        if (suffix, value) in {('8', 'MakeFace'), ('10', 'Open'), ('12', 'LookAt'), ('14', 'ClearLook')}:
            return 'preserve-exactly-reflection-member', REFLECTION_GET_METHOD
        if (suffix, value) in {('7', 'MakeFace'), ('9', 'Open'), ('11', 'BeginDialogue'), ('13', 'FinishDialogue')}:
            return 'preserve-exactly-command', REGISTER_REFLECTED_COMMAND
    return None


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


def stacked_argument_role(steps):
    # Count values above the literal, or above the string produced from it.
    # Stop when an instruction can consume or move that tracked value.
    above = 0
    for step in steps:
        opcode, target = step['opcode'], step['operand']
        role = TYPED_ARGUMENT_ROLES.get((opcode, target, above))
        if role is not None:
            return role, target
        arity = ABOVE_VALUE_CALL_ARITY.get((opcode, target))
        if opcode in SINGLE_VALUE_LOADS:
            above += 1
        elif opcode in ('ldfld', 'ldflda', 'box') and above:
            continue
        elif opcode == 'constrained.' and above and step['operand'] is not None:
            continue
        elif opcode in ('call', 'callvirt') and above and target in SINGLE_VALUE_CALLS:
            continue
        elif arity is not None and above >= arity:
            above += 1 - arity
        elif opcode == 'call' and target in STRING_COMPOSITION_ARITY and above < STRING_COMPOSITION_ARITY[target]:
            above = 0
        elif opcode == 'call' and DEBUG_SINK_ARITY.get(target) == above + 1:
            return 'diagnostic-text-needs-visibility-review', target
        elif opcode == 'newobj' and above == 0 and DIRECT_ROLES.get(target) == 'diagnostic-text-needs-visibility-review':
            return DIRECT_ROLES[target], target
        else:
            return None
    return None


def context_role(row):
    steps = row['following']
    if not steps or steps[0]['offset'] != row['ilOffset'] + 5:
        return None
    first = steps[0]
    if row['method'] == MISSING_LINE and row['value'] == '!! ERROR: Missing line!':
        pattern = [(step['opcode'], step['operand']) for step in steps[:4]]
        if pattern[0] == ('stfld', MISSING_BODY_FIELD):
            return 'error-fallback-text-needs-runtime-review', MISSING_BODY_FIELD
        if pattern == [('newobj', EMPTY_MARKUP_LIST), ('newobj', MARKUP_RESULT),
                       ('callvirt', SET_PARSED_TEXT), ('stsfld', INVALID_LINE_FIELD)]:
            return 'error-fallback-text-needs-runtime-review', SET_PARSED_TEXT
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
    return stacked_argument_role(steps)


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
