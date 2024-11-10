#include <windows.h>

// Window Procedure function to process messages
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    default:
        return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
}

int main() {
    // Define window class
    WNDCLASS wc = {};
    wc.lpfnWndProc = WindowProc;     // Window procedure
    wc.hInstance = GetModuleHandle(nullptr); // Instance handle
    wc.lpszClassName = L"MyWindowClass";
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);

    // Register the window class
    RegisterClass(&wc);

    // Create the window
    HWND hwnd = CreateWindowEx(
        0,                                // Optional window styles
        wc.lpszClassName,                 // Window class name
        L"Hello, WinAPI!",                // Window title
        WS_OVERLAPPEDWINDOW,              // Window style
        CW_USEDEFAULT, CW_USEDEFAULT,    // Position
        800, 600,                         // Size
        nullptr,                          // Parent window
        nullptr,                          // Menu
        wc.hInstance,                     // Instance handle
        nullptr                           // Additional application data
    );

    // Create a button inside the window
    HWND hwndButton = CreateWindow(
        L"BUTTON",  // Predefined class; Unicode assumed 
        L"OK",      // Button text 
        WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,  // Styles 
        10,         // x position 
        10,         // y position 
        100,        // Button width
        100,        // Button height
        hwnd,       // Parent window (use hwnd, the main window handle)
        NULL,       // No menu.
        wc.hInstance, // Instance handle
        NULL);      // Pointer not needed.

    if (hwnd == nullptr) {
        return 0;
    }

    ShowWindow(hwnd, SW_SHOW);
    UpdateWindow(hwnd);

    // Message loop - проверяет ввод с мыши, клавиатуры
    MSG msg = {};
    while (GetMessage(&msg, nullptr, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}
