#!/usr/bin/env pipenv-shebang
import os
import time
import datetime
import logging.config

import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException
)

from telegrambot import TelegramBot


class Presensi:

    def driver(self):
        self.path = os.path.join(os.path.dirname(__file__), 'chromedriver')
        self.options = Options()
        self.options.add_argument('--headless')
        return webdriver.Chrome(executable_path=self.path, options=self.options)

    def login_app(self, action, userid='991483728', password='1991091812'):
        try:
            driver = self.driver()
            driver.get('http://presensi.posindonesia.co.id/')
            driver.find_element(By.NAME, 'UserID').send_keys(userid)
            driver.find_element(By.NAME, 'Password').send_keys(password)
            driver.find_element(
                By.XPATH, "//button[normalize-space()='Login']").click()

            # wait until 3 sec until alert is present
            # if present, execute code in this block
            WebDriverWait(driver, 3).until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            driver.quit()

            logger.info(f'{userid} | login_app(): NOK')
            message = 'User ID or Password you entered is not valid'
            bot.send_message(text=message)
        except (TimeoutException):
            # alert not present, execute code in this block
            logger.info(f'{userid} | login_app(): OK')

            if action == 'check_in':
                self.check_in(driver, userid)
            elif action == 'check_out':
                self.check_out(driver, userid)
        except(NoSuchElementException) as e:
            driver.quit()

            logger.exception(e)
            message = 'Unable to login because an unexpected error is occurs'
            bot.send_message(text=message)

    def logout_app(self, driver, message):
        driver.find_element(By.XPATH, "//img[@title='LOGOUT']").click()
        driver.quit()

        bot.send_message(text=message)

    def check_in(self, driver, userid):
        try:
            driver.find_element(
                By.XPATH, "//button[normalize-space()='Presensi Masuk']").click()
            alert_container = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='sweet-alert showSweetAlert']")))

            # get alert message
            alert_message = alert_container.find_element(
                By.TAG_NAME, 'h2').text
            if alert_message == 'Anda Tidak Bisa Melakukan Presensi Dikarenakan Hari Libur':
                message = 'Unable to check in because it\'s holidays'
                logger.info(f'{userid} | check_in(): NOK')
            elif alert_message == 'Anda Sudah Melakukan Presensi':
                message = 'Already check in before'
                logger.info(f'{userid} | check_in(): AOK')
            else:
                message = f'Check in success at {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")} WIB'
                logger.info(f'{userid} | check_in(): OK')

            # click "OK" button and logout
            time.sleep(1)
            alert_container.find_element(By.XPATH,
                                         "//button[@class='confirm'][normalize-space()='OK']").click()
            self.logout_app(driver, message)
        except(NoSuchElementException, TimeoutException) as e:
            driver.quit()

            logger.exception(e)
            message = 'Unable to check in because an unexpected error is occurs'
            bot.send_message(text=message)

    def check_out(self, driver, userid):
        try:
            driver.find_element(
                By.XPATH, "//button[normalize-space()='Presensi Pulang']").click()
            alert_container = WebDriverWait(driver, 3).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='sweet-alert showSweetAlert']")))

            # click "OK" button (confirmation)
            time.sleep(1)
            alert_container.find_element(
                By.XPATH, "//button[@class='confirm'][normalize-space()='OK']").click()

            # get alert message
            time.sleep(1)
            alert_message = alert_container.find_element(
                By.TAG_NAME, 'h2').text

            # clik "OK" button and logout
            alert_container.find_element(By.XPATH,
                                         "//button[@class='confirm'][normalize-space()='OK']").click()
            message = f'Check out success at {datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")} WIB'
            logger.info(f'{userid} | check_out(): OK')
            self.logout_app(driver, message)
        except(NoSuchElementException, TimeoutException) as e:
            driver.quit()

            logger.exception(e)
            message = 'Unable to check out because an unexpected error is occurs'
            bot.send_message(text=message)


def setup_logs():
    dirpath = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.isdir(dirpath):
        os.mkdir(dirpath)

    logs = ['info.log', 'error.log', 'cron.log']
    for log in logs:
        filepath = os.path.join(dirpath, log)
        if not os.path.isfile(filepath):
            with open(filepath, 'w') as f:
                pass


def init_logger():
    with open('logging.yaml', 'r') as file:
        config = yaml.load(file, Loader=yaml.FullLoader)
        logging.config.dictConfig(config)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    return logger


if __name__ != '__main__':
    setup_logs()
    logger = init_logger()
    bot = TelegramBot()
