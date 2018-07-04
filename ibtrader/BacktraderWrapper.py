from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
from datetime import datetime
from ibtrader.SectorRotationStrategy import SectorRotationStrategy
import ibtrader.PandasRepo as datarepo


# TODO:
# finish integration into IB
#   still not getting data to strategy - delayed, no live notification
#       make the timer set a flag that trading is OK to go
#       make the notify_data look for live (see ibtest sample), and set flag
#       make both call method to see if flags set and trading can execute
#       if so, call separate method to execute trade
#           ... or, put trade logic in next() and check for live data and timer exec on each call
#
# next branch
#   add market pullout indicator to strategy
#   Get better notebook analysis
#   add trailing stop


class BacktraderWrapper:
    def __init__(self,
                 startCash=10000,
                 universe=["IYM", "IYC", "IYK", "IYE", "IYF", "IYH", "IYR", "IYW", "IDU"],
                 startDate=datetime(2017, 1, 3),
                 endDate=datetime(2017, 12, 29)):
        self._startCash = startCash
        self._universe = universe
        self._startDate = startDate
        self._endDate = endDate

    def run_backtest(self):
        cerebro = bt.Cerebro()
        cerebro.broker = bt.brokers.BackBroker()

        cerebro.addstrategy(SectorRotationStrategy)
        for symbol in self._universe:
            df = datarepo().GetData(symbol, self._startDate, self._endDate)
            data = bt.feeds.PandasData(dataname=df)
            cerebro.adddata(data, name=symbol)
        cerebro.broker.setcash(self._startCash)
        cerebro.broker.setcommission(commission=1.0,
                                     commtype=bt.CommInfoBase.COMM_FIXED,
                                     stocklike=True)
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    def live_trade(self):
        cerebro = bt.Cerebro(stdstats=False)
        store = bt.stores.IBStore(host='127.0.0.1', port=4002, clientId=168)
        for symbol in self._universe:
            data = store.getdata(dataname=symbol, timeframe=bt.TimeFrame.Ticks)
            cerebro.resampledata(data, timeframe=bt.TimeFrame.Minutes, compression=10)
        cerebro.broker = store.getbroker()
        cerebro.addstrategy(SectorRotationStrategy)
        cerebro.run(runonce=True)
