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
PLAYER_LOG_SINKS = {
    *DEBUG_SINK_ARITY,
    'System.Void UnityEngine.Debug::LogException(System.Exception)',
    'System.Void UnityEngine.UI.StencilMaterial::LogWarningWhenNotInBatchmode(System.String,UnityEngine.Object)',
}
EXCEPTION_CONSTRUCTORS = {
    'System.Void System.ArgumentException::.ctor(System.String)',
    'System.Void System.ArgumentException::.ctor(System.String,System.Exception)',
    'System.Void System.ArgumentException::.ctor(System.String,System.String)',
    'System.Void System.ArgumentNullException::.ctor(System.String,System.String)',
    'System.Void System.ArgumentOutOfRangeException::.ctor(System.String)',
    'System.Void System.Exception::.ctor(System.String)',
    'System.Void System.InvalidOperationException::.ctor(System.String)',
    'System.Void System.NotSupportedException::.ctor(System.String)',
    'System.Void System.NullReferenceException::.ctor(System.String)',
    'System.Void UnityEngine.UnityException::.ctor(System.String)',
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
    ('newobj', BARK_NOTIFY, 0): 'preserve-exactly-dragon-transition-reason',
    ('newobj', BARK_TRANSITION, 0): 'preserve-exactly-dragon-transition-reason',
    ('newobj', BARK_SEX_ACT, 0): 'preserve-exactly-dragon-metadata',
    ('newobj', BARK_SEX_ACT, 2): 'preserve-exactly-animation-key',
    ('newobj', BARK_OVIPOSITION, 1): 'preserve-exactly-dragon-metadata',
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
        ({'Idle'}, 'preserve-exactly-dragon-metadata', 'System.String DragonBark::GetDescription()'),
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


DEFAULT_UI_NAMES = {
    'Panel': ('Panel', {}),
    'Button': ('Button (Legacy)', {'Text (Legacy)'}),
    'Text': ('Text (Legacy)', {}),
    'Image': ('Image', {}),
    'RawImage': ('RawImage', {}),
    'Slider': ('Slider', {'Background', 'Fill Area', 'Fill', 'Handle Slide Area', 'Handle'}),
    'Scrollbar': ('Scrollbar', {'Sliding Area', 'Handle'}),
    'Toggle': ('Toggle', {'Background', 'Checkmark', 'Label'}),
    'InputField': ('InputField (Legacy)', {'Placeholder', 'Text (Legacy)'}),
    'Dropdown': ('Dropdown (Legacy)', {'Label', 'Arrow', 'Template', 'Viewport', 'Content',
                                       'Item', 'Item Background', 'Item Checkmark', 'Item Label'}),
    'ScrollView': ('Scroll View', {'Viewport', 'Content'}),
}
DEFAULT_UI_METHODS = {
    f'UnityEngine.GameObject UnityEngine.UI.DefaultControls::Create{kind}(UnityEngine.UI.DefaultControls/Resources)':
        names for kind, names in DEFAULT_UI_NAMES.items()
}
UI_STENCIL_ADD = (
    'UnityEngine.Material UnityEngine.UI.StencilMaterial::Add(UnityEngine.Material,System.Int32,'
    'UnityEngine.Rendering.StencilOp,UnityEngine.Rendering.CompareFunction,UnityEngine.Rendering.ColorWriteMask,'
    'System.Int32,System.Int32)')
UI_STENCIL_KEYS = {'_Stencil', '_StencilOp', '_StencilComp', '_StencilReadMask', '_StencilWriteMask', '_ColorMask'}
UI_ARGUMENT_EXCEPTION = 'System.Void System.ArgumentException::.ctor(System.String)'
UI_PARAMETER_EXCEPTION = 'System.Void System.ArgumentException::.ctor(System.String,System.String)'
UI_EVENT_GET_LIST = (
    'System.Void UnityEngine.EventSystems.ExecuteEvents::GetEventList(UnityEngine.GameObject,'
    'System.Collections.Generic.IList`1<UnityEngine.EventSystems.IEventSystemHandler>)')
UI_EMPTY_INPUT_CONSUMERS = {
    'System.Void UnityEngine.UI.InputField::.ctor()': 'System.String UnityEngine.UI.InputField::m_OriginalText',
    'System.Void UnityEngine.UI.InputField::SetText(System.String,System.Boolean)':
        'UnityEngine.UI.InputField::SetText input normalization',
    'System.Void UnityEngine.UI.InputField::LateUpdate()': 'System.String UnityEngine.UI.InputField::m_Text',
    'UnityEngine.UI.InputField/EditState UnityEngine.UI.InputField::KeyPressed(UnityEngine.Event)':
        'System.Void UnityEngine.UI.InputField::set_clipboard(System.String)',
    'System.String UnityEngine.UI.InputField::GetSelectedString()': 'empty selection return value',
    'System.Void UnityEngine.UI.InputField::ActivateInputFieldInternal()': 'UnityEngine.TouchScreenKeyboard::Open',
    'System.Void UnityEngine.UI.Text::set_text(System.String)': 'System.String UnityEngine.UI.Text::m_Text',
}
UI_TEXT_REPRESENTATIONS = {
    'System.String UnityEngine.UI.LayoutRebuilder::ToString()',
    *{f'System.String UnityEngine.EventSystems.{owner}::ToString()' for owner in (
        'PointerEventData', 'EventSystem', 'PointerInputModule', 'TouchInputModule', 'RaycastResult', 'BaseRaycaster',
    )},
}
UI_DIAGNOSTICS = {
    'System.Void UnityEngine.UI.ToggleGroup::ValidateToggleIsInGroup(UnityEngine.UI.Toggle)': UI_ARGUMENT_EXCEPTION,
    'T UnityEngine.EventSystems.ExecuteEvents::ValidateEventData(UnityEngine.EventSystems.BaseEventData)':
        UI_ARGUMENT_EXCEPTION,
    'System.Void UnityEngine.EventSystems.EventSystem::set_current(UnityEngine.EventSystems.EventSystem)':
        'System.Void UnityEngine.Debug::LogError(System.Object)',
    ('System.Void UnityEngine.EventSystems.EventSystem::SetSelectedGameObject(UnityEngine.GameObject,'
     'UnityEngine.EventSystems.BaseEventData)'): 'System.Void UnityEngine.Debug::LogError(System.Object)',
    ('System.Boolean UnityEngine.EventSystems.ExecuteEvents::Execute(UnityEngine.GameObject,'
     'UnityEngine.EventSystems.BaseEventData,UnityEngine.EventSystems.ExecuteEvents/EventFunction`1<T>)'):
        'System.Void UnityEngine.Debug::LogException(System.Exception)',
}

DEBUG_LOG = 'System.Void UnityEngine.Debug::Log(System.Object)'
DEBUG_WARNING = 'System.Void UnityEngine.Debug::LogWarning(System.Object)'
DEBUG_WARNING_CONTEXT = 'System.Void UnityEngine.Debug::LogWarning(System.Object,UnityEngine.Object)'
DEBUG_ERROR = 'System.Void UnityEngine.Debug::LogError(System.Object)'
DEBUG_ERROR_CONTEXT = 'System.Void UnityEngine.Debug::LogError(System.Object,UnityEngine.Object)'
SET_OBJECT_NAME = 'System.Void UnityEngine.Object::set_name(System.String)'
TMP_ASSET_VERSION = 'System.String TMPro.TMP_Asset::m_Version'

TMP_DIAGNOSTICS = {
    'TMP_FontAsset::CreateFontAsset(System.String,System.String,System.Int32)': DEBUG_LOG,
    'TMP_FontAsset::TryAddGlyphInternal(System.UInt32,UnityEngine.TextCore.Glyph&)': DEBUG_WARNING_CONTEXT,
    'TMP_FontAsset::TryAddCharacterInternal(System.UInt32,TMPro.TMP_Character&)': DEBUG_WARNING_CONTEXT,
    'TMP_MaterialManager::ReleaseBaseMaterial(UnityEngine.Material)': DEBUG_LOG,
    'TMP_Text::CalculatePreferredValues(System.Single&,UnityEngine.Vector2,System.Boolean,TMPro.TextWrappingModes)':
        DEBUG_WARNING,
    'TMP_Text::ValidateHtmlTag(TMPro.TMP_Text/TextProcessingElement[],System.Int32,System.Int32&)': DEBUG_LOG,
    'TextMeshPro::OnPreRenderObject()': DEBUG_WARNING_CONTEXT,
    'TextMeshProUGUI::OnPreRenderCanvas()': DEBUG_WARNING_CONTEXT,
    **{f'{owner}::{method}': sink
       for owner in ('TextMeshPro', 'TextMeshProUGUI')
       for method, sink in (
           ('LoadFontAsset()', DEBUG_WARNING_CONTEXT),
           ('SetArraySizes(TMPro.TMP_Text/TextProcessingElement[])', DEBUG_WARNING_CONTEXT),
           ('GenerateTextMesh()', DEBUG_WARNING),
       )},
}
TMP_EMPTY_INPUT = {
    'TMP_InputField::.ctor()': 'System.String TMPro.TMP_InputField::m_OriginalText',
    'TMP_InputField::SetText(System.String,System.Boolean)': 'TMPro.TMP_InputField::SetText input normalization',
    'TMP_InputField::LateUpdate()': 'System.String TMPro.TMP_InputField::m_Text',
    'TMP_InputField::KeyPressed(UnityEngine.Event)': 'System.Void TMPro.TMP_InputField::set_clipboard(System.String)',
    'TMP_InputField::GetSelectedString()': 'empty selection return value',
    'TMP_InputField::ActivateInputFieldInternal()': 'UnityEngine.TouchScreenKeyboard::Open',
}
TMP_OBJECT_NAMES = {
    'TMP_Dropdown::AddItem(TMPro.TMP_Dropdown/OptionData,System.Boolean,TMPro.TMP_Dropdown/DropdownItem,'
    'System.Collections.Generic.List`1<TMPro.TMP_Dropdown/DropdownItem>)',
    'TextMeshPro::CreateMaterialInstance()',
    *{f'{owner}::CreateMaterialInstance(UnityEngine.Material)' for owner in ('TMP_SubMesh', 'TMP_SubMeshUI', 'TMP_Text')},
}
TMP_REPRESENTATIONS = {
    f'{owner}::ToString()' for owner in ('Extents', 'Mesh_Extents',
        'SpriteAssetUtilities.TexturePacker_JsonArray/SpriteFrame',
        'SpriteAssetUtilities.TexturePacker_JsonArray/SpriteSize')
}
TMP_ASCII_TABLES = {
    f'{owner}::{case}(System.{arg})'
    for owner, case, arg in (
        ('TMP_TextParsingUtilities', 'ToLowerASCIIFast', 'Char'),
        ('TMP_TextParsingUtilities', 'ToUpperASCIIFast', 'Char'),
        ('TMP_TextParsingUtilities', 'ToLowerASCIIFast', 'UInt32'),
        ('TMP_TextParsingUtilities', 'ToUpperASCIIFast', 'UInt32'),
        ('TMP_TextUtilities', 'ToLowerFast', 'Char'),
        ('TMP_TextUtilities', 'ToUpperFast', 'Char'),
        ('TMP_TextUtilities', 'ToUpperASCIIFast', 'UInt32'),
    )
}


def tmp_dependency_role(row):
    full_method, value, offset = row['method'], row['value'], row['ilOffset']
    method = full_method.split(' ', 1)[1].removeprefix('TMPro.')
    if method in TMP_DIAGNOSTICS:
        return 'diagnostic-text-needs-visibility-review', TMP_DIAGNOSTICS[method]
    if method == 'TMP_DynamicFontAssetUtilities::InitializeSystemFontReferenceCache()':
        return 'diagnostic-text-needs-visibility-review', DEBUG_WARNING if offset <= 126 else DEBUG_LOG
    if method == 'TMP_FontAsset::ReadFontAssetDefinition()':
        return 'diagnostic-text-needs-visibility-review', DEBUG_LOG if offset <= 433 else DEBUG_ERROR
    if method == 'TMP_SpriteAsset::UpgradeSpriteAsset()':
        if (value, offset) == ('1.1.0', 1):
            return 'preserve-exactly-version', TMP_ASSET_VERSION
        return 'diagnostic-text-needs-visibility-review', 'System.Void UnityEngine.Debug::Log(System.Object,UnityEngine.Object)'
    if method in TMP_EMPTY_INPUT and not value:
        return 'preserve-exactly-empty-value', TMP_EMPTY_INPUT[method]
    if method == 'TMP_InputField::SetText(System.String,System.Boolean)' and value == '\0':
        return 'preserve-exactly-input-control', 'System.String System.String::Replace(System.String,System.String)'
    if method == 'TMP_InputField::Validate(System.String,System.Int32,System.Char)':
        return 'preserve-exactly-input-control', 'System.Int32 System.String::IndexOf(System.Char)'
    if method == 'TMP_InputField::UpdateLabel()' and value in ('<u>', '</u>', '\u200b'):
        return ('preserve-exactly-markup' if value.startswith('<') else 'preserve-exactly-input-control',
                'System.Void TMPro.TMP_Text::set_text(System.String)')
    if method == 'TMP_InputField::OnEnable()' and value == 'Caret':
        return 'preserve-exactly-object-name', 'System.Void UnityEngine.GameObject::.ctor(System.String,System.Type[])'
    if method in TMP_OBJECT_NAMES:
        return 'preserve-exactly-object-name', SET_OBJECT_NAME
    if method == 'TMP_FontAsset::.cctor()' and value == ' Atlas Material':
        return 'preserve-exactly-object-name', 'System.String TMPro.TMP_FontAsset::s_DefaultMaterialSuffix'
    if method in TMP_ASCII_TABLES:
        return 'preserve-exactly-input-control', 'System.Char System.String::get_Chars(System.Int32)'
    if method in TMP_REPRESENTATIONS or method == 'TextProcessingElement::DebuggerDisplay()':
        return 'string-representation-needs-visibility-review', full_method
    if method == ('TMP_FontAsset::CreateFontAssetInstance(UnityEngine.Font,System.Int32,'
                  'UnityEngine.TextCore.LowLevel.GlyphRenderMode,System.Int32,System.Int32,TMPro.AtlasPopulationMode,System.Boolean)'):
        return 'preserve-exactly-version', TMP_ASSET_VERSION
    if method == 'TMP_Settings::get_version()':
        return 'preserve-exactly-version', full_method
    if method == 'TMP_Settings::.cctor()' and value == '2':
        return 'preserve-exactly-version', 'System.String TMPro.TMP_Settings::s_CurrentAssetVersion'
    if method == 'TMP_ResourceManager::.cctor()' and value == 'Regular':
        return 'preserve-exactly-font-style-key', 'System.Int32 TMPro.TMP_TextUtilities::GetHashCode(System.String)'
    if method in ('TMP_Style::get_NormalStyle()', 'TMP_StyleSheet::LoadStyleDictionaryInternal()') and value == 'Normal':
        return ('preserve-exactly-font-style-key',
                'System.Int32 TMPro.TMP_TextParsingUtilities::GetHashCode(System.String)' if offset == 141 else
                'System.Void TMPro.TMP_Style::.ctor(System.String,System.String,System.String)')
    return None


YARN_MARKER_PROCESSOR_ARGS = (
    '(Yarn.Markup.MarkupAttribute,System.Text.StringBuilder,'
    'System.Collections.Generic.List`1<Yarn.Markup.MarkupAttribute>,System.String)')
YARN_MARKUP_DIAGNOSTIC = 'System.Void Yarn.Markup.LineParser/MarkupDiagnostic::.ctor(System.String,System.Int32)'
YARN_MARKUP_LOOKUP = ('System.Boolean System.Collections.Generic.IReadOnlyDictionary`2<'
                      'System.String,Yarn.Markup.MarkupValue>::TryGetValue(!0,!1&)')
YARN_DIAGNOSTICS = {
    'PaletteMarkerProcessor::ProcessReplacementMarker' + YARN_MARKER_PROCESSOR_ARGS: YARN_MARKUP_DIAGNOSTIC,
    'Actions::CreateConverters(System.Reflection.MethodInfo)': UI_ARGUMENT_EXCEPTION,
    'Actions/<>c__DisplayClass22_0::<CreateConverterFunction>b__3(System.String,System.Int32)':
        UI_ARGUMENT_EXCEPTION,
    'Actions/<>c__DisplayClass22_0::<CreateConverterFunction>b__4(System.String,System.Int32)':
        'System.Void System.ArgumentException::.ctor(System.String,System.Exception)',
    'DialogueRunner::get_LineProvider()': DEBUG_WARNING_CONTEXT,
    'DialogueRunner/<OnOptionsReceivedAsync>d__81::MoveNext()': DEBUG_ERROR,
    'BuiltinLocalisedLineProvider/<GetLocalizedLineAsync>d__15::MoveNext()': DEBUG_WARNING_CONTEXT,
    'Cultures::GetCulture(System.String)': UI_PARAMETER_EXCEPTION,
    'GeneratedVariableStorageExtensions::GetValueOrDefault(Yarn.Unity.IGeneratedVariableStorage,System.String)': DEBUG_LOG,
    'GeneratedVariableStorageExtensions::SetValue(Yarn.Unity.IGeneratedVariableStorage,System.String,T)':
        'System.Void System.ArgumentOutOfRangeException::.ctor(System.String)',
    'GeneratedVariableStorageExtensions::GetEnumValueOrDefault(Yarn.Unity.IGeneratedVariableStorage,System.String)':
        DEBUG_ERROR,
    'InMemoryVariableStorage::SetAllVariables(System.Collections.Generic.Dictionary`2<System.String,System.Single>,'
    'System.Collections.Generic.Dictionary`2<System.String,System.String>,'
    'System.Collections.Generic.Dictionary`2<System.String,System.Boolean>,System.Boolean)': DEBUG_LOG,
    'LinePresenter/<RunLineAsync>d__23::MoveNext()': DEBUG_ERROR,
    'YarnProject::get_InitialValues()': DEBUG_WARNING,
}
YARN_DIAGNOSTIC_FORMATS = {
    'DiagnosticUtility::EnglishPluraliseNounCount(System.Int32,System.String,System.Boolean)',
    'DiagnosticUtility::EnglishPluraliseWasVerb(System.Int32)',
    'InMemoryVariableStorage::GetDebugList()',
    'LineMetadataTableEntry::ToString()',
    'StringTableEntry::ToString()',
}


def yarn_dependency_role(row):
    full_method, value, offset = row['method'], row['value'], row['ilOffset']
    method = full_method.split(' ', 1)[1].removeprefix('Yarn.Unity.')
    if method in YARN_DIAGNOSTICS:
        return 'diagnostic-text-needs-visibility-review', YARN_DIAGNOSTICS[method]
    if method in YARN_DIAGNOSTIC_FORMATS:
        return 'string-representation-needs-visibility-review', full_method
    if method == 'Actions::GetFullMethodName(System.Reflection.MethodInfo)' and value == '.':
        return 'preserve-exactly-format', full_method
    if method in ('Actions/CommandRegistration::.ctor(System.String,System.Delegate)',
                  'Actions/CommandRegistration::.ctor(System.String,System.Reflection.MethodInfo)'):
        if value in ('number', 'string', 'bool'):
            return ('preserve-exactly-command-help-template',
                    'System.Collections.Generic.Dictionary`2<System.Type,System.String> '
                    'Yarn.Unity.Actions/CommandRegistration::TypeFriendlyNames')
        return 'diagnostic-text-needs-visibility-review', UI_ARGUMENT_EXCEPTION
    if method == 'Actions/CommandRegistration::get_UsageString()':
        return 'preserve-exactly-command-help-template', full_method
    if method == 'Actions/CommandRegistration::TryParseArgs(System.String[],System.Object[]&,System.String&)':
        if offset == 0x2ae:
            return ('diagnostic-text-needs-visibility-review',
                    'System.Void System.InvalidOperationException::.ctor(System.String)')
        return ('preserve-exactly-command-diagnostic',
                'Yarn.Unity.Actions/CommandRegistration::TryParseArgs error result')
    if method == ('Actions/CommandRegistration::Invoke(UnityEngine.MonoBehaviour,'
                  'System.Collections.Generic.List`1<System.String>)'):
        if offset < 0x109:
            return 'preserve-exactly-command-diagnostic', 'System.String Yarn.Unity.CommandDispatchResult::Message'
        return ('diagnostic-text-needs-visibility-review',
                'System.Void System.InvalidOperationException::.ctor(System.String)')
    if method == 'DialogueRunner/<OnCommandReceivedAsync>d__76::MoveNext()':
        if offset == 475:
            return ('diagnostic-text-needs-visibility-review',
                    'System.Void System.ArgumentOutOfRangeException::.ctor(System.String)')
        return 'diagnostic-text-needs-visibility-review', DEBUG_ERROR_CONTEXT if offset < 296 else DEBUG_ERROR
    if method == 'VariableStorageBehaviour::AddChangeListener(System.String,System.Action`1<T>)':
        return 'diagnostic-text-needs-visibility-review', UI_ARGUMENT_EXCEPTION
    if method == 'DialogueRunner::.ctor()' and value == 'Start':
        return 'preserve-exactly-yarn-node-reference', 'System.String Yarn.Unity.DialogueRunner::startNode'
    if method == 'LocalizedLine::get_CharacterName()' and value == 'name':
        return 'preserve-exactly-markup-key', YARN_MARKUP_LOOKUP
    if method == 'Cultures::MakeCultureList()':
        return {
            'mi': ('preserve-exactly-locale-key', 'System.String Yarn.Unity.Culture::Name'),
            'Maori': ('locale-name-needs-visibility-review', 'System.String Yarn.Unity.Culture::DisplayName'),
            'Māori': ('preserve-exactly-locale-name', 'System.String Yarn.Unity.Culture::NativeName'),
        }.get(value)
    if method == 'Localization::GetAddressForLine(System.String,System.String)' and value in ('line_', '_', 'line:', ''):
        return 'preserve-exactly-resource-key', full_method
    if method == 'LineAdvancer::ValidateInputMode()':
        return 'editor-message-needs-visibility-review', 'Yarn.Unity.Attributes.MessageBoxAttribute/Message'
    if method in ('MarkupPalette::PaletteForMarker(System.String,Yarn.Unity.MarkupPalette/CustomMarker&)',
                  'OptionItem::set_Option(Yarn.Unity.DialogueOption)') and value.startswith('<'):
        return 'preserve-exactly-markup', (
            'Yarn.Unity.MarkupPalette/CustomMarker::Start or End' if method.startswith('MarkupPalette::') else
            'System.Void TMPro.TMP_Text::set_text(System.String)')
    if method == 'OptionsPresenter/<RunOptionsAsync>d__18::MoveNext()' and value == '...':
        return 'preserve-exactly-format', 'System.Void TMPro.TMP_Text::set_text(System.String)'
    if method == 'PauseEventProcessor::OnLineDisplayBegin(Yarn.Markup.MarkupParseResult,TMPro.TMP_Text)':
        if value == 'pause':
            return 'preserve-exactly-markup-key', YARN_MARKUP_LOOKUP
        return 'diagnostic-text-needs-visibility-review', DEBUG_WARNING
    if method == 'StyleMarkerProcessor::ProcessReplacementMarker' + YARN_MARKER_PROCESSOR_ARGS:
        if value in ('<style="', '">', '</style>'):
            return ('preserve-exactly-markup',
                    'System.Text.StringBuilder System.Text.StringBuilder::Append(System.String)' if offset == 77 else
                    'System.Text.StringBuilder System.Text.StringBuilder::Insert(System.Int32,System.String)')
        return 'diagnostic-text-needs-visibility-review', YARN_MARKUP_DIAGNOSTIC
    if method in ('LineMetadata::AddMetadata(System.Collections.Generic.IEnumerable`1<Yarn.Unity.LineMetadataTableEntry>)',
                  'LineMetadata::AddMetadata(System.String,System.Collections.Generic.IEnumerable`1<System.String>)') and value == ' ':
        return 'preserve-exactly-metadata-format', 'System.String::Join'
    if method in ('LineMetadata::GetShadowLineSource(System.String)',
                  'UnityLocalization.LineMetadata::get_ShadowLineSource()') and value in ('line:', 'shadow:'):
        return 'preserve-exactly-metadata-key', full_method
    if method in ('LineMetadataTableEntry::CreateCSV(System.Collections.Generic.IEnumerable`1<Yarn.Unity.LineMetadataTableEntry>)',
                  'StringTableEntry::CreateCSV(System.Collections.Generic.IEnumerable`1<Yarn.Unity.StringTableEntry>)'):
        return 'preserve-exactly-csv-format', 'System.Void CsvHelper.CsvWriter::WriteField(System.String)'
    if method in ('YarnTask::op_Implicit(System.Threading.Tasks.Task)', 'YarnTask`1::op_Implicit(UnityEngine.Awaitable`1<T>)'):
        return ('preserve-exactly-parameter-name' if value in ('task', 'awaitable') else
                'diagnostic-text-needs-visibility-review',
                'System.Void System.ArgumentNullException::.ctor(System.String,System.String)')
    if method == 'UnityLocalization.LineMetadata::.ctor()' and not value:
        return 'preserve-exactly-empty-value', 'System.String Yarn.Unity.UnityLocalization.LineMetadata::nodeName'
    if method == 'UnityLocalization.UnityLocalisedLineProvider/<GetLocalizedLineAsync>d__8::MoveNext()':
        if offset == 287:
            return ('error-fallback-text-needs-runtime-review',
                    'Yarn.Unity.UnityLocalization.UnityLocalisedLineProvider/<GetLocalizedLineAsync>d__8::<text>5__3')
        if offset == 513:
            return 'diagnostic-text-needs-visibility-review', DEBUG_WARNING
    return None


def dependency_role(row, assembly):
    method, value, offset = row['method'], row['value'], row['ilOffset']
    if assembly == 'UnityScriptableSettings' and (
            method, value, offset) == (
            'ScriptableSettingString[] UnityScriptableSettings.SettingResolution::GetLocalizedDropdowns()',
            '{0} x {1}', 77):
        return 'preserve-exactly-resolution-format', 'System.String System.String::Format(System.String,System.Object,System.Object)'
    if assembly == 'Unity.TextMeshPro':
        return tmp_dependency_role(row)
    if assembly == 'YarnSpinner.Unity':
        return yarn_dependency_role(row)
    if assembly != 'UnityEngine.UI':
        return None
    names = DEFAULT_UI_METHODS.get(method)
    if names:
        root, children = names
        if offset == 0 and value == root:
            return 'preserve-exactly-object-name', (
                'UnityEngine.GameObject UnityEngine.UI.DefaultControls::CreateUIElementRoot('
                'System.String,UnityEngine.Vector2,System.Type[])')
        if value in children:
            return 'preserve-exactly-object-name', (
                'UnityEngine.GameObject UnityEngine.UI.DefaultControls::CreateUIObject('
                'System.String,UnityEngine.GameObject,System.Type[])')
    if method in UI_TEXT_REPRESENTATIONS:
        return 'string-representation-needs-visibility-review', method
    if method in UI_DIAGNOSTICS:
        return 'diagnostic-text-needs-visibility-review', UI_DIAGNOSTICS[method]
    if method in UI_EMPTY_INPUT_CONSUMERS and not value:
        return 'preserve-exactly-empty-value', UI_EMPTY_INPUT_CONSUMERS[method]
    if method == 'System.Void UnityEngine.UI.InputField::SetText(System.String,System.Boolean)' and value in ('\0', '\n', '\t'):
        return 'preserve-exactly-input-control', 'System.String System.String::Replace(System.String,System.String)'
    if method == 'System.Char UnityEngine.UI.InputField::Validate(System.String,System.Int32,System.Char)' and value == "!#$%&'*+-/=?^_`{|}~":
        return 'preserve-exactly-input-control', 'System.Int32 System.String::IndexOf(System.Char)'
    if method == 'System.Void UnityEngine.UI.InputField::UpdateGeometry()' and value == ' Input Caret':
        return 'preserve-exactly-object-name', 'System.Void UnityEngine.GameObject::.ctor(System.String,System.Type[])'
    if method == 'System.Void UnityEngine.UI.CanvasUpdateRegistry::.ctor()' and value in {
            'CanvasUpdate.Prelayout', 'CanvasUpdate.Layout', 'CanvasUpdate.PostLayout',
            'CanvasUpdate.PreRender', 'CanvasUpdate.LatePreRender'}:
        return 'profiler-label', 'System.String[] UnityEngine.UI.CanvasUpdateRegistry::m_CanvasUpdateProfilerStrings'
    if method == 'System.Void UnityEngine.UI.ReflectionMethodsCache::.ctor()' and value in {
            'Raycast', 'RaycastAll', 'RaycastNonAlloc', 'GetRayIntersectionAll', 'GetRayIntersectionNonAlloc'}:
        return 'preserve-exactly-reflection-member', 'System.Reflection.MethodInfo System.Type::GetMethod(System.String,System.Type[])'
    if method == UI_EVENT_GET_LIST:
        if value == 'results':
            return 'preserve-exactly-parameter-name', UI_PARAMETER_EXCEPTION
        if value == 'Results array is null':
            return 'diagnostic-text-needs-visibility-review', UI_PARAMETER_EXCEPTION
    if method == UI_STENCIL_ADD:
        if value in UI_STENCIL_KEYS or value == '_UseUIAlphaClip':
            return 'preserve-exactly-renderer-key', 'System.Void UnityEngine.Material::SetFloat(System.String,System.Single)'
        if value == 'Material ' or value in {f" doesn't have {key} property" for key in UI_STENCIL_KEYS}:
            return 'diagnostic-text-needs-visibility-review', (
                'System.Void UnityEngine.UI.StencilMaterial::LogWarningWhenNotInBatchmode(System.String,UnityEngine.Object)')
        if value == 'Stencil Id:{0}, Op:{1}, Comp:{2}, WriteMask:{3}, ReadMask:{4}, ColorMask:{5} AlphaClip:{6} ({7})':
            return 'preserve-exactly-object-name', 'System.Void UnityEngine.Object::set_name(System.String)'
    if method == ('UnityEngine.UI.Dropdown/DropdownItem UnityEngine.UI.Dropdown::AddItem('
                  'UnityEngine.UI.Dropdown/OptionData,System.Boolean,UnityEngine.UI.Dropdown/DropdownItem,'
                  'System.Collections.Generic.List`1<UnityEngine.UI.Dropdown/DropdownItem>)') and value in {'Item ', '', ': '}:
        return 'preserve-exactly-object-name', 'System.Void UnityEngine.Object::set_name(System.String)'
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
        if role == 'engine-default-text-needs-visibility-review' and row['method'].startswith((
                'UnityEngine.GameObject UnityEngine.UI.DefaultControls::Create',
                'UnityEngine.GameObject TMPro.TMP_DefaultControls::Create')):
            role = 'preserve-exactly-engine-factory-template'
        if (assembly == 'Unity.TextMeshPro' and row['method'] == 'System.Void TMPro.TMP_Dropdown::.cctor()'
                and row['value'] in ('Nothing', 'Everything', 'Mixed...')):
            role = 'preserve-exactly-unused-multiselect-label'
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
        roles[rows[0]['id']] = ('preserve-exactly-unbound-objective-label', 'ObjectiveDisplay.SetObjective')
    return roles
