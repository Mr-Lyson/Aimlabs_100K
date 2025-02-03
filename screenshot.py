import pyautogui
import time

def take_screenshot(save_path):
    screenshot = pyautogui.screenshot()
    screenshot.save(save_path)
    return save_path


# Example usage
if __name__ == "__main__":
    screenshot_path = take_screenshot("aimlab_screenshot.png")
    print(f"Screenshot taken and saved at: {screenshot_path}")
