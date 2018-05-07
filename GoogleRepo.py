###
# todo: replace this repo with something other than google that will work
# Separate app to get google data, or some other data source
###



import csv
from datetime import datetime, timedelta
from collections import OrderedDict
import requests
from os.path import dirname, abspath

class GoogleRepo:
    def __init__(self):
        self._downloadUrlFormat = "https://finance.google.com/finance/historical?q={}&startdate=22-Feb-2002&output=csv"
        self._dataFileFormat = dirname(abspath(__file__)) + "/data/{}.csv"

    def GetData(self, symbol):
        url = self._downloadUrlFormat.format(symbol)
        filename = self.DataFileName(symbol)
        r = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)

    def ClosingPrices(self, symbol):
        prices = {}
        with open(self.DataFileName(symbol)) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                day = datetime.strptime(row['\ufeffDate'], "%d-%b-%y").date()
                prices[day] = float(row['Close'])

        # fill forward gaps
        gaps = {}
        previousDay = min(prices.keys()) - timedelta(days=1)
        previousValue = 0
        for day, value in sorted(prices.items(), key=lambda t: t[0]):
            expectedDay = previousDay + timedelta(days=1)
            while expectedDay < day:
                gaps[expectedDay] = previousValue
                expectedDay += timedelta(days=1)
            previousDay = day
            previousValue = prices[previousDay]
        prices.update(gaps)
        return OrderedDict(sorted(prices.items(), key=lambda t: t[0]))

    def DataFileName(self, symbol):
        return self._dataFileFormat.format(symbol)
