class Asset:
    def __init__(self, symbol, sharePrice, numShares):
        self._symbol = symbol
        self._sharePrice = sharePrice
        self._numShares = numShares

    @property
    def Value(self):
        return self._sharePrice * self._numShares