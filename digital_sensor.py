segment_map = {
    0: (1, 1, 1, 1, 1, 1, 0),
    1: (0, 1, 1, 0, 0, 0, 0),
    2: (1, 1, 0, 1, 1, 0, 1),
    3: (1, 1, 1, 1, 0, 0, 1),
    4: (0, 1, 1, 0, 0, 1, 1),
    5: (1, 0, 1, 1, 0, 1, 1),
    6: (1, 0, 1, 1, 1, 1, 1),
    7: (1, 1, 1, 0, 0, 0, 0),
    8: (1, 1, 1, 1, 1, 1, 1),
    9: (1, 1, 1, 1, 0, 1, 1)
}
def guess_possible_digits(active_segments):
    possible_digits = []
    for digit, pattern in segment_map.items():
        if all((seg == pat or pat == 0) for seg, pat in zip(active_segments, pattern)):
            possible_digits.append(digit)
    return possible_digits
import cv2
import numpy as np

def find_percentage_sign(image):
    # Assuming the percentage sign is a small white area in the bottom right
    h, w = image.shape
    roi = image[int(h * 0.8):, int(w * 0.8):]  # Adjust these as needed
    _, thresh = cv2.threshold(roi, 200, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Find the contour closest to the bottom-right corner
    percentage_contour = max(contours, key=lambda x: cv2.boundingRect(x)[0] + cv2.boundingRect(x)[1])
    x, y, _, _ = cv2.boundingRect(percentage_contour)
    return x + int(w * 0.8), y + int(h * 0.8)  # Map back to original image coordinates

def define_digit_areas(percent_pos, image):
    # Define relative positions based on the location of the percentage sign
    digits = {}
    x_offset = percent_pos[0]
    y_offset = percent_pos[1]
    
    # Example offsets, need to be adjusted to your specific image
    digits['humidity_tens'] = image[y_offset-180:y_offset-130, x_offset-100:x_offset-50]
    digits['humidity_units'] = image[y_offset-180:y_offset-130, x_offset-50:x_offset]
    digits['temperature_tens'] = image[y_offset-230:y_offset-180, x_offset-150:x_offset-100]
    digits['temperature_units'] = image[y_offset-230:y_offset-180, x_offset-100:x_offset-50]

    return digits

def process_image_for_display_data(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    percent_pos = find_percentage_sign(image)
    digits = define_digit_areas(percent_pos, image)

    # Here you would process each digit's image to extract segments and then digit values
    # This step would involve further processing as described previously

    # Display or process digits for debugging
    for label, digit_img in digits.items():
        cv2.imshow(label, digit_img)
        cv2.waitKey(0)

process_image_for_display_data('path_to_your_image.jpg')
