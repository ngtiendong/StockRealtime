from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import re, json, sys, os
from threading import Thread
import threading
import logging
from time import sleep
from datetime import datetime
from config import *

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database.mysql import MySQL


class RealtimeCrawler:
    LOGIN_URL = 'https://www.facebook.com/login.php?login_attempt=1&lwv=111'

    def __init__(self, type):
        self.database = MySQL()
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("disable-infobars")
        chrome_options.add_argument("--disable-extensions")

        self.driver = webdriver.Chrome(executable_path=DRIVER, chrome_options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

        logging.basicConfig(filename='realtime.log', level=logging.INFO)

        if type == 0:
            # CURRENCY
            self.driver.get("https://vn.tradingview.com/symbols/EURUSD/")
            currency = threading.Thread(target=self.get_realtime_data, kwargs={
                "table": TABLE_REALTIME_CURRENCY,
                "symbol": "USD",
                "type": type,
                "wait_time": WAIT_CURRENCY,
                "xpath_value": "//*[@id='anchor-page-1']/div/div[3]/div[1]/div/div/div/div[1]/div[1]",
                "xpath_change_1": "//*[@id='anchor-page-1']/div/div[3]/div[1]/div/div/div/div[1]/div[3]/span[1]",
                "xpath_change_2": "//*[@id='anchor-page-1']/div/div[3]/div[1]/div/div/div/div[1]/div[3]/span[2]"
            })
            currency.start()
            currency.join()

        else:
            # STOCK
            self.driver.get("http://banggia2.ssi.com.vn/")

            vnindex_stock = threading.Thread(target=self.get_realtime_data, kwargs={
                "table": TABLE_REALTIME_STOCK,
                "symbol": "VNIndex",
                "type": type,
                "wait_time": WAIT_STOCK,
                "xpath_value": '//*[@id="tdHoseVnIndex"]',
                "xpath_change_1": '//*[@id="tdHoseChangeIndex"]',
                "xpath_change_2": ''
            })

            vn30_stock = threading.Thread(target=self.get_realtime_data, kwargs={
                "table": TABLE_REALTIME_STOCK,
                "symbol": "VN30INDEX",
                "type": type,
                "wait_time": WAIT_STOCK,
                "xpath_value": '//*[@id="tdHose30VnIndex"]',
                "xpath_change_1": '//*[@id="tdHose30ChangeIndex"]',
                "xpath_change_2": ''
            })

            hnxindex_stock = threading.Thread(target=self.get_realtime_data, kwargs={
                "table": TABLE_REALTIME_STOCK,
                "symbol": "HNXINDEX",
                "type": type,
                "wait_time": WAIT_STOCK,
                "xpath_value": '//*[@id="tdHnxIndex"]',
                "xpath_change_1": '//*[@id="tdHnxChangeIndex"]',
                "xpath_change_2": ''
            })
            hnx30_stock = threading.Thread(target=self.get_realtime_data, kwargs={
                "table": TABLE_REALTIME_STOCK,
                "symbol": "HNX30INDEX",
                "type": type,
                "wait_time": WAIT_STOCK,
                "xpath_value": '//*[@id="tdHnx30Index"]',
                "xpath_change_1": '//*[@id="tdHnx30ChangeIndex"]',
                "xpath_change_2": ''
            })

            vnindex_stock.start()
            vn30_stock.start()
            hnxindex_stock.start()
            hnx30_stock.start()

            vnindex_stock.join()
            vn30_stock.join()
            hnxindex_stock.join()
            hnx30_stock.join()
        # Thread currency
        # self.get_currency_data()

        # Thread stock

    def get_value_element(self, selector):
        value = self.driver.find_element_by_xpath(selector).text
        # print(value)
        return value

    def get_realtime_data(self, table, symbol, type, wait_time, xpath_value, xpath_change_1, xpath_change_2):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_value)))
        stock_value = self.get_value_element(xpath_value)

        while True:
            try:
                # VNIndex
                new_value = self.get_value_element(xpath_value)
                WebDriverWait(self.driver, wait_time).until(lambda value: new_value != stock_value)
                stock_value = new_value
                moment = datetime.now()
                if type == 0:
                    # CURRENCY
                    change_1 = self.driver.find_element_by_xpath(xpath_change_1).text
                    change_2 = self.driver.find_element_by_xpath(xpath_change_2).text
                else:
                    # STOCK
                    change = self.driver.find_element_by_xpath(xpath_change_1).text
                    change = change.replace(" ", "")
                    change_1 = re.match(r'(.*?)\(.*', change).group(1)
                    change_2 = re.match(r'.*?\((.*?)\).*', change).group(1)

                # Save to database / currency_in_day
                logging.info(str(datetime.now()) + ": " + table + " " + symbol + " " + new_value + " " + change_1 + " " + change_2)
                self.database.insert_data_realtime(
                    table=table,
                    symbol=symbol,
                    value=new_value,
                    change_1=change_1,
                    change_2=change_2.replace("(", "").replace(")", ""),
                    moment=moment
                )

            except TimeoutException:
                continue  # no more friends loaded

    def _get_friends_list(self):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "li._698")))
        return self.driver.find_elements_by_css_selector("li._698")

    def get_friends(self):
        # navigate to "friends" page
        # self.driver.find_element_by_css_selector("div[data-click='profile_icon']").click()

        self.driver.find_element_by_css_selector("a[data-tab-key='friends']").click()

        # continuous scroll until no more new friends loaded
        num_of_loaded_friends = len(self._get_friends_list())

        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                self.wait.until(lambda driver: len(self._get_friends_list()) > num_of_loaded_friends)
                num_of_loaded_friends = len(self._get_friends_list())
            except TimeoutException:
                break  # no more friends loaded

        return [friend for friend in self._get_friends_list()]


if __name__ == '__main__':
    currency = threading.Thread(target=RealtimeCrawler, kwargs={
        'type': 0
    })
    stocks = threading.Thread(target=RealtimeCrawler, kwargs={
        'type': 1
    })

    currency.start()
    stocks.start()

    currency.join()
    stocks.join()





