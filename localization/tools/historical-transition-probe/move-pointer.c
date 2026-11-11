#define UNICODE
#define _UNICODE
#define WINVER 0x0600
#include <windows.h>
#include <shellapi.h>
#include <stdio.h>
#include <wchar.h>

int WINAPI wWinMain(HINSTANCE instance, HINSTANCE previous, PWSTR command, int show) {
    int argc;
    wchar_t **argv = CommandLineToArgvW(GetCommandLineW(), &argc);
    if (!argv || argc != 5) return 1;
    FILE *log = _wfopen(argv[4], L"a");
    if (!log) return 2;
    HWND window = GetForegroundWindow();
    DWORD pid = 0;
    GetWindowThreadProcessId(window, &pid);
    HANDLE process = OpenProcess(PROCESS_QUERY_LIMITED_INFORMATION, FALSE, pid);
    wchar_t image[MAX_PATH * 4] = {0};
    DWORD length = sizeof(image) / sizeof(image[0]);
    if (!process || !QueryFullProcessImageNameW(process, 0, image, &length)
                 || _wcsicmp(image, argv[1]) != 0) {
        fwprintf(log, L"Refused foreground pid=%lu path=%ls\n", pid, image);
        fclose(log);
        return 3;
    }
    CloseHandle(process);
    wchar_t *end_x, *end_y;
    long dx = wcstol(argv[2], &end_x, 10);
    long dy = wcstol(argv[3], &end_y, 10);
    if (*end_x || *end_y || dx < -1500 || dx > 1500 || dy < -1500 || dy > 1500)
        return 4;
    INPUT move = {0};
    move.type = INPUT_MOUSE;
    move.mi.dx = dx;
    move.mi.dy = dy;
    move.mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_MOVE_NOCOALESCE;
    UINT sent = SendInput(1, &move, sizeof(move));
    fwprintf(log, L"pid=%lu dx=%ld dy=%ld delivered=%u error=%lu\n", pid, dx, dy, sent, GetLastError());
    fclose(log);
    LocalFree(argv);
    return sent == 1 ? 0 : 5;
}
