from Asset import Asset


class Order():
    def __init__(self, type, asset: Asset):
        self._type = type
        self._asset = asset
        self._commission = 1

    def Proceeds(self):
        if self._type == "Buy":
            return -self._asset.Value - self._commission
        return self._asset.Value - self._commission