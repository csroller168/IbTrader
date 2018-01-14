import time
from datetime import date
import urllib.request


class YahooRepo:
    def __init__(self):
        self._downloadUrlFormat = "https://query1.finance.yahoo.com/v7/finance/download/{}?period1={}&period2={}&interval=1d&events=history&crumb=6IXeKuSZjHD"
        self._dstFormat = "./data/{}.csv"

    def GetData(self, symbol):
        beginDate = int(time.mktime(date(2000, 6, 28).timetuple()))
        today = int(time.mktime(date.today().timetuple()))
        url = self._downloadUrlFormat.format(symbol, beginDate, today)
        urllib.request.urlretrieve(url, self._dstFormat.format(symbol))
        # todo: resolve 401 error

        # csv = urllib.request.urlopen(url).read()
        # with open(self._dstFormat.format(symbol), 'wb') as fx:
        #     fx.write(csv)
