from GoogleRepo import GoogleRepo
from Asset import Asset

class SectorRotationStrategy:
    def __init__(self, holdingsValue, tradingDay):
        self._symbols = ("IYM", "IYC", "IYK", "IYE", "IYF", "IYH", "IYR", "IYW", "IDU")
        self._benchmarkSymbol = "SPY"
        self._maxNumPositions = 6
        self._holdingsValue = holdingsValue
        self._tradingDay = tradingDay

    def IsInMarket(self):
        repo = GoogleRepo()
        benchmarkPrices = repo.ClosingPrices(self._benchmarkSymbol)
        return (self.Momentum(benchmarkPrices) > 1)

    def GetTargetPortfolio(self):
        repo = GoogleRepo()
        repo.GetData(self._benchmarkSymbol)

        if(not self.IsInMarket()):
            return {}

        prices = {}
        momentums = {}
        for symbol in self._symbols:
            repo.GetData(symbol)
            priceData = repo.ClosingPrices(symbol)
            momentum = self.Momentum(priceData)
            if momentum > 1:
                prices[symbol] = priceData
                momentums[symbol] = momentum

        buyThreshold = sorted(momentums.values())[-min(self._maxNumPositions,len(momentums))]
        symbolsToBuy = {k: v for k,v in momentums.items() if v >= buyThreshold}
        assets = []
        for symbol in symbolsToBuy:
            idx = len(prices[symbol])-1
            if self._tradingDay in list(prices[symbol].keys()):
                idx = list(prices[symbol].keys()).index(self._tradingDay)
            sharePrice = list(prices[symbol].values())[idx]
            numShares = int(self._holdingsValue / len(symbolsToBuy) / sharePrice)
            assets.append(Asset(symbol, sharePrice, numShares))
        return assets

    def Momentum(self, prices):
        idx = len(prices)-1
        try:
            idx = list(prices.keys()).index(self._tradingDay)
        except:
            pass

        sma50Values = list(prices.values())[idx-50:idx]
        sma50 = sum(sma50Values) / len(sma50Values)
        sma200Values = list(prices.values())[idx-200:idx]
        sma200 = sum(sma200Values) / len(sma200Values)
        return sma50 / sma200