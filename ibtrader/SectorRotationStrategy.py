import backtrader as bt
from datetime import timedelta
import ibtrader.PandasRepo as datarepo
import numpy as np
from queue import Queue
from threading import Lock

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
            weekdays=[1,2,3,4,5],
            weekcarry=True
        )
        self.maxNumPositions = 6
        self.universe = universe
        self.fastSmaDays = fastSmaDays
        self.slowSmaDays = slowSmaDays
        self.datarepo = datarepo()
        self.allDataLiveSignal = Queue()
        self.liveDataSymbols = []
        self.lock = Lock()

    def notify_data(self, data, status, *args, **kwargs):
        print("notify_data: {} {}".format(data.contract.m_localSymbol, data._getstatusname(status)))
        if status == data.LIVE:
            self.lock.acquire()
            self.liveDataSymbols.append(data.contract.m_localSymbol)
            self.lock.release()
            if len(set(self.universe) - set(self.liveDataSymbols)) == 0:
                self.allDataLiveSignal.put(True)

    def notify_store(self, msg, *args, **kwargs):
        print("notify_store: {}".format(msg))

    def notify_cashvalue(self, cash, value):
        print("notify_cashvalue: {}, {}".format(cash, value))

    def notify_order(self, order):
        if order.status == order.Completed:
            buysell = 'BUY ' if order.isbuy() else 'SELL'
            txt = '{},{},{},{}@{}'.format(self.data.datetime.date(),
                                          buysell,
                                          order.data._name,
                                          order.executed.size,
                                          order.executed.price)
            print(txt)

    def notify_timer(self, timer, when, *args, **kwargs):
        #self.allDataLiveSignal.get(timeout=999999)
        momentums = dict()
        repoEndDate = when - timedelta(days=1)
        repoStartDate = repoEndDate - timedelta(days=self.slowSmaDays+1)
        for symbol in self.universe:
            closes = self.datarepo.GetData(symbol, repoStartDate, repoEndDate)['Close'].values
            smaFast = np.mean(closes[-self.fastSmaDays:])
            smaSlow = np.mean(closes[-self.slowSmaDays:])
            momentums[symbol] = smaFast / smaSlow

        buyThreshold = sorted(momentums.values())[-min(self.maxNumPositions, len(momentums))]
        symbolsToBuy = {k: v for k, v in momentums.items() if v >= buyThreshold}
        pct = 1.0 / len(symbolsToBuy) if len(symbolsToBuy) > 0 else 0.0

        # Sell things first, then buy
        for symbol in self.universe:
            if symbol not in symbolsToBuy.keys():
                symbolData = self.getdatabyname(name=symbol)
                holding = self.getpositionbyname(name=symbol, data=symbolData)
                self.sell(data=symbolData, size=holding)

        for symbol in symbolsToBuy:
            self.order_target_percent(data=self.getdatabyname(symbol), target=pct)

    def next(self):
        pass
