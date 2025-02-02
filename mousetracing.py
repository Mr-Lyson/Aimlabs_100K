import pyautogui
import time

try:
    print("开始检测鼠标位置，按 Ctrl+C 停止...")
    while True:
        # 获取当前鼠标的坐标
        x, y = pyautogui.position()

        # 打印当前鼠标位置
        print(f"当前鼠标位置: X={x}, Y={y}")

        # 每隔 0.1 秒检测一次
        time.sleep(0.1)

except KeyboardInterrupt:
    print("鼠标位置检测已停止。")