import cv2 as cv
import numpy as np

def BGR_2_SHSV(_pixel):
        pixel = [int(_pixel[0]), int(_pixel[1]), int(_pixel[2])]
        b, g, r = pixel

        _max = max(b, g, r)
        _min = min(b, g, r)

        _max_channel = ["b", "g", "r"][pixel.index(_max)]

        # Defining HUE (H)
        if _max == _min:
            pixel[0] = 0
            
        else:
            match(_max_channel):

                case "r":
                    pixel[0] = (60 * ((g-b)/(_max-_min))) + 60
                        
                case "g":
                    pixel[0] = (60 * ((b-r)/(_max-_min))) + 180

                case "b":
                    pixel[0] = (60 * ((r-g)/(_max-_min))) + 300

        pixel[0] /= 2

        # Defining SATURATION (S)
        pixel[1] = 0 if _max == 0 else 1 - (_min/_max)
        pixel[1] *= 255

        # Defining VALUE (V)
        pixel[2] = _max
        
        # truncking
        pixel[0] = int( round(pixel[0], 0) )
        pixel[1] = int( round(pixel[1], 0) )
        
        return pixel

def HSX_2_SHSX(pixel):
    pixel[0] += 30
    if pixel[0] > 180: 
        pixel[0] -= 180
    return pixel

def SHSX_2_HSX(pixel):
    pixel[0] -= 30
    if pixel[0] < 0: 
        pixel[0] += 180
    return pixel

def map_rows(map_func):
    def _map_rows(row):
        row = list( map(map_func, row) )
        return row
    return _map_rows

def convert_img_to(img, map_func):
    return np.array( list( map(map_rows(map_func), img) ) )
