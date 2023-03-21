import cv2 as cv
import numpy as np
import SHSX

def return_tree_color_interval(reference_tree, color_space=cv.COLOR_BGR2HSV):
    reference_tree_on_other_color_system = cv.cvtColor(reference_tree, color_space)
    if color_space in [cv.COLOR_BGR2HSV, cv.COLOR_BGR2HLS]:
        reference_tree_on_other_color_system = SHSX.convert_img_to(reference_tree_on_other_color_system, SHSX.HSX_2_SHSX)

    max_values = (256, 256, 256)
    lowest = np.array([255, 255, 255])
    highest = np.array([0, 0, 0])

    for channel in range(3):
        max_value = max_values[channel]
        reference_tree_on_other_color_system_histogram = cv.calcHist([reference_tree_on_other_color_system], [channel], None, [max_value], [0, max_value])
        for value, pixel_amount in enumerate(reference_tree_on_other_color_system_histogram):
            if pixel_amount <= 0: continue

            if value > highest[channel]:
                highest[channel] = value 
            if value < lowest[channel]:
                lowest[channel] = value

    return [lowest, highest]