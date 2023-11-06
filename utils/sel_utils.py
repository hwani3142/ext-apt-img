import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webdriver import WebElement
from typing import Union, Tuple


def build_browser(url: str, full_screen: bool = True):
    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    # service = webdriver.ChromeService(executable_path="chromedriver-mac-arm64/chromedriver")

    driver = webdriver.Chrome(options=options)
    if full_screen:
        driver.maximize_window()
    driver.get(url)
    time.sleep(5)
    return driver


def delete_element_by_class(driver: WebDriver, class_name: str):
    element = driver.find_element(by=By.CLASS_NAME, value=class_name)
    driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)


def delete_element_by_xpath(driver: WebDriver, value: str):
    element = driver.find_element(by=By.XPATH, value=value)
    driver.execute_script("""
        var element = arguments[0];
        element.parentNode.removeChild(element);
        """, element)


def lazy_click(driver: WebDriver, mark: Union[WebElement, Tuple[str, str]]):
    timeout = 20
    driver.execute_script("arguments[0].click();",
                          WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(mark)))