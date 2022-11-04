import cv2 as cv
import numpy as np
from return_constant_pixel_to_meter import return_constant_pixel_to_meter
from initial_mask_identifier import return_initial_mask
from feature_tracker import return_tree_hsv_interval

# Paths
original_image_path = "imagem_original.png"
delimitated_image_path = "imagem_delimitadora.png"
reference_tree_path = "referencia.png"
scale_path = "escala.png"

# Input
print("Você deseja aplicar uma imagem delimitadora? [S/N]")
print("(Qualquer outra entrada diferente de [S/N], será compreendida como [N])")
should_apply_initial_mask = input() in ["S", "s"]
print("Qual o tamanho que representa sua escala? ")
print("Distancias consideradas invalidas serão automaticamente reajustadas para 20m")
real_distance_representated = input()
if not real_distance_representated.isdigit():
    real_distance_representated = 20
real_distance_representated = int(real_distance_representated)

# Definidor de Escala
pixel_to_meter = return_constant_pixel_to_meter(real_distance_representated, scale_path)
square_pixel_to_square_meter = pixel_to_meter**2

# Rastreador de Características
lowest, highest = return_tree_hsv_interval(reference_tree_path)

# Importar Imagem Base
img = cv.imread(original_image_path)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Aplicar máscara inicial
if should_apply_initial_mask:
    initial_mask, inital_mask_pixel_amout = return_initial_mask(original_image_path, delimitated_image_path)
    hsv = cv.bitwise_and(hsv, hsv, mask=initial_mask)

# Aplicar máscara de cor
color_mask = cv.inRange(hsv, lowest, highest)
img_with_color_mask = cv.bitwise_and(img, img, mask=color_mask)

cv.imshow('Original', img)
cv.imshow('masked', img_with_color_mask)

# Definição do Centroíde
gray_img_with_color_mask = cv.cvtColor(img_with_color_mask, cv.COLOR_BGR2GRAY)
ret, img_with_color_mask_thresholded = cv.threshold(gray_img_with_color_mask, 15, 255 , cv.THRESH_BINARY)
blurred_thresh = cv.blur(img_with_color_mask_thresholded, (7,7))
ret, smooth_thresh = cv.threshold(blurred_thresh, 20, 255, cv.THRESH_BINARY)

vegetation_pixel_amount = 0
sum_of_x_coordinates = 0
sum_of_y_coordinates = 0

masked_height, masked_width = gray_img_with_color_mask.shape
for y in range(masked_height):
    for x in range(masked_width):
        if img_with_color_mask_thresholded[y,x]:
            vegetation_pixel_amount += 1
            sum_of_y_coordinates += y
            sum_of_x_coordinates += x

centroid_y = round(sum_of_y_coordinates/vegetation_pixel_amount)
centroid_x = round(sum_of_x_coordinates/vegetation_pixel_amount)
centroid_position = (centroid_y, centroid_x)

# Definidor de area efetivamente arborizada
total_area_pixel_amount = img.shape[0] * img.shape[1] if not should_apply_initial_mask else inital_mask_pixel_amout
vegetation_percentage_area = round((vegetation_pixel_amount / (total_area_pixel_amount)) * 100, 3)

real_total_area = round(total_area_pixel_amount * square_pixel_to_square_meter, 2)
real_vegetation_area = round(vegetation_pixel_amount * square_pixel_to_square_meter, 2)

# Determinador de Contornos
edges = cv.Canny(cv.bitwise_not(smooth_thresh), 120, 140)
contours, hierarch = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
img_with_contours = cv.drawContours(img_with_color_mask.copy(), contours, -1, (255, 0, 0), 2)

# Gerador de Imagem Final
base_darkened_img = cv.convertScaleAbs(img.copy(), alpha=0.2, beta=0)
result_over_base_img = cv.bitwise_or(base_darkened_img, img_with_contours)
cv.imshow('Resultado sobre Imagem Base', result_over_base_img)
cv.imwrite("Resultado sobre Imagem Base.png",  result_over_base_img)


if should_apply_initial_mask:
    initial_mask_darkened_img = cv.bitwise_and(base_darkened_img, base_darkened_img, mask=initial_mask)
    result_over_inital_mask = cv.bitwise_or(initial_mask_darkened_img, img_with_contours)
    cv.imshow('Resultado sobre Imagem sob mascara inicial', result_over_inital_mask )

# Output das Informações Obtidas:
print()
print(f"De um total de {real_total_area}m², {real_vegetation_area}m² estão arborizados!")
print(f"Isso representa uma arborização de {vegetation_percentage_area}%")

cv.waitKey(0)

