#!/usr/bin/env pipenv-shebang
import os
import time
import logging.config

import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    UnexpectedAlertPresentException, NoSuchElementException, TimeoutException)

from telegrambot import PythonTelegramBot


# create bot object
bot = PythonTelegramBot()

# init logging
with open('logging.yaml', 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
    logging.config.dictConfig(config)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# chrome options
path = os.path.join(os.path.dirname(__file__), 'chromedriver')
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path=path, options=options)
wait = WebDriverWait(driver, 10)


def login_app(action):
    try:
        driver.get("https://presensi.posindonesia.co.id/")
        driver.find_element(By.NAME, "UserID").send_keys('991483728')
        driver.find_element(By.NAME, "Password").send_keys('1991091812')
        driver.find_element(By.XPATH,
                            "//button[normalize-space()='Login']").click()
    except (UnexpectedAlertPresentException, NoSuchElementException, TimeoutException) as e:
        logger.exception(e)
        driver.quit()
        bot.send_message(ptext='Sir.. you can\'t login coz of error')
    else:
        if action == 'check_in':
            check_in()
        elif action == 'check_out':
            check_out()


def logout_app(message):
    try:
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//img[@title='LOGOUT']"))).click()
    except (NoSuchElementException, TimeoutException) as e:
        logger.exception(e)
    finally:
        driver.quit()
        bot.send_message(ptext=message)


def check_in():
    try:
        # click "Presensi Masuk" button
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//button[normalize-space()='Presensi Masuk']"))).click()
        alert_container = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='sweet-alert showSweetAlert']")))
        alert_message = alert_container.find_element(By.TAG_NAME, 'h2').text
        logger.info(f'Check In: {alert_message}')
        # click "OK" button
        time.sleep(1)
        alert_container.find_element(By.XPATH,
                                     "//button[@class='confirm'][normalize-space()='OK']").click()
    except (NoSuchElementException, TimeoutException) as e:
        logger.exception(e)
        driver.quit()
    else:
        logout_app(f'Check In: {alert_message}')


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
        alert_message = alert_container.find_element(By.TAG_NAME, 'h2').text
        logger.info(f'Check Out: {alert_message}')
        alert_container.find_element(By.XPATH,
                                     "//button[@class='confirm'][normalize-space()='OK']").click()
    except (NoSuchElementException, TimeoutException) as e:
        logger.exception(e)
        driver.quit()
    else:
        logout_app(f'Check Out: {alert_message}')
