import cv2 as cv
import matplotlib.pyplot as pyplot
from main import filter_image

initial_year= 1984
last_year = 2020

vegetation_percentage_variation = []

for year in range(initial_year, last_year+1):
    original_image = cv.imread(f"./desmatamento/desmatamento_{year}.png")
    reference_tree = original_image[137:200, 932:1041]

    vegetation_percentage_variation.append( filter_image(original_image, reference_tree, False, False)[0] )

print(vegetation_percentage_variation)
pyplot.figure()
pyplot.plot(vegetation_percentage_variation)
pyplot.show()