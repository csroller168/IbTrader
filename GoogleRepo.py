import urllib.request
import csv
from datetime import datetime
from collections import OrderedDict


class GoogleRepo:
    def __init__(self):
        self._downloadUrlFormat = "https://finance.google.com/finance/historical?q={}&startdate=22-Feb-2002&output=csv"
        self._dataFileFormat = "./data/{}.csv"

    def GetData(self, symbol):
        url = self._downloadUrlFormat.format(symbol)
        urllib.request.urlretrieve(url, self.DataFileName(symbol))

    def ClosingPrices(self, symbol):
        prices = {}
        with open(self.DataFileName(symbol)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                day = datetime.strptime(row['\ufeffDate'], "%d-%b-%y").date()
                prices[day] = float(row['Close'])
        return OrderedDict(sorted(prices.items(), key=lambda t: t[0]))

    def DataFileName(self, symbol):
        return self._dataFileFormat.format(symbol)