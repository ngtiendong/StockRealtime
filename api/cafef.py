import requests, json, pymysql, re, sys, os
from datetime import datetime

# Bring your packages onto the path
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database.mysql import MySQL


class StockHistory():
    def __init__(self):
        self.api_bridge = MySQL()

    def get_stock_history(self):
        raw_data = requests.get(
            "http://s.cafef.vn/ajax/bieudokythuat.ashx?symbol=VNINDEX,VN30INDEX,HNX30INDEX,HNXINDEX,VNINDEX&type=compare")
        str_data = raw_data.content.decode('utf-8')
        result = re.findall(r'.*\[(.*?)\].*', str_data)
        # print(len(result))
        del result[1:3]
        # print(type(result), len(result), result[1])
        try:
            for index, data in enumerate(result):
                symbol = self.api_bridge.get_symbol(index)
                for ele in re.findall(r'({.*?})', data):
                    detail = json.loads(ele)
                    print(symbol, detail)
                    self.api_bridge.insert_stock(detail, symbol)
                    # sys.exit()
        finally:
            # close connection
            self.api_bridge.close()


class CurrencyHistory():
    def __init__(self):
        self.api_bridge = MySQL()

    def get_currency_history(self):
        now = str(datetime.now().date())
        raw_data = requests.get(
            "https://api.exchangeratesapi.io/history?start_at=2000-01-01&end_at="+now+"&symbols=USD")
        result = json.loads(raw_data.content.decode('utf-8'))["rates"]
        try:
            for key, value in result.items():
                print(key, value)
                self.api_bridge.insert_currency(key, value["USD"], symbol="USD")
        finally:
            # close connection
            self.api_bridge.close()


if __name__ == "__main__":
    currency = CurrencyHistory()
    currency.get_currency_history()
