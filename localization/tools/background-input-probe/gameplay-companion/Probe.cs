using System.Reflection;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.Events;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;
using UnityEngine.SceneManagement;
using UnityEngine.UI;

namespace Dragons.BackgroundInputProbe;

public static class Probe
{
    private static Keyboard? keyboard;
    private static Mouse? mouse;
    private static Vector2 pointer;
    private static float next;
    private static int stage;
    private static int mainScene;
    private static int equipmentTarget;
    private static int attempts;
    private static bool moving;
    private static Component? target;
    private static Component? mountCrate, insertCrate;
    private static Camera? playerCamera;
    private static float waitDeadline;
    private static bool introStarted, introCompleted, dialogueCompleted, advanceDown;
    private static int choiceIndex, optionClickPhase;
    private static float nextInspect;
    private static readonly string[] IntroChoices = { "line:83ac5b68", "line:0b7589ff", "line:4d692a01" };
    private static readonly Assembly Game = Assembly.Load("Assembly-CSharp");

    public static void Start()
    {
        if (stage != 0) return;
        if (!Application.identifier.StartsWith("com.codex.test.dragnwash.probe", StringComparison.Ordinal) ||
            !Application.isBatchMode)
            throw new InvalidOperationException("Expected isolated batch-mode profile");
        Application.runInBackground = true;
        keyboard = InputSystem.AddDevice<Keyboard>();
        mouse = InputSystem.AddDevice<Mouse>();
        mainScene = SceneManager.GetActiveScene().handle;
        stage = 1;
        next = Time.realtimeSinceStartup + 3;
        InputSystem.onAfterUpdate += Tick;
        InputSystem.onActionChange += ObserveAction;
        SceneManager.sceneLoaded += (scene, mode) =>
            Debug.Log($"VN-BG-SCENE {scene.name} index={scene.buildIndex} mode={mode}");
        Debug.Log($"VN-BG-PATH {Application.persistentDataPath}");
    }

    private static void Tick()
    {
        if (Time.realtimeSinceStartup < next || keyboard == null || mouse == null) return;
        next = Time.realtimeSinceStartup + 0.4f;
        try
        {
            switch (stage)
            {
                case 1: AimAt("MenuMain", "loadButton"); break;
                case 2: ClickDown(); break;
                case 3: SetPointer(false); next += 1f; break;
                case 4: AimAt("MenuSlotsLoad", "slot1Button"); break;
                case 5: ClickDown(); break;
                case 6: SetPointer(false); next += 4f; break;
                case 7:
                    if (SceneManager.GetActiveScene().handle == mainScene || Camera.main == null) return;
                    playerCamera = Camera.main;
                    ObserveYarnNodes();
                    if (Flag("BuiltMount") || Flag("PlacedMount") || Flag("HasMountFrame"))
                        throw new InvalidOperationException("Mount state already set at scene entry");
                    Debug.Log("VN-BG-MOUNT-BASELINE BuiltMount=False PlacedMount=False HasMountFrame=False");
                    next += 0.5f;
                    break;
                case 8:
                    if (equipmentTarget == 8 && DragonStateCode() != 2)
                    {
                        if (Time.realtimeSinceStartup >= waitDeadline)
                            throw new InvalidOperationException("The dragon did not become ready at the window");
                        return;
                    }
                    if (!TryAimForEquipment()) return;
                    break;
                case 9:
                    if (CachedTarget() != target)
                        throw new InvalidOperationException("Stock selector changed before input");
                    Debug.Log($"VN-BG-USE step={equipmentTarget} {target!.name}");
                    InputState.Change(keyboard, new KeyboardState(Key.E));
                    break;
                case 10:
                    InputState.Change(keyboard, new KeyboardState());
                    VerifyEquipment();
                    if (equipmentTarget == 7)
                    {
                        Debug.Log($"VN-BG-MOUNT-FINAL HasMountFrame={Flag("HasMountFrame")} PlacedMount={Flag("PlacedMount")}");
                        waitDeadline = Time.realtimeSinceStartup + 45;
                    }
                    if (equipmentTarget++ < 8)
                    {
                        attempts = 0;
                        stage = 8;
                        return;
                    }
                    waitDeadline = Time.realtimeSinceStartup + 12;
                    next += 3;
                    break;
                case 11:
                    if (!introStarted && Time.realtimeSinceStartup < waitDeadline) return;
                    var dragonState = SceneStateType.GetMethod("GetDragonState", StaticMembers)?.Invoke(null, null);
                    Debug.Log($"VN-BG-INTRO started={introStarted} state={dragonState}");
                    if (!introStarted) throw new InvalidOperationException("The window input did not start Conrad's intro");
                    waitDeadline = Time.realtimeSinceStartup + 65;
                    break;
                case 12:
                    if (dialogueCompleted && introCompleted)
                    {
                        if (choiceIndex != IntroChoices.Length)
                            throw new InvalidOperationException("Intro completed without the expected choices");
                        var state = SceneStateType.GetMethod("GetDragonState", StaticMembers)?.Invoke(null, null);
                        Debug.Log($"VN-BG-INTRO-FINAL choices={choiceIndex} state={state}");
                        Finish();
                        break;
                    }
                    if (Time.realtimeSinceStartup >= waitDeadline)
                        throw new InvalidOperationException("Ordinary intro input timed out");
                    AdvanceIntro();
                    return;
            }
            stage++;
        }
        catch (Exception error)
        {
            Debug.Log($"VN-BG-FAIL stage={stage} {error}");
            Finish();
        }
    }

