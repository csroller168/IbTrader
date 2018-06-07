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

    def notify_data(self, data, status, *args, **kwargs):
        print("got notify_data")
        pass
        #print('*' * 5, 'DATA NOTIF:', data._getstatusname(status), *args)
        #if status == data.LIVE:
        #    self.data_live = True

    def notify_order(self, order):
        print("got notify_order")
        if order.status == order.Completed:
            buysell = 'BUY ' if order.isbuy() else 'SELL'
            txt = '{} {}@{}'.format(buysell, order.executed.size,
                                    order.executed.price)
            print(txt)

    def notify_timer(self, timer, when, *args, **kwargs):
        print("got notify_timer")
        momentums = dict()
        for symbol in self.getdatanames():
            momentums[symbol] = self.momentum[symbol][0]

        buyThreshold = sorted(momentums.values())[-min(self.maxNumPositions, len(momentums))]
        symbolsToBuy = {k: v for k, v in momentums.items() if v >= buyThreshold}
        pct = 1.0 / len(symbolsToBuy)

        for symbol in self.getdatanames():
            if symbol in symbolsToBuy:
                self.order_target_percent(data=self.getdatabyname(symbol), target=pct)
                print('Buy ' + str(pct) + '% ' + symbol)
                # self.buy(data=self.getdatabyname(symbol), size=1)
            else:
                self.order_target_percent(data=self.getdatabyname(symbol), target=0)
                print('Sell ' + symbol)

    def next(self):
        print("got next")
        pass

