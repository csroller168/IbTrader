import backtrader as bt
import datetime

class SectorRotationStrategy(bt.Strategy):

    def __init__(self, fastSmaDays=40, slowSmaDays=200):
        self.add_timer(
            when=bt.timer.SESSION_START,
            offset=datetime.timedelta(),
            repeat=False,
            weekdays=[1],
            weekcarry=True
        )
        self.maxNumPositions = 6
        self.momentum = dict()
        for symbol in self.getdatanames():
            data = self.getdatabyname(symbol)
            smaFast = bt.ind.SMA(data, period=fastSmaDays)
            smaSlow = bt.ind.SMA(data, period=slowSmaDays)
            self.momentum[symbol] = smaFast / smaSlow

    def notify_order(self, order):
        if order.status == order.Completed:
            buysell = 'BUY ' if order.isbuy() else 'SELL'
            txt = '{},{},{},{}@{}'.format(self.data.datetime.date(),
                                          buysell,
                                          self.data._dataname['Symbol'][0],
                                          order.executed.size,
                                          order.executed.price)
            print(txt)

    def notify_timer(self, timer, when, *args, **kwargs):
        momentums = dict()
        for symbol in self.getdatanames():
            momentums[symbol] = self.momentum[symbol][0]

        buyThreshold = sorted(momentums.values())[-min(self.maxNumPositions, len(momentums))]
        symbolsToBuy = {k: v for k, v in momentums.items() if v >= buyThreshold}
        pct = 1.0 / len(symbolsToBuy) if len(symbolsToBuy) > 0 else 0.0

        for symbol in self.getdatanames():
            if symbol in symbolsToBuy:
                self.order_target_percent(data=self.getdatabyname(symbol), target=pct)
                print('{} Buy {}% {}'.format(when, pct, symbol))
            else:
                self.order_target_percent(data=self.getdatabyname(symbol), target=0)
                print('{} Sell 100% {}'.format(when, symbol))
