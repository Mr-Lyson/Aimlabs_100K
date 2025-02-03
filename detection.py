import cv2
import numpy as np


def extract_cyan_ball(image_path, save_path="extracted_ball.png"):
    """
    Extracts the cyan ball from an image and returns its center coordinates.
    Saves the extracted ball image.

    Parameters:
        image_path (str): Path to the input image.
        save_path (str): Path to save the extracted ball image.

    Returns:
        tuple: (ball_x, ball_y) coordinates of the detected ball or (None, None) if not found.
    """
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Image not found or invalid path.")

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define HSV range for cyan color
    lower_cyan = np.array([80, 150, 50])
    upper_cyan = np.array([100, 255, 255])

    # Create a mask to extract the cyan ball
    mask = cv2.inRange(hsv, lower_cyan, upper_cyan)

    # Apply morphological operations to clean the mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # Extract the ball from the original image using the mask
    result = cv2.bitwise_and(image, image, mask=mask)

    # Find contours of the detected ball
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Initialize variables for ball coordinates
    ball_x, ball_y = None, None

    # Find the largest contour (assuming it's the ball)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        ball_x = x + w // 2  # Center X coordinate
        ball_y = y + h // 2  # Center Y coordinate

    # Save the extracted ball as a PNG image
    cv2.imwrite(save_path, result)

    return ball_x, ball_y


# Example usage
if __name__ == "__main__":
    image_path = "aimlab_screen.png"  # Update with actual image path
    save_path = "extracted_ball.png"
    coords = extract_cyan_ball(image_path, save_path)
    print(f"Extracted ball coordinates: {coords}")
