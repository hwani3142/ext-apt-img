from pandas import Series, DataFrame
import cv2, random
from matplotlib import pyplot as plt
import datasource.transform as tf
import numpy as np
from PIL import Image
import os

BORDER_R_1 = 200
BORDER_R_2 = 230
BORDER_G_1 = 100
BORDER_G_2 = 120
BORDER_B_1 = 160
BORDER_B_2 = 180

def blur(code: str):
    file = f"./datasource/captured/map-crop/{code}.png"
    result_filename = f'./datasource/captured/map-blur/{code}.png'

    if not os.path.isfile(f"{os.getcwd()}/{file}"):
        print(f"skip empty address - {code}")
        return

    if os.path.isfile(f"{os.getcwd()}/{result_filename}"):
        print(f"skip already done -- {code}")
        return

    print(file)

    im = Image.open(file, 'r')
    width, height = im.size
    rgb = im.convert("RGBA")

    blur_up(width, height, rgb, im)
    blur_left(width, height, rgb, im)
    blur_down(width, height, rgb, im)
    blur_right(width, height, rgb, im)

    # 저장
    try:
        im.save(result_filename)
    except:
        print(file)

def blur_up(outer, inner, rgb, im):
    for x in range(0, outer):
        for y in range(0, inner):
            r, g, b, a = rgb.getpixel((x, y))

            if BORDER_R_1 <= r <= BORDER_R_2 and BORDER_G_1 <= g <= BORDER_G_2 and BORDER_B_1 <= b <= BORDER_B_2:
                break
            else:
                im.putpixel((x, y), (255, 255, 255, 0))

def blur_left(outer, inner, rgb, im):
    for y in range(0, inner):
        for x in range(0, outer):
            r, g, b, a = rgb.getpixel((x, y))

            if BORDER_R_1 <= r <= BORDER_R_2 and BORDER_G_1 <= g <= BORDER_G_2 and BORDER_B_1 <= b <= BORDER_B_2:
                break
            else:
                im.putpixel((x, y), (255, 255, 255, 0))

def blur_down(outer, inner, rgb, im):
    for x in range(0, outer):
        for y in range(inner-1, -1, -1):
            r, g, b, a = rgb.getpixel((x, y))

            if BORDER_R_1 <= r <= BORDER_R_2 and BORDER_G_1 <= g <= BORDER_G_2 and BORDER_B_1 <= b <= BORDER_B_2:
                break
            else:
                im.putpixel((x, y), (255, 255, 255, 0))

def blur_right(outer, inner, rgb, im):
    for y in range(0, inner):
        for x in range(outer-1, -1, -1):
            r, g, b, a = rgb.getpixel((x, y))

            if BORDER_R_1 <= r <= BORDER_R_2 and BORDER_G_1 <= g <= BORDER_G_2 and BORDER_B_1 <= b <= BORDER_B_2:
                break
            else:
                im.putpixel((x, y), (255, 255, 255, 0))


if __name__ == "__main__":
    data: DataFrame = tf.read()
    # for i in range(0, 18422):
    subset = data.iloc[0:18522]
    for index, row in subset.iterrows():
        blur(row['코드'])




