import cv2 as cv

from main import filter_image

area_efetiva = [11619.71, 4938.85, 6983.48, 930.67, 6639.72, 10673.67, 21207.25, 7249.32, 9198.49, 12340.8]
real_vegetation_list = [2421, 307.89, 1087.73, 452.85, 599.44, 690.03, 11167.5, 922.28, 758.56, 802.53]
links = [
"https://www.google.com.br/maps/@-5.0589665,-42.7684833,52m/data=!3m1!1e3",
"https://www.google.com.br/maps/@-5.0591587,-42.7671089,146m/data=!3m1!1e3",
"https://www.google.com.br/maps/@-5.0859707,-42.7964782,195m/data=!3m1!1e3",
"https://www.google.com.br/maps/@-5.0674646,-42.8086068,52m/data=!3m1!1e3",
"https://www.google.com.br/maps/@-5.0880791,-42.8147817,158m/data=!3m1!1e3",
"https://www.google.com/maps/@-5.0887517,-42.8161394,103m/data=!3m1!1e3",
"https://www.google.com/maps/@-5.1025247,-42.8110188,113m/data=!3m1!1e3",
"https://www.google.com/maps/@-5.1013194,-42.8125332,213m/data=!3m1!1e3",
"https://www.google.com/maps/@-5.0853919,-42.8064593,207m/data=!3m1!1e3"
"https://www.google.com/maps/@-5.0696333,-42.7835492,103m/data=!3m1!1e3",
"https://www.google.com/maps/@-5.0970276,-42.8136381,53m/data=!3m1!1e3"
]

from return_constant_pixel_to_meter import return_constant_pixel_to_meter
return_constant_pixel_to_meter(20, cv.imread("C:/Users/Luiz Gonzaga/Desktop/Projects/Analista-De-Aborizacao - Para Enviar Git/Condominios_Usados/escala_0.png"))

# --------------------------
# Individual-Plot Analysis
# --------------------------

index = 6
original_image = cv.imread(f"./Condominios_Usados/Condominio_{index}_original.png")
delimitated_image = cv.imread(f"./Condominios_Usados/delimitado_1px/Condominio_{index}_delimitado_photo.png")
reference_tree = cv.imread(f"./Condominios_Usados/referencia_{index}.png")
scale = cv.imread(f"./Condominios_Usados/escala_{index}.png")

result = filter_image( original_image, reference_tree, True, True, scale, 20, False, delimitated_image, cv.COLOR_BGR2HSV)
cv.imshow(str(index), result["img"])
cv.waitKey(0)


# --------------------------
# All-Plots Analysis
# --------------------------


# for color_space in ["HSV", "HLS", "LAB", "LUV"]:
#     general_result = []
#     color_space_convertor = eval(f"cv.COLOR_BGR2{color_space}")

#     for index in range(5):
#         original_image = cv.imread(f"./Condominios_Usados/Condominio_{index}_original.png")
#         delimitated_image = cv.imread(f"./Condominios_Usados/delimitado_1px/Condominio_{index}_delimitado_photo.png")
#         reference_tree = cv.imread(f"./Condominios_Usados/referencia_{index}.png")
#         scale = cv.imread(f"./Condominios_Usados/escala_{index}.png")


#         if index == 3:
#             result = filter_image( original_image, reference_tree, True, True, scale, 5, False, delimitated_image, color_space_convertor)
#         else:
#             result = filter_image( original_image, reference_tree, True, True, scale, 20, False, delimitated_image, color_space_convertor)

#         cv.imshow(str(index) + " HSV", result["img"])
#         cv.waitKey(1)

#         result = result["data"]

#         result["index"] = index
#         result["link"] = links[index]
#         result["total_area"] = area_efetiva[index]
#         result["vegetation_area"] = real_vegetation_list [index]
#         result["vegetation_percentage"] = round((result["vegetation_area"] * 100)/ result["total_area"], 3)
#         result["scale_precision"] = min(result["total_area_calculated"], result["total_area"]) / max(result["total_area_calculated"], result["total_area"])

#         general_result.append(result)

#     print(f"dados_{color_space} = {general_result}")

#     # cv.waitKey(0)