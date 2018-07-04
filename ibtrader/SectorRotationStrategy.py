import backtrader as bt
from datetime import timedelta, datetime
import ibtrader.PandasRepo as datarepo
import numpy as np


class SectorRotationStrategy(bt.Strategy):

    def __init__(
            self,
            fastSmaDays=40,
            slowSmaDays=200,
            universe=["IYM", "IYC", "IYK", "IYE", "IYF", "IYH", "IYR", "IYW", "IDU"]):
        self.add_timer(
         when=bt.timer.SESSION_START,
         offset=timedelta(),
         repeat=False,
         weekdays=[1],
         weekcarry=True
        )
        self.maxNumPositions = 6
        self.universe = universe
        self.fastSmaDays = fastSmaDays
        self.slowSmaDays = slowSmaDays
        self.datarepo = datarepo()
        self.isTimerNotified = False
        self.isDataLive = False
        self.isLiveTrading = False

    def notify_data(self, data, status, *args, **kwargs):
        print("notify_data: {}".format(data._getstatusname(status)))
        print ("symbol: " + data.tradecontract.m_symbol)
        self.isLiveTrading = True
        if status == data.LIVE:
            print("*** LIVE ***")
            self.isDataLive = True
            self.execute_trades_if_ready()

    def notify_store(self, msg, *args, **kwargs):
        print("notify_store: {}".format(msg))

    def notify_cashvalue(self, cash, value):
        pass

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
        print("*** TIMER NOTIFIED ***")
        self.isTimerNotified = True
        self.execute_trades_if_ready()

    # def next(self):
    #     print("*** NEXT CALLED ***")

    def execute_trades_if_ready(self):
        if not self.isLiveTrading:
            self.execute_trades()

        if self.isTimerNotified and self.isDataLive:
            self.isTimerNotified = False
            self.execute_trades()

    def execute_trades(self):
        momentums = dict()
        prices = dict()
        possibledate = datetime.fromtimestamp(self.data.datetime[0])
        repoEndDate = possibledate - timedelta(days=1)
        repoStartDate = repoEndDate - timedelta(days=self.slowSmaDays + 1)
        for symbol in self.universe:
            closes = self.datarepo.GetData(symbol, repoStartDate, repoEndDate)['Close'].values
            smaFast = np.mean(closes[-self.fastSmaDays])
            smaSlow = np.mean(closes[-self.slowSmaDays])
            momentums[symbol] = smaFast / smaSlow
            prices[symbol] = closes[-1]

        buyThreshold = sorted(momentums.values())[-min(self.maxNumPositions, len(momentums))]
        symbolsToBuy = {k: v for k, v in momentums.items() if v >= buyThreshold}
        tgtPositionValue = self.broker.getvalue() / len(symbolsToBuy) if len(symbolsToBuy) > 0 else 0.0

        # Sell things first, then buy
        for symbol in self.universe:
            if symbol not in symbolsToBuy:
                print("Selling " + symbol)
                self.order_target_size(data=self.getdatabyname(symbol), target=0)

        for symbol in symbolsToBuy:
            print("Buying " + symbol)
            self.order_target_value(data=self.getdatabyname(symbol), target=tgtPositionValue)
