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
    private static bool introStarted, introCompleted, dialogueCompleted, advanceDown, mountNodeStarted;
    private static bool mountNodeCompleted, mountDialogueCompleted, finishNodeStarted, finishNodeCompleted, finishDialogueCompleted;
    private static readonly string[] MountChoices = { "line:0372e0d1" };
    private static readonly string[] FinishChoices = { "line:82cf49aa", "line:aeae4744", "line:a983ffa3", "line:6a2e4e0d" };
    private static int choiceIndex, optionClickPhase;
    private static int gateWaypoint;
    private static readonly Vector2[] GateWaypoints = { new(4.0f, -6.7f), new(-3.6f, -6.7f) };
    private static readonly Vector2[] StorageWaypoints = { new(-3.6f, -6.7f), new(3.3f, -6.7f) };
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
                    var waypoints = equipmentTarget == 9 ? GateWaypoints :
                        equipmentTarget == 10 ? StorageWaypoints : Array.Empty<Vector2>();
                    if (gateWaypoint < waypoints.Length)
                    {
                        if (ApproachGateWaypoint(waypoints[gateWaypoint]))
                        {
                            gateWaypoint++;
                            attempts = 0;
                        }
                        return;
                    }
                    if (equipmentTarget == 9 ? !TryAimHandAtGate() : !TryAimForEquipment()) return;
                    break;
                case 9:
                    if (equipmentTarget == 9 ? !HandRayHitsGate() : CachedTarget() != target)
                        throw new InvalidOperationException("Stock selector changed before input");
                    Debug.Log($"VN-BG-USE step={equipmentTarget} {target!.name}");
                    InputState.Change(keyboard, new KeyboardState(Key.E));
                    if (equipmentTarget == 9) next += .8f;
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
                    if (equipmentTarget == 10)
                    {
                        waitDeadline = Time.realtimeSinceStartup + 45;
                        stage = 13;
                        return;
                    }
                    if (equipmentTarget == 11)
                    {
                        gateWaypoint = 0;
                        attempts = 0;
                        stage = 8;
                        return;
                    }
                    if (equipmentTarget == 12)
                    {
                        waitDeadline = Time.realtimeSinceStartup + 35;
                        stage = 14;
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
                        attempts = 0;
                        stage = 8;
                        return;
                    }
                    if (Time.realtimeSinceStartup >= waitDeadline)
                        throw new InvalidOperationException("Ordinary intro input timed out");
                    AdvanceDialogue(IntroChoices);
                    return;
                case 13:
                    var code = DragonStateCode();
                    if (code == 5)
                    {
                        Debug.Log("VN-BG-GATE-FINAL WaitingOnBeingWashed");
                        gateWaypoint = 0;
                        attempts = 0;
                        stage = 8;
                        return;
                    }
                    if (Time.realtimeSinceStartup >= waitDeadline)
                        throw new InvalidOperationException($"The dragon did not reach the wash area, state {code}");
                    return;
                case 14:
                    if (mountNodeStarted)
                    {
                        Debug.Log($"VN-BG-PERFORMANCE PlacedMountForUse={Flag("PlacedMountForUse")} node=Conrad_placed_mount_3");
                        choiceIndex = 0;
                        waitDeadline = Time.realtimeSinceStartup + 65;
                        break;
                    }
                    if (Time.realtimeSinceStartup >= waitDeadline)
                        throw new InvalidOperationException("The mount performance dialogue did not start");
                    return;
                case 15:
                    if (mountNodeCompleted && mountDialogueCompleted)
                    {
                        VerifyChoices(MountChoices);
                        Debug.Log($"VN-BG-MOUNT-DIALOGUE-FINAL choices={choiceIndex}");
                        waitDeadline = Time.realtimeSinceStartup + 85;
                        break;
                    }
                    if (Time.realtimeSinceStartup >= waitDeadline)
                        throw new InvalidOperationException("The mount performance dialogue did not complete");
                    AdvanceDialogue(MountChoices);
                    return;
                case 16:
                    if (finishNodeStarted)
                    {
                        choiceIndex = 0;
                        waitDeadline = Time.realtimeSinceStartup + 65;
                        break;
                    }
                    if (Time.realtimeSinceStartup >= waitDeadline)
                        throw new InvalidOperationException("The original coroutine did not start the finish node");
                    return;
                case 17:
                    if (finishNodeCompleted && finishDialogueCompleted)
                    {
                        VerifyChoices(FinishChoices);
                        waitDeadline = Time.realtimeSinceStartup + 15;
                        break;
                    }
                    if (Time.realtimeSinceStartup >= waitDeadline)
                        throw new InvalidOperationException("The finish dialogue did not complete");
                    AdvanceDialogue(FinishChoices);
                    return;
                case 18:
                    var performanceType = Game.GetType("DragonPerformanceTriggerDragonMount", throwOnError: true)!;
                    if (performanceType.GetField("doingPerformance", StaticMembers)!.GetValue(null) is false)
                    {
                        Debug.Log($"VN-BG-PERFORMANCE-FINAL choices={choiceIndex} inProgress={Flag("DragonOnaholeSexInProgress")} completed={Flag("DragonOnaholeSexCompleted")}");
                        Finish();
                        break;
                    }
                    if (Time.realtimeSinceStartup >= waitDeadline)
                        throw new InvalidOperationException("The original performance coroutine did not exit");
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
                if (node == "Conrad_placed_mount_3") mountNodeStarted = true;
                if (node == "Conrad_finished_mount_3") finishNodeStarted = true;
            });
            if (type.GetField("onNodeComplete", InstanceMembers)?.GetValue(runner) is UnityEvent<string> complete)
                complete.AddListener(node => {
                    Debug.Log($"VN-BG-YARN-COMPLETE {node}");
                    if (node == "Conrad_Intro_3") introCompleted = true;
                    if (node == "Conrad_placed_mount_3") mountNodeCompleted = true;
                    if (node == "Conrad_finished_mount_3") finishNodeCompleted = true;
                });
            if (type.GetField("onDialogueComplete", InstanceMembers)?.GetValue(runner) is UnityEvent dialogue)
                dialogue.AddListener(() => {
                    Debug.Log("VN-BG-YARN-DIALOGUE-COMPLETE");
                    if (introCompleted) dialogueCompleted = true;
                    if (mountNodeCompleted) mountDialogueCompleted = true;
                    if (finishNodeCompleted) finishDialogueCompleted = true;
                });
            listeners++;
        }
        if (listeners == 0) throw new InvalidOperationException("No original Yarn node event available");
        Debug.Log($"VN-BG-YARN-LISTENERS {listeners}");
    }

    private static void VerifyChoices(string[] choices)
    {
        if (choiceIndex != choices.Length)
            throw new InvalidOperationException($"Completed a different dialogue branch: {choiceIndex} choices");
    }

    private static void AdvanceDialogue(string[] choices)
    {
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
            if (choiceIndex >= choices.Length) return;
            var choice = choices[choiceIndex];
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
            9 => candidates.Single(c => c.name == "DoneButton" && c.GetType().Name == "InteractableDismissButton"),
            10 => candidates.Single(c => Equals(c.GetType().GetField("placeFlag", InstanceMembers)?.GetValue(c), "PlacedMount")),
            11 => candidates.Single(c => Equals(c.GetType().GetField("placeFlag", InstanceMembers)?.GetValue(c), "PlacedMountForUse")),
            _ => throw new InvalidOperationException("Unexpected equipment step"),
        };
    }

    private static bool ApproachGateWaypoint(Vector2 waypoint)
    {
        if (++attempts > 60) throw new InvalidOperationException($"Gate waypoint {gateWaypoint} timed out");
        if (moving)
        {
            InputState.Change(keyboard!, new KeyboardState());
            moving = false;
            return false;
        }
        var view = playerCamera!.transform;
        var position = view.position;
        var offset = new Vector3(waypoint.x - position.x, 0, waypoint.y - position.z);
        var yaw = Vector3.SignedAngle(Vector3.ProjectOnPlane(view.forward, Vector3.up), offset, Vector3.up);
        Debug.Log($"VN-BG-ROUTE step={equipmentTarget} waypoint={gateWaypoint} position={position:F3} distance={offset.magnitude:F3} yaw={yaw:F3}");
        if (offset.magnitude < .9f) return true;
        if (Mathf.Abs(yaw) > 7)
        {
            InputState.Change(mouse!, new MouseState { position = pointer, delta = new Vector2(Mathf.Clamp(yaw * 8f, -100, 100), 0) });
            return false;
        }
        InputState.Change(keyboard!, new KeyboardState(Key.W));
        moving = true;
        next = Time.realtimeSinceStartup + Mathf.Clamp(offset.magnitude / 8, .12f, .25f);
        return false;
    }

    private static readonly Type HandType = Game.GetType("PlapperHand", throwOnError: true)!;
    private static readonly Type LookType = Game.GetType("LookController", throwOnError: true)!;

    private static (Vector3 Origin, Vector3 Direction) HandLook()
    {
        var hand = UnityEngine.Object.FindObjectsByType(HandType, FindObjectsSortMode.None).OfType<Behaviour>()
            .Single(x => x.isActiveAndEnabled);
        var offset = (Vector2)HandType.GetField("lookOffset", InstanceMembers)!.GetValue(hand);
        var pos = (Vector3)LookType.GetMethod("GetLookPosition", StaticMembers)!.Invoke(null, null);
        var rot = (Quaternion)LookType.GetMethod("GetLookRotation", StaticMembers)!.Invoke(null, null);
        return (pos, rot * Quaternion.Euler(-offset.y, offset.x, 0) * Vector3.forward);
    }

    private static bool HandRayHitsGate()
    {
        var (origin, direction) = HandLook();
        return Physics.Raycast(origin + direction * .1f, direction, out var hit, 2f, 385)
            && hit.collider.transform.IsChildOf(target!.transform);
    }

    private static bool TryAimHandAtGate()
    {
        if (++attempts > 65) throw new InvalidOperationException("Hand aim at the gate timed out");
        if (moving)
        {
            InputState.Change(keyboard!, new KeyboardState());
            moving = false;
            return false;
        }
        target = EquipmentTarget();
        var (origin, direction) = HandLook();
        var button = target.GetComponentsInChildren<SphereCollider>().Single(c => c.name == "Plappable");
        var offset = button.bounds.center - origin;
        var horizontal = Vector3.ProjectOnPlane(offset, Vector3.up);
        var view = playerCamera!.transform;
        var moveYaw = Vector3.SignedAngle(Vector3.ProjectOnPlane(view.forward, Vector3.up), horizontal, Vector3.up);
        var handYaw = Vector3.SignedAngle(Vector3.ProjectOnPlane(direction, Vector3.up), horizontal, Vector3.up);
        var pitch = Mathf.Atan2(offset.y, horizontal.magnitude) * Mathf.Rad2Deg -
            Mathf.Asin(Mathf.Clamp(direction.y, -1, 1)) * Mathf.Rad2Deg;
        var hit = Physics.Raycast(origin + direction * .1f, direction, out var ray, 3f, 385);
        Debug.Log($"VN-BG-HAND distance={offset.magnitude:F3} horizontal={horizontal.magnitude:F3} yaw={handYaw:F3} pitch={pitch:F3} ray={ (hit ? ray.collider.name : "<none>") } rayDistance={(hit ? ray.distance : -1):F3}");
        if (HandRayHitsGate()) return true;
        var yaw = horizontal.magnitude > 1.55f ? moveYaw : handYaw;
        if (Mathf.Abs(yaw) > 2.5f || (horizontal.magnitude <= 1.55f && Mathf.Abs(pitch) > 2.5f))
        {
            var delta = new Vector2(Mathf.Clamp(yaw * 8f, -100, 100),
                horizontal.magnitude <= 1.55f ? Mathf.Clamp(pitch * 8f, -100, 100) : 0);
            InputState.Change(mouse!, new MouseState { position = pointer, delta = delta });
            return false;
        }
        if (horizontal.magnitude > .9f)
        {
            InputState.Change(keyboard!, new KeyboardState(Key.W));
            moving = true;
            next = Time.realtimeSinceStartup + .14f;
            return false;
        }
        throw new InvalidOperationException("The hand ray did not reach the gate button");
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
            case 0 or 4 or 6 or 10:
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
            case 9:
                var code = DragonStateCode();
                if (code is not (4 or 5)) throw new InvalidOperationException($"The button did not admit the dragon, state {code}");
                Debug.Log($"VN-BG-GATE-OPEN state={code}");
                break;
            case 11:
                if (emptyTool == null || tool != emptyTool || !Flag("PlacedMountForUse"))
                    throw new InvalidOperationException("The mount was not placed into its performance socket");
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
