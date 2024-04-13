import cv2
import numpy as np

def find_black_box(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Threshold to isolate the black box
    _, thresholded = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
    
    # Find contours
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Assume the largest contour is the black box
    max_contour = max(contours, key=cv2.contourArea)
    
    # Get the bounding rectangle of the largest contour
    x, y, w, h = cv2.boundingRect(max_contour)
    return x, y, w, h

def process_image(datetime):
    # Load the image
    image = cv2.imread('frame.jpg')
    
    # Find the black box
    x, y, w, h = find_black_box(image)
    
    # Crop the black box region and rotate it 180 degrees
    black_box = image[y:y+h, x:x+w]
    rotated_black_box = cv2.rotate(black_box, cv2.ROTATE_180)
    
    # Replace the original black box in the image with the rotated version
    image[y:y+h, x:x+w] = rotated_black_box
    cv2.imwrite("digital/"+datetime+'-digital.jpg', rotated_black_box)
    # Crop the thermometer area, assuming it's directly above the black box
    thermometer = image[0:y, x:x+w]
    rotated_thermometer = cv2.rotate(thermometer, cv2.ROTATE_90_CLOCKWISE)
    cv2.imwrite('thermometer/'+datetime+'thermometer.jpg', rotated_thermometer)
    # Height adjustment after rotation
    new_h, new_w = rotated_thermometer.shape[:2]
    image[0:new_h, x:x+new_w] = rotated_thermometer

    # Save the modified image
    cv2.imwrite('modified_frame.jpg', image)
    print("Image processing complete and saved as 'modified_frame.jpg'.")

if __name__ == "__main__":
    process_image()
