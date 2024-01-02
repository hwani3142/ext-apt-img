from pandas import Series, DataFrame
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
import os
import datasource.transform as tf
import time
from utils.sel_utils import build_browser, delete_element_by_class, delete_element_by_xpath, lazy_click

# 카카오 지도
url = "https://map.kakao.com/"
result_path = "datasource/captured/map"
raw_result_path = "datasource/captured/map-raw"
ignore_done = True
start_index = 13973
end_index = -1


def zoom_in(driver: WebDriver):
    lazy_click(driver, (By.XPATH, "//button[@title='확대']"))


def search(driver: WebDriver, address: str, result_filename: str, raw_result_filename: str):
    search_area = driver.find_element(by=By.CLASS_NAME, value="box_searchbar")
    search_input = search_area.find_element(value="search.keyword.query")

    # search
    search_input.send_keys(address)
    lazy_click(driver, (By.ID, "search.keyword.submit"))

    time.sleep(3)
    try:
        # delete popup
        delete_element_by_class(driver, "AddressInfoWindow")

        # delete center mark
        delete_element_by_class(driver, "inner_coach_layer")

        # delete position mark
        delete_element_by_xpath(driver,
                                "//div[@style='position: absolute; z-index: 1; width: 100%; height: 0px; transform: translateZ(0px);']")
    except:
        print("except1")

    # zoom_in(driver)
    # time.sleep(2)

    driver.save_screenshot(result_filename)
    time.sleep(1)

    # delete address area
    try:
        area = driver.find_element(by=By.XPATH, value="//*[starts-with(@id, 'daum-maps-shape-')]")
        driver.execute_script("arguments[0].setAttribute('style', arguments[1])", area, "display: none;")
        time.sleep(1)
        driver.save_screenshot(raw_result_filename)
    except:
        print("")

    # clear
    lazy_click(driver, (By.CLASS_NAME, "clear"))
    print(f"done -- {result_filename}")


def run(data: DataFrame):
    try:
        driver = build_browser(url)

        for index, row in data.iterrows():
            if index < start_index:
                continue

            if 0 < end_index == index:
                break

            result_filename = f"{result_path}/{index}.png"
            raw_result_filename = f"{raw_result_path}/{index}.png"
            address: str = row['도로명주소']
            print(f"{os.getcwd()}/{result_filename} - {address}")

            if len(address) == 0:
                print(f"skip empty address - {index} {address}")
                continue

            if ignore_done and os.path.isfile(f"{os.getcwd()}/{result_filename}") and os.path.isfile(f"{os.getcwd()}/{raw_result_filename}"):
                print(f"skip already done -- {index}  {address}")
                continue
            if "," in address:
                address = row['도로명주소'].split(",")[0]
            search(driver, address, result_filename, raw_result_filename)

        time.sleep(5)
        driver.quit()
        return True
    except:
        return False


if __name__ == "__main__":
    data: DataFrame = tf.read()

    while True:
        res = run(data)
        if res:
            print("retry..")
            break