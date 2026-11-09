using System.Reflection;
using UnityEngine;
using UnityEngine.EventSystems;
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
    private static Camera? playerCamera;
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
                    next += 0.5f;
                    break;
                case 8:
                    if (!TryAimForEquipment()) return;
                    break;
                case 9:
                    Debug.Log($"VN-BG-USE {target!.name}");
                    InputState.Change(keyboard, new KeyboardState(Key.E));
                    break;
                case 10:
                    InputState.Change(keyboard, new KeyboardState());
                    VerifyEquipment();
                    if (equipmentTarget++ == 0)
                    {
                        attempts = 0;
                        stage = 8;
                        return;
                    }
                    Finish();
                    break;
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
    private static bool TryAimForEquipment()
    {
        var type = Game.GetType("Interactable", throwOnError: true)!;
        var name = equipmentTarget == 0 ? "crowbar_socket" : "ShipmentCrateMountFrame";
        var view = playerCamera!.transform;
        target = UnityEngine.Object.FindObjectsByType(type, FindObjectsSortMode.None).OfType<Component>()
            .Single(component => component.name == name);
        if (++attempts > 24) throw new InvalidOperationException("Equipment target timed out: " + name);
        if (moving)
        {
            InputState.Change(keyboard!, new KeyboardState());
            moving = false;
            return false;
        }
        var offset = target.transform.position - view.position;
        var candidate = type.GetMethod("GetCachedInteractable", StaticMembers)?.Invoke(null, null) as Component;
        var horizontal = Vector3.ProjectOnPlane(offset, Vector3.up);
        var yaw = Vector3.SignedAngle(Vector3.ProjectOnPlane(view.forward, Vector3.up), horizontal, Vector3.up);
        var pitch = Mathf.Atan2(offset.y, horizontal.magnitude) * Mathf.Rad2Deg -
            Mathf.Asin(Mathf.Clamp(view.forward.y, -1, 1)) * Mathf.Rad2Deg;
        Debug.Log($"VN-BG-GUIDE {name} position={view.position:F3} forward={view.forward:F3} distance={offset.magnitude:F3} yaw={yaw:F3} pitch={pitch:F3} cached={candidate?.name}");
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
        var manager = Game.GetType("com.gatordragongames.washnwalk.tools.ToolManager", throwOnError: true)!;
        var tool = manager.GetMethod("GetCurrentTool", StaticMembers)?.Invoke(null, null) as UnityEngine.Object;
        var opened = target!.GetType().GetField("opened", InstanceMembers)?.GetValue(target);
        Debug.Log($"VN-BG-EQUIPMENT target={target.name} tool={tool?.name} opened={opened}");
        if (equipmentTarget == 0)
        {
            var expectedTool = target.GetType().GetField("tool", InstanceMembers)?.GetValue(target) as UnityEngine.Object;
            if (expectedTool == null || expectedTool != tool)
                throw new InvalidOperationException("The equipped tool was not the exact crowbar asset");
        }
        if (equipmentTarget == 1)
        {
            if (opened is not true) throw new InvalidOperationException("The crate did not open");
            var interactable = Game.GetType("Interactable", throwOnError: true)!;
            foreach (var item in UnityEngine.Object.FindObjectsByType(interactable, FindObjectsSortMode.None).OfType<Component>()
                .Where(item => item.name.IndexOf("mount", StringComparison.OrdinalIgnoreCase) >= 0))
                Debug.Log($"VN-BG-MOUNT {item.name} {item.transform.position:F4} {item.GetType().Name}");
        }
    }

    private static void AimAt(string typeName, string fieldName)
    {
        var type = Game.GetType(typeName, throwOnError: true)!;
        var component = UnityEngine.Object.FindObjectsByType(type, FindObjectsSortMode.None).Single();
        var field = type.GetField(fieldName, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);
        if (field?.GetValue(component) is not Button button || !button.isActiveAndEnabled || !button.IsInteractable())
            throw new InvalidOperationException($"Unavailable button {typeName}.{fieldName}");
        var rect = (RectTransform)button.transform;
        var canvas = button.GetComponentInParent<Canvas>();
        var camera = canvas.renderMode == RenderMode.ScreenSpaceOverlay ? null : canvas.worldCamera;
        pointer = RectTransformUtility.WorldToScreenPoint(camera, rect.TransformPoint(rect.rect.center));
        var data = new PointerEventData(EventSystem.current) { position = pointer };
        var hits = new List<RaycastResult>();
        EventSystem.current.RaycastAll(data, hits);
        var hit = hits.FirstOrDefault().gameObject;
        Debug.Log($"VN-BG-AIM {typeName}.{fieldName} button={button.name} {pointer} hit={hit?.name} screen={Screen.width}x{Screen.height}");
        if (hit == null || !hit.transform.IsChildOf(button.transform))
            throw new InvalidOperationException($"Raycast missed {typeName}.{fieldName}");
        SetPointer(false);
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
