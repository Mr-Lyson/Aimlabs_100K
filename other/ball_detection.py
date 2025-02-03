import cv2
import numpy as np
import mss
import pygetwindow as gw
import time
import win32api
import win32con
import math

# 🎯 颜色范围（只要像素在这个范围内，就触发检测）
LOWER_COLOR = np.array([18, 176, 189])
UPPER_COLOR = np.array([24, 216, 218])


def get_aimlab_window():
    """
    获取 AimLab 游戏窗口位置
    """
    windows = gw.getWindowsWithTitle("aimlab_tb")  # 查找 "aimlab_tb" 窗口
    if windows:
        win = windows[0]
        return (win.left, win.top, win.width, win.height)
    return None


def capture_aimlab():
    """
    截取 AimLab 游戏窗口内容
    """
    window = get_aimlab_window()
    if window:
        x, y, w, h = window
        with mss.mss() as sct:
            screenshot = sct.grab({"top": y, "left": x, "width": w, "height": h})
            img = np.array(screenshot)
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # 转换 BGR 格式
    return None


def draw_star_with_mouse(size=200):
    """
    以当前鼠标位置为起点，绘制一个五角星的轨迹（使用相对鼠标移动）
    """
    start_x, start_y = win32api.GetCursorPos()
    angles = [math.radians(a) for a in [270, 342, 54, 126, 198]]  # 五角星的角度
    points = [(start_x + size * math.cos(a), start_y + size * math.sin(a)) for a in angles]
    order = [0, 2, 4, 1, 3, 0]  # 画五角星的顺序

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)  # 按住鼠标左键
    for i in range(len(order) - 1):
        start = points[order[i]]
        end = points[order[i + 1]]
        dx = int((end[0] - start[0]) / 2)
        dy = int((end[1] - start[1]) / 2)
        for step in range(2):  # 细分 2 步完成平滑移动
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx, dy, 0, 0)
            time.sleep(0.02)  # 控制鼠标移动速度
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)  # 释放鼠标左键
    print("[INFO] 五角星轨迹绘制完成")


def move_and_click(x, y):
    """
    平滑移动鼠标到目标位置并点击
    """
    win32api.SetCursorPos((x, y))
    time.sleep(0.1)  # 添加短暂延迟确保鼠标已移动
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print(f"[INFO] 鼠标已移动至 ({x}, {y}) 并执行点击")


def main():
    print("🎯 尝试在 AimLab 游戏中检测小球...")

    window = get_aimlab_window()
    if not window:
        print("[ERROR] AimLab 窗口未找到，程序终止")
        return

    print("[INFO] AimLab 窗口已找到，5 秒准备时间...")
    time.sleep(5)

    # 以当前鼠标位置绘制五角星轨迹
    draw_star_with_mouse()

    for i in range(5):  # 进行5次检测
        screen = capture_aimlab()
        if screen is None:
            print("[ERROR] 未找到 AimLab 窗口")
            return

        ball_region = detect_ball(screen)

        # 继续截图检测小球位置变化，并移动鼠标点击
        if ball_region:
            x, y, w, h = ball_region
            ball_center_x = x + w // 2
            ball_center_y = y + h // 2
            move_and_click(ball_center_x, ball_center_y)
            print(f"[INFO] 第 {i + 1} 次检测成功，小球位置已变化，鼠标已移动并点击")

    print("[INFO] 5 次检测完成")


if __name__ == "__main__":
    main()
