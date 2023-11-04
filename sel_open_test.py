from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 건축데이터 민간개방 시스템 - 도면 배치도 검색
url = "https://open.eais.go.kr/opnsvc/opnSvcInqireView.do#"


def build_browser():
    print("hi")
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # service = webdriver.ChromeService(executable_path="chromedriver-mac-arm64/chromedriver")

    browser = webdriver.Chrome(options=options)
    browser.get(url)
    return browser


def open_layout(browser):
    # depth1 6th, 도면정보
    infos = browser.find_elements(by=By.CLASS_NAME, value="dep1th")
    info = infos[6]
    info.click()

    # depth2, 배치도
    map = info.find_element(by=By.CLASS_NAME, value="dep2th")
    map.click()
    return map


def run():
    browser = build_browser()
    print("opened")

    time.sleep(30)
    browser.quit()
    print("end")


if __name__ == "__main__":
    run()
