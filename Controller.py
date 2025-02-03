import win32api
import win32con
import time
import math

def click_mouse(button='left', clicks=1, interval=0.02):
    """
    Clicks the mouse at the current position.

    Parameters:
        button (str): Mouse button to use ('left', 'right', 'middle').
        clicks (int): Number of times to click (default is 1).
        interval (float): Delay between clicks (default is 0.1s).
    """
    button_map = {'left': win32con.MOUSEEVENTF_LEFTDOWN, 'right': win32con.MOUSEEVENTF_RIGHTDOWN,
                  'middle': win32con.MOUSEEVENTF_MIDDLEDOWN}
    release_map = {'left': win32con.MOUSEEVENTF_LEFTUP, 'right': win32con.MOUSEEVENTF_RIGHTUP,
                   'middle': win32con.MOUSEEVENTF_MIDDLEUP}

    for _ in range(clicks):
        win32api.mouse_event(button_map[button], 0, 0, 0, 0)
        time.sleep(0.02)
        win32api.mouse_event(release_map[button], 0, 0, 0, 0)
        time.sleep(interval)


def drag_mouse_to_target(x, y):
    centerX, centerY = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, (x - centerX)*2, (y - centerY)*2 , 0, 0)


def draw_star_with_mouse(size=400):
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


def draw_line_with_mouse(x, y):
    centerX, centerY = win32api.GetCursorPos()
    #print(centerX, centerY, x, y)
    #if x <= centerX and y <= centerY:
        #print("top_left")
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, (x - centerX)*2, (y - centerY)*2 , 0, 0)
    #if x <= centerX and y >= centerY:
        #print("bottom_left")
        #win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, (x - centerX)*2, (y - centerY)*2 , 0, 0)
    #if x >= centerX and y <= centerY:
        #print("top_right")
        #win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, (x - centerX)*2, (y - centerY)*2 , 0, 0)
    #if x >= centerX and y >= centerY:
        #print("buttom_right")
        #win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, (x - centerX)*2, (y - centerY)*2 , 0, 0)



# Example usage
if __name__ == "__main__":
    print("Dragging mouse along a path")
    time.sleep(3)
    #draw_star_with_mouse()
    draw_line_with_mouse(870,413)
