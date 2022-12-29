import cv2 as cv
import numpy as np

def return_constant_pixel_to_meter(real_distance_representated, scale_image_path):
    escala = cv.imread(scale_image_path)

    escala_gray = cv.cvtColor(escala, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(escala_gray, 200, 255, cv.THRESH_BINARY)

    bigger_line_length = 0
    bigger_line = []

    for y in range(0, thresh.shape[0]):
        line_in_analysis = [[0,0], [0,0]]
        last_pixel_was_white = False
        for x in range(0, thresh.shape[1]):
            pixel_is_white = thresh[y,x] == 255

            if pixel_is_white:
                if not last_pixel_was_white:
                    line_in_analysis[0] = [y,x]
            else:
                if last_pixel_was_white:
                    line_in_analysis[1] = [y,x]

                    line_length = (line_in_analysis[1][1] - line_in_analysis[0][1]) #+ 1

                    if line_length > bigger_line_length:
                        bigger_line_length = line_length
                        bigger_line = line_in_analysis

            last_pixel_was_white = pixel_is_white


    return real_distance_representated / (bigger_line_length-4)
