from GoogleRepo import GoogleRepo

class SectorRotationStrategy:
    def __init__(self, holdingsValue):
        self._symbols = ("IYM", "IYC", "IYK", "IYE", "IYF", "IYH", "IYR", "IYW", "IDU")
        self._benchmarkSymbol = "SPY"
        self._maxNumPositions = 6
        self._holdingsValue = holdingsValue

    def Execute(self):
        repo = GoogleRepo()
        #for symbol in self._symbols:
            #repo.GetData(symbol)
        # Debug
        repo.ClosingPrices("IYR")

        # Get Closing prices for each symbol and benchmark
        # if out of market, go all cash
        # if in market...
            # Rank by momentum
            # Buy equal weight top 6 ETFs
