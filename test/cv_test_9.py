from pandas import Series, DataFrame
import cv2, random
from matplotlib import pyplot as plt
import datasource.transform as tf
import numpy as np
from PIL import Image

BORDER_R_1 = 200
BORDER_R_2 = 230
BORDER_G_1 = 100
BORDER_G_2 = 120
BORDER_B_1 = 160
BORDER_B_2 = 180

def crop(code: str, margin: int):
    file = f"./datasource/captured/map/{code}.png"
    print(file)

    im = Image.open(file, 'r')
    width, height = im.size

    rgb = im.convert("RGB")

    min_x = width + 1
    min_y = height + 1
    max_x = -1
    max_y = -1

    for x in range(0, width):
        for y in range(0, height):
            r, g, b = rgb.getpixel((x, y))
            if x == 3745 and y == 3:
                print(r, g, b)
            if BORDER_R_1 <= r <= BORDER_R_2 and BORDER_G_1 <= g <= BORDER_G_2 and BORDER_B_1 <= b <= BORDER_B_2:
                # print(x, y)
                if min_x >= x:
                    min_x = x
                if min_y >= y:
                    min_y = y
                if max_x <= x:
                    max_x = x
                if max_y <= y:
                    max_y = y

    min_x -= margin
    min_y -= margin
    max_x += margin
    max_y += margin

    # print(min_x, min_y)
    # print(max_x, max_y)

    x = min_x
    y = min_y
    w = max_x - min_x
    h = max_y - min_y

    image = cv2.imread(file)
    img_trim = image[y:y+h, x:x+w]
    try:
        cv2.imwrite(f'./datasource/captured/map-crop/{code}.png', img_trim)
    except:
        print(file)
    # org_image = cv2.imread('res.png')

    # cv2.imshow('org_image', org_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

if __name__ == "__main__":
    data: DataFrame = tf.read()
    # for i in range(0, 18422):
    subset = data.iloc[18000:20000]
    for index, row in subset.iterrows():
        crop(row['코드'], 0)

    # file = f"./datasource/captured/map-crop/0.png"
    #
    # image = cv2.imread(file)
    # image_gray = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    # image_gray2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #
    # b,g,r = cv2.split(image)
    # image2 = cv2.merge([r,g,b])
    #
    # plt.imshow(image2)
    # plt.xticks([])
    # plt.yticks([])
    # plt.show()
    #
    # blur = cv2.GaussianBlur(image_gray, ksize=(3,3), sigmaX=0)
    # ret, thresh1 = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
    #
    # # ret, img_binary = cv2.threshold(image_gray2, 127, 255, 0)
    # contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE) # 컨투어 검출
    #
    # for cnt in contours:
    #     for p in cnt:
    #         cv2.circle(image, (p[0][0], p[0][1]), 10, (255, 0, 0), -1) # 모든좌표마다 파란원을 그리도록 함
    #
    # # cv2.drawContours(image, contours, 0, (0, 255, 0), 3)
    #
    # cv2.imshow("result", image)
    # cv2.waitKey(0)

    # edged = cv2.Canny(blur, 10, 250)
    # cv2.imshow('Edged', edged)
    # cv2.waitKey(0)




    # mode = [cv2.RETR_EXTERNAL, cv2.RETR_LIST, cv2.RETR_CCOMP, cv2.RETR_TREE]
    # name = ['RETR_EXTERNAL', 'RETR_LIST', 'RETR_CCOMP', 'RETR_TREE']
    #
    # for m in mode:
    #     contours, hier = cv2.findContours(image_gray, m, cv2.CHAIN_APPROX_NONE)
    #
    #     dst = cv2.cvtColor(image_gray, cv2.COLOR_GRAY2BGR)
    #
    #     idx = 0
    #     while idx >= 0:
    #         c = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # 랜덤 BGR값 생성
    #         cv2.drawContours(dst, contours, idx, c, 2, cv2.LINE_8, hier)
    #         idx = hier[0, idx, 0]  # 다음 외곽선이 없으면 -1 반환
    #     cv2.imshow(name[m], dst)
    #
    # cv2.waitKey()
    # cv2.destroyAllWindows()



    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
    # closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow('closed', closed)
    # cv2.waitKey(0)
    #
    # contours, _ = cv2.findContours(closed.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # total = 0
    #
    # contours_xy = np.array(contours)
    # contours_xy.shape