    private const BindingFlags InstanceMembers = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance;
    private const BindingFlags StaticMembers = BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Static;
    private static readonly Type InteractableType = Game.GetType("Interactable", throwOnError: true)!;
    private static readonly Type ToolManagerType = Game.GetType(
        "com.gatordragongames.washnwalk.tools.ToolManager", throwOnError: true)!;
    private static readonly Type SceneStateType = Game.GetType("WalkNWashSceneState", throwOnError: true)!;

    private static void ObserveYarnNodes()
    {
        var type = Assembly.Load("YarnSpinner.Unity").GetType("Yarn.Unity.DialogueRunner", throwOnError: true)!;
        var runners = UnityEngine.Object.FindObjectsByType(type, FindObjectsInactive.Include, FindObjectsSortMode.None);
        int listeners = 0;
        foreach (var runner in runners)
        {
            if (type.GetField("onNodeStart", InstanceMembers)?.GetValue(runner) is not UnityEvent<string> start)
                continue;
            start.AddListener(node => {
                Debug.Log($"VN-BG-YARN-START {node}");
                if (node == "Conrad_Intro_3") introStarted = true;
            });
            if (type.GetField("onNodeComplete", InstanceMembers)?.GetValue(runner) is UnityEvent<string> complete)
                complete.AddListener(node => {
                    Debug.Log($"VN-BG-YARN-COMPLETE {node}");
                    if (node == "Conrad_Intro_3") introCompleted = true;
                });
            if (type.GetField("onDialogueComplete", InstanceMembers)?.GetValue(runner) is UnityEvent dialogue)
                dialogue.AddListener(() => {
                    Debug.Log("VN-BG-YARN-DIALOGUE-COMPLETE");
                    if (introCompleted) dialogueCompleted = true;
                });
            listeners++;
        }
        if (listeners == 0) throw new InvalidOperationException("No original Yarn node event available");
        Debug.Log($"VN-BG-YARN-LISTENERS {listeners}");
    }

