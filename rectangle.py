import cv2

def apply_adaptive_threshold(image):
    """
    explain:
    - Adaptive thresholding separates the front (white cards) from the background.
    - It calculates the threshold value locally for each pixel based on a small neighborhood.
    -  Helps a lot with light

    steps:
    1. Convert the image to a binary image using a global threshold.
    2. Apply adaptive thresholding using the average of the neighborhood pixels.

    """
    _, threshold = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY_INV)
    adaptive_threshold = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    combined_threshold = cv2.bitwise_and(threshold, adaptive_threshold)
    return combined_threshold

def draw_rectangles(image, threshold_image):
    """
    look for and draw rectangles around the white cards in the image.

    explain:
    - Find the contours (boundaries of them) of connected white sectors in the new image.
    - re iterate over the contours and filter out the smaller (side length based)
    - Draw a green(should I change?) rectangle around each valid white card and label its size.

    how to do:
    1. identify the contours using the thresholded image.
    2. For each contour:
        - evaluate the bounding rectangle.
        - CHECK SIZE (IMPORTANT)
        - If yes, draw a green rectangle around it and label its size.
    """
    contours, _ = cv2.findContours(threshold_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w < 150 or h < 150:
            continue
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f'{w}x{h}', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2, cv2.LINE_AA)
