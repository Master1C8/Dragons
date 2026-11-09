using System.Reflection;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;

namespace Dragons.BackgroundInputProbe;

public static class Probe
{
    private static Keyboard? keyboard;
    private static float next;
    private static int stage;
    private static InputAction? control;

    public static void Start()
    {
        if (stage != 0) return;
        Application.runInBackground = true;
        keyboard = InputSystem.AddDevice<Keyboard>();
        next = Time.realtimeSinceStartup + 3f;
        stage = 1;
        control = new InputAction("ProbeEscape", InputActionType.Button, "<Keyboard>/escape");
        control.Enable();
        InputSystem.onEvent += (eventPtr, device) => {
            if (device == keyboard) Debug.Log($"VN-BG-RAW {eventPtr.type} stage={stage}");
        };
        InputSystem.onAfterUpdate += Tick;
        InputSystem.onActionChange += ObserveAction;
        Debug.Log($"VN-BG-START focused={Application.isFocused} keyboard={keyboard.deviceId}");
    }

    private static void Tick()
    {
        if (Time.realtimeSinceStartup < next || keyboard == null) return;
        if (stage == 1)
        {
            Debug.Log($"VN-BG-NEUTRAL focused={Application.isFocused} enabled={keyboard.enabled}");
            InputState.Change(keyboard, new KeyboardState());
        }
        if (stage == 2)
        {
            Debug.Log($"VN-BG-ESCAPE focused={Application.isFocused} enabled={keyboard.enabled}");
            InputState.Change(keyboard, new KeyboardState(Key.Escape));
        }
        if (stage == 3)
        {
            Debug.Log($"VN-BG-STATE escape={keyboard.escapeKey.isPressed} control={control?.ReadValue<float>()}");
            InputState.Change(keyboard, new KeyboardState());
            control?.Dispose();
            Debug.Log($"VN-BG-DONE focused={Application.isFocused}");
            InputSystem.onAfterUpdate -= Tick;
            InputSystem.onActionChange -= ObserveAction;
        }
        stage++;
        next = Time.realtimeSinceStartup + 2f;
    }

    private static void ObserveAction(object subject, InputActionChange change)
    {
        if (change != InputActionChange.ActionPerformed || subject is not InputAction action ||
            action.activeControl?.device != keyboard)
            return;
        Debug.Log($"VN-BG-ACTION {action.actionMap?.name}/{action.name} {action.activeControl.path}");
    }

    public static void ObserveMenu(object menuEvent)
    {
        var type = menuEvent?.GetType();
        if (type?.FullName != "MenuEventUserIntent") return;
        var name = type.GetField("name", BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic)?.GetValue(menuEvent);
        Debug.Log($"VN-BG-MENU {name} focused={Application.isFocused}");
    }
}
