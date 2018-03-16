import urllib.request
import csv
from datetime import datetime, timedelta
from collections import OrderedDict



class GoogleRepo:
    def __init__(self):
        self._downloadUrlFormat = "https://finance.google.com/finance/historical?q={}&startdate=22-Feb-2002&output=csv"
        self._dataFileFormat = "./data/{}.csv"

    def GetData(self, symbol):
        url = self._downloadUrlFormat.format(symbol)
        #urllib.request.urlretrieve(url, self.DataFileName(symbol))
        request = urllib.request.Request(url)
        request.add_header('User-Agent', "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36")
        with urllib.request.urlopen(url) as response, open(self.DataFileName(symbol), 'wb') as out_file:
            data = response.read()
            out_file.write(data)

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
