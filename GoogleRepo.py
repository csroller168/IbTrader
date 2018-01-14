import urllib.request


class GoogleRepo:
    def __init__(self):
        self._downloadUrlFormat = "https://finance.google.com/finance/historical?q={}&startdate=22-Feb-2002&output=csv"
        self._dstFormat = "./data/{}.csv"

    def GetData(self, symbol):
        url = self._downloadUrlFormat.format(symbol)
        urllib.request.urlretrieve(url, self._dstFormat.format(symbol))