    private static void InspectDialogue()
    {
        var unity = Assembly.Load("YarnSpinner.Unity");
        foreach (var name in new[] { "LinePresenter", "LineAdvancer", "OptionItem" })
        {
            var type = unity.GetType("Yarn.Unity." + name, throwOnError: true)!;
            foreach (var item in UnityEngine.Object.FindObjectsByType(type, FindObjectsInactive.Include, FindObjectsSortMode.None).OfType<Behaviour>())
            {
                if (name == "LinePresenter")
                {
                    var text = type.GetField("lineText", InstanceMembers)?.GetValue(item);
                    var shown = text?.GetType().GetProperty("text")?.GetValue(text) as string;
                    var visible = text?.GetType().GetProperty("maxVisibleCharacters")?.GetValue(text);
                    var group = type.GetField("canvasGroup", InstanceMembers)?.GetValue(item) as CanvasGroup;
                    Debug.Log($"VN-BG-LINE active={item.isActiveAndEnabled} alpha={group?.alpha} visible={visible} text={shown?.Replace("\n", " ")}");
                }
                if (name == "LineAdvancer")
                {
                    var mode = type.GetField("inputMode", InstanceMembers)?.GetValue(item);
                    var action = (type.GetField("nextLineAction", InstanceMembers)?.GetValue(item) as InputActionReference)?.action;
                    Debug.Log($"VN-BG-ADVANCER active={item.isActiveAndEnabled} mode={mode} action={action?.actionMap?.name}/{action?.name} enabled={action?.enabled} controls={string.Join(",", action?.controls.Select(c => c.path) ?? Array.Empty<string>())}");
                }
                if (name == "OptionItem" && item.isActiveAndEnabled)
                {
                    var option = type.GetField("_option", InstanceMembers)?.GetValue(item);
                    var textId = option?.GetType().GetField("TextID", InstanceMembers)?.GetValue(option) as string;
                    var view = (Selectable)item;
                    var savedPointer = pointer;
                    var raycast = TryAimAt(view);
                    pointer = savedPointer;
                    Debug.Log($"VN-BG-OPTION-VIEW {textId} enabled={view.IsInteractable()} raycast={raycast}");
                }
            }
        }
    }

    private static void AdvanceIntro()
    {
        if (Time.realtimeSinceStartup >= nextInspect)
        {
            nextInspect = Time.realtimeSinceStartup + 2;
            InspectDialogue();
        }
        if (advanceDown)
        {
            InputState.Change(keyboard!, new KeyboardState());
            advanceDown = false;
            return;
        }
        if (optionClickPhase == 1)
        {
            SetPointer(true);
            optionClickPhase = 2;
            return;
        }
        if (optionClickPhase == 2)
        {
            SetPointer(false);
            optionClickPhase = 0;
            choiceIndex++;
            next += .5f;
            return;
        }
        var optionType = Assembly.Load("YarnSpinner.Unity").GetType("Yarn.Unity.OptionItem", throwOnError: true)!;
        var views = UnityEngine.Object.FindObjectsByType(optionType, FindObjectsSortMode.None).OfType<Selectable>()
            .Where(view => view.isActiveAndEnabled && view.IsInteractable()).ToArray();
        if (views.Length != 0)
        {
            if (choiceIndex >= IntroChoices.Length) return;
            var choice = IntroChoices[choiceIndex];
            foreach (var view in views)
            {
                var option = optionType.GetField("_option", InstanceMembers)?.GetValue(view);
                var textId = option?.GetType().GetField("TextID", InstanceMembers)?.GetValue(option) as string;
                if (textId != choice || !TryAimAt(view)) continue;
                Debug.Log($"VN-BG-YARN-CHOICE {choice}");
                SetPointer(false);
                optionClickPhase = 1;
                break;
            }
            return;
        }
        InputState.Change(keyboard!, new KeyboardState(Key.E));
        advanceDown = true;
    }

    private static Component? CachedTarget() =>
        InteractableType.GetMethod("GetCachedInteractable", StaticMembers)?.Invoke(null, null) as Component;

    private static int DragonStateCode() =>
        Convert.ToInt32(SceneStateType.GetMethod("GetDragonState", StaticMembers)!.Invoke(null, null));

