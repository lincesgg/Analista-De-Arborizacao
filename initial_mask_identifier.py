from typing import final
import cv2 as cv
import numpy as np
from skimage.metrics import structural_similarity as compare_ssim

def return_initial_mask(base_img_path, initial_mask_image_path):
    pixel_areas = []

    def is_pixel_of_color(img, y, x, color):
        pixel = img[y, x]
        for i in range(0, len(color)):
            if color[i] != pixel:
                return False
        return True

    def change_pixel_color_to(color=(0,0,255),img=[], y=0, x=0):
        img[y, x,] = color

    def contamine_pixel(pixel, pixel_area, contamination_reference):
        contamination_reference[pixel[0], pixel[1]] = 0
        pixel_area.append(pixel)

    def contamine_adjacent_pixels(origin_pixel, pixel_area_index, contamination_reference):
        origin_y, origin_x, _ = origin_pixel
        contamined_pixels = []

        for offset in [[0, 1], [0,-1], [1, 0], [-1, 0], [1, 1], [-1, 1], [1, -1], [-1, -1]]:
            
            contamined_pixel_data = [origin_y, origin_x, 0]
            contamined_pixel_data[0] += offset[0]
            contamined_pixel_data[1] += offset[1]
            contamined_pixel = tuple(contamined_pixel_data)

            _y, _x, _c = contamined_pixel
            if (_x < 0 or _y < 0) or (_x > contamination_reference.shape[1]-1 or _y > contamination_reference.shape[0]-1):
                continue

            if is_pixel_of_color(contamination_reference, _y, _x, [255]):
                contamined_pixels.append(contamined_pixel)
                contamine_pixel(contamined_pixel, pixel_areas[pixel_area_index], contamination_reference)
                    
                    
        return contamined_pixels

    a = cv.imread(base_img_path)
    b = cv.imread(initial_mask_image_path)

    graya = cv.cvtColor(a, cv.COLOR_BGR2GRAY)
    grayb = cv.cvtColor(b, cv.COLOR_BGR2GRAY)

    score, diff = compare_ssim(graya, grayb, full=True)
    diff = (diff*255).astype('uint8')

    ret, thresh = cv.threshold(diff, 244, 255, cv.THRESH_BINARY)
    inverse_thresh = cv.bitwise_not(thresh)

    _kernel = cv.getStructuringElement(cv.MORPH_RECT, (3,3))
    inverse_thresh = cv.morphologyEx(inverse_thresh, cv.MORPH_CLOSE, _kernel, iterations=3)

    contamination_reference = np.zeros(inverse_thresh.shape[:2], dtype='uint8')
    contours, hierarch = cv.findContours(inverse_thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cv.drawContours(contamination_reference, contours, -1, 255, -1)

    # print(contours[contour_index][point_index][0][x/y])
    for contour in contours:
        for point in contour:
            x, y = point[0]
            initial_pixel = (y, x, 0)
            last_pixels_contaminated = [initial_pixel]

            current_pixel_area_index = []
            
            if not is_pixel_of_color(contamination_reference, y, x, [255]): 
                continue
            else:
                pixel_areas.append([])
                current_pixel_area_index = len(pixel_areas)-1
                contamine_pixel(initial_pixel, pixel_areas[current_pixel_area_index], contamination_reference)

            while last_pixels_contaminated != []:
                next_pixels_contaminated = []
                for pixel in last_pixels_contaminated:
                    pixels_contaminated = contamine_adjacent_pixels(pixel, current_pixel_area_index, contamination_reference)
                    for pixel_contaminated in pixels_contaminated:
                        next_pixels_contaminated.append(pixel_contaminated)
                last_pixels_contaminated = next_pixels_contaminated

    bigger_pixel_area = []
    for pixel_area in pixel_areas:
        if len(pixel_area) > len(bigger_pixel_area):
            bigger_pixel_area = pixel_area

    final_mask = np.zeros(inverse_thresh.shape[:2], dtype='uint8')
    mask_pixel_amount = len(bigger_pixel_area)
    for pixel in bigger_pixel_area:
        final_mask[pixel[0], pixel[1]] = 255

    cv.imshow('Initial_Mask', final_mask)
    return (final_mask, mask_pixel_amount)