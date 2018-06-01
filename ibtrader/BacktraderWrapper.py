from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
from datetime import datetime
from ibtrader.SectorRotationStrategy import SectorRotationStrategy
import ibtrader.PandasRepo as datarepo

# TODO:
# Integrate into IB
# Delete dead classes
# clean up weak pep8 warnings
# Get better notebook analysis
# update strategy
    # add market pullout indicator


class BacktraderWrapper:
    def __init__(self,
                 startCash = 10000,
                 universe = ["IYM", "IYC", "IYK", "IYE", "IYF", "IYH", "IYR", "IYW", "IDU"],
                 startDate = datetime(2016, 1, 1),
                 endDate = datetime(2017, 12, 29)):
        self._startCash = startCash
        self._universe = universe
        self._startDate = startDate
        self._endDate = endDate

    def RunBackTest(self):
        cerebro = bt.Cerebro()
        cerebro.addstrategy(SectorRotationStrategy)
        for symbol in self._universe:
            df = datarepo().GetData(symbol, self._startDate, self._endDate)
            data = bt.feeds.PandasData(dataname=df)
            cerebro.adddata(data, name=symbol)
        cerebro.broker.setcash(self._startCash)
        cerebro.addanalyzer(bt.analyzers.PyFolio, _name='pyfolio')
        cerebro.run()
        print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    def LiveTrade(self):
        cerebro = bt.Cerebro(stdstats=False)
        store = bt.stores.IBStore(host='127.0.0.1', port=4002, clientId=168)
        for symbol in self._universe:
            data = store.getdata(dataname=symbol, timeframe=bt.TimeFrame.Ticks)
            cerebro.resampledata(data, timeframe=bt.TimeFrame.Seconds, compression=10)

        cerebro.broker = store.getbroker()
        cerebro.addstrategy(SectorRotationStrategy)
        cerebro.run()

