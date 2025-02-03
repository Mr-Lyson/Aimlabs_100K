import time
from Controller import draw_line_with_mouse, click_mouse
from detection import extract_cyan_ball
from screenshot import take_screenshot

if __name__ == "__main__":
    time.sleep(4)
    start_time = time.time()  # Record start time
    duration = 60  # Run for 60 seconds

    while time.time() - start_time < duration:
        image_path = take_screenshot("aimlab.png")
        location_x, location_y = extract_cyan_ball(image_path)

        if location_x is not None and location_y is not None:
            draw_line_with_mouse(location_x, location_y)
            # drag_mouse_to_target(location_x, location_y)

            click_mouse()

    print("Script execution finished after 70 seconds.")


