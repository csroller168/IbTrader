from Asset import Asset


class Order():
    def __init__(self, type, asset: Asset):
        self._type = type
        self._asset = asset
