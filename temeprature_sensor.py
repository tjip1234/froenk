import cv2
import numpy as np

def measure_mercury_length(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to HSV for better color segmentation
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range of red color in HSV
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    lower_red2 = np.array([170, 50, 50])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Find contours in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Assuming the largest contour corresponds to the mercury bulb at the base
        mercury_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(mercury_contour)

        # Crop the thermometer from the bulb to the top to analyze the column
        thermometer_column = mask[y:y+h, x:x+w]

        # Iterate through the column from bottom to top until a non-red area is detected
        length_pixels = 0
        for row in range(h-1, -1, -1):
            length_pixels += 1
            if np.all(thermometer_column[row] == 0):  # Check for the first non-red row
                length_pixels = h - row
                break

        # Draw the contour and markers for visualization
        cv2.drawContours(image, [mercury_contour], -1, (0, 255, 0), 2)
        cv2.line(image, (x, y + h), (x + w, y + h), (255, 0, 0), 2)  # blue line at the bottom
        cv2.line(image, (x, y + row), (x + w, y + row), (255, 255, 0), 2)  # yellow line at the transition

        # Save the image with contours drawn for verification
        cv2.imwrite('contoured_image.jpg', image)

        return length_pixels
    else:
        return 0  # Return 0 if no contours are found

# Use the function with the path to your image
image_path = 'thermometer.jpg'  # Replace with your image path
length = measure_mercury_length(image_path)
print(f"The length of the red mercury column is {length:.2f} pixels.")
