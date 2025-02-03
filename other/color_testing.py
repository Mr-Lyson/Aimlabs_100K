import time
import pyautogui
import win32api


def debug_mouse_color():
    """调试鼠标当前位置的颜色"""
    x, y = win32api.GetCursorPos()
    try:
        pixel = pyautogui.pixel(x, y)
        print(f"[DEBUG] 鼠标当前位置 ({x}, {y}) 颜色: {pixel}")
    except Exception as e:
        print(f"[ERROR] 获取鼠标颜色失败: {e}")

if __name__ == "__main__":
    while True:
        debug_mouse_color()
        time.sleep(0.5)  # 每 0.5 秒打印一次
