from pandas import Series, DataFrame
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support.select import Select
import os
import time
import datasource.transform as tf
from utils.sel_utils import build_browser, delete_element_by_class, delete_element_by_xpath, lazy_click

# 건축데이터 민간개방 시스템 - 도면 배치도 검색
url = "https://open.eais.go.kr/opnsvc/opnSvcInqireView.do#"
result_path = "datasource/captured/open"
ignore_done = True
first_index = 114
last_index = -1

def select_layout(driver: WebDriver):
    # depth1 6th, 도면정보
    print("select 도면정보")
    infos = driver.find_elements(by=By.CLASS_NAME, value="dep1th")
    info = infos[6]
    # lazy_click(driver, (By.CLASS_NAME, "dep1th"))
    info.click()
    time.sleep(2)

    # depth2, 배치도
    print("select 배치도")
    map = info.find_element(by=By.CLASS_NAME, value="dep2th")
    map.click()
    time.sleep(2)

def screenshot_and_close_popup(driver: WebDriver, filename: str):
    tabs = driver.window_handles
    while len(tabs) != 1:
        driver.switch_to.window(tabs[1])
        driver.save_screenshot(filename)
        driver.close()
        tabs = driver.window_handles
    driver.switch_to.window(tabs[0])

def force_reload(driver: WebDriver):
    try:
        infos = driver.find_elements(by=By.CLASS_NAME, value="dep1th")
        info = infos[6]
        map = info.find_element(by=By.CLASS_NAME, value="dep2th")
        map.click()
        time.sleep(2)
    except:
        print("force refresh")
        driver.refresh()
        select_layout(driver)

def select_filter(driver: WebDriver, data: Series, result_filename: str):
    # click sidoCd
    sido_cd = Select(driver.find_element(by=By.XPATH, value="//select[@id='sidoCd']"))
    sido_cd.select_by_visible_text(data['시도'])

    # click sigungu
    sigungu_cd = Select(driver.find_element(by=By.XPATH, value="//select[@id='sigunguCdList']"))
    sigungu_cd.select_by_visible_text(data['시군구'])

    # click bjdong
    bjdong_cd = Select(driver.find_element(by=By.XPATH, value="//select[@id='bjdongCdList']"))
    bjdong_cd.select_by_visible_text(data['법정동'])

    # bjdong
    bun = driver.find_element(by=By.XPATH, value="//input[@name='bun']")
    if len(data["번지-1"]) > 0:
        bun.send_keys(data["번지-1"])

    ji = driver.find_element(by=By.XPATH, value="//input[@name='ji']")
    if len(data["번지-2"]) > 0:
        ji.send_keys(data["번지-2"])

    time.sleep(1)

    # search
    driver.find_element(by=By.CLASS_NAME, value="btn_search").click()
    time.sleep(10)

    # focus popup btn
    results = driver.find_elements(by=By.CLASS_NAME, value="GMPopupRight")
    if len(results) == 0:
        print("no result!")
        force_reload(driver)
        return

    actions = ActionChains(driver)
    actions.move_to_element(results[0]).perform()

    # click popup btn
    index = len(results) - 1
    driver.execute_script("arguments[0].click();", results[index])
    results[index].click()
    driver.execute_script("arguments[0].click();", results[index])
    results[index].click()
    time.sleep(20)

    # close popup
    screenshot_and_close_popup(driver, result_filename)
    time.sleep(5)

    # reset
    force_reload(driver)


def run():
    driver = build_browser(url, False)
    select_layout(driver)

    data: DataFrame = tf.append_jibun_addr(tf.read())
    for index, row in data.iterrows():
        if index < first_index:
            print(f"skip by range -- {index}  {row['도로명주소']}")
            continue

        if 0 < last_index == index:
            break

        result_filename = f"{result_path}/{index}.png"

        print(f"{index} -- {row['도로명주소']}")
        if ignore_done and os.path.isfile(f"{os.getcwd()}/{result_filename}"):
            print(f"skip already done -- {index}  {row['도로명주소']}")
            continue

        select_filter(driver, row, result_filename)

    time.sleep(2)
    driver.quit()
    print("end")


if __name__ == "__main__":
    run()
