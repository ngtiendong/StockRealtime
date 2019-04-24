import requests, json, pymysql, re
from datetime import datetime

# Bring your packages onto the path
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from global_config import *

class MySQL():
    def __init__(self):
        os.environ['TZ'] = 'Asia/Ho_Chi_Minh'
        self.connection = pymysql.connect(DB_HOST, DB_USERNAME, DB_PASSWORD, DB_DATABASE, DB_PORT)

    def close(self):
        self.connection.close()

    def get_symbol(self, index):
        if index == 0:
            return "VNIndex"
        elif index == 1:
            return "VN30INDEX",
        elif index == 2:
            return "HNXINDEX",
        else:
            return "HNX30INDEX"

    def insert_stock(self, element, symbol):
        with self.connection.cursor() as cursor:
            sql_search = "SELECT * FROM `stocks` WHERE `symbol`=%s AND `date`=%s"
            search_exist = cursor.execute(sql_search, (symbol, self.parse_date(element['dateVN'])))

            if not search_exist:
                sql_insert = "INSERT INTO `stocks` (`symbol`, `open`, `close`, `high`, `low`, `volume`," \
                      " `date`, `created_at`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                cursor.execute(sql_insert, (
                    symbol,
                    element['open'],
                    element['close'],
                    element['high'],
                    element['low'],
                    element['Volume'],
                    self.parse_date(element['dateVN']),
                    datetime.now()
                ))

            # commit
            self.connection.commit()

    def insert_currency(self, date, value, symbol):
        year, month, day = [int(i) for i in date.split("-")]
        date = datetime(year, month, day)
        with self.connection.cursor() as cursor:
            sql_search = "SELECT * FROM `currency` WHERE `symbol`=%s AND `date`=%s"
            search_exist = cursor.execute(sql_search, (symbol, date))

            if not search_exist:
                sql_insert = "INSERT INTO `currency` (`symbol`, `value`, `date`, `created_at`)" \
                             " VALUES (%s, %s, %s, %s)"
                cursor.execute(sql_insert, (
                    symbol,
                    value,
                    date,
                    datetime.now()
                ))

            # commit
            self.connection.commit()

    def insert_data_realtime(self, table, symbol, value, change_1, change_2, moment):
        with self.connection.cursor() as cursor:
            sql_insert = "INSERT INTO `"+table+"` (`symbol`, `value`, `change_1`, `change_2`, `moment`, `created_at`)" \
                         " VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql_insert, (
                symbol,
                value,
                change_1,
                change_2,
                moment,
                datetime.now()
            ))

            # commit
            self.connection.commit()

    def parse_date(self, init_date):
        day, month, year = [int(i) for i in init_date.split("/")]
        return datetime(year, month, day)