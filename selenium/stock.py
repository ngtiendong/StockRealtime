from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import re, json, sys, os, time
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
            self.database_currency = MySQL()
            self.driver.get("https://vn.tradingview.com/symbols/EURUSD/")
            currency = threading.Thread(target=self.get_realtime_data, kwargs={
                "table": TABLE_REALTIME_CURRENCY,
                "symbol": "USD",
                "type": type,
                "wait_time": WAIT_CURRENCY,
                "xpath_value": "//*[@id='anchor-page-1']/div/div[3]/div[1]/div/div/div/div[1]/div[1]",
                "xpath_change_1": "//*[@id='anchor-page-1']/div/div[3]/div[1]/div/div/div/div[1]/div[3]/span[1]",
                "xpath_change_2": "//*[@id='anchor-page-1']/div/div[3]/div[1]/div/div/div/div[1]/div[3]/span[2]",
                "xpath_volumn": "//*[@id='anchor-page-1']/div/div[3]/div[3]/div[3]/div[1]",
                "database": self.database_currency
            })
            currency.start()
            currency.join()

        else:
            # STOCK
            self.driver.get("http://banggia2.ssi.com.vn/")
            self.database_vnindex = MySQL()
            vnindex_stock = threading.Thread(target=self.get_realtime_data, kwargs={
                "table": TABLE_REALTIME_STOCK,
                "symbol": "VNIndex",
                "type": type,
                "wait_time": WAIT_STOCK,
                "xpath_value": '//*[@id="tdHoseVnIndex"]',
                "xpath_change_1": '//*[@id="tdHoseChangeIndex"]',
                "xpath_change_2": '',
                "database": self.database_vnindex
            })

            self.database_vn30index = MySQL()
            vn30_stock = threading.Thread(target=self.get_realtime_data, kwargs={
                "table": TABLE_REALTIME_STOCK,
                "symbol": "VN30INDEX",
                "type": type,
                "wait_time": WAIT_STOCK,
                "xpath_value": '//*[@id="tdHose30VnIndex"]',
                "xpath_change_1": '//*[@id="tdHose30ChangeIndex"]',
                "xpath_change_2": '',
                "database": self.database_vn30index
            })

            self.database_hnxindex = MySQL()
            hnxindex_stock = threading.Thread(target=self.get_realtime_data, kwargs={
                "table": TABLE_REALTIME_STOCK,
                "symbol": "HNXINDEX",
                "type": type,
                "wait_time": WAIT_STOCK,
                "xpath_value": '//*[@id="tdHnxIndex"]',
                "xpath_change_1": '//*[@id="tdHnxChangeIndex"]',
                "xpath_change_2": '',
                "database": self.database_hnxindex
            })

            self.database_hnx30index = MySQL()
            hnx30_stock = threading.Thread(target=self.get_realtime_data, kwargs={
                "table": TABLE_REALTIME_STOCK,
                "symbol": "HNX30INDEX",
                "type": type,
                "wait_time": WAIT_STOCK,
                "xpath_value": '//*[@id="tdHnx30Index"]',
                "xpath_change_1": '//*[@id="tdHnx30ChangeIndex"]',
                "xpath_change_2": '',
                "database": self.database_hnx30index
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
        return float(value)

    def get_volumn_element(self, selector):
        value = self.driver.find_element_by_xpath(selector).text
        value = value.replace('K', '')
        return float(value)*1000

    def get_realtime_data(self, table, symbol, type, wait_time, xpath_value, xpath_change_1, xpath_change_2, xpath_volumn, database):
        self.wait.until(EC.visibility_of_element_located((By.XPATH, xpath_value)))
        stock_value = self.get_value_element(xpath_value)

        old_volumn_value = 0
        close = 0
        if datetime.now().second != 00 :
            time.sleep(60-datetime.now().second)

        while True:
            try:
                # moment = datetime.now()
                if type == 0:
                    # CURRENCY
                    open = high = low = close = change_1 = change_2 = 0
                    value = self.get_value_element(xpath_value)
                    volumn = self.get_volumn_element(xpath_volumn)
                    time.sleep(0.98)
                    # if old_volumn_value == 0:
                    #     old_volumn_value = self.get_volumn_element(xpath_volumn)
                    #     open = self.get_value_element(xpath_value)
                    # else:
                    #     open = close
                    #
                    # # get high/low
                    # high = open
                    # low = open
                    # time_remaining = 60-datetime.now().second
                    # while True:
                    #     if time_remaining <= wait_time or time_remaining <= 2:
                    #         break
                    #     else:
                    #         new_value = self.get_value_element(xpath_value)
                    #         if new_value > high:
                    #             high = new_value
                    #         elif new_value < low:
                    #             low = new_value
                    #         time.sleep(wait_time)
                    #
                    #     time_remaining = 60-datetime.now().second
                    #
                    # close = self.get_value_element(xpath_value)
                    # new_volumn_value = self.get_volumn_element(xpath_volumn)
                    #
                    # volumn = int(new_volumn_value - old_volumn_value)
                    # old_volumn_value = new_volumn_value
                    #
                    # logging.info("Currency change | "
                    #              + str(datetime.now()) +": open="+  str(open) +", high="+ str(high) +", low="+ str(low)
                    #                                                 +", close="+ str(close) +", volumn="+ str(volumn))
                    #
                    change_1 = self.driver.find_element_by_xpath(xpath_change_1).text
                    change_2 = self.driver.find_element_by_xpath(xpath_change_2).text
                    # time.sleep(60-datetime.now().second)
                else:
                    value=0
                    new_value = self.get_value_element(xpath_value)
                    WebDriverWait(self.driver, wait_time, poll_frequency=1).until(
                        lambda value: new_value != stock_value)
                    stock_value = new_value
                    # STOCK
                    change = self.driver.find_element_by_xpath(xpath_change_1).text
                    change = change.replace(" ", "")
                    change_1 = re.match(r'(.*?)\(.*', change).group(1)
                    change_2 = re.match(r'.*?\((.*?)\).*', change).group(1)
                    volumn = 0,
                    high = 0,
                    low = 0,
                    open=0,
                    close=0

                # Save to database / currency_in_day
                # logging.info(str(datetime.now()) + ": " + table + " " + symbol + " " + str(high) + " " + str(low) + " " + str(volumn))
                database.insert_data_realtime(
                    table=table,
                    symbol=symbol,
                    value=value,
                    change_1=change_1,
                    change_2=change_2.replace("(", "").replace(")", ""),
                    moment=datetime.now(),
                    open=open,
                    high=high,
                    low=low,
                    close=close,
                    volumn=volumn
                )

            except TimeoutException:
                # time.sleep(2)
                pass

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
    # import time as time_
    # print(int(round(time_.time())), datetime.now().microsecond, datetime.now().second)
    # while True:
    #     old = int(round(time_.time()))
    #     if datetime.now().microsecond != 00 :
    #         print(1000-int(round(time_.time()))+old)
    #         time.sleep(1000-int(round(time_.time()))+old)
    #         print(datetime.now())

    currency = threading.Thread(target=RealtimeCrawler, kwargs={
        'type': 0
    })
    # # stocks = threading.Thread(target=RealtimeCrawler, kwargs={
    # #     'type': 1
    # # })
    #
    currency.start()
    # # stocks.start()

    currency.join()
    # # stocks.join()





