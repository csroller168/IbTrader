import backtrader as bt
import numpy as np

class SectorRotationStrategy(bt.Strategy):

    def __init__(self,
                 fastSmaDays = 40,
                 slowSmaDays = 200):
        self.maxNumPositions = 6
        self.momentum = dict()
        for symbol in self.getdatanames():
            data = self.getdatabyname(symbol)
            smaFast = bt.ind.SMA(data, period=fastSmaDays)
            smaSlow = bt.ind.SMA(data, period=slowSmaDays)
            self.momentum[symbol] = smaFast/smaSlow

    def next(self):
        momentums = dict()
        for symbol in self.getdatanames():
            momentums[symbol] = self.momentum[symbol][0]

        buyThreshold = sorted(momentums.values())[-min(self.maxNumPositions, len(momentums))]
        symbolsToBuy = {k: v for k, v in momentums.items() if v >= buyThreshold}
        pct = 1.0 / len(symbolsToBuy)

        for symbol in self.getdatanames():
            if symbol in symbolsToBuy:
                self.order_target_percent(data=self.getdatabyname(symbol), target=pct)
            else:
                self.order_target_percent(data=self.getdatabyname(symbol), target=0)
