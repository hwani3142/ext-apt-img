from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import datasource.transform as tf
import time

# 카카오 지도
url = "https://map.kakao.com/"
result_path = "datasource/captured/map"
raw_result_path = "datasource/captured/map-raw"
ignore_done = True
last_index = -1

def build_browser():
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # service = webdriver.ChromeService(executable_path="chromedriver-mac-arm64/chromedriver")

    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.get(url)
    return driver


def delete_element_by_class(driver, class_name):
    element = driver.find_element(by=By.CLASS_NAME, value=class_name)
    driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)


def delete_element_by_xpath(driver, value):
    element = driver.find_element(by=By.XPATH, value=value)
    driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)


def lazy_click(driver, mark):
    timeout = 20
    driver.execute_script("arguments[0].click();",
                          WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(mark)))


def zoom_in(driver):
    # lazy_click(driver, (By.XPATH, "//button[@title='확대']"))
    lazy_click(driver, (By.XPATH, "//button[@title='확대']"))


def search(driver, address, result_filename, raw_result_filename):
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

    zoom_in(driver)
    time.sleep(2)

    driver.save_screenshot(result_filename)
    time.sleep(1)

    # delete address area
    area = driver.find_element(by=By.XPATH, value="//*[starts-with(@id, 'daum-maps-shape-')]")
    driver.execute_script("arguments[0].setAttribute('style', arguments[1])", area, "display: none;")
    time.sleep(1)
    driver.save_screenshot(raw_result_filename)

    # clear
    lazy_click(driver, (By.CLASS_NAME, "clear"))
    print(f"done -- {result_filename}")


def run():
    driver = build_browser()

    data = tf.read()
    for index, row in data.iterrows():
        if 0 < last_index == index:
            break

        result_filename = f"{result_path}/{index}.png"
        raw_result_filename = f"{raw_result_path}/{index}.png"
        print(f"{os.getcwd()}/{result_filename}")
        if ignore_done and os.path.isfile(f"{os.getcwd()}/{result_filename}") and os.path.isfile(f"{os.getcwd()}/{raw_result_filename}"):
            print(f"skip already done -- {index}  {row['도로명주소']}")
            continue
        address = row['도로명주소']
        search(driver, address, result_filename, raw_result_filename)

    time.sleep(5)
    driver.quit()


if __name__ == "__main__":
    run()