    private static bool Flag(string name) =>
        (bool)SceneStateType.GetMethod("GetFlag", StaticMembers, null, new[] { typeof(string) }, null)!
            .Invoke(null, new object[] { name });

    private static UnityEngine.Object? GetTool(string method) =>
        ToolManagerType.GetMethod(method, StaticMembers)?.Invoke(null, null) as UnityEngine.Object;

    private static Component EquipmentTarget()
    {
        var candidates = UnityEngine.Object.FindObjectsByType(InteractableType, FindObjectsSortMode.None).OfType<Component>();
        return equipmentTarget switch
        {
            0 or 3 => candidates.Single(c => c.name == "crowbar_socket"),
            1 => candidates.Single(c => c.name == "ShipmentCrateMountFrame"),
            2 => candidates.Single(c => c.name == "ShipmentCrateMountFrame (1)"),
            4 => candidates.Single(c => c.name == "Onahole_Socket" && c.transform.IsChildOf(insertCrate!.transform)),
            5 => candidates.Single(c => Equals(c.GetType().GetField("placeFlag", InstanceMembers)?.GetValue(c), "BuiltMount")),
            6 => candidates.Single(c => c.name == "MountFrame_Socket_Complete" && c.transform.IsChildOf(mountCrate!.transform)),
            7 => candidates.Single(c => Equals(c.GetType().GetField("placeFlag", InstanceMembers)?.GetValue(c), "PlacedMount")),
            8 => candidates.Single(c => c.name == "DragonWindow" && c.GetType().Name == "InteractableDragonWindow"),
            _ => throw new InvalidOperationException("Unexpected equipment step"),
        };
    }

    private static bool TryAimForEquipment()
    {
        var view = playerCamera!.transform;
        target = EquipmentTarget();
        var name = target.name;
        if (++attempts > 100) throw new InvalidOperationException("Equipment target timed out: " + name);
        if (moving)
        {
            InputState.Change(keyboard!, new KeyboardState());
            moving = false;
            return false;
        }
        var offset = target.transform.position - view.position;
        var candidate = CachedTarget();
        var horizontal = Vector3.ProjectOnPlane(offset, Vector3.up);
        var yaw = Vector3.SignedAngle(Vector3.ProjectOnPlane(view.forward, Vector3.up), horizontal, Vector3.up);
        var pitch = Mathf.Atan2(offset.y, horizontal.magnitude) * Mathf.Rad2Deg -
            Mathf.Asin(Mathf.Clamp(view.forward.y, -1, 1)) * Mathf.Rad2Deg;
        Debug.Log($"VN-BG-GUIDE step={equipmentTarget} {name} position={view.position:F3} forward={view.forward:F3} distance={offset.magnitude:F3} yaw={yaw:F3} pitch={pitch:F3} cached={candidate?.name}");
        if (candidate == target) return true;
        if (Mathf.Abs(yaw) > 6 || (offset.magnitude < 2.9f && Mathf.Abs(pitch) > 6))
        {
            var delta = new Vector2(Mathf.Clamp(yaw * 8f, -100, 100),
                offset.magnitude < 2.9f ? Mathf.Clamp(pitch * 8f, -100, 100) : 0);
            InputState.Change(mouse!, new MouseState { position = pointer, delta = delta });
            return false;
        }
        if (offset.magnitude >= 2.9f)
        {
            InputState.Change(keyboard!, new KeyboardState(Key.W));
            moving = true;
            next = Time.realtimeSinceStartup + .25f;
            return false;
        }
        throw new InvalidOperationException("Stock selector did not accept " + name);
    }

