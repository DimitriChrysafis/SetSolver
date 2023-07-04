import cv2
import rectangles

# Read the image file
image_path = '/Users/dimitri.chrysafis/Desktop/thing.png'  # Replace with the actual path to your image file
image = cv2.imread(image_path)

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply adaptive thresholding to obtain a binary image
combined_threshold = rectangles.apply_adaptive_threshold(gray_image)

# Find and draw rectangles around the falid contours
rectangles.draw_rectangles(image, combined_threshold)

# Display the image with rectangles and labels
cv2.imshow("White Card Detection", image)
cv2.waitKey(0)
cv2.destroyAllWindows()
