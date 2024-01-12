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

def blur(code: str, margin: int):
    file = f"./datasource/captured/map-crop/{code}.png"
    result_filename = f'./datasource/captured/map-blur/{code}.png'

    if not os.path.isfile(f"{os.getcwd()}/{file}"):
        print(f"skip empty address - {code}")
        return

    # if os.path.isfile(f"{os.getcwd()}/{result_filename}"):
    #     print(f"skip already done -- {code}")
    #     return

    print(file)

    im = Image.open(file, 'r')
    width, height = im.size
    rgb = im.convert("RGB")

    print(width, height)

    blur_iter(width, height, rgb, im)

    # 회전
    # im.rotate(90)
    # width, height = im.size
    # rgb = im.convert("RGB")
    # blur_iter(width, height, rgb, im)
    #
    # im.rotate(-90)

    # 저장
    try:
        im.save(result_filename)
    except:
        print(file)

def blur_iter(outer, inner, rgb, im):
    for x in range(0, outer):
        count = 0
        points = []
        detect = False

        for y in range(0, inner):
            r, g, b = rgb.getpixel((x, y))

            # detect area
            if BORDER_R_1 <= r <= BORDER_R_2 and BORDER_G_1 <= g <= BORDER_G_2 and BORDER_B_1 <= b <= BORDER_B_2:
                # 개
                if not detect:
                    detect = True
                    points.append(y)
            else:
                # 폐
                if detect:
                    detect = False
                    count += 1
                    points.append(y)

        if detect == True:
            count += 1
            detect = False
            points.append(inner)

        '''
        1개 -> 양끝
        2개 -> 양끝
        3개 -> 양끝 
        4개 -> 양끝, 2~3번
        5개 -> 양끝, 2~3번 3~4번
        '''
        if count == 1:
            # print(x, points)
            process_1(im, x, inner, points)
        elif count == 2:
            # print(x, points)
            process_2(im, x, inner, points)
        elif count == 3:
            # print(x, points)
            process_3(im, x, inner, points)
        elif count == 4:
            # print(x, points)
            process_4(im, x, inner, points)
        elif count == 5:
            # print(x, points)
            process_5(im, x, inner, points)


def process_1(image, x: int, height: int, points: list[int]):
    for y in range(0, height):
        if y <= points[0] or points[1] <= y:
            # print(x, y)
            # image[x][y] = (0, 0, 0)
            image.putpixel((x,y), (0, 0, 0))

def process_2(image, x: int, height: int, points: list[int]):
    for y in range(0, height):
        if y <= points[0] or points[3] <= y:
            # print(x, y)
            image.putpixel((x,y), (0, 0, 0))

def process_3(image, x: int, height: int, points: list[int]):
    for y in range(0, height):
        if y <= points[0] or points[5] <= y:
            # print(x, y)
            image.putpixel((x,y), (0, 0, 0))
        # elif points[3] <= y <= points[4]:
        #     image.putpixel((x,y), (0, 0, 0))

def process_4(image, x: int, height: int, points: list[int]):
    for y in range(0, height):
        if y <= points[0] or points[7] <= y:
            # print(x, y)
            image.putpixel((x,y), (0, 0, 0))
        elif points[3] <= y <= points[4]:
            image.putpixel((x,y), (0, 0, 0))

def process_5(image, x: int, height: int, points: list[int]):
    for y in range(0, height):
        if y <= points[0] or points[9] <= y:
            # print(x, y)
            image.putpixel((x,y), (0, 0, 0))
        elif points[3] <= y <= points[4]:
            image.putpixel((x,y), (0, 0, 0))
        elif points[5] <= y <= points[6]:
            image.putpixel((x,y), (0, 0, 0))


if __name__ == "__main__":
    data: DataFrame = tf.read()
    # for i in range(0, 18422):
    subset = data.iloc[0:100]
    for index, row in subset.iterrows():
        blur(row['코드'], 0)




