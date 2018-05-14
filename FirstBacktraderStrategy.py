import backtrader as bt

class FirstBacktraderStrategy(bt.Strategy):

    def __init__(self):
        self.rsi = dict()
        for symbol in self.getdatanames():
            self.rsi[symbol] = bt.indicators.RSI_SMA(self.getdatabyname(symbol).close, period=21)

    def next(self):
        for symbol in self.getdatanames():
            pos = self.getpositionbyname(symbol).size or 0
            if pos == 0:
                if self.rsi[symbol][0] < 30:
                    self.buy(data=self.getdatabyname(symbol), size=100)
            else:
                if self.rsi[symbol][0] > 70:
                    self.sell(data=self.getdatabyname(symbol), size=100)
