import cv2 as cv
import numpy as np

def return_tree_hsv_interval(reference_tree_img_path):
    reference_tree = cv.imread(reference_tree_img_path)
    reference_tree_hsv = cv.cvtColor(reference_tree, cv.COLOR_BGR2HSV)

    max_values = (256, 256, 256)
    lowest = np.array([255, 255, 255])
    highest = np.array([0, 0, 0])

    for channel in range(3):
        max_value = max_values[channel]
        reference_tree_hsv_histogram = cv.calcHist([reference_tree_hsv], [channel], None, [max_value], [0, max_value])
        for value, pixel_amount in enumerate(reference_tree_hsv_histogram):
            if pixel_amount <= 0: continue

            if value > highest[channel]:
                highest[channel] = value 
            if value < lowest[channel]:
                lowest[channel] = value

    return [lowest, highest]