import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import *

# user config
NIPPOS = '991483728'
PASSWORD = '1991091812'

# chrome options
path = os.path.join(os.path.dirname(__file__), 'chromedriver')
options = Options()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(executable_path=path, options=options)
wait = WebDriverWait(driver, 10)


def login_app(action):
    try:
        driver.get("https://presensi.posindonesia.co.id/")
        driver.find_element(By.NAME, "UserID").send_keys(NIPPOS)
        driver.find_element(By.NAME, "Password").send_keys(PASSWORD)
        driver.find_element(By.XPATH,
                            "//button[normalize-space()='Login']").click()
    except (UnexpectedAlertPresentException, NoSuchElementException) as e:
        # TODO logger.error()
        driver.quit()
    else:
        if action == 'check_in':
            check_in()
        elif action == 'check_out':
            check_out()


def logout_app():
    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//img[@title='LOGOUT']"))).click()
    except (NoSuchElementException, TimeoutException) as e:
        # TODO logger.error()
        print(e)
    finally:
        driver.quit()


def check_in():
    try:
        # click "Presensi Masuk" button
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[normalize-space()='Presensi Masuk']"))).click()
        alert_container = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='sweet-alert showSweetAlert']")))
        # click "OK" button
        time.sleep(1)
        # TODO logger.info()
        alert_container.find_element(By.XPATH,
                                     "//button[@class='confirm'][normalize-space()='OK']").click()
    except (NoSuchElementException, TimeoutException) as e:
        # TODO logger.error()
        print(e)
        driver.quit()
    else:
        logout_app()


def check_out():
    try:
        # click "Presensi Pulang" button
        wait.until(
            EC.presence_of_element_located((By.XPATH,
                                            "//button[normalize-space()='Presensi Pulang']"))).click()
        alert_container = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='sweet-alert showSweetAlert']")))
        # click "OK" button (confirmation)
        time.sleep(1)
        alert_container.find_element(By.XPATH,
                                     "//button[@class='confirm'][normalize-space()='OK']").click()
        # click "OK" button
        time.sleep(1)
        # TODO logger.info()
        alert_container.find_element(By.XPATH,
                                     "//button[@class='confirm'][normalize-space()='OK']").click()
    except (NoSuchElementException, TimeoutException) as e:
        # TODO logger.error()
        print(e)
        driver.quit()
    else:
        logout_app()
