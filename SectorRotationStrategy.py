from GoogleRepo import GoogleRepo

class SectorRotationStrategy:
    def __init__(self, holdingsValue, tradingDay):
        self._symbols = ("IYM", "IYC", "IYK", "IYE", "IYF", "IYH", "IYR", "IYW", "IDU")
        self._benchmarkSymbol = "SPY"
        self._maxNumPositions = 6
        self._holdingsValue = holdingsValue
        self._tradingDay = tradingDay

    def IsInMarket(self):
        repo = GoogleRepo()
        #repo.GetData(self._benchmarkSymbol)
        benchmarkPrices = repo.ClosingPrices(self._benchmarkSymbol)
        return (self.Momentum(benchmarkPrices) > 1)

    def GetPortfolio(self):
        repo = GoogleRepo()

        if(not self.IsInMarket()):
            return {}

        prices = {}
        momentums = {}
        for symbol in self._symbols:
            #repo.GetData(symbol)
            priceData = repo.ClosingPrices(symbol)
            momentum = self.Momentum(priceData)
            if momentum > 1:
                prices[symbol] = priceData
                momentums[symbol] = momentum

        buyThreshold = sorted(momentums.values())[-min(self._maxNumPositions,len(momentums))]
        symbolsToBuy = {k: v for k,v in momentums.items() if v >= buyThreshold}
        # TODO: buy equal weight symbolsToBuy - return portfolio of assets

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