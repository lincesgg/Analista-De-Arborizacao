import cv2 as cv
import numpy as np
import SHSX
from return_constant_pixel_to_meter import return_constant_pixel_to_meter
from initial_mask_identifier import return_initial_mask
from feature_tracker import return_tree_color_interval

def filter_image(
    original_image,
    reference_tree,
    should_convert_area_in_scale,
    should_apply_initial_mask,
    scale=[],
    real_distance_represented_by_scale=20,
    should_analyze_just_the_biggest_shape=True,
    delimitated_image=[],
    color_space_used_by_feature_tracker=cv.COLOR_BGR2HSV
    ):

    # Definidor de Escala
    if should_convert_area_in_scale:
        pixel_to_meter = return_constant_pixel_to_meter(real_distance_represented_by_scale, scale)
        square_pixel_to_square_meter = pixel_to_meter**2

    # Rastreador de Características
    lowest, highest = return_tree_color_interval(reference_tree, color_space_used_by_feature_tracker)

    # Importar Imagem Base
    img = original_image
    # img_in_other_color_system = img
    img_in_other_color_system = cv.cvtColor(img, color_space_used_by_feature_tracker)
    if color_space_used_by_feature_tracker in [cv.COLOR_BGR2HSV, cv.COLOR_BGR2HLS]:
        img_in_other_color_system = SHSX.convert_img_to(img_in_other_color_system, SHSX.HSX_2_SHSX)

    # Aplicar máscara inicial
    if should_apply_initial_mask:
        initial_mask, inital_mask_pixel_amout = return_initial_mask(original_image, delimitated_image, should_analyze_just_the_biggest_shape)
        img_in_other_color_system = cv.bitwise_and(img_in_other_color_system, img_in_other_color_system, mask=initial_mask)

    # Aplicar máscara de cor
    color_mask = cv.inRange(img_in_other_color_system, lowest, highest)
    img_with_color_mask = cv.bitwise_and(img, img, mask=color_mask)

    cv.imshow('Original', img)
    cv.imshow('mask', color_mask)
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

    if should_convert_area_in_scale:
        real_total_area = round(total_area_pixel_amount * square_pixel_to_square_meter, 2)
        real_vegetation_area = round(vegetation_pixel_amount * square_pixel_to_square_meter, 2)

    # Determinador de Contornos
    edges = cv.Canny(cv.bitwise_not(smooth_thresh), 120, 140)
    contours, hierarch = cv.findContours(edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    img_with_contours = cv.drawContours(img_with_color_mask.copy(), contours, -1, (255, 0, 0), 2)

    # Gerador de Imagem Final
    base_darkened_img = cv.convertScaleAbs(img.copy(), alpha=.2, beta=0)
    result_over_base_img = cv.bitwise_or(base_darkened_img, img_with_contours)
    cv.imshow('Resultado sobre Imagem Base', result_over_base_img)

    if should_apply_initial_mask:
        initial_mask_darkened_img = cv.bitwise_and(base_darkened_img, base_darkened_img, mask=initial_mask)
        result_over_inital_mask = cv.bitwise_or(initial_mask_darkened_img, img_with_contours)
        cv.imshow('Resultado sobre Imagem sob mascara inicial', result_over_inital_mask )

    # Output das Informações Obtidas:
    if should_convert_area_in_scale:
        print(f"De um total de {real_total_area}m², {real_vegetation_area}m² estão arborizados!")
    print(f"Isso representa uma arborização de {vegetation_percentage_area}%")

    return {
        "data":{
            "vegetation_percentage_calculated":vegetation_percentage_area,
            "vegetation_area_calculated":real_vegetation_area ,
            "total_area_calculated":real_total_area
        },
        "img": result_over_base_img
    }

if __name__ == "__main__":
    # Paths
    original_image = "Condominio_original.png"
    delimitated_image = "Condominio_delimitado.png"
    reference_tree = "referencia.png"
    scale = "escala.png"

    # Image Reading
    original_image = cv.imread("./Condominio_original.png")
    delimitated_image = cv.imread("./Condominio_delimitado.png")
    reference_tree = cv.imread("./referencia.png")
    scale = cv.imread("./escala.png")

    # Input
    print("Você deseja aplicar uma imagem delimitadora? [S/N]")
    print("(Qualquer outra entrada diferente de [S/N], será compreendida como [N])")
    should_apply_initial_mask = input() in ["S", "s"]
    should_analyze_just_the_biggest_shape = False
    if should_apply_initial_mask:
        print("Você quer analisar somente a Maior forma delimitada ou Todas as formas delimitadas? [M/T]")
        print("(Qualquer outra entrada diferente de [M/T], será compreendida como [T])")
        should_analyze_just_the_biggest_shape = input() in ["M", "m"]
    print("Qual o tamanho que representa sua escala? ")
    print("Distancias consideradas invalidas serão automaticamente reajustadas para 20m")
    real_distance_representated = input()
    if not real_distance_representated.isdigit():
        real_distance_representated = 20
    real_distance_representated = int(real_distance_representated)

    results = filter_image( original_image, reference_tree, True, True, scale, 20, False, delimitated_image)

    cv.imshow("Result", results["img"])
    # cv.imwrite("Result.png", results[2])
    cv.waitKey(0)
