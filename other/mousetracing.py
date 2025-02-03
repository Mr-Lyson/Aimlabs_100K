import time
import numpy as np
import win32api
import win32con
import random
import keyboard
import pyautogui  # 用于颜色检测
from PIL import ImageGrab

# 🎯 颜色范围（只要像素在这个范围内，就触发点击）
LOWER_COLOR = np.array([18, 176, 189])
UPPER_COLOR = np.array([24, 216, 218])

# 颜色容差
TOLERANCE = 20

# 鼠标检测区域大小 (15x15)
DETECTION_SIZE = 15

# 只要有 1 个像素匹配目标颜色，就触发点击
MATCH_THRESHOLD = 0.004

def get_mouse_region_pixels():
    """获取鼠标附近 15x15 区域的颜色数据"""
    x, y = win32api.GetCursorPos()
    bbox = (x - DETECTION_SIZE // 2, y - DETECTION_SIZE // 2,
            x + DETECTION_SIZE // 2, y + DETECTION_SIZE // 2)
    screenshot = ImageGrab.grab(bbox)  # 截取鼠标附近的小区域
    frame = np.array(screenshot)  # 转换为 NumPy 数组 (RGB)
    return frame  # 返回 RGB 颜色数据

def color_in_range(color, lower, upper):
    """检查颜色是否在指定范围内"""
    return all(lower[i] <= color[i] <= upper[i] for i in range(3))

def is_target_in_area():
    """检测鼠标区域内是否存在符合颜色范围的像素"""
    region_pixels = get_mouse_region_pixels()

    for row in region_pixels:
        for pixel in row:
            # **如果颜色在范围内，就立即触发点击**
            if color_in_range(pixel, LOWER_COLOR, UPPER_COLOR):
                print(f"[DEBUG] 发现匹配像素：{pixel}")  # 发现匹配像素时打印
                return True

    return False  # 如果遍历完 15x15 仍未找到匹配像素，则返回 False

def auto_click(duration=70):
    """自动检测鼠标下的颜色，并在匹配目标颜色时点击"""
    start_time = time.time()
    print("🔫 自动点击已启动... 按 'ESC' 退出")

    while time.time() - start_time < duration:
        if keyboard.is_pressed("esc"):  # 监听 ESC 键停止
            print("❌ 自动点击手动终止")
            break

        if is_target_in_area():
            x, y = win32api.GetCursorPos()  # 获取鼠标当前位置

            # 模拟鼠标按下和释放
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            time.sleep(random.uniform(0.005, 0.01))  # 随机按下时间
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

            print(f"✅ 目标颜色匹配！鼠标点击：({x}, {y})")
            time.sleep(random.uniform(0.008, 0.015))  # 随机延迟

        time.sleep(0.05)  # 50ms 间隔，避免 CPU 过载

    print("🔄 自动点击已停止")

if __name__ == "__main__":
    print("🎯 启动自动点击程序...")
    print("请将鼠标移动到目标颜色区域，按 'ESC' 退出")
    time.sleep(2)  # 启动前等待 2 秒
    auto_click(duration=70)
