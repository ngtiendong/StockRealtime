import sys, os
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))

DRIVER = sys.path[0]+"/chromedriver"

WAIT_CURRENCY=5
WAIT_STOCK=10

TABLE_REALTIME_CURRENCY="currency_in_day"
TABLE_REALTIME_STOCK="stock_in_day"
# if __name__ == "__main__":
#     print(sys.path[0]+"/chromedriver")