    private static void VerifyEquipment()
    {
        var tool = GetTool("GetCurrentTool");
        var expectedTool = target!.GetType().GetField("tool", InstanceMembers)?.GetValue(target) as UnityEngine.Object;
        var emptyTool = GetTool("GetEmptyTool");
        var opened = target.GetType().GetField("opened", InstanceMembers)?.GetValue(target);
        Debug.Log($"VN-BG-EQUIPMENT step={equipmentTarget} target={target.name} tool={tool?.name} expected={expectedTool?.name} opened={opened} BuiltMount={Flag("BuiltMount")} HasMountFrame={Flag("HasMountFrame")} PlacedMount={Flag("PlacedMount")}");
        switch (equipmentTarget)
        {
            case 0 or 4 or 6:
                if (expectedTool == null || expectedTool != tool)
                    throw new InvalidOperationException("The equipped tool did not match the socket's asset");
                break;
            case 1 or 2:
                if (opened is not true) throw new InvalidOperationException("The crate did not open");
                if (equipmentTarget == 1) mountCrate = target;
                else insertCrate = target;
                break;
            case 3:
                if (emptyTool == null || tool != emptyTool)
                    throw new InvalidOperationException("The crowbar was not returned");
                break;
            case 5:
                if (emptyTool == null || tool != emptyTool || !Flag("BuiltMount"))
                    throw new InvalidOperationException("The mount was not assembled by the stock handler");
                break;
            case 7:
                if (emptyTool == null || tool != emptyTool || !Flag("PlacedMount") || !Flag("HasMountFrame"))
                    throw new InvalidOperationException("The frame was not placed by the stock handler");
                break;
        }
    }

    private static void AimAt(string typeName, string fieldName)
    {
        var type = Game.GetType(typeName, throwOnError: true)!;
        var component = UnityEngine.Object.FindObjectsByType(type, FindObjectsSortMode.None).Single();
        var field = type.GetField(fieldName, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
        if (field?.GetValue(component) is not Button button || !button.isActiveAndEnabled || !button.IsInteractable())
            throw new InvalidOperationException($"Unavailable button {typeName}.{fieldName}");
        if (!TryAimAt(button))
            throw new InvalidOperationException($"Raycast missed {typeName}.{fieldName}");
        Debug.Log($"VN-BG-AIM {typeName}.{fieldName} button={button.name} {pointer} screen={Screen.width}x{Screen.height}");
        SetPointer(false);
    }

    private static bool TryAimAt(Selectable control)
    {
        var rect = (RectTransform)control.transform;
        var canvas = control.GetComponentInParent<Canvas>();
        var camera = canvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : canvas.worldCamera;
        pointer = RectTransformUtility.WorldToScreenPoint(camera, rect.TransformPoint(rect.rect.center));
        var data = new PointerEventData(EventSystem.current) { position = pointer };
        var hits = new List<RaycastResult>();
        EventSystem.current.RaycastAll(data, hits);
        var hit = hits.FirstOrDefault().gameObject;
        return hit != null && hit.transform.IsChildOf(control.transform);
    }

    private static void ClickDown() => SetPointer(true);

    private static void SetPointer(bool pressed)
    {
        var state = new MouseState { position = pointer };
        InputState.Change(mouse!, pressed ? state.WithButton(MouseButton.Left) : state);
    }

    private static void Finish()
    {
        InputSystem.onAfterUpdate -= Tick;
        InputSystem.onActionChange -= ObserveAction;
        Debug.Log("VN-BG-DONE");
    }

    private static void ObserveAction(object subject, InputActionChange change)
    {
        if (change != InputActionChange.ActionPerformed || subject is not InputAction action) return;
        var active = action.activeControl;
        if (active?.device == keyboard || active?.device == mouse)
            Debug.Log($"VN-BG-ACTION {action.actionMap?.name}/{action.name} {active?.path}");
    }

    public static void ObserveMenu(object menuEvent)
    {
        var type = menuEvent?.GetType();
        if (type?.FullName != "MenuEventUserIntent") return;
        var name = type.GetField("name", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)?.GetValue(menuEvent);
        Debug.Log($"VN-BG-MENU {name}");
    }
}
