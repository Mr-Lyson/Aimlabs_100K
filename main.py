import cv2
import numpy as np
import pyautogui
import mss
import time

# 屏幕捕获区域（根据显示器调整）
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()
MONITOR = {"top": 0, "left": 0, "width": SCREEN_WIDTH, "height": SCREEN_HEIGHT}

# 颜色范围 (青色小球, HSV 色彩空间)
LOWER_COLOR = np.array([85, 100, 100])  # 低阈值 (适应青色)
UPPER_COLOR = np.array([100, 255, 255])  # 高阈值 (适应青色)


def capture_screen():
    """ 截取屏幕并返回图像 """
    with mss.mss() as sct:
        screen = sct.grab(MONITOR)
        print(screen)
        img = np.array(screen)  # 转换为 numpy 数组
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # 转换为 OpenCV 颜色格式
    return img


def find_target(img):
    """ 在屏幕上找到青色小球并返回其坐标 """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # 转换为 HSV 颜色空间
    mask = cv2.inRange(hsv, LOWER_COLOR, UPPER_COLOR)  # 生成颜色掩码
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 轮廓检测

    if contours:
        # 选取最大轮廓（假设目标是最大的青色物体）
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        target_x, target_y = x + w // 2, y + h // 2  # 计算中心点
        return target_x, target_y
    return None


def aim_and_shoot():
    """ 识别青色小球并自动瞄准和射击 """
    while True:
        img = capture_screen()
        target = find_target(img)

        if target:
            # 获取目标坐标
            target_x, target_y = target
            print(f"发现青色小球: {target_x}, {target_y}")

            # 移动鼠标到目标位置
            #一点一点移动
            pyautogui.moveTo(target_x, target_y, duration=0.05)

            # 模拟鼠标点击
            pyautogui.click()

        # 添加延迟，防止 CPU 过载
        time.sleep(0.01)


if __name__ == "__main__":
    print("程序将在 3 秒后开始...")
    time.sleep(3)  # 给予玩家准备时间
    aim_and_shoot()
