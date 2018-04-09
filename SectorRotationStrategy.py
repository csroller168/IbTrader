from GoogleRepo import GoogleRepo
from PandasRepo import PandasRepo
from Asset import Asset

class SectorRotationStrategy:
    def __init__(self, holdingsValue, tradingDay):
        self._symbols = ("IYM", "IYC", "IYK", "IYE", "IYF", "IYH", "IYR", "IYW", "IDU")
        self._benchmarkSymbol = "SPY"
        self._maxNumPositions = 6
        self._holdingsValue = holdingsValue
        self._tradingDay = tradingDay
        self._repo = PandasRepo()

    def IsInMarket(self):
        close = self._repo.GetData(self._benchmarkSymbol)['Close']
        smaSmall = close.rolling(50).mean()[-1]
        smaLarge = close.rolling(200).mean()[-1]
        return (smaSmall > smaLarge)

    def GetTargetPortfolio(self):
        if(not self.IsInMarket()):
            return {}

        prices = {}
        momentums = {}
        for symbol in self._symbols:
            priceData = self._repo.GetData(symbol)['Close']
            momentum = self.Momentum(priceData)
            if momentum > 1:
                prices[symbol] = priceData
                momentums[symbol] = momentum

        buyThreshold = sorted(momentums.values())[-min(self._maxNumPositions,len(momentums))]
        symbolsToBuy = {k: v for k,v in momentums.items() if v >= buyThreshold}
        assets = []
        for symbol in symbolsToBuy:
            # TODO: refactor get shareprice by date (or most recent if date not present
            idx = len(prices[symbol])-1
            if self._tradingDay in list(prices[symbol].keys()):
                idx = list(prices[symbol].keys()).index(self._tradingDay)
            sharePrice = list(prices[symbol].values())[idx]
            numShares = int(self._holdingsValue / len(symbolsToBuy) / sharePrice)
            assets.append(Asset(symbol, sharePrice, numShares))
        return assets

    def Momentum(self, df):
        sma50 = df.rolling(50).mean()[-1]
        sma200 = df.rolling(200).mean()[-1]
        return sma50/sma200